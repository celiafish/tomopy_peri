#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    Copyright 2014-2015 Dake Feng, Peri LLC, dakefeng@gmail.com
#
#    This file is part of TomograPeri.
#
#    TomograPeri is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TomograPeri is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with TomograPeri.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import os
import ctypes

# --------------------------------------------------------------------

# Get the shared library.
if os.name == 'nt':
    libpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib/pml_cuda.dll'))
    librecon_cuda = ctypes.CDLL(libpath)
else:
    libpath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', 'lib/pml_cuda.so'))
    librecon_cuda = ctypes.CDLL(libpath)

# --------------------------------------------------------------------

def pml_cuda(data, theta, center, num_grid, iters, beta, init_matrix):
    """
    Applies Accelerated Penalized Maximum-Likelihood (APML)
    method to obtain reconstructions, with GPGPU acceleration support.
    
    It is based on standard decoupled surrogate functions
    for the ML objective function assuming a Poisson model and 
    decoupled surrogate functions for a certain class of 
    penalty functions [1].
    
    Needs NVIDIA CUDA sm2.0+  hardware platform. Please build libpml_cuda 
    first. (Peri http://www.perillc.com)
    
    Parameters
    ----------
    data : ndarray, float32
        3-D tomographic data with dimensions:
        [projections, slices, pixels]
        
    theta : ndarray, float32
        Projection angles in radians.
        
    center : scalar, float32
        Pixel index corresponding to the 
        center of rotation axis.
        
    num_grid : scalar, int32
        Grid size of the econstructed images.
        
    iters : scalar int32
        Number of mlem iterations.
       
    beta : scalar, float32
        Regularization parameter. Determines the 
        amount of regularization.
    
    init_matrix : ndarray
       Initial guess for the reconstruction. Its
       shape is the same as the reconstructed data.
       
    Returns
    -------
    output : ndarray
        Reconstructed data with dimensions:
        [slices, num_grid, num_grid]

    References
    ----------
    - `IEEE-TMI, Vol 23(9), 1165-1175(2004) \
    <http://dx.doi.org/10.1109/TMI.2004.831224>`_
    """
    num_projections = np.array(data.shape[0], dtype='int32')
    num_slices = np.array(data.shape[1], dtype='int32')
    num_pixels = np.array(data.shape[2], dtype='int32')

    # Call C function.
    c_float_p = ctypes.POINTER(ctypes.c_float)
    librecon_cuda.pml_cuda.restype = ctypes.POINTER(ctypes.c_void_p)
    librecon_cuda.pml_cuda(data.ctypes.data_as(c_float_p),
                  theta.ctypes.data_as(c_float_p),
                  ctypes.c_float(center),
                  ctypes.c_int(num_projections),
                  ctypes.c_int(num_slices),
                  ctypes.c_int(num_pixels),
                  ctypes.c_int(num_grid),
                  ctypes.c_int(iters),
                  ctypes.c_float(beta),
                  init_matrix.ctypes.data_as(c_float_p))
    return init_matrix
