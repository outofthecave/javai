#!/usr/bin/python
# coding: UTF-8

import getopt
import os
import os.path
import sys

JAVA_INSTANT_HOME = os.path.dirname(os.path.realpath(sys.argv[0]))
JAVA_CLASS_NAME = "Instant"

# browser is used for opening the Java API
BROWSER = "google-chrome"
if os.environ.get("BROWSER"):
    BROWSER = os.environ.get("BROWSER")

JAVA_CODE_PREFIX = """\
import java.io.*;
import java.math.*;
import java.util.*;
import java.util.regex.*;

public class %(JAVA_CLASS_NAME)s {

    public static final String BROWSER = "%(BROWSER)s";
    public static final String API_URL_PREFIX = "http://docs.oracle.com/javase/7/docs/api/";
    public static final String API_URL_SUFFIX = ".html";

    public static void help(String className) {
        String pathToClassApi = className.replaceAll("[.]", "/");
        String[] cmdarray = {BROWSER, API_URL_PREFIX + pathToClassApi + API_URL_SUFFIX};
        try {
            Runtime.getRuntime().exec(cmdarray);
        } catch (IOException e){
            print(e);
        }
    }

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

USAGESTRING="""\
run any Java code instantly

usage: javai JAVACODE...

Convenience methods:

static void print(Object...)
    print the arguments to stdout, separated by a space

static void help(String)
    open the Java 7 API for the given class name (must be fully qualified) in
    your favourite browser (relying on the BROWSER env var)
"""

def usage(exitSt):
    print USAGESTRING
    sys.exit(exitSt)

def execute(javaCode):
    """ execute the given java code by creating a new file in the CWD """
    # cd to the javai dir (java requires this for compilation)
    os.chdir(JAVA_INSTANT_HOME)

    # check for forgotten semicolon
    if not (javaCode.endswith(";") or javaCode.endswith("}")):
        javaCode += ";"

    f = open(JAVA_CLASS_NAME + ".java", "w")
    f.write(JAVA_CODE_PREFIX + javaCode + JAVA_CODE_SUFFIX)
    f.close()

    compileStatus = os.system("javac " + JAVA_CLASS_NAME + ".java")
    # only execute if compilation was successful
    if compileStatus == 0:
        os.system("java " + JAVA_CLASS_NAME)

def main(clargs):
    # parse CL options and arguments
    try:
        (optArgs, prgArgs) = getopt.getopt(clargs, "h")
    except GetoptError:
        usage(2)

    for (opt, arg) in optArgs:
        # check for help option
        if opt == "-h":
            usage(0)

    if not prgArgs:
        usage(1)

    argstr = " ".join(prgArgs)
    execute(argstr)

if __name__ == "__main__":
    main(sys.argv[1:])
