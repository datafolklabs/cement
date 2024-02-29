
import os
import sys
import warnings
from cement.core.foundation import TestApp


class TestDeprecations(object):
    def test_3_0_8__1(self):
        os.environ['CEMENT_FRAMEWORK_LOGGING'] = '1'

        with TestApp() as app:
            with warnings.catch_warnings(record=True) as w:
                app.run()
                assert "3.0.8-1" in str(w[-1].message)

    def test_3_0_8__2(self):
        orig_argv = sys.argv
        sys.argv = ['--debug']

        with TestApp() as app:
            with warnings.catch_warnings(record=True) as w:
                app.run()
                assert "3.0.8-2" in str(w[-1].message)
        sys.argv = orig_argv

    def test_3_0_10__1(self):
        with TestApp() as app:
            with warnings.catch_warnings(record=True) as w:
                app.log.set_level('FATAL')
                assert "3.0.10-1" in str(w[-1].message)
