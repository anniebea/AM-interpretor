import sys
import AM_processor
from antlr4 import *

def main(argv):
    inputFile = FileStream(argv[1])
    print("============RAW INPUT============")
    print(inputFile)
    print("=================================")

    file = open(argv[1])
    interpreter = AM_processor.AMprocessor()
    interpreter.AMFileToTree(file)

    print("=============RESULT=============")
    print("Stack: " + str(interpreter.stack))
    print("Value list: " + str(interpreter.varVal))
    print("================================")

if __name__ == "__main__":
    main(sys.argv)
