from __future__ import absolute_import, division, print_function
import unittest

__metaclass__ = type


class AddTester(unittest.TestCase):
    a = 10
    b = 23

    # this function will
    def test_add(self):
        c = 33
        assert self.a + self.b == c

    # this function will
    def test_subtract(self):
        c = -13
        assert self.a - self.b == c
