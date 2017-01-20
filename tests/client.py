import os
import time
import logging

from puppetbeacon.monitors import PuppetAgent

# Assume the `assets` directory is adjacent to the `tests` directory.
ASSETS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'assets')
)

logging.basicConfig(level=logging.DEBUG)

kwargs = {
    'summary_file': '/'.join([ASSETS_DIR, 'last_run_summary.yaml']),
    'run_lock': '/'.join([ASSETS_DIR, 'agent_catalog_run.lock']),
    # 'disabled_lock': '/'.join([ASSETS_DIR, 'agent_disabled.lock']),
    'disabled_lock': '/opt/puppetlabs/puppet/cache/state/agent_disabled.lock'
}


# TODO: Create context manager methods in a base class for wiring up
# puppet state files to mimic agent behavior.
def mimic_running_agent(path, operation='create'):
    run_lock = '/'.join([path, 'agent_catalog_run.lock'])
    if 'delete' in operation:
        os.remove(run_lock)
        return True

    with open(run_lock, 'w+') as f:
        f.write('12345')
        return True

    return False

puppet_agent = PuppetAgent(**kwargs)
mimic_running_agent(ASSETS_DIR)
time.sleep(3)
puppet_agent.get_last_run()
print puppet_agent.disabled
print puppet_agent.disabled_message
print puppet_agent.run_duration
print puppet_agent.events_failed
mimic_running_agent(ASSETS_DIR, operation='delete')
