import sys, shlex, readline, os, string
List, assign, call, add, sub, div, Pow, mul, mod, fac, duf, read,\
kill, clr, STO, RET, fib, curs = {}, "set", "get", "+", "-", "/", "^", "*",\
"%", "fact", "func", "read", "kill", "clear", ">", "@", "fib", "vars"
def fact(num):
    if num == 1: return 1
    else: return num*fact(num-1)
def builtin_op(op, stack):
    global List
    if op == mul: stack.append(float(stack.pop())*float(stack.pop()))
    elif op == div: stack.append(float(stack.pop())/float(stack.pop()))
    elif op == sub: stack.append(float(stack.pop())-float(stack.pop()))
    elif op == add: stack.append(float(stack.pop())+float(stack.pop()))
    elif op == Pow: stack.append(float(stack.pop())**float(stack.pop()))
    elif op == assign: val = List[stack.pop()] = stack.pop(); stack.append(val)
    elif op == call: stack.append(List[stack.pop()])
    elif op == fac: stack.append(fact(stack.pop()))
    elif op == duf: stack.append("%s %s %s" % (duf, stack.pop(), stack.pop()))
    elif op == mod: stack.append(float(stack.pop())%float(stack.pop()))
    elif op == kill: del List[stack.pop()]
    elif op == clr: os.system("clear")
    elif op == STO: val = List[stack.pop()] = stack.pop(); stack.append(val)
    elif op == RET: stack.append(List[stack.pop()])
    elif op == curs: stack.append(List)
    elif op == read: prompt = stack.pop(); List[prompt] = Eval(raw_input("%s "%prompt)); stack.append(List[prompt])
def Eval(expr):
    ops = "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(mul, add, sub, div, Pow, assign, call, fac, duf, mod, read, kill, clr, STO, RET, curs)
    stack, expr, ops = [], shlex.split(string.lower(expr)), ops.split()
    for i in expr:
        if i[0] != ';':
            if i not in ops: stack.append(i)
            elif i in ops: builtin_op(i, stack)
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
