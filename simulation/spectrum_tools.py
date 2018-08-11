
import lmfit.lineshapes as lineshapes
import bisect
import numpy as np


def add_gauss(xxx, yyy, line, sigma):
    index_left = bisect.bisect_left(xxx, line.freq - 5 * sigma)
    index_right = bisect.bisect_left(xxx, line.freq + 5 * sigma)

    peak = lineshapes.gaussian(x=xxx[index_left:index_right],
                               center=line.freq, sigma=sigma,
                               amplitude=np.sqrt(2 * np.pi) * max(1.e-15, sigma))

    yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], peak)


def add_impulse(xxx, yyy, line, sigma):
    index_left = bisect.bisect_left(xxx, line.freq - sigma)
    index_right = bisect.bisect_left(xxx, line.freq + sigma)

    peak = np.ones(xxx[index_left:index_right].shape)
    yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], peak)


def make_grid(min_freq, max_freq, resolution):
    return np.arange(min_freq, max_freq, resolution)


def make_spectrum(linelist, sigma, xxx, add_peak_function):
    yyy = np.zeros(xxx.shape)
    for line in linelist:
        add_peak_function(xxx, yyy, line, sigma)
    return yyy


def make_rotor_spectrum(rotor, min_freq, max_freq, params):
    xxx = make_grid(min_freq, max_freq, params.resolution)
    yyy = make_spectrum(rotor.sim_lines, params.sigma, xxx, add_peak_function=add_gauss)
    return yyy * params.intensity_factor