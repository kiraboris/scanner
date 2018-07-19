
from bidict import bidict

from .db import quanta_headers, param_code
from ..entities.line import Line
from ..entities.state import State
from ..entities.rotor import RotorParameter


class CatConverter:
    """Manages entries of .cat files"""

    mapper = bidict([('a', '-1'), ('b', '-2'), ('c', '-3'), ('d', '-4'),
                     ('e', '-5'), ('P', '25'), ('f', '-6'), ('g', '-7'),
                     ('h', '-8'), ('i', '-9'), ('j', '-10'), ('k', '-11'),
                     ('l', '-12'), ('m', '-13'), ('n', '-14'), ('o', '-15'),
                     ('p', '-16'), ('A', '10'), ('B', '11'), ('C', '12'),
                     ('D', '13'), ('E', '14'), ('F', '15'), ('G', '16'),
                     ('H', '17'), ('I', '18'), ('J', '19'), ('K', '20'),
                     ('L', '21'), ('M', '22'), ('N', '23'), ('O', '24')])

    @staticmethod
    def __decode_quant(str_q):
        """replace a -> -1, A -> 10, etc."""

        str_s = str_q[0:1]
        if str_s in CatConverter.mapper:
            str_q = str_q.replace(str_s, CatConverter.mapper[str_s])

        return str_q

    @staticmethod
    def __encode_quant(str_q):
        """replace -1 -> a, 10 -> A, etc."""

        if len(str_q) >= 3:
            str_s = str_q[0:2]
            if str_s in CatConverter.mapper.inv:
                str_q = str_q.replace(str_s, CatConverter.mapper.inv[str_s])

        return str_q

    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .cat to dict
           returns (dict_upper, dict_lower)
        """
        dict_ql = {}
        dict_qu = {}

        count = 6
        for i in range(0, count):

            str_qu = str_quanta[i * 2: (i + 1) * 2]
            str_ql = str_quanta[(i + count) * 2: (i + count + 1) * 2]

            if str_qu != "  " and str_ql != "  ":
                str_qu = CatConverter.__decode_quant(str_qu)
                str_ql = CatConverter.__decode_quant(str_ql)

                headers = quanta_headers(int_fmt)
                dict_ql[headers[i]] = int(str_ql)
                dict_qu[headers[i]] = int(str_qu)
            else:
                break

        return dict_qu, dict_ql

    @staticmethod
    def __write_quanta(dict_qu, dict_ql, int_fmt):
        """convert quanta from (dict,dict) to .cat str"""

        count = 6
        str_quanta = ""

        headers = quanta_headers(int_fmt)[0:len(dict_qu)]
        for str_q in ["%2d" % dict_qu[x] for x in headers]:
            str_q = CatConverter.__encode_quant(str_q)
            str_quanta += str_q
        for i in range(len(headers), count):
            str_quanta += "  "

        headers = quanta_headers(int_fmt)[0:len(dict_ql)]
        for str_q in ["%2d" % dict_ql[x] for x in headers]:
            str_q = CatConverter.__encode_quant(str_q)
            str_quanta += str_q
        for i in range(len(headers), count):
            str_quanta += "  "

        return str_quanta

    @staticmethod
    def str2line(str_line):
        """str to Line object"""

        obj_line = Line()

        obj_line.freq = float(str_line[0:13])
        obj_line.freq_err = float(str_line[13:21])

        obj_line.log_I = float(str_line[21:29])
        obj_line.extended['int_deg_freedom'] = int(str_line[29:31])

        obj_line.E = float(str_line[31:41])
        obj_line.g = int(str_line[41:44])

        obj_line.extended['int_cat_tag'] = int(str_line[44:51])

        str_q = str_line[55:79]
        int_fmt = int(str_line[51:55])
        dict_qu, dict_ql = CatConverter.__read_quanta(str_q, int_fmt)

        obj_line.q_upper = dict_qu
        obj_line.q_lower = dict_ql
        obj_line.int_fmt = int_fmt

        return obj_line

    @staticmethod
    def line2str(obj_line):
        """Line object to str"""

        str_out = ""

        str_quanta = CatConverter.__write_quanta(obj_line.q_upper,
                                                 obj_line.q_lower,
                                                 obj_line.int_fmt)

        str_out += "%13.4f%8.4f" % (obj_line.freq, obj_line.freq_err)
        str_out += "%8.4f%2d" % (obj_line.log_I, obj_line.extended['int_deg_freedom'])
        str_out += "%10.4f%3d" % (obj_line.E, obj_line.g)
        str_out += "%7d" % obj_line.extended['int_cat_tag']
        str_out += "%4d%s " % (obj_line.int_fmt, str_quanta)

        return str_out


class EgyConverter:
    """Manages entries of .egy files."""

    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .egy to dict
        """
        dict_q = {}

        headers = quanta_headers(int_fmt)
        count = min(int_fmt % 10, len(str_quanta) // 3)
        for i in range(0, count):
            str_q = str_quanta[i * 3: (i + 1) * 3]
            dict_q[headers[i]] = int(str_q)

        return dict_q

    @staticmethod
    def __write_quanta(dict_q, int_fmt):
        """convert quanta from dict to .egy str"""

        str_quanta = ""

        headers = quanta_headers(int_fmt)[0:len(dict_q)]
        for str_q in ["%3d" % dict_q[x] for x in headers]:
            str_quanta += str_q

        return str_quanta

    @staticmethod
    def str2state(str_state, int_fmt):
        """str to State object (needs Pickett quanta format code)"""

        obj_state = State()

        obj_state.extended['str_H_iblk'] = str_state[0:6]
        obj_state.extended['str_H_indx'] = str_state[6:11]

        obj_state.E = float(str_state[11:29])
        obj_state.E_err = float(str_state[29:47])

        obj_state.extended['str_pmix'] = str_state[47:58]

        obj_state.int_fmt = int_fmt
        obj_state.q = EgyConverter.__read_quanta(str_state[64:], int_fmt)
        obj_state.g = int(str_state[58:63])

        return obj_state

    @staticmethod
    def state2str(obj_state):
        """Line object to str (needs Pickett quanta format code)"""

        str_out = ""

        str_out += "%s%s" % (obj_state.extended['str_H_iblk'], obj_state.extended['str_H_indx'])
        str_out += "%18.6f%18.6f" % (obj_state.E, obj_state.E_err)
        str_out += "%s%5d:" % (obj_state.extended['str_pmix'], obj_state.g)
        str_out += EgyConverter.__write_quanta(obj_state.q, obj_state.int_fmt)

        return str_out


class LinConverter:
    """Manages entries of .lin files"""

    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .cat to dict
           returns (dict_upper, dict_lower)
        """
        dict_ql = {}
        dict_qu = {}

        count = int_fmt % 10
        for i in range(0, count):
            str_qu = str_quanta[i * 3: (i + 1) * 3]
            str_ql = str_quanta[(i + count) * 3: (i + count + 1) * 3]

            headers = quanta_headers(int_fmt)
            dict_ql[headers[i]] = int(str_ql)
            dict_qu[headers[i]] = int(str_qu)

        return dict_qu, dict_ql

    @staticmethod
    def __write_quanta(dict_qu, dict_ql, int_fmt):
        """convert quanta from (dict,dict) to .cat str"""

        if int_fmt is None:
            int_fmt = 300

        count_max = 6
        count = int_fmt % 10
        str_quanta = ""

        headers = quanta_headers(int_fmt)[0:len(dict_qu)]
        for str_q in ["%3d" % dict_qu[x] for x in headers]:
            str_quanta += str_q
        for i in range(len(headers), count):
            str_quanta += "   "

        headers = quanta_headers(int_fmt)[0:len(dict_ql)]
        for str_q in ["%3d" % dict_ql[x] for x in headers]:
            str_quanta += str_q
        for i in range(len(headers), count):
            str_quanta += "   "

        for i in range(2 * count, 2 * count_max):
            str_quanta += "   "

        return str_quanta

    @staticmethod
    def str2line(str_line, int_fmt):
        """str to Line object"""

        obj_line = Line()
        obj_line.freq = float(str_line[36:51])
        obj_line.freq_err = float(str_line[51:60])

        obj_line.extended['str_lin_text'] = str_line[60:-1]

        str_q = str_line[0:36]
        dict_qu, dict_ql = LinConverter.__read_quanta(str_q, int_fmt)

        obj_line.int_fmt = int_fmt
        obj_line.q_upper = dict_qu
        obj_line.q_lower = dict_ql

        return obj_line

    @staticmethod
    def line2str(obj_line):
        """Line object to str"""

        str_out = ""

        str_quanta = LinConverter.__write_quanta(obj_line.q_upper,
                                                 obj_line.q_lower,
                                                 obj_line.int_fmt)

        freq_err = obj_line.freq_err if obj_line.freq_err is not None else 0.0

        str_out += "%s" % str_quanta
        str_out += "%15.4f" % obj_line.freq
        str_out += ("%10.3f" % freq_err).replace('0.', '.')
        str_out += "%s" % obj_line.extended['str_lin_text']

        return str_out


class PGopherLinConverter:
    """Manages entries of .lin files"""

    @staticmethod
    def __read_quanta(str_quanta, int_fmt):
        """convert quanta from .cat to dict
           returns (dict_upper, dict_lower)
        """
        dict_ql = {}
        dict_qu = {}

        count = int_fmt % 10
        for i in range(0, count):
            str_qu = str_quanta[i * 3: i * 3 + 2]
            str_ql = str_quanta[(i + count) * 3: (i + count) * 3 + 2]

            headers = quanta_headers(int_fmt)
            dict_ql[headers[i]] = int(str_ql)
            dict_qu[headers[i]] = int(str_qu)

        return dict_qu, dict_ql

    @staticmethod
    def str2line(str_line, int_fmt):
        """str to Line object"""

        obj_line = Line()

        count = int_fmt % 10
        str_q = str_line[0:count * 2 * 3 - 1]
        dict_qu, dict_ql = PGopherLinConverter.__read_quanta(str_q, int_fmt)

        obj_line.freq = float(str_line[count * 2 * 3:count * 2 * 3 + 18])
        obj_line.freq_err = float(str_line[count * 2 * 3 + 38:count * 2 * 3 + 59])

        obj_line.int_fmt = int_fmt
        obj_line.q_upper = dict_qu
        obj_line.q_lower = dict_ql

        return obj_line


class ParameterConverter:
    """Manages entries of .par and .var files"""

    @staticmethod
    def signum(flag):
        if flag:
            return '+'
        else:
            return '-'

    @staticmethod
    def obj_to_par_str(obj):
        return ("%13i  %.23e 1.00000000E%s50 /%s\n"
                % (param_code(obj.name), obj.value,
                   ParameterConverter.signum(obj.flag_fit), obj.name))

    @staticmethod
    def obj_to_var_str(obj):
        return ("%13i %.23e %.14e /%s\n"
                % (param_code(obj.name), obj.value, obj.error, obj.name))

    @staticmethod
    def par_str_to_obj(line, param=None, thresh_flag_fit=1.0):

        line_lst = line.strip().split()
        name = line_lst[-1]
        value = float(line_lst[1])
        if float(line_lst[2]) > thresh_flag_fit:
            flag_fit = True
        else:
            flag_fit = False

        if not param:
            return RotorParameter(name=name, value=value, flag_fit=flag_fit)
        else:
            if not param.name:
                param.name = name
            if not param.value:
                param.value = value

            param.flag_fit = flag_fit

            return param

    @staticmethod
    def var_str_to_obj(line, param=None):
        line_lst = line.strip().split()
        name = line_lst[-1]
        value = float(line_lst[1])
        error = float(line_lst[2])

        if not param:
            return RotorParameter(name=name, value=value, error=error)
        else:
            if not param.name:
                param.name = name
            if not param.value:
                param.value = value

            param.error = error

            return param



