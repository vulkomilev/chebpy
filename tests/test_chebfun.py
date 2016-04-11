# -*- coding: utf-8 -*-
"""
Unit-tests for pyfun/chebtech.py
"""
from __future__ import division

#from itertools import combinations
from unittest import TestCase

#from operator import __add__
#from operator import __sub__
#from operator import __pos__
#from operator import __neg__
#from operator import __mul__

#from numpy import arange
from numpy import array
#from numpy import sin
#from numpy import cos
from numpy import exp
from numpy import sum
#from numpy import pi
#from numpy import all
#from numpy import diff
#from numpy import linspace
#from numpy.random import rand
#from numpy.random import seed
#
#from matplotlib.pyplot import subplots

from pyfun.settings import DefaultPrefs
from pyfun.bndfun import Bndfun
from pyfun.utilities import Subdomain

from pyfun.chebfun import Chebfun
from pyfun.chebfun import verify
from pyfun.chebfun import breakdata

from pyfun.exceptions import SubdomainGap
from pyfun.exceptions import SubdomainOverlap
from pyfun.exceptions import BadDomainArgument
from pyfun.exceptions import BadFunLengthArgument

#from utilities import testfunctions
from utilities import infnorm
#from utilities import scaled_tol
#from utilities import infNormLessThanTol

eps = DefaultPrefs.eps


# ------------------------
class Auxilliary(TestCase):
    """Unit-tests for Chebtech2"""

    def setUp(self):
        f = lambda x: exp(x)
        self.fun0 = Bndfun.initfun_adaptive(f, Subdomain(-1,0) )
        self.fun1 = Bndfun.initfun_adaptive(f, Subdomain(0,1) )
        self.fun2 = Bndfun.initfun_adaptive(f, Subdomain(-.5,0.5) )
        self.fun3 = Bndfun.initfun_adaptive(f, Subdomain(2,2.5) )
        self.fun4 = Bndfun.initfun_adaptive(f, Subdomain(-3,-2) )
        self.funs_a = array([self.fun1, self.fun0, self.fun2])
        self.funs_b = array([self.fun1, self.fun2])       
        self.funs_c = array([self.fun0, self.fun3])
        self.funs_d = array([self.fun1, self.fun4])

    def test_verify_empty(self):
        funs = verify(array([]))
        self.assertTrue(funs.size==0)

    def test_verify_contiguous(self):
        funs = verify(array([self.fun0, self.fun1]))
        self.assertTrue(funs[0]==self.fun0)
        self.assertTrue(funs[1]==self.fun1)

    def test_verify_sort(self):
        funs = verify(array([self.fun1, self.fun0]))
        self.assertTrue(funs[0]==self.fun0)
        self.assertTrue(funs[1]==self.fun1)
    
    def test_verify_overlapping(self):
        self.assertRaises(SubdomainOverlap, verify, self.funs_a)
        self.assertRaises(SubdomainOverlap, verify, self.funs_b)

    def test_verify_gap(self):
        self.assertRaises(SubdomainGap, verify, self.funs_c)
        self.assertRaises(SubdomainGap, verify, self.funs_d)

    def test_breakdata_empty(self):
        breaks = breakdata(array([]))
        self.assertTrue(array(breaks.items()).size==0)

    def test_breakdata_1(self):
        funs = array([self.fun0])
        breaks = breakdata(funs)
        x, y = breaks.keys(), breaks.values()
        self.assertLessEqual(infnorm(x-array([-1,0])), eps)
        self.assertLessEqual(infnorm(y-array([exp(-1),exp(0)])), 2*eps) 

    def test_breakdata_2(self):
        funs = array([self.fun0, self.fun1])
        breaks = breakdata(funs)
        x, y = breaks.keys(), breaks.values()
        self.assertLessEqual(infnorm(x-array([-1,0,1])), eps)
        self.assertLessEqual(infnorm(y-array([exp(-1),exp(0),exp(1)])), 2*eps) 

      
class Construction(TestCase):

    def setUp(self):
        f = lambda x: exp(x)
        self.f = f
        self.fun0 = Bndfun.initfun_adaptive(f, Subdomain(-1,0) )
        self.fun1 = Bndfun.initfun_adaptive(f, Subdomain(0,1) )
        self.fun2 = Bndfun.initfun_adaptive(f, Subdomain(-.5,0.5) )
        self.fun3 = Bndfun.initfun_adaptive(f, Subdomain(2,2.5) )
        self.fun4 = Bndfun.initfun_adaptive(f, Subdomain(-3,-2) )
        self.funs_a = array([self.fun1, self.fun0, self.fun2])
        self.funs_b = array([self.fun1, self.fun2])
        self.funs_c = array([self.fun0, self.fun3])
        self.funs_d = array([self.fun1, self.fun4])

    def test__init__pass(self):
        Chebfun([self.fun0])
        Chebfun([self.fun1])
        Chebfun([self.fun2])
        Chebfun([self.fun0, self.fun1])

    def test__init__fail(self):
        self.assertRaises(SubdomainOverlap, Chebfun, self.funs_a)
        self.assertRaises(SubdomainOverlap, Chebfun, self.funs_b)
        self.assertRaises(SubdomainGap, Chebfun, self.funs_c)
        self.assertRaises(SubdomainGap, Chebfun, self.funs_d)

    def test__init__empty(self):
        emptyfun = Chebfun.initempty()
        self.assertEqual(emptyfun.funs.size, 0)

#    def test_initfun_adaptive_default_domain(self):
#        ff = Chebfun.initfun_adaptive(self.f)
#        self.assertEqual(ff.funs.size, 1)
#        a, b = ff.breaks.keys()
#        fa, fb, = ff.breaks.values()
#        self.assertEqual(a,-1)
#        self.assertEqual(b, 1)
#        self.assertLessEqual(abs(fa-self.f(-1)), eps)
#        self.assertLessEqual(abs(fb-self.f(1)), 2*eps)

    def test_initfun_adaptive_continuous_domain(self):
        ff = Chebfun.initfun_adaptive(self.f, [-2,-1])
        self.assertEqual(ff.funs.size, 1)
        a, b = ff.breaks.keys()
        fa, fb, = ff.breaks.values()
        self.assertEqual(a,-2)
        self.assertEqual(b,-1)
        self.assertLessEqual(abs(fa-self.f(-2)), eps)
        self.assertLessEqual(abs(fb-self.f(-1)), eps)

    def test_initfun_adaptive_piecewise_domain(self):
        ff = Chebfun.initfun_adaptive(self.f, [-2,0,1])
        self.assertEqual(ff.funs.size, 2)
        a, b, c = ff.breaks.keys()
        fa, fb, fc = ff.breaks.values()
        self.assertEqual(a,-2)
        self.assertEqual(b, 0)
        self.assertEqual(c, 1)
        self.assertLessEqual(abs(fa-self.f(-2)), eps)
        self.assertLessEqual(abs(fb-self.f( 0)), eps)
        self.assertLessEqual(abs(fc-self.f( 1)), 2*eps)

    def test_initfun_adaptive_raises(self):
        initfun = Chebfun.initfun_adaptive
        self.assertRaises(BadDomainArgument, initfun, self.f, [-2])
        self.assertRaises(BadDomainArgument, initfun, self.f, domain=[-2])
        self.assertRaises(BadDomainArgument, initfun, self.f, domain=None)

    def test_initfun_fixedlen_continuous_domain(self):
        ff = Chebfun.initfun_fixedlen(self.f, [-2,-1], 20)
        self.assertEqual(ff.funs.size, 1)
        a, b = ff.breaks.keys()
        fa, fb, = ff.breaks.values()
        self.assertEqual(a,-2)
        self.assertEqual(b,-1)
        self.assertLessEqual(abs(fa-self.f(-2)), eps)
        self.assertLessEqual(abs(fb-self.f(-1)), eps)

    def test_initfun_fixedlen_piecewise_domain_0(self):
        ff = Chebfun.initfun_fixedlen(self.f, [-2,0,1], 30)
        self.assertEqual(ff.funs.size, 2)
        a, b, c = ff.breaks.keys()
        fa, fb, fc = ff.breaks.values()
        self.assertEqual(a,-2)
        self.assertEqual(b, 0)
        self.assertEqual(c, 1)
        self.assertLessEqual(abs(fa-self.f(-2)), 3*eps)
        self.assertLessEqual(abs(fb-self.f( 0)), 3*eps)
        self.assertLessEqual(abs(fc-self.f( 1)), 3*eps)

    def test_initfun_fixedlen_piecewise_domain_1(self):
        ff = Chebfun.initfun_fixedlen(self.f, [-2,0,1], [30,20])
        self.assertEqual(ff.funs.size, 2)
        a, b, c = ff.breaks.keys()
        fa, fb, fc = ff.breaks.values()
        self.assertEqual(a,-2)
        self.assertEqual(b, 0)
        self.assertEqual(c, 1)
        self.assertLessEqual(abs(fa-self.f(-2)), 3*eps)
        self.assertLessEqual(abs(fb-self.f( 0)), 3*eps)
        self.assertLessEqual(abs(fc-self.f( 1)), 6*eps)

    def test_initfun_fixedlen_raises(self):
        initfun = Chebfun.initfun_fixedlen
        self.assertRaises(BadDomainArgument, initfun, self.f, [-2], 10)
        self.assertRaises(BadDomainArgument, initfun, self.f, domain=[-2], n=10)
        self.assertRaises(BadDomainArgument, initfun, self.f, domain=None, n=10)
        self.assertRaises(BadFunLengthArgument, initfun, self.f, [-1,1], [30,40])
        self.assertRaises(TypeError, initfun, self.f, [-1,1], None)

    def test_initfun_fixedlen_succeeds(self):
        self.assertTrue(Chebfun.initfun_fixedlen(self.f, [-2,-1,0], []).isempty)
        # check that providing a vector with None elements calls the
        # Tech adaptive constructor
        g0 = Chebfun.initfun_adaptive(self.f, [-2,-1,0])
        g1 = Chebfun.initfun_fixedlen(self.f, [-2,-1,0], [None,None])
        g2 = Chebfun.initfun_fixedlen(self.f, [-2,-1,0], [None,40])
        for fun1, fun2 in zip(g1,g0):
            self.assertEqual(sum(fun1.coeffs()-fun2.coeffs()), 0)
        self.assertEqual(sum(g2.funs[0].coeffs()-g0.funs[0].coeffs()), 0)

# ------------------------------------------------------------------------
# Tests to verify the mutually inverse nature of vals2coeffs and coeffs2vals
# ------------------------------------------------------------------------
#def vals2coeffs2valsTester(n):
#    def asserter(self):
#        values = rand(n)
#        coeffs = _vals2coeffs(values)
#        _values_ = _coeffs2vals(coeffs)
#        self.assertLessEqual( infnorm(values-_values_), scaled_tol(n) )
#    return asserter
#
#def coeffs2vals2coeffsTester(n):
#    def asserter(self):
#        coeffs = rand(n)
#        values = _coeffs2vals(coeffs)
#        _coeffs_ = _vals2coeffs(values)
#        self.assertLessEqual( infnorm(coeffs-_coeffs_), scaled_tol(n) )
#    return asserter
#
#for k, n in enumerate(2**arange(2,18,2)+1):
#
#    # vals2coeffs2vals
#    _testfun_ = vals2coeffs2valsTester(n)
#    _testfun_.__name__ = "test_vals2coeffs2vals_{:02}".format(k)
#    setattr(ChebyshevPoints, _testfun_.__name__, _testfun_)
#
#    # coeffs2vals2coeffs
#    _testfun_ = coeffs2vals2coeffsTester(n)
#    _testfun_.__name__ = "test_coeffs2vals2coeffs_{:02}".format(k)
#    setattr(ChebyshevPoints, _testfun_.__name__, _testfun_)
# ------------------------------------------------------------------------

# reset the testsfun variable so it doesn't get picked up by nose
_testfun_ = None
