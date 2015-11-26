#!/usr/bin/env python
# coding: utf-8


import re
import sys
import runpy
import tempfile
import argparse



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


class Compiler(object):

    def __init__(self, filename, output=None):
        self.input_filename = filename
        self.output_filename = output or get_name(filename) + ".py"

    def run(self, silent=False):
        if get_ext(self.input_filename) != "vam":
            raise ValueError("file extension wrong")

        with file(self.input_filename) as f:
            output = f.read()

            for key, code in VAM_TO_PY.items():
                if key in output:
                    output = output.replace(key, code)

        with file(self.output_filename, "w") as f:
            f.write(output)

        if not silent:
            print "{} generate sucessful".format(self.output_filename)



class Decompiler(object):

    def __init__(self, filename, output):
        self.input_filename = filename
        self.output_filename = output or get_name(filename) + ".vam"

    def run(self):
        if get_ext(self.input_filename) != "py":
            raise ValueError("file extension wrong")

        with file(self.input_filename) as f:
            output = f.read()

            for key, code in PY_TO_VAM.items():
                stmt = " "+key
                if stmt in output:
                    output = output.replace(stmt, " " + code)
                stmt = "^"+key
                if stmt in output:
                    output = output.replace(stmt, "^" + code)
                stmt = key
                if stmt in output:
                    output = output.replace(stmt, code)
                stmt = key + ":"
                if stmt in output:
                    output = output.replace(stmt, code + ":")
                stmt = key + "("
                if stmt in output:
                    output = output.replace(stmt, code + "(")
                stmt = key + " "
                if stmt in output:
                    output = output.replace(stmt, code + " ")

        with file(self.output_filename, "w") as f:
            f.write(output)

        print "{} generate sucessful".format(self.output_filename)


def main():
    parser = argparse.ArgumentParser(description='the vamcode tool.')
    parser.add_argument('-o', help="output filename", dest="output", type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', help="run the vamcode", dest="run", action="store_true")
    group.add_argument('-c', help="compile vamcode to python", dest="compile", action="store_true")
    group.add_argument('-d', help="decompile python to vamcode", dest="decompile", action="store_true")
    parser.add_argument('filename', help="input filename")
    args = parser.parse_args()
    if args.compile:
        compiler = Compiler(args.filename, args.output)
        compiler.run()
    elif args.decompile:
        decompiler = Decompiler(args.filename, args.output)
        decompiler.run()
    else:
        compiler = Compiler(args.filename, tempfile.mktemp(".py"))
        compiler.run(silent=True)
        runpy.run_path(compiler.output_filename)
        


if __name__ == "__main__":
    main()