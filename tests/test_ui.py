# -*- coding: utf-8 -*-

import unittest
import numpy as np
from chebpy import chebfun
from chebpy.core.settings import DefaultPrefs

# check we get default domain for no domain argument

class chebfun_ui(unittest.TestCase):

    def test_null_args(self):
        self.assertTrue(chebfun().isempty)
        
    def test_callable(self):
        n = 100
        d = np.array([-2,0,1])
        f1 = chebfun(np.sin)
        f2 = chebfun(np.sin, d)
        f3 = chebfun(np.sin, n=n)
        f4 = chebfun(np.sin, d, n)
        
        # check domains
        self.assertTrue(f1.domain==DefaultPrefs.domain)
        self.assertTrue(f2.domain==d)
        self.assertTrue(f3.domain==DefaultPrefs.domain)
        self.assertTrue(f4.domain==d)
        
        # check lengths of f3 and f4
        self.assertEqual(f3.funs[0].size, n)
        self.assertTrue(np.all([fun.size==n for fun in f4]))

    def test_alphanum_char(self):
        n = 100
        d = np.array([-2,0,1])
        f1 = chebfun('x')
        f2 = chebfun('y', d)
        f3 = chebfun('z', n=n)
        f4 = chebfun('a', d, n)
        
        # check domains
        self.assertTrue(f1.domain==DefaultPrefs.domain)
        self.assertTrue(f2.domain==d)
        self.assertTrue(f3.domain==DefaultPrefs.domain)
        self.assertTrue(f4.domain==d)
        
        # check lengths of f3 and f4
        self.assertEqual(np.sum([fun.size for fun in f3]), n)
        self.assertTrue(np.all([fun.size==n for fun in f4]))
        
    def test_float_arg(self):
        d = np.array([-2,0,1])
        f1 = chebfun(3.14)
        f2 = chebfun('3.14')
        f3 = chebfun(2.72, d)
        f4 = chebfun('2.72', d)
        
        # check domains
        self.assertTrue(f1.domain==DefaultPrefs.domain)
        self.assertTrue(f2.domain==DefaultPrefs.domain)
        self.assertTrue(f3.domain==d)
        self.assertTrue(f4.domain==d)
        
        # check all are constant
        self.assertTrue(f1.isconst)
        self.assertTrue(f2.isconst)
        self.assertTrue(f3.isconst)
        self.assertTrue(f4.isconst)

    def test_raises(self):
        self.assertRaises(ValueError, chebfun, 'asdfasdf')
