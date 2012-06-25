import doctest
import unittest

import pghstore
from tests.dumps import DumpsTests
from tests.loads import LoadsTests


tests = unittest.TestSuite()
loader = unittest.TestLoader()
tests.addTest(loader.loadTestsFromTestCase(DumpsTests))
tests.addTest(loader.loadTestsFromTestCase(LoadsTests))
tests.addTests(doctest.DocTestSuite(pghstore))

