import reusable


def clean_cypress():
    reusable.processes.kill_processes('cypress')
    reusable.processes.kill_processes('emulators pubsub')


def clean():
    clean_cypress()
