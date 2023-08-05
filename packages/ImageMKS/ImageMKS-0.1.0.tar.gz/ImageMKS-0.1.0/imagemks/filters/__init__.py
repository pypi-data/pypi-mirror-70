from .fftedges import local_avg
from .fftgaussian import fftgauss
from .morphological import smooth_binary
from ._fftconvolve import fftconvolve2d

__all__ = ['local_avg',
           'fftgauss',
           'smooth_binary',
           'fftconvolve2d']
