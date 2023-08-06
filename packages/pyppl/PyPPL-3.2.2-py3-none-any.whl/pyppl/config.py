"""Configuration for PyPPL
@variables:
    DEFAULT_CFGFILES (tuple): default configuration files
    DEFAULT_CONFIG (dict): default configurations to be loaded
    config (dict): The default configuration that will be
        used in the whole session
"""
from multiprocessing import cpu_count
from pathlib import Path
from diot import Diot
from simpleconf import Config
from .plugin import config_plugins, pluginmgr, PMNAME
from .runner import runnermgr, RMNAME, register_runner

# priority: lowest -> highest
DEFAULT_CFGFILES = (Path('~/.PyPPL.toml').expanduser(), Path('./.PyPPL.toml'),
                    'PYPPL.osenv')

# default configurations
DEFAULT_CONFIG = dict(default=dict(
    # plugins
    plugins=[],
    # logger options
    logger=dict(file=None, theme='green_on_black', level='info',
                leveldiffs=[]),
    # The cache option, True/False/export
    cache=True,
    # Whether expand directory to check signature
    dirsig=True,
    # How to deal with the errors
    # retry, ignore, halt
    # halt to halt the whole pipeline, no submitting new jobs
    # terminate to just terminate the job itself
    errhow='terminate',
    # How many times to retry to jobs once error occurs
    errntry=3,
    # The directory to export the output files
    forks=1,
    # Default shell/language
    lang='bash',
    # number of threads used to build jobs and to check job cache status
    nthread=min(int(cpu_count() / 2), 16),
    # Where cache file and workdir located
    ppldir='./workdir',
    # Select the runner
    runner='local',
    # The tag of the job
    tag='notag',
    # The template engine (name)
    template='liquid',
    # The template environment
    envs=Diot(),
    # configs for plugins
    config={},
))

config = Config()  # pylint: disable=invalid-name

def _config_factory(conf):
    """The factory to convert runner to a dict"""
    # we have profiles
    for _, con in conf.items():
        if 'runner' not in con or isinstance(con['runner'], dict):
            continue
        # you can't set profile in config, so it's direct runner
        con['runner'] = {'runner': con['runner']}
    return conf

def load_config(default_config, *config_files):
    """@API
    Load the configurations
    @params:
        default_config (dict|path): A configuration dictionary or
              a path to a configuration file
        *config_files: A list of configuration or configuration files
    """
    config.clear()
    config._load(DEFAULT_CONFIG, default_config, *config_files,
                 factory=_config_factory)

load_config(*DEFAULT_CFGFILES)
pluginmgr.load_setuptools_entrypoints(PMNAME)
runnermgr.load_setuptools_entrypoints(RMNAME)
for runner in runnermgr.get_plugins():
    # save runners in memory
    register_runner(runner)
config_plugins(*config.plugins)
# deprecate this, since at this point, no plugins are loaded yet
pluginmgr.hook.setup(config=config)
