import unittest

from testlib.testcase import BaseTestCase
from puppetbeacon.monitors import PuppetAgent


class BasicTestSuite(BaseTestCase):
    """Basic test cases."""

    def test_object_instantion_completes_successfully(self):
        puppet_agent = PuppetAgent()
        stuff = self.asset_filename('last_run_summary.yaml')
        assert puppet_agent is not None


if __name__ == '__main__':
    unittest.main()
