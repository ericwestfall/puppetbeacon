# tests/base.py

import os
import unittest
from unittest import TestCase

from puppetbeacon.monitors import PuppetAgent


class BaseTestCase(TestCase):
    """
    A base test case which mocks out the Puppet agent state files and lock
    files to prevent test failures when tests are executed on a machine without
    the puppet agent installed.

    All test cases should inherit from this class as any common
    functionality that is added here will then be available to all
    subclasses. This facilitates the ability to update in one spot
    and allow all tests to get the update for easy maintenance.
    """

    # Assume the `assets` dir is adjacent to the `tests` dir
    ASSETS_DIR = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
    )

    def asset_filename(self, path):
        """
        Given a path relative to the assets directory, returns the absolute
        path to the filename.
        """
        return os.path.normpath(os.path.join(self.ASSETS_DIR, path))


class BasicTestSuite(BaseTestCase):
    """Basic test cases."""

    def test_object_instantion_completes_successfully(self):
        puppet_agent = PuppetAgent()
        stuff = self.asset_filename('last_run_summary.yaml')
        assert puppet_agent is not None


if __name__ == '__main__':
    unittest.main()
