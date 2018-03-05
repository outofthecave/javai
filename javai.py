#!/usr/bin/python
# coding: UTF-8

import argparse
import codecs
import os
import sys

JAVA_INSTANT_HOME = os.path.dirname(os.path.realpath(sys.argv[0]))
JAVA_CLASS_NAME = "Instant"
JAVA_FILE_NAME = "{0}.java".format(JAVA_CLASS_NAME)

JAVA_CODE_PREFIX = """\
import java.io.*;
import java.math.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;

public class %(JAVA_CLASS_NAME)s {

    public static void print(Object... args) {
        for (Object arg : args) {
            System.out.print(arg);
            System.out.print(" ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        """ % (vars())
JAVA_CODE_SUFFIX = """
    }
}
"""

SHORT_DESCR="run any Java code instantly"

LONG_DESCR="""\
Convenience methods:

static void print(Object...):
    Print the arguments to stdout, separated by a space.
"""

def execute(java_code, classpath=""):
    """Execute the given java code by placing it in the Instant class."""
    os.chdir(JAVA_INSTANT_HOME)

    if not (java_code.endswith(";") or java_code.endswith("}")):
        java_code += ";"

    with codecs.open(JAVA_FILE_NAME, "wb", "utf-8") as f:
        f.write(JAVA_CODE_PREFIX)
        f.write(java_code)
        f.write(JAVA_CODE_SUFFIX)

    compiler_flags = []
    jvm_flags = []

    if classpath:
        compiler_flags.append("-cp")
        compiler_flags.append(".:'{0}'".format(classpath))
        jvm_flags.append("-cp")
        jvm_flags.append(".:'{0}'".format(classpath))

    compile_status = os.system("javac {0} {1}".format(" ".join(compiler_flags), JAVA_FILE_NAME))
    if compile_status != 0:
        return

    os.system("java {0} {1}".format(" ".join(jvm_flags), JAVA_CLASS_NAME))

def main(arguments):
    parser = argparse.ArgumentParser(description=SHORT_DESCR, epilog=LONG_DESCR)

    parser.add_argument("java_code", metavar="JAVACODE", nargs="+")

    parser.add_argument("-cp", "--classpath", dest="classpath",
            help="Set the Java classpath")

    cl = parser.parse_args(arguments)

    # We need to make all classpath entries absolute paths because we need to
    # cd into the directory that contains Instant.java for compilation.
    classpath_entries = cl.classpath.split(":")
    for i in range(len(classpath_entries)):
        classpath_entries[i] = os.path.abspath(classpath_entries[i])

    execute(" ".join(cl.java_code), classpath=":".join(classpath_entries))

if __name__ == "__main__":
    main(sys.argv[1:])
