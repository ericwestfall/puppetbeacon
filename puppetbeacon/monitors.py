# -*- coding: utf-8 -*-
"""


"""

import logging
import os

import yaml

from .utils import get_timedelta, safe_get

LOG = logging.getLogger('puppetbeacon.monitor')


class AgentState(object):
    """Base class that provides an object for working with Puppet agent state.
    """

    def __init__(self, summary_file=None, run_lock=None, disabled_lock=None):
        self.summary_file = summary_file if summary_file is not None else \
            '/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml'
        self.run_lock = run_lock if run_lock is not None else \
            '/opt/puppetlabs/puppet/cache/state/agent_catalog_run.lock'
        self.disabled_lock = disabled_lock if disabled_lock is not None else \
            '/opt/puppetlabs/puppet/cache/state/agent_disabled.lock'

        self._disabled = None
        self.disabled_message = None

    @property
    def disabled(self):
        """docstring stuff"""

        try:
            with open(self.disabled_lock, 'r') as disabled_lock:
                LOG.debug('Located agent disabled lock at %s, looking ' +
                          'for an administrative message.', self.disabled_lock)
                self.disabled_message = \
                    safe_get(yaml.safe_load(disabled_lock), 'disabled_message')
                LOG.warning('Puppet agent has been administratively ' +
                            'disabled. Message: %s', self.disabled_message)
                return True
        except EnvironmentError:
            LOG.debug('No agent disabled lock present at %s, agent is ' +
                      'enabled.', self.disabled_lock)

        return False

    def get_run_summary(self):
        """Retrieves and deserializes last run summary data.
        """
        run_summary = None

        try:
            with open(self.summary_file, 'r') as summary_file:
                run_summary = yaml.safe_load(summary_file)
                LOG.debug('Successfully parsed Puppet agent summary data in ' +
                          'file %s', self.summary_file)
        except IOError as error:
            LOG.error('Unable to locate or open summary file %s. Error: %s',
                      self.summary_file, error)
        except yaml.YAMLError as error:
            LOG.error('Unable to parse summary file %s. Error: %s',
                      self.summary_file, error)

        return run_summary if run_summary else None


class PuppetAgent(AgentState):
    """Stuff and things.
    """

    def __init__(self, *args, **kwargs):
        AgentState.__init__(self, *args, **kwargs)

        self._run_duration = None
        self.last_run = None
        self.last_run_duration = None
        self.events_failed = None
        self.resources_failed = None
        self.resources_failed_restart = None

    @property
    def run_duration(self):
        """Gets run duration
        """
        run_duration = None

        try:
            run_duration = get_timedelta(os.path.getmtime(self.run_lock))
            LOG.debug('Located agent run lock at %s, Puppet agent has been ' +
                      'executing a configuration run for %s seconds.',
                      self.run_lock, run_duration)
        except OSError:
            LOG.debug('Puppet agent is not executing a configuration run.')

        return run_duration

    def get_last_run(self):
        """Gets last run.
        """
        run_summary = self.get_run_summary()

        if not run_summary:
            return False

        self.last_run = \
            get_timedelta(safe_get(run_summary, 'time', 'last_run'))
        self.last_run_duration = \
            int(safe_get(run_summary, 'time', 'total'))
        self.events_failed = safe_get(run_summary, 'events', 'failure')
        self.resources_failed = \
            safe_get(run_summary, 'resources', 'failed')
        self.resources_failed_restart = \
            safe_get(run_summary, 'resources', 'failed_to_restart')

        LOG.debug('Puppet agent last executed a configuration run ' +
                  '%s seconds ago and ran for %s seconds.', self.last_run,
                  self.last_run_duration)

        return True
