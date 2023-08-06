"""
Make runners as plugins for PyPPL
@variables:
    RMNAME (str): The name of the runner manager
    RUNNERS (dict): All ever registered runners
    DEFAULT_POLL_INTERVAL (int): The default poll interval to check job status
    hookimpl (pluggy.HookimplMarker): The marker for runner hook Implementations
    hookspec (pluggy.HookspecMarker): The marker for runner hooks
"""
# pylint: disable=unused-argument,invalid-name
import sys
import pluggy
import psutil
from .exception import (RunnerNoSuchRunner, RunnerMorethanOneRunnerEnabled,
                        RunnerTypeError)

RMNAME = "pyppl_runner"
# save all runners ever registered
RUNNERS = {}
# poll interval to check job status
DEFAULT_POLL_INTERVAL = 1

hookimpl = pluggy.HookimplMarker(RMNAME)
hookspec = pluggy.HookspecMarker(RMNAME)


@hookspec
def runner_init(proc):
    """@API
    RUNNER API
    Initiate runner
    @params:
        proc (Proc): The Proc instance
    """


@hookspec(firstresult=True)
def isrunning(job):
    """@API
    RUNNER API
    Tell if the job is running
    @params:
        job (Job): the job instance
    """


@hookspec(firstresult=True)
def submit(job):
    """@API
    RUNNER API
    Submit a job
    @params:
        job (Job): the job instance
    """


@hookspec(firstresult=True)
def kill(job):
    """@API
    RUNNER API
    Try to kill the job
    @params:
        job (Job): the job instance
    """


@hookspec(firstresult=True)
def script_parts(job, base):
    """@API
    RUNNER API
    Overwrite script parts
    @params:
        job (Job): the job instance
        base (Diot): The base script parts
    """


runnermgr = pluggy.PluginManager(RMNAME)
runnermgr.add_hookspecs(sys.modules[__name__])


def _runner_name(runner):
    if hasattr(runner, '__name__'):
        name = runner.__name__
    else:
        name = runner.__class__.__name__

    if name[:13] in ('pyppl_runner_', 'pyppl-runner-'):
        name = name[13:]
    elif name[:11] == 'PyPPLRunner':
        name = name[11:].lower()
    return name


def use_runner(runner):
    """@API
    runner should be a module or the name of a module,
    with or without "pyppl_runner_" prefix
    To enable a runner, we need to disable other runners
    @params:
        runner (str): the name of runner
    """
    if runner not in RUNNERS:
        raise RunnerNoSuchRunner(runner)
    for plugin in RUNNERS.values():
        if _runner_name(plugin) == runner:
            if not runnermgr.is_registered(plugin):
                runnermgr.register(plugin)
        elif runnermgr.is_registered(plugin):
            runnermgr.unregister(plugin)
    assert len(runnermgr.get_plugins()) == 1, (
        'One runner is allow at a time. We have {}'.format(
            runnermgr.get_plugins()
        )
    )


def current_runner():
    """@API
    Get current runner name
    @returns:
        (str): current runner name
    """
    all_runners = list(runnermgr.get_plugins())
    if len(all_runners) > 1:
        raise RunnerMorethanOneRunnerEnabled(str(all_runners))
    if not all_runners:
        raise RunnerNoSuchRunner('No runners registered.')

    for name, plugin in RUNNERS.items():
        if plugin is all_runners[0]:
            return name
    raise RunnerNoSuchRunner('No runners registered.')


def poll_interval():
    """@API
    Get the poll interval for current runner
    @returns:
        (int): poll interval for querying job status
    """
    runner = RUNNERS[current_runner()]
    if hasattr(runner, 'POLL_INTERVAL'):
        return int(runner.POLL_INTERVAL)
    return DEFAULT_POLL_INTERVAL


def register_runner(runner, name=None):
    """@API
    Register a runner
    @params:
        runner (callable): The runner, a module or a class object
        name (str): The name of the runner to registered
    """
    name = name or _runner_name(runner)
    if not runnermgr.is_registered(runner):
        # we only allow an object from one class to be registered once
        for plugin in runnermgr.get_plugins():
            if _runner_name(plugin) == name:
                raise RunnerTypeError(
                    'Runner %r has already been registered.' % (name))
        runnermgr.register(runner, name=name)
    RUNNERS[name] = runner

def killtree(pid, killme=True, signal=9):
    """Kill a process tree"""
    myself = psutil.Process(int(pid))
    children = myself.children(recursive=True)
    if killme:
        children.append(myself)
    for proc in children:
        proc.send_signal(signal)

    return bool(psutil.wait_procs(children))

class PyPPLRunnerLocal:
    """@API
    PyPPL's default runner"""
    # pylint: disable=no-self-use

    __version__ = 'builtin'

    @hookimpl
    def kill(self, job):
        """@API
        Try to kill the running jobs if I am exiting
        @params:
            job (Job): the job instance
        """
        if int(job.pid) > 0:
            return killtree(job.pid)
        return True

    @hookimpl
    def submit(self, job):
        """@API
        Try to submit the job
        @params:
            job (Job): the job instance
        """
        import cmdy
        cmd = cmdy._(*job.script[1:], _exe=job.script[0], _raise=False).iter
        cmd._rc = 0
        job.pid = cmd.pid
        return cmd

    @hookimpl
    def isrunning(self, job):
        """@API
        Try to tell whether the job is still running.
        @params:
            job (Job): the job instance
        @returns:
            `True` if yes, otherwise `False`
        """
        if not job.pid or int(job.pid) < 0:
            return False
        return psutil.pid_exists(int(job.pid))


register_runner(PyPPLRunnerLocal())
