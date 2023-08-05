#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test model interface using C03 model."""

from numpy.testing import assert_array_equal, assert_allclose

from pygmm.model import Scenario
from pygmm import Campbell2003 as C03

import pytest


@pytest.fixture
def model():
    return C03(Scenario(mag=6.5, dist_rup=20))


def test_ln_std(model):
    assert_array_equal(model._ln_std, model.ln_stds)


def test_scenario():
    s = Scenario(mag=6, dist_jb=20)
    assert_allclose(s.mag, s['mag'])
    assert_allclose(s.dist_jb, s['dist_jb'])


@pytest.mark.parametrize(
    'attr', ['pga', 'ln_std_pga', 'pgv', 'ln_std_pgv', 'pgd', 'ln_std_pgd'])
def test_pga(model, attr):
    with pytest.raises(NotImplementedError):
        getattr(model, attr)
