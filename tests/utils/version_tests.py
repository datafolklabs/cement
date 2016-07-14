"""Tests for cement.utils.version."""

from cement.utils import version, test


class VersionUtilsTestCase(test.CementCoreTestCase):

    def test_get_version(self):
        ver = version.get_version()
        self.ok(ver.startswith('2.10'))

        ver = version.get_version((2, 1, 1, 'alpha', 1))
        self.eq(ver, '2.1.1a1')

        ver = version.get_version((2, 1, 2, 'beta', 2))
        self.eq(ver, '2.1.2b2')

        ver = version.get_version((2, 1, 2, 'rc', 3))
        self.eq(ver, '2.1.2c3')

        ver = version.get_version((2, 1, 3, 'final', 0))
        self.eq(ver, '2.1.3')
