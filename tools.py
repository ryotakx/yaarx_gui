import subprocess
import toml
import re
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp


class ConfigDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

    def allow(self, state=True):
        if state:
            self.__dict__ = self
        else:
            self.__dict__ = dict()


def configs():
    f = open('config.toml', 'r')
    config = toml.load(f, ConfigDict)
    if config.choice_list == 'default':
        config.choice_list = list(config.programs.keys())

    for key, val in config.programs.items():
        if 'output_lines' not in config.programs[key].keys():
            config.programs[key]['output_lines'] = config.default_output_lines
        for i, param in enumerate(config.programs[key].param):
            if 'type' not in param.keys():
                config.programs[key].param[i]['type'] = config.default_parameter_type
    return config


def compute(program, word_size, addr, *param):
    run = subprocess.Popen(
        addr + '/bin' + str(word_size) + '/' + program.name,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    for i in param:
        run.stdin.write(i + '\n')
    run.stdin.close()
    output = []
    for line in run.stdout:
        print(line)
        output.append(str(line))
    return prettify(output, program.output_lines)


def prettify(output, lines):
    return_list = []
    for line in lines:
        for i in re.split('[\]\[()]', output[line].strip().replace('=', '\n='))[2:]:
            if i != '':
                return_list.append(i.strip())
        return_list.append('')
    print(return_list)
    return '\n'.join(return_list)


def conversion(input_type, text, output_type):
    output = text
    if input_type == 'decimal' and output_type == 'hex':
        output = hex(int(text))[2:]
    if input_type == 'decimal' and output_type == 'binary':
        output = bin(int(text))[2:]
    if input_type == 'hex' and output_type == 'decimal':
        output = str(int(text, 16))
    if input_type == 'hex' and output_type == 'binary':
        output = bin(int(text, 16))[2:]
    if input_type == 'binary' and output_type == 'decimal':
        output = str(int(text, 2))
    if input_type == 'binary' and output_type == 'hex':
        output = hex(int(text, 2))[2:]
    return output


def input_validator(length, input_type):
    if input_type == 'hex':
        return QRegExpValidator(QRegExp('[0-9a-fA-F]{1,%i}' % length))
    if input_type == 'decimal':
        return QIntValidator(0, int('9' * min(9, length)))
    if input_type == 'binary':
        return QRegExpValidator(QRegExp('[01]{1,%i}' % length * 4))


def validator_equal_to(val1, val2):
    if type(val1) == type(val2) == QRegExpValidator and val1.regExp() == val2.regExp():
        return True
    elif type(val1) == type(val2) == QIntValidator:
        return True
    else:
        return False
