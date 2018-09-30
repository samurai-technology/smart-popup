import unittest

from DecisionHandlersTests import DecisionHandlersTests
from EncryptionServiceTests import EncryptionServiceTests
from HomeHandlersTests import HomeHandlersTests
from UserDaoTests import UserDaoTests
from UserHandlersTests import UserHandlersTests
from UserServiceTests import UserServiceTests

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(EncryptionServiceTests().get_suite())
    suite.addTests(UserDaoTests().get_suite())
    suite.addTests(UserServiceTests().get_suite())
    suite.addTests(HomeHandlersTests().get_suite())
    suite.addTests(UserHandlersTests().get_suite())
    suite.addTests(DecisionHandlersTests().get_suite())

    # MGR: Make sure DB is running
    unittest.TextTestRunner().run(suite)
