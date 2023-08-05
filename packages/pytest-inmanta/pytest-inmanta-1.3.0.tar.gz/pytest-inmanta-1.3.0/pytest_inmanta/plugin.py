"""
    Copyright 2019 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import json
import tempfile
import os
import shutil
import sys
import logging
import imp
import glob
import importlib
import types
from distutils import dir_util
from pathlib import Path


from inmanta import compiler, module, config, const, protocol
from inmanta.agent.handler import HandlerContext, ResourceHandler
from inmanta.data import LogLine
from inmanta.protocol import json_encode
from inmanta.agent import cache, handler
from inmanta.agent import io as agent_io
from inmanta.execute.proxy import DynamicProxy
from inmanta.export import cfg_env, Exporter


import pytest
from collections import defaultdict
import yaml
from inmanta.resources import Resource
from tornado import ioloop
from typing import Dict, Union, Optional, List

from .handler import DATA


CURDIR = os.getcwd()
LOGGER = logging.getLogger()


option_to_env = {
    "inm_venv":"INMANTA_TEST_ENV",
    "inm_module_repo":"INMANTA_MODULE_REPO",
    "inm_install_mode":"INMANTA_INSTALL_MODE",
    "inm_no_load_plugins":"INMANTA_TEST_NO_LOAD_PLUGINS",
}


def pytest_addoption(parser):
    group = parser.getgroup(
        'inmanta', 'inmanta module testing plugin')
    group.addoption('--venv', dest='inm_venv',
                    help='folder in which to place the virtual env for tests (will be shared by all tests), overrides INMANTA_TEST_ENV')
    group.addoption('--use-module-in-place', action='store_true',
                    help="tell pytest-inmanta to run with the module in place, useful for debugging")
    group.addoption('--module_repo', dest='inm_module_repo', action="append",
                    help='location to download modules from, overrides INMANTA_MODULE_REPO.'
                         'Can be specified multiple times to add multiple locations')
    group.addoption('--install_mode', dest='inm_install_mode',
                    help='Install mode for modules downloaded during this test',
                    choices=module.INSTALL_OPTS)
    group.addoption('--no_load_plugins', action='store_true', dest='inm_no_load_plugins',
                    help='Don\'t load plugins in the Project class.')


def get_opt_or_env_or(config, key, default):
    if config.getoption(key):
        return config.getoption(key)
    if option_to_env[key] in os.environ:
        return os.environ[option_to_env[key]]
    return default


def get_module_info():
    curdir = CURDIR
    # Make sure that we are executed in a module
    dir_path = curdir.split(os.path.sep)
    while not os.path.exists(os.path.join(os.path.join("/", *dir_path), "module.yml")) and len(dir_path) > 0:
        dir_path.pop()

    if len(dir_path) == 0:
        raise Exception("Module test case have to be saved in the module they are intended for. "
                        "%s not part of module path" % curdir)

    module_dir = os.path.join("/", *dir_path)
    with open(os.path.join(module_dir, "module.yml")) as m:
        module_name = yaml.safe_load(m)["name"]

    return module_dir, module_name


@pytest.fixture()
def project(project_shared, capsys):
    DATA.clear()
    project_shared.clean()
    project_shared.init(capsys)
    yield project_shared
    project_shared.clean()


@pytest.fixture()
def project_no_plugins(project_shared_no_plugins, capsys):
    DATA.clear()
    project_shared_no_plugins.clean()
    project_shared_no_plugins.init(capsys)
    yield project_shared_no_plugins
    project_shared_no_plugins.clean()


def get_module_data(filename: str) -> str:
    """
        Get the given filename from the module directory in the source tree
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(current_path, "module", filename), "r") as fd:
        return fd.read()


@pytest.fixture(scope="session")
def project_shared(project_factory):
    """
        A test fixture that creates a new inmanta project with the current module in. The returned object can be used
        to add files to the unittest module, compile a model and access the results, stdout and stderr.
    """
    yield project_factory()


# Temporary workaround for plugins loading multiple times (inmanta/pytest-inmanta#49)
@pytest.fixture(scope="session")
def project_shared_no_plugins(project_factory):
    """
        A test fixture that creates a new inmanta project with the current module in. The returned object can be used
        to add files to the unittest module, compile a model and access the results, stdout and stderr.
        This project is initialized with load_plugins == False.
    """
    yield project_factory(load_plugins=False)


@pytest.fixture(scope="session")
def project_factory(request):
    """
        A factory that constructs a single Project.
    """
    _sys_path = sys.path
    test_project_dir = tempfile.mkdtemp()
    os.mkdir(os.path.join(test_project_dir, "libs"))

    repo_options = get_opt_or_env_or(request.config, "inm_module_repo", "https://github.com/inmanta/")
    repos = []
    if isinstance(repo_options, list):
        for repo in repo_options:
            repos += repo.split(" ")
    else:
        repos = repo_options.split(" ")

    install_mode = get_opt_or_env_or(request.config, "inm_install_mode", "release")        

    modulepath = ["libs"]
    in_place = request.config.getoption("--use-module-in-place")
    if in_place:
        modulepath.append(str(Path(os.getcwd()).parent))

    env_override = get_opt_or_env_or(request.config, "inm_venv", None)
    if env_override is not None:
        try:
            os.symlink(env_override, os.path.join(test_project_dir, ".env"))
        except OSError:
            LOGGER.exception(
                "Unable to use shared env (symlink creation from %s to %s failed).",
                env_override,
                os.path.join(test_project_dir, ".env")
            )
            raise

    with open(os.path.join(test_project_dir, "project.yml"), "w+") as fd:
        fd.write("""name: testcase
description: Project for testcase
repo: ['%(repo)s']
modulepath: ['%(modulepath)s']
downloadpath: libs
install_mode: %(install_mode)s
""" % {"repo": "', '".join(repos), "install_mode": install_mode, "modulepath": "', '".join(modulepath)})

    # copy the current module in
    module_dir, module_name = get_module_info()
    if not in_place:
        dir_util.copy_tree(module_dir, os.path.join(test_project_dir, "libs", module_name))

    def create_project(**kwargs):
        extended_kwargs: Dict[str, object] = {
            "load_plugins": not get_opt_or_env_or(request.config, "inm_no_load_plugins", False),
            **kwargs,
        }
        test_project = Project(test_project_dir, **extended_kwargs)

        # create the unittest module
        test_project.create_module("unittest", initcf=get_module_data("init.cf"), initpy=get_module_data("init.py"))

        return test_project

    yield create_project

    try:
        shutil.rmtree(test_project_dir)
    except PermissionError:
        LOGGER.warning(
            "Cannot cleanup test project %s. This can be caused because we try to remove a virtual environment, "
            "loaded by this python process. Try to use a shared environment with --venv", test_project_dir
        )

    sys.path = _sys_path


class MockProcess(object):
    """
        A mock agentprocess
    """

    def __init__(self):
        self._io_loop = ioloop.IOLoop.current()


class MockAgent(object):
    """
        A mock agent for unit testing
    """
    def __init__(self, uri):
        self.uri = uri
        self.process = MockProcess()
        self._env_id = cfg_env.get()


class Project():
    """
        This class provides a TestCase class for creating module unit tests. It uses the current module and loads required
        modules from the provided repositories. Additional repositories can be provided by setting the INMANTA_MODULE_REPO
        environment variable. Repositories are separated with spaces.
    """
    def __init__(self, project_dir, load_plugins = True):
        self._test_project_dir = project_dir
        self._stdout = None
        self._stderr = None
        self.types = None
        self.version = None
        self.resources = {}
        self._root_scope = {}
        self._exporter = None
        self._blobs = {}
        self._facts = defaultdict(dict)
        self._load()
        self._plugins = self._load_plugins() if load_plugins else None
        self._capsys = None
        self.ctx = None
        self._handlers = set()
        config.Config.load_config()

    def init(self, capsys):
        self._stdout = None
        self._stderr = None
        self._capsys = capsys
        self.types = None
        self.version = None
        self.resources = {}
        self._root_scope = {}
        self._exporter = None
        self._blobs = {}
        self._facts = defaultdict(dict)
        self.ctx = None
        self._handlers = set()
        config.Config.load_config()

    def add_blob(self, key, content, allow_overwrite=True):
        """
            Add a blob identified with the hash of the content as key
        """
        if key in self._blobs and not allow_overwrite:
            raise Exception("Key %s already stored in blobs" % key)
        self._blobs[key] = content

    def stat_blob(self, key):
        return key in self._blobs

    def get_blob(self, key):
        return self._blobs[key]

    def add_fact(self, resource_id, name, value):
        self._facts[resource_id][name] = value

    def get_handler(self, resource, run_as_root):
        # TODO: if user is root, do not use remoting
        c = cache.AgentCache()
        if run_as_root:
            agent = MockAgent("ssh://root@localhost")
        else:
            agent = MockAgent("local:")

        c.open_version(resource.id.version)
        try:
            p = handler.Commander.get_provider(c, agent, resource)
            p.set_cache(c)
            p.get_file = lambda x: self.get_blob(x)
            p.stat_file = lambda x: self.stat_blob(x)
            p.upload_file = lambda x, y: self.add_blob(x, y)
            p.run_sync = ioloop.IOLoop.current().run_sync
            self._handlers.add(p)
            return p
        except Exception as e:
            raise e

    def finalize_context(self, ctx: handler.HandlerContext):
        # ensure logs can be serialized
        json_encode({"message": ctx.logs})

    def get_resource(self, resource_type: str, **filter_args: dict):
        """
            Get a resource of the given type and given filter on the resource attributes. If multiple resource match, the
            first one is returned. If none match, None is returned.

            :param resource_type: The exact type used in the model (no super types)
        """
        def apply_filter(resource):
            for arg, value in filter_args.items():
                if not hasattr(resource, arg):
                    return False

                if getattr(resource, arg) != value:
                    return False

            return True

        for resource in self.resources.values():
            if not resource.is_type(resource_type):
                continue

            if not apply_filter(resource):
                continue

            resource = self.check_serialization(resource)
            return resource

        return None

    def deploy(self, resource, dry_run=False, run_as_root=False):
        """
            Deploy the given resource with a handler
        """
        assert resource is not None

        h = self.get_handler(resource, run_as_root)

        assert h is not None

        ctx = handler.HandlerContext(resource)
        h.execute(ctx, resource, dry_run)
        self.finalize_context(ctx)
        self.ctx = ctx
        self.finalize_handler(h)
        return ctx

    def dryrun(self, resource, run_as_root=False):
        return self.deploy(resource, True, run_as_root)

    def deploy_resource(self, resource_type: str, status=const.ResourceState.deployed, run_as_root=False, **filter_args: dict):
        res = self.get_resource(resource_type, **filter_args)
        assert res is not None, "No resource found of given type and filter args"

        ctx = self.deploy(res, run_as_root)
        if ctx.status != status:
            print("Deploy did not result in correct status")
            print("Requested changes: ", ctx._changes)
            for l in ctx.logs:
                print("Log: ", l._data["msg"])
                print("Kwargs: ", ["%s: %s" % (k, v) for k, v in l._data["kwargs"].items() if k != "traceback"])
                if "traceback" in l._data["kwargs"]:
                    print("Traceback:\n", l._data["kwargs"]["traceback"])

        assert ctx.status == status
        self.finalize_context(ctx)
        return res

    def dryrun_resource(self, resource_type: str, status=const.ResourceState.dry, run_as_root=False, **filter_args: dict):
        """
            Run a dryrun for a specific resource.

            :param resource_type: the type of resource to run, as a fully qualified inmanta type (e.g. `unittest::Resource`), see :py:meth:`get_resource`
            :param status: the expected result status (for dryrun the success status is :py:attr:`inmanta.const.ResourceState.dry`)
            :param run_as_root: run the mock agent as root
            :param filter_args: filters for selecting the resource, see :py:meth:`get_resource`
        """
        res = self.get_resource(resource_type, **filter_args)
        assert res is not None, "No resource found of given type and filter args"

        ctx = self.dryrun(res, run_as_root)
        assert ctx.status == status
        return ctx.changes

    def io(self, run_as_root=False):
        version = 1
        if run_as_root:
            ret = agent_io.get_io(None, "ssh://root@localhost", version)
        else:
            ret = agent_io.get_io(None, "local:", version)
        return ret

    def create_module(self, name, initcf="", initpy=""):
        module_dir = os.path.join(self._test_project_dir, "libs", name)
        os.mkdir(module_dir)
        os.mkdir(os.path.join(module_dir, "model"))
        os.mkdir(os.path.join(module_dir, "files"))
        os.mkdir(os.path.join(module_dir, "templates"))
        os.mkdir(os.path.join(module_dir, "plugins"))

        with open(os.path.join(module_dir, "model", "_init.cf"), "w+") as fd:
            fd.write(initcf)

        with open(os.path.join(module_dir, "plugins", "__init__.py"), "w+") as fd:
            fd.write(initpy)

        with open(os.path.join(module_dir, "module.yml"), "w+") as fd:
            fd.write(f"""name: {name}
version: 0.1
license: Test License
            """)

    def _load(self) -> None:
        """
            Load the current module and compile an otherwise empty project
        """
        _, module_name = get_module_info()
        with open(os.path.join(self._test_project_dir, "main.cf"), "w+") as fd:
            fd.write(f"import {module_name}")
        test_project = module.Project(self._test_project_dir)
        module.Project.set(test_project)
        test_project.load()

    def compile(self, main, export=False):
        """
            Compile the configuration model in main. This method will load all required modules.
        """
        # write main.cf
        with open(os.path.join(self._test_project_dir, "main.cf"), "w+") as fd:
            fd.write(main)

        # compile the model
        test_project = module.Project(self._test_project_dir)
        module.Project.set(test_project)

        # flush io capture buffer
        self._capsys.readouterr()

        (types, scopes) = compiler.do_compile(refs={"facts": self._facts})

        exporter = Exporter()

        version, resources = exporter.run(types, scopes, no_commit=not export)

        for key, blob in exporter._file_store.items():
            self.add_blob(key, blob)

        self._root_scope = scopes
        self.version = version
        self.resources = resources
        self.types = types
        self._exporter = exporter

        captured = self._capsys.readouterr()

        self._stdout = captured.out
        self._stderr = captured.err

    def deploy_latest_version(self, full_deploy=False):
        """ Release and push the latest version to the server (uses the current configuration, either with a fixture or
            set by the test.
        """
        conn = protocol.SyncClient("compiler")
        LOGGER.info("Triggering deploy for version %d" % self.version)
        tid = cfg_env.get()
        agent_trigger_method = const.AgentTriggerMethod.get_agent_trigger_method(full_deploy)
        conn.release_version(tid, self.version, True, agent_trigger_method)

    def get_last_context(self) -> Optional[HandlerContext]:
        return self.ctx

    def get_last_logs(self) -> Optional[List[LogLine]]:
        if self.ctx:
            return self.ctx.logs
        return None

    def get_stdout(self):
        return self._stdout

    def get_stderr(self):
        return self._stderr

    def get_root_scope(self):
        return self._root_scope

    def add_mock_file(self, subdir, name, content):
        """
            This method can be used to register mock templates or files in the virtual "unittest" module.
        """
        dir_name = os.path.join(self._test_project_dir, "libs", "unittest", subdir)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        with open(os.path.join(dir_name, name), "w+") as fd:
            fd.write(content)

    def _load_plugins(self):
        module_dir, _ = get_module_info()
        plugin_dir = os.path.join(module_dir, "plugins")
        if not os.path.exists(plugin_dir):
            return
        if not os.path.exists(os.path.join(plugin_dir, "__init__.py")):
            raise Exception("Plugins directory doesn't have a __init__.py file.")
        result = {}
        mod_name = os.path.basename(module_dir)
        imp.load_package("inmanta_plugins." + mod_name, plugin_dir)
        for py_file in glob.glob(os.path.join(plugin_dir, "*.py")):
            sub_mod_path = "inmanta_plugins." + mod_name + "." + os.path.basename(py_file).split(".")[0]
            imp.load_source(sub_mod_path, py_file)
            sub_mod = importlib.import_module(sub_mod_path)
            for k, v in sub_mod.__dict__.items():
                if isinstance(v, types.FunctionType):
                    result[k] = v
        return result

    def get_plugin_function(self, function_name):
        if self._plugins is None:
            raise Exception("Plugins not loaded, perhaps you should use the `project` fixture or initialize the Project with load_plugins == True")
        if function_name not in self._plugins:
            raise Exception(f"Plugin function with name {function_name} not found")
        return self._plugins[function_name]

    def get_plugins(self):
        if self._plugins is None:
            raise Exception("Plugins not loaded, perhaps you should use the `project` fixture or initialize the Project with load_plugins == True")
        return dict(self._plugins)

    def get_instances(self, fortype: str="std::Entity"):
        if fortype not in self.types:
            raise Exception(f"No entities of type {fortype} found in the model")

        # extract all objects of a specific type from the compiler
        allof = self.types[fortype].get_all_instances()
        # wrap in DynamicProxy to hide internal compiler structure
        # and get inmanta objects as if they were python objects
        return [DynamicProxy.return_value(port) for port in allof]

    def unittest_resource_exists(self, name: str) -> bool:
        """
            Check if a unittest resource with name exists or not
        """
        return name in DATA

    def unittest_resource_get(self, name: str) -> Dict[str, Union[str, bool, float, int]]:
        """
            Get the state of the unittest resource
        """
        return DATA[name]

    def unittest_resource_set(self, name: str, **kwargs: Union[str, bool, float, int]) -> None:
        """
            Change a value of the unittest resource
        """
        DATA[name].update(kwargs)

    def check_serialization(self, resource: Resource) -> Resource:
        """ Check if the resource is serializable """
        serialized = json.loads(json_encode(
            resource.serialize()))
        return Resource.deserialize(serialized)

    def clean(self) -> None:
        shutil.rmtree(os.path.join(self._test_project_dir, "libs", "unittest"))
        self.finalize_all_handlers()
        self.create_module("unittest", initcf=get_module_data("init.cf"), initpy=get_module_data("init.py"))

    def finalize_handler(self, handler: ResourceHandler) -> None:
        versions = sorted(handler.cache.counterforVersion.keys())
        for version in versions:
            while handler.cache.is_open(version):
                handler.cache.close_version(version)

    def finalize_all_handlers(self):
        for handler_instance in self._handlers:
            self.finalize_handler(handler_instance)

