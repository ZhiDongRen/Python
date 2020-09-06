import sys
import unittest
import test1
import test2
import test3
import test4
import test5
import test6
import test7
import test8
import test9



class Test_Suite(unittest.TestCase):

    def test_main(self):

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(test1.Test1),
            unittest.defaultTestLoader.loadTestsFromTestCase(test2.Test2),
            unittest.defaultTestLoader.loadTestsFromTestCase(test3.Test3),
            unittest.defaultTestLoader.loadTestsFromTestCase(test4.Test4),
            unittest.defaultTestLoader.loadTestsFromTestCase(test5.Test5),
            unittest.defaultTestLoader.loadTestsFromTestCase(test6.Test6),
            unittest.defaultTestLoader.loadTestsFromTestCase(test7.Test7),
            unittest.defaultTestLoader.loadTestsFromTestCase(test8.Test8),
            unittest.defaultTestLoader.loadTestsFromTestCase(test9.Test9),
            ])
        runner = unittest.TextTestRunner()
        runner.run (self.suite)

import unittest
if __name__ == "__main__":
    unittest.main()