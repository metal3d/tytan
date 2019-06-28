"""Jupyter and conda management"""

import json
import os
import subprocess
import socket
import time
from threading  import Thread
from queue import Queue
import sys

CONDA_ENV_NAME = "TyTan"
CONDA_EXE_NAME = "conda"


def __endqueue(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    # finally...
    queue.put(None)
    out.close()



def check_conda() -> bool:
    """True if conda is found in path"""
    return True in [os.path.exists("%s/%s" % (p, CONDA_EXE_NAME)) \
        for p in os.environ.get('PATH', '').split(':')]


def conda_env_installed() -> bool:
    """Check if conda environment is installed"""
    ret = subprocess.run(["conda", "env", "list", "--json"], capture_output=True)
    envs = json.loads(ret.stdout)

    for env in envs.get('envs', []):
        print("checking", env)
        if '/%s' % CONDA_ENV_NAME in env:
            return True

    return False

def init_conda() -> Queue:
    """Initialize a conda environment to install jupyterlab"""
    # no __titan env, do it now
    installer = subprocess.Popen([
        "conda", "create",
        "--name", CONDA_ENV_NAME,
        "-y",
        "jupyterlab",
        "nb_conda_kernels"
    ], stdout=subprocess.PIPE, bufsize=1, close_fds='posix' in sys.builtin_module_names)

    q = Queue()
    t = Thread(target=__endqueue, args=(installer.stdout, q))
    t.daemon = True
    t.start()
    return q

def wait_for_port(
        host: str = 'localhost',
        port: int = 8888,
    ):
    """Wait for the JupyterLab port to be opened"""

    timeout = 10
    maxtry = 6
    tries = 0
    print(host, port)
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as error:
            if tries >= maxtry:
                raise error
            time.sleep(1)
            tries += 1

def start_jupyter(
        host: str = 'localhost',
        port: str = 8888,
    ):
    """Start jupyter"""

    # the script to launch
    script = """
    source ~/.bashrc;
    conda activate {environment};
    jupyter-lab --host={host} --port={port} \
            --no-browser --LabApp.token='' &
    echo $! > /tmp/jupyter-{port}.pidfile;
    """.format(
        host=host,
        port=port,
        environment=CONDA_ENV_NAME,
    )

    subprocess.Popen(script, shell=True)
    print("Jupyter is launched")

def stop_jupyter(port: int = 8888):
    """Stop jupyter right now"""
    pidfile = '/tmp/jupyter-%d.pidfile' % port

    with open(pidfile, 'r') as pid:
        pidid = int(pid.read())

        try:
            os.kill(pidid, 9)
        except ProcessLookupError:
            print("Jupyter pid %d not found, maybe was stopped earlier" % pidid)

    os.remove(pidfile)

if __name__ == "__main__":
    init_conda()
