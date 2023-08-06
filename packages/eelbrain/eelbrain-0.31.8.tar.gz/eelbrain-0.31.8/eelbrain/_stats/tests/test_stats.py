# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
import warnings

import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pytest
import scipy.stats

from eelbrain import datasets
from eelbrain._stats import stats
from eelbrain._stats.permutation import permute_order, rand_rotation_matrices


def test_corr():
    "Test stats.corr"
    ds = datasets.get_uts()
    y = ds.eval("uts.x[:,:3]")
    x = ds.eval('Y.x')
    n_cases = len(y)
    df = n_cases - 2

    corr = stats.corr(y, x)
    p = stats.rtest_p(corr, df)
    for i in range(len(corr)):
        r_sp, p_sp = scipy.stats.pearsonr(y[:, i], x)
        assert corr[i] == pytest.approx(r_sp)
        assert p[i] == pytest.approx(p_sp)

    # NaN
    with warnings.catch_warnings():  # divide by 0
        warnings.simplefilter("ignore")
        assert stats.corr(np.arange(10), np.zeros(10)) == 0

    # perm
    y_perm = np.empty_like(y)
    for perm in permute_order(n_cases, 2):
        y_perm[perm] = y
        stats.corr(y, x, corr, perm)
        for i in range(len(corr)):
            r_sp, _ = scipy.stats.pearsonr(y_perm[:, i], x)
            assert corr[i] == pytest.approx(r_sp)


def test_lm():
    "Test linear model function against scipy lstsq"
    ds = datasets.get_uts(True)
    uts = ds['uts']
    utsnd = ds['utsnd']
    x = ds.eval("A*B")
    p = x._parametrize()
    n = ds.n_cases

    # 1d betas
    betas = stats.betas(uts.x, x)
    sp_betas = scipy.linalg.lstsq(p.x, uts.x.reshape((n, -1)))[0]
    # sp_betas = sp_betas.reshape((x.df,) + uts.shape[1:])
    assert_allclose(betas, sp_betas)

    # 2d betas
    betas = stats.betas(utsnd.x, x)
    sp_betas = scipy.linalg.lstsq(p.x, utsnd.x.reshape((n, -1)))[0]
    sp_betas = sp_betas.reshape((x.df,) + utsnd.shape[1:])
    assert_allclose(betas, sp_betas)


def test_variability():
    "Test variability functions"
    ds = datasets.get_loftus_masson_1994()
    y = ds['n_recalled'].x.astype(np.float64)
    x = ds['exposure'].as_factor()
    match = ds['subject']

    sem = scipy.stats.sem(y, 0, 1)
    ci = sem * scipy.stats.t.isf(0.05 / 2., len(y) - 1)

    # invalid spec
    with pytest.raises(ValueError):
        stats.variability(y, 0, 0, '1mile', 0)
    with pytest.raises(ValueError):
        stats.variability(y, 0, 0, 'ci7ci', 0)

    # standard error
    assert stats.variability(y, None, None, 'sem', False) == sem
    assert stats.variability(y, None, None, '2sem', False) == 2 * sem
    # within subject standard-error
    target = scipy.stats.sem(stats.residuals(y[:, None], match), 0, len(match.cells))[0]
    assert stats.variability(y, None, match, 'sem', True) == pytest.approx(target)
    assert stats.variability(y, None, match, 'sem', False) == pytest.approx(target)
    # one data point per match cell
    n = match.df + 1
    with pytest.raises(ValueError):
        stats.variability(y[:n], None, match[:n], 'sem', True)

    target = np.array([scipy.stats.sem(y[x == cell], 0, 1) for cell in x.cells])
    es = stats.variability(y, x, None, 'sem', False)
    assert_allclose(es, target)

    stats.variability(y, x, None, 'sem', True)

    # confidence intervals
    assert stats.variability(y, None, None, '95%ci', False) == pytest.approx(ci)
    assert stats.variability(y, x, None, '95%ci', True) == pytest.approx(3.86, abs=1e-2)  # L&M: 3.85
    assert stats.variability(y, x, match, '95%ci', True) == pytest.approx(0.52, abs=1e-2)

    assert_equal(stats.variability(y, x, None, '95%ci', False)[::-1],
                 stats.variability(y, x, None, '95%ci', False, x.cells[::-1]))


def test_t_1samp():
    "Test 1-sample t-test"
    ds = datasets.get_uts(True)

    y = ds['uts'].x
    t = scipy.stats.ttest_1samp(y, 0, 0)[0]
    assert_allclose(stats.t_1samp(y), t, 10)

    y = ds['utsnd'].x
    t = scipy.stats.ttest_1samp(y, 0, 0)[0]
    assert_allclose(stats.t_1samp(y), t, 10)


def test_t_ind():
    "Test independent samples t-test"
    ds = datasets.get_uts(True)
    y = ds.eval("utsnd.x")
    n_cases = len(y)
    n = n_cases // 2
    groups = (np.arange(n_cases) < n)
    groups.dtype = np.int8

    t = stats.t_ind(y, groups)
    p = stats.ttest_p(t, n_cases - 2)
    t_sp, p_sp = scipy.stats.ttest_ind(y[:n], y[n:])
    assert_allclose(t, t_sp)
    assert_allclose(p, p_sp)
    assert_allclose(stats.ttest_t(p, n_cases - 2), np.abs(t))

    # permutation
    y_perm = np.empty_like(y)
    for perm in permute_order(n_cases, 2):
        stats.t_ind(y, groups, out=t, perm=perm)
        y_perm[perm] = y
        t_sp, _ = scipy.stats.ttest_ind(y_perm[:n], y_perm[n:])
        assert_allclose(t, t_sp)


def test_vector():
    rotation = rand_rotation_matrices(4, 0)
    zeros = np.zeros((4, 3))
    assert stats.t2_1samp(zeros) == 0
    assert stats.t2_1samp(zeros, rotation) == 0
