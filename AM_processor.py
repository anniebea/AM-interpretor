from collections import deque


class AMprocessor:
    stack = deque()
    varVal = {}
    inbranch = 0
    inloop = 0
    currcommand = ""
    lparencount = 0

    def push(self, value):
        self.stack.appendleft(value)

    def fetch(self, var):
        self.stack.appendleft(self.varVal[var])

    def store(self, var):
        self.varVal[var] = self.stack[0]
        self.stack.popleft()

    def add(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        self.push(val1+val2)

    def sub(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        self.push(val1-val2)

    def mult(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        self.push(val1*val2)

    def div(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        self.push(val1/val2)

    def neg(self):
        if self.stack[0] == "tt":
            self.stack.popleft()
            self.push("ff")
        else:
            self.stack.popleft()
            self.push("tt")

    def le(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        if val1 <= val2:
            self.push("tt")
        else:
            self.push("ff")

    def eq(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        if val1 == val2:
            self.push("tt")
        else:
            self.push("ff")

    def logor(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        if val1 == "tt" or val2 == "tt":
            self.push("tt")
        else:
            self.push("ff")

    def logand(self):
        val1 = self.stack[0]
        self.stack.popleft()
        val2 = self.stack[0]
        self.stack.popleft()
        if val1 == "ff" or val2 == "ff":
            self.push("ff")
        else:
            self.push("tt")

    def AMFileToTree(self, inputFile):
        currWord = ""
        char = ''
        while 1:
            char = inputFile.read(1)
            if not char:  # EOF
                command = currWord
                if command == "ADD":
                    self.add()
                elif command == "SUB":
                    self.sub()
                elif command == "MULT":
                    self.mult()
                elif command == "DIV":
                    self.div()
                elif command == "LE":
                    self.le()
                elif command == "EQ":
                    self.eq()
                elif command == "NEG":
                    self.neg()
                elif command == "OR":
                    self.logor()
                elif command == "AND":
                    self.logand()
                break
            if char != ":" and char != "(" and char != ")" and char != "," and char != ";":
                currWord = currWord + char
            elif char == ":" or char == ",":
                command = currWord
                if command == "ADD":
                    self.add()
                elif command == "SUB":
                    self.sub()
                elif command == "MULT":
                    self.mult()
                elif command == "DIV":
                    self.div()
                elif command == "LE":
                    self.le()
                elif command == "EQ":
                    self.eq()
                elif command == "NEG":
                    self.neg()
                elif command == "OR":
                    self.logor()
                elif command == "AND":
                    self.logand()
                currWord = ""
                if char == ",":  # skip "else" statement in "if-then-else"
                    while 1:
                        # print(char)
                        char = inputFile.read(1)
                        if char == "(":
                            self.lparencount = self.lparencount + 1
                        if char == ")":
                            if self.lparencount == 0:
                                break
                            else:
                                self.lparencount = self.lparencount - 1
                    self.inbranch = self.inbranch - 1
            elif char == "(":  # FETCH | PUSH | STORE | BRANCH | LOOP | READ | WRITE
                command = currWord
                currWord = ""
                if command == "PUSH":
                    char = inputFile.read(1)
                    while char != ")":
                        currWord = currWord + char
                        char = inputFile.read(1)
                    self.push(int(currWord))
                elif command == "FETCH":
                    char = inputFile.read(1)
                    while char != ")":
                        currWord = currWord + char
                        char = inputFile.read(1)
                    self.fetch(currWord)
                elif command == "STORE":
                    char = inputFile.read(1)
                    while char != ")":
                        currWord = currWord + char
                        char = inputFile.read(1)
                    self.store(currWord)
                elif command == "BRANCH":
                    self.currcommand = command
                    if self.stack[0] == "tt":
                        self.stack.popleft()
                        self.inbranch = self.inbranch + 1
                    else:
                        self.stack.popleft()
                        while char != ",":
                            char = inputFile.read(1)
                elif command == "LOOP":
                    self.inloop = self.inloop + 1
                    self.currcommand = command

                    condstring = ""
                    char = inputFile.read(1)
                    condfile = open("loopcond" + str(self.inloop) + ".txt", "w")
                    while char != ",":
                        condstring = condstring + char
                        char = inputFile.read(1)
                    # print("LOOPCOND: " + condstring)
                    condfile.write(condstring)
                    condfile.close()

                    loopstring = ""
                    char = inputFile.read(1)
                    loopfile = open("loopbody" + str(self.inloop) + ".txt", "w")
                    while 1:
                        loopstring = loopstring + char
                        char = inputFile.read(1)
                        if char == "(":
                            self.lparencount = self.lparencount + 1
                        if char == ")":
                            if self.lparencount == 0:
                                break
                            else:
                                self.lparencount = self.lparencount - 1
                    # print("LOOPBODY: " + loopstring)
                    loopfile.write(loopstring)
                    loopfile.close()

                    condfile = open("loopcond" + str(self.inloop) + ".txt")
                    self.AMFileToTree(condfile)
                    condfile.close()
                    while self.stack[0] == "tt":
                        loopfile = open("loopbody" + str(self.inloop) + ".txt")
                        self.AMFileToTree(loopfile)
                        loopfile.close()
                        self.stack.popleft()
                        condfile = open("loopcond" + str(self.inloop) + ".txt")
                        self.AMFileToTree(condfile)
                        condfile.close()
                    self.inloop = self.inloop - 1
                    self.stack.popleft()
                    break
                currWord = ""
            elif char == ")":
                # print("):" + currWord)
                currWord = ""
