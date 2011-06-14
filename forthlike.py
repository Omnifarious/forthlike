import sys, shlex, readline, os, string
List, assign, call, add, sub, div, Pow, mul, mod, fac, duf, read,\
kill, clr, STO, RET, fib, curs = {}, "set", "get", "+", "-", "/", "^", "*",\
"%", "fact", "func", "read", "kill", "clear", ">", "@", "fib", "vars"
def fact(num):
    if num == 1: return 1
    else: return num*fact(num-1)
def Simp(op, num2, num1):
    global List
    try: num1, num2 = float(num1), float(num2)
    except:
        try: num1 = float(num1)
        except:
            try: num2 = float(num2)
            except: pass
    if op == mul: return num1*num2
    elif op == div: return num1/num2
    elif op == sub: return num1-num2
    elif op == add: return num1+num2
    elif op == Pow: return num1**num2
    elif op == assign: List[num1] = num2; return "ok"
    elif op == call: return List[num1]
    elif op == fac: return fact(num1)
    elif op == duf: return "%s %s %s"%(duf, num1, num2)
    elif op == mod: return num1%num2
    elif op == kill: del List[num1]; return "ok"
    elif op == clr: os.system("clear")
    elif op == STO: List[num2] = num1; return "ok"
    elif op == RET: return List[num1]
    elif op == curs: return List
    elif op == read: List[num1] = Eval(raw_input("%s "%num1)); return "ok"
def Eval(expr):
    ops = "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(mul, add, sub, div, Pow, assign, call, fac, duf, mod, read, kill, clr, STO, RET, curs)
    stack, expr, ops = [], shlex.split(string.lower(expr)), ops.split()
    for i in expr:
        if i[0] != ';':
            if i not in ops: stack.append(i)
            elif i in ops: stack.append(Simp(i, stack.pop(), stack.pop()))
        else: stack.append("ok")
    return stack[0]
def shell():
    try:
        x = ""
        while x != "quit":
            x = raw_input("star>   ")
            try: l = Eval(x)
            except KeyError: l = "does not exist"
            except: l = "parse error!"
            if l != None: print "   =>",l,"\n"
    except (EOFError, KeyboardInterrupt): print
if len(sys.argv) > 1:
    x = open(sys.argv[1], 'r'); l = x.readlines(); x.close()
    for i in l:
        if i[0] != ";":
            i = ' '.join(i.split())
            x = Eval(i)
            if x != None: print i,"\n   =>",x,"\n"
        else: pass
    shell()
else: shell()
