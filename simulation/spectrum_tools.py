
import lmfit.lineshapes as lineshapes
import bisect
import numpy as np


def add_gauss(xxx, yyy, line, sigma):
    index_left = bisect.bisect_left(xxx, line.freq - 5 * sigma)
    index_right = bisect.bisect_left(xxx, line.freq + 5 * sigma)

    peak = lineshapes.gaussian(x=xxx[index_left:index_right],
                               center=line.freq, sigma=sigma,
                               amplitude=np.exp(line.log_I))  #amplitude=np.sqrt(2 * np.pi) * max(1.e-15, sigma))

    yyy[index_left:index_right] = yyy[index_left:index_right] + peak


def add_impulse(xxx, yyy, line, sigma):
    index_left = bisect.bisect_left(xxx, line.freq - sigma)
    index_right = bisect.bisect_left(xxx, line.freq + sigma)

    peak = np.ones(xxx[index_left:index_right].shape)
    yyy[index_left:index_right] = np.maximum(yyy[index_left:index_right], peak)


def make_grid(min_freq, max_freq, resolution):
    return np.arange(min_freq, max_freq, resolution)


def conditions_match(line, params):
    if not (params.min_freq <= line.freq <= params.max_freq):
        return False
    if not line.log_I >= params.threshold:
        return False
    J_upper = line.q_upper.get('J', line.q_upper.get('N', None))
    if J_upper and not (params.J_min <= J_upper <= params.J_max):
        return False
    Ka_upper = line.q_upper.get('Ka', line.q_upper.get('K', None))
    if Ka_upper and not (params.Ka_min <= Ka_upper <= params.Ka_max):
        return False
    Kc_upper = line.q_upper.get('Kc', line.q_upper.get('K', None))
    if Kc_upper and not (params.Kc_min <= Kc_upper <= params.Kc_max):
        return False
    return True

def make_spectrum(linelist, xxx, params, add_peak_function):
    yyy = np.zeros(xxx.shape)
    for line in linelist:
        if conditions_match(line, params):
            add_peak_function(xxx, yyy, line, params.sigma)
    return yyy


def make_rotor_spectrum(rotor, params):
    xxx = make_grid(params.min_freq, params.max_freq, params.resolution)
    yyy = make_spectrum(rotor.sim_lines, xxx, params, add_peak_function=add_gauss)
    return np.column_stack((xxx, yyy * params.intensity_factor))
