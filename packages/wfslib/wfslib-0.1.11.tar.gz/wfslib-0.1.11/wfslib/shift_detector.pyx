# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:00:47 2020

@author: mi
"""

from cython.parallel import prange
import numpy as np
cimport numpy as np
#cimport wfs.Frame as Frame

ctypedef np.float_t DTYPE_t

cpdef tuple[int] translation(DTYPE_t[:]  ref1, DTYPE_t[:]  ref2):
    s = np.abs(np.fft.ifft2(np.fft.fft2(ref1) * np.conjugate(np.fft.fft2(ref2))))
    x, y = np.where(s == np.min(s))
    return x, y

cpdef list translations(DTYPE_t[:] subs, DTYPE_t[:] ref):
    cdef list offsets = []
    cdef list ofst = [2,2]
    cdef int i
    cdef int maxi = len(subs)
    cdef x, y
    x = 0    
    y = 0
    cdef DTYPE_t s
    for i in prange(maxi, nogil=True):
           # ofst = translation(subs[i], ref)
            s = np.abs(np.fft.ifft2(np.fft.fft2(subs[i]) * np.conjugate(np.fft.fft2(ref))))
            x, y = np.where(s == np.min(s))
            offsets.append(ofst)
    return offsets