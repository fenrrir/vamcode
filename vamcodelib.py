# coding: utf-8

import sys
import tempfile

CODE_MAP = (
    ('assert', '👀'),
    ('break', '✋'),
    ('class', '🏠'),
    ('continue', '⏩'),
    ('def', '🍀'),
    ('del', '☠'),
    ('elif', '⁉️'),
    ('else', '❗️'),
    ('except', '🙏'),
    ('exec', '🛌'),
    ('finally', '🍾'),
    ('global', '☝️'),
    ('import', '⚡️'),
    ('lambda', '🦄'),
    ('pass', '♻️'),
    ('raise', '🚀'),
    ('return', '⤴️'),
    ('try', '⚽️'),
    ('while', '🔃'),
    ('yield', '⏏'),
    ('as', '🕵'), 
    ('for', '🏃'),
    ('not', '🚫'),
    ('with', '✊'),
    ('or', '💔'),
    ('if', '❓'),
    ('in', '⛵'),
    ('is', '🖇'),
    ('from', '✋'),
    ('and', '❤'),
    ('True', '👍'),
    ('False', '👎'),
    ('None', '⭕️'),
    ('=', '⬅️'),
    ('print', '👉'),
)

VAM_TO_PY = dict( reversed(x) for x in CODE_MAP)
PY_TO_VAM = dict( x for x in CODE_MAP)

def get_ext(filename):
    return filename.split('.')[-1]

def get_name(filename):
    index = filename.rindex(".")
    return filename[:index]


def open_file(filename, mode="r"):
    if sys.version_info.major == 2:
        return file(filename, mode=mode)
    else:
        return open(filename, mode=mode, encoding="utf-8")

class Compiler(object):

    def __init__(self, filename, output=None):
        self.input_filename = filename
        self.output_filename = output or tempfile.mktemp(".py")

    def run(self, silent=False):
        if get_ext(self.input_filename) != "vam":
            raise ValueError("file extension wrong")

        output = self.get_output()

        with open(self.output_filename, "w") as f:
            f.write(output)

        if not silent:
            print("{} generate successful".format(self.output_filename))

    def get_output(self):
        with open_file(self.input_filename) as f:
            output = f.read()
            for key, code in VAM_TO_PY.items():
                if key in output:
                    output = output.replace(key, code)
        return output



class Decompiler(object):

    def __init__(self, filename, output=None):
        self.input_filename = filename
        self.output_filename = output or tempfile.mktemp(".vam")

    def run(self, silent=False):
        if get_ext(self.input_filename) != "py":
            raise ValueError("file extension wrong")

        output = self.get_output()

        with open_file(self.output_filename, "w") as f:
            f.write(output) 

        if not silent:
            print("{} generate successful".format(self.output_filename))

    def get_output(self):
        with open_file(self.input_filename) as f:
            output = f.read()

            for key, code in PY_TO_VAM.items():
                stmt = " "+key
                if stmt in output:
                    output = output.replace(stmt, " " + code)
                stmt = "^"+key
                if stmt in output:
                    output = output.replace(stmt, "^" + code)
                stmt = key + ":"
                if stmt in output:
                    output = output.replace(stmt, code + ":")
                stmt = key + "("
                if stmt in output:
                    output = output.replace(stmt, code + "(")
                stmt = key + " "
                if stmt in output:
                    output = output.replace(stmt, code + " ")

        return output
