import signal
import subprocess
import os


def list_processes(contains=None):
    out = subprocess.check_output(['ps', '-aef'], universal_newlines=True)
    lines = out.splitlines()[1:]
    if contains is not None:
        lines = [line for line in lines if contains in line]
    return lines


def kill_processes(contains=None):
    lines = list_processes(contains=contains)
    for line in lines:
        pid = int(line.split(None, 2)[1])
        os.kill(pid, signal.SIGKILL)
        print(f'KILLED: {line}')