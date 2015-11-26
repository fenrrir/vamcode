#!/usr/bin/env python
# coding: utf-8


import runpy
import tempfile
import argparse
import vamcodelib



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
        compiler = vamcodelib.Compiler(args.filename, args.output)
        compiler.run()
    elif args.decompile:
        decompiler = vamcodelib.Decompiler(args.filename, args.output)
        decompiler.run()
    else:
        compiler = vamcodelib.Compiler(args.filename, tempfile.mktemp(".py"))
        compiler.run(silent=True)
        runpy.run_path(compiler.output_filename)
        


if __name__ == "__main__":
    main()