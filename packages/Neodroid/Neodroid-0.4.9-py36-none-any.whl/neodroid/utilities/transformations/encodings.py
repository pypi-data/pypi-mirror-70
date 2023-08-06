#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Iterable

__author__ = "Christian Heider Nielsen"

import numpy

__doc__ = r"""
"""

__all__ = ["signed_ternary_encoding", "to_one_hot", "agg_double_list"]


def signed_ternary_encoding(*, size: int, index: int):
    """

    @param size:
    @type size:
    @param index:
    @type index:
    @return:
    @rtype:
    """
    # assert isinstance(size,(int,numpy.int64)), f'size was {type(size)}'
    # assert isinstance(index,(int,numpy.int64)), f'index was {type(index)}'
    # assert size*2 > index, f'signed size was {size*2}, index was {index}'

    if not isinstance(index, Iterable):
        index = [index]
    acs = []
    for i in index:
        a = numpy.zeros(size)
        if i < 0:
            return a
        elif 0 <= i < size:
            a[i] = 1
        elif size <= i < size * 2:
            a[i - size] = -1
        acs.append(a)
    return acs


def to_one_hot(dims, index):
    """

    @param dims:
    @type dims:
    @param index:
    @type index:
    @return:
    @rtype:
    """
    if not isinstance(index, Iterable):
        index = [index]
    acs = []
    for i in index:
        if isinstance(i, numpy.int) or isinstance(i, numpy.int64) or isinstance(i, int):
            one_hot = numpy.zeros(dims)
            one_hot[i] = 1.0
        else:
            one_hot = numpy.zeros((len(i), dims))
            one_hot[numpy.arange(len(i)), i] = 1.0
        acs.append(one_hot)

    return acs


def agg_double_list(l):
    """

    @param l:
    @type l:
    @return:
    @rtype:
    """
    # l: [ [...], [...], [...] ]
    # l_i: result of each step in the i-th episode
    s = [numpy.sum(numpy.array(l_i), 0) for l_i in l]
    s_mu = numpy.mean(numpy.array(s), 0)
    s_std = numpy.std(numpy.array(s), 0)
    return s_mu, s_std


if __name__ == "__main__":
    a_size = 2
    a_index = 0
    print(signed_ternary_encoding(size=a_size, index=a_index))
