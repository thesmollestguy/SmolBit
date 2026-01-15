import colorama

class checker():
    def __init__(self, bitcode:str):
        self.bitcode = bitcode#.replace("[", "").replace("(", "").replace(")", "")
        self.pos=0
        self.line=1
        self.posinline=1
        self.lastpos = (0,0)
        self.blockdepth = 0
        self.blockslist = []

        self.ignored = "()["
        self.numbers = "1234567890abcdef"
        self.boolops = "ijkl"
        self.booloptable = {
            "i":"==",
            "j":"<=",
            "k":">=",
            "l":"!="
        }
    
    def read(self, n, incpos=True):
        if self.pos + n > len(self.bitcode):
            raise RuntimeError("Unexpected end of bitstream")
        out = self.bitcode[self.pos:self.pos+n]
        if(incpos):
            self.lastpos = (self.line, self.posinline)
            self.pos += n
            self.posinline += n
            if('\n' in out):
                self.line+=1
                self.posinline=1
        return out

    def expect(self, mode:tuple|list, checkNext=True):
        if(mode[0]=="num"):
            num = ''
            for i in range(mode[1]):
                nextnum = self.read(1)
                if nextnum in self.numbers:
                    num += nextnum
                else:
                    if(not nextnum.isspace() and nextnum not in self.ignored):
                        raise SyntaxError(f"Character at {self.lastpos} was not a number")
                    else:
                        num+=self.expect(("num",1), False)
            if(self.read(1, False) in self.numbers and checkNext):
                raise SyntaxError(f"Unexpected number at ({self.line}, {self.posinline})")
            return num
        elif(mode[0]=="boolop"):
            op = self.read(1)
            if(op in self.boolops):
                return op
            else:
                if(not op.isspace() and op not in self.ignored):
                    raise SyntaxError(f"Character at {self.lastpos} was not a boolean operator (i, j, k, l)")
                else:
                    return self.expect(("boolop"))
        elif(mode[0]=="all"):
            num = ''
            for i in range(mode[1]):
                nextnum = self.read(1)
                if(nextnum.isspace() or nextnum in self.ignored):
                    num+=self.expect(("all",1), False)
                else:
                    num+=nextnum
            return num
    
    def check(self):
        while not self.pos >= len(self.bitcode):
            operation = self.read(1)
            if(operation in self.numbers):
                raise SyntaxError(f"{operation} at {self.lastpos} is not an operation")

            if(operation == "P"):
                n=self.expect(("num", 2))
                print(f"Print immediate 0x{n} ({int(n, 16).to_bytes(1).decode()})")
            elif(operation == "p"):
                n=self.expect(("num",1))
                print(f"Print register {n} (utf8)")
            elif(operation == "%"):
                n=self.expect(("num",1))
                print(f"Print register {n} (dec)")
            elif(operation == "h"):
                n=self.expect(("num",1))
                print(f"Print register {n} (hex)")
            elif(operation == "+"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{n} + reg{m}")
            elif(operation == "-"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{n} - reg{m}")
            elif(operation == "*"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{n} * reg{m}")
            elif(operation == "/"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{n} / reg{m}")
            elif(operation == "="):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{m}")
            elif(operation == "#"):
                n=self.expect(("num",1), False)
                m=self.expect(("num",2))
                print(f"reg{n} = 0x{m}")
            elif(operation == ">"):
                n=self.expect(("num",1))
                print(f"INC reg{n}")
            elif(operation == "<"):
                n=self.expect(("num",1))
                print(f"DEC reg{n}")
            elif(operation == "_"):
                n=self.expect(("num", 1))
                print(f"reg{n} = 0")
            elif(operation == "~"):
                n=self.expect(("num", 1))
                print(f"reg{n} = {int({n}, base=16)}")
            elif(operation == "^"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = reg{n} ^ reg{m}")
            elif(operation == "v"):
                n=self.expect(("num",2))
                m=n[1]
                n=n[0]
                print(f"reg{n} = (reg{m})root of reg{n}")
            elif(operation == "]"):
                self.blockdepth-=1
                if(len(self.blockslist)):
                    print(f"END{self.blockslist.pop()}")
                if(self.blockdepth<0 and not self.pos + 1 > len(self.bitcode)):
                    print(f"{colorama.Fore.YELLOW}SyntaxWarning{colorama.Fore.RESET} ']' at {self.lastpos} will end the script, possibly prematurely. if this is intentional, ignore this message.")
            elif(operation == "?"):
                self.blockdepth+=1
                self.blockslist.append("IF")
                n = self.expect(("num",1))
                o = self.expect(["boolop"])
                m = self.expect(("num",1))
                print(f"IF reg{n} {self.booloptable[o]} reg{m}")
            elif(operation == "R"):
                self.blockdepth+=1
                self.blockslist.append("REPEAT")
                n = self.expect(("num",1))
                print(f"REPEAT reg{n}")
            elif(operation == "F"):
                self.blockdepth+=1
                self.blockslist.append("FUNCDEF")
                n = self.expect(("num",1))
                print(f"FUNCDEF func{n}")
            elif(operation == "U"):
                n = self.expect(("num",1))
                print(f"FUNCUNDEF func{n}")
            elif(operation == "S"):
                n = self.expect(("num",1))
                print(f"FUNCCALL func{n}")
            elif(operation == "L"):
                self.blockdepth+=1
                self.blockslist.append("FOR")
                n = self.expect(("num",1), False)
                m = self.expect(("num",2))
                print(f"FOR (reg{n}=1; reg{n}<={int(m, 16)}; reg{n}++)")
            elif(operation == "V"):
                self.blockdepth+=1
                self.blockslist.append("FOR")
                n = self.expect(("num",1), False)
                m = self.expect(("num",1))
                print(f"FOR (reg{n}=1; reg{n}<=reg{m}; reg{n}++)")
            elif(operation == "W"):
                self.blockdepth+=1
                self.blockslist.append("WHILE")
                n = self.expect(("num",1))
                o = self.expect(["boolop"])
                m = self.expect(("num",1))
                print(f"WHILE reg{n} {self.booloptable[o]} reg{m}")
            elif(operation == "@"):
                print("PAGE 0")
            elif(operation == "A"):
                print("PAGE 1")
            elif(operation == "B"):
                print("PAGE 2")
            elif(operation == "C"):
                print("PAGE 3")
            elif(operation == "X"):
                print("PAGE 4")
            elif(operation == "Y"):
                print("PAGE 5")
            elif(operation == "Z"):
                print("PAGE 6")
            elif(operation == "&"):
                print("PAGE 7")
        if(self.blockdepth>0):
            print(f"Unclosed block found, possibly a {self.blockslist.pop()}")
