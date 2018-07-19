
from .converters import *


def get_fit_rms(str_fit_filename):
    rms_fit = None
    with open(str_fit_filename) as f:
        for line in reversed(f.readlines()):
            line = line.strip()
            if line[11:14] == "RMS":
                rms_fit = float(line[21:32])

    return rms_fit


def __write_parvar_header(rotor, max_lines=2000, max_error=1.0E+005, max_iters=10):
    text = ""
    text += "%s \n" % rotor.name
    text += ("   %d  %d   %d    0    0.000E+000   %.4e    1.0000E+000 1.0000000000\n" %
             (len(rotor.params), max_lines, max_iters, max_error))
    text += rotor.extended['pickett_header']
    return text


def load_int(str_filename, rotor):
    with open(str_filename, "r") as fh:
        for i, line in enumerate(fh):
            if i == 0:
                if not rotor.name:
                    rotor.name = line.strip()
            if i == 1:
                line_lst = line.strip().split()
                rotor.flag_wavenumbers = bool(line_lst[0] % 1000)
                if not rotor.tag:
                    rotor.tag = int(line_lst[1])
            if i >= 2:
                line_lst = line.strip().split()
                axis = int(line_lst[0])
                if axis == 1:
                    rotor.u_A = float(line_lst[1])
                elif axis == 2:
                    rotor.u_B = float(line_lst[1])
                elif axis == 3:
                    rotor.u_C = float(line_lst[1])
    return rotor


def save_int(str_filename, rotor, J_min=0, J_max=100, inten=-15.0, max_freq=150.0, temperature=300.0):
    input_file = ""
    input_file += "%s \n" % rotor.name
    input_file += ("%1d  %d  %f  %3d  %3d  %f  %f  %f  %f\n" %
                   (int(rotor.flag_wavenumbers)*1000, 0, rotor.Q(temperature),
                    J_min, J_max, inten, inten, max_freq, temperature))

    if rotor.mu_A:
        input_file += " 001  %f \n" % rotor.mu_A

    if rotor.mu_B:
        input_file += " 002  %f \n" % rotor.mu_B

    if rotor.mu_C:
        input_file += " 003  %f \n" % rotor.mu_C

    with open(str_filename, "w") as fh:
        fh.write(input_file)


def save_par(str_filename, rotor):
    text = __write_parvar_header(rotor)

    for param in rotor.params.values():
        if param.flag_enabled:
            text += ParameterConverter.obj_to_par_str(param)

    with open(str_filename, 'w') as f:
        f.write(text)


def save_var(str_filename, rotor):
    text = __write_parvar_header(rotor)

    for param in rotor.params.values():
        if param.flag_enabled:
            text += ParameterConverter.obj_to_var_str(param)

    with open(str_filename, 'w') as f:
        f.write(text)


def load_par(str_filename, rotor):
    with open(str_filename, 'r') as f:
        _ = f.readline()
        _ = f.readline()
        _ = f.readline()
        for line, param in zip(f, rotor.params.values()):
            ParameterConverter.par_str_to_obj(line, param)


def load_var(str_filename, rotor):
    with open(str_filename, 'r') as f:
        _ = f.readline()
        _ = f.readline()
        _ = f.readline()
        for line, param in zip(f, rotor.params.values()):
            ParameterConverter.var_str_to_obj(line, param)


def get_quantum_fmt(str_filename):
    """Get the FMT from .cat file"""
    int_quanta_fmt = None
    with open(str_filename, 'r') as f:
        str_line = f.readline()
        obj_line = CatConverter.str2line(str_line)
        int_quanta_fmt = obj_line.int_fmt

    return int_quanta_fmt


def load_cat(str_filename):
    """Read from .cat"""
    lst_lines = []
    with open(str_filename, 'r') as f:
        for str_line in f:
            try:
                obj = CatConverter.str2line(str_line)
            except ValueError:
                return []

            lst_lines.append(obj)

    return lst_lines


def save_cat(str_filename, lst_lines):
    """docstring"""
    with open(str_filename, 'w') as f:
        for obj_line in lst_lines:
            textline = CatConverter.line2str(obj_line)
            f.write(textline + "\n")


def load_lin(str_filename, int_quanta_fmt):
    """Read from .cat"""
    lst_lines = []
    with open(str_filename, 'r') as f:
        for i, str_line in enumerate(f):
            try:
                obj = LinConverter.str2line(str_line, int_quanta_fmt)
                lst_lines.append(obj)
            except ValueError:
                print('Warning: skipping bad line %i' % (i + 1))

    return lst_lines


def load_pgo_lin(str_filename, int_quanta_fmt):
    """Read from .cat"""
    lst_lines = []
    with open(str_filename, 'r') as f:
        for i, str_line in enumerate(f):
            try:
                obj = PGopherLinConverter.str2line(str_line, int_quanta_fmt)
                lst_lines.append(obj)
            except ValueError:
                print('Warning: skipping bad line %i' % (i + 1))

    return lst_lines


def save_lin(str_filename, lst_lines):
    """docstring"""
    with open(str_filename, 'w') as f:
        for obj_line in lst_lines:
            textline = LinConverter.line2str(obj_line)
            f.write(textline + "\n")


def load_egy(str_filename, int_quanta_fmt):
    """Read from .egy"""
    lst_states = []
    with open(str_filename, 'r') as f:
        for str_state in f:
            obj = EgyConverter.str2state(str_state, int_quanta_fmt)
            lst_states.append(obj)

    return lst_states


def save_egy(str_filename, lst_states):
    """docstring"""
    with open(str_filename, 'w') as f:
        for obj_state in lst_states:
            textline = EgyConverter.state2str(obj_state)
            f.write(textline + "\n")