import shlex, functools, sys, StringIO, readline

def bin_numeric_op(func):
    @functools.wraps(func)
    def execute(self):
        n2, n1 = self._stack.pop(), self._stack.pop()
        n1 = float(n1)
        n2 = float(n2)
        self._stack.append(func(n1, n2))
    return execute

def relational_op(func):
    @functools.wraps(func)
    def execute(self):
        n2, n1 = self._stack.pop(), self._stack.pop()
        self._stack.append(bool(func(n1, n2)))
    return execute

def bin_bool_op(func):
    @functools.wraps(func)
    def execute(self):
        n2, n1 = self._stack.pop(), self._stack.pop()
        n1 = bool(n1)
        n2 = bool(n2)
        self._stack.append(bool(func(n1, n2)))
    return execute

class Interpreter(object):
    def __init__(self):
        self._stack = []
        self._vars = {}
        self._squarestack = []

    def processToken(self, token):
        if token == '[':
            self._squarestack.append(len(self._stack))
        # Currently inside square brackets, don't execute
        elif len(self._squarestack) > 0:
            if token == ']':
                startlist = self._squarestack.pop()
                lst = self._stack[startlist:]
                self._stack[startlist:] = [tuple(lst)]
            else:
                self._stack.append(token)
        # Not current inside list and close square token, something's wrong.
        elif token == ']':
            raise ValueError("Unmatched ']'")
        elif token in self.builtin_ops:
            self.builtin_ops[token](self)
        else:
            self._stack.append(token)
    def get_stack(self):
        return self._stack
    def get_vars(self):
        return self._vars
    @bin_numeric_op
    def add(n1, n2):
        return n1 + n2
    @bin_numeric_op
    def mul(n1, n2):
        return n1 * n2
    @bin_numeric_op
    def div(n1, n2):
        return n1 / n2
    @bin_numeric_op
    def sub(n1, n2):
        return n1 - n2
    @bin_numeric_op
    def mod(n1, n2):
        return n1 % n2
    @bin_numeric_op
    def Pow(n1, n2):
        return n1**n2
    @relational_op
    def less(v1, v2):
        return v1 < v2
    @relational_op
    def lesseq(v1, v2):
        return v1 <= v2
    @relational_op
    def greater(v1, v2):
        return v1 > v2
    @relational_op
    def greatereq(v1, v2):
        return v1 > v2
    @relational_op
    def isequal(v1, v2):
        return v1 == v2
    @relational_op
    def isnotequal(v1, v2):
        return v1 != v2
    @bin_bool_op
    def bool_and(v1, v2):
        return v1 and v2
    @bin_bool_op
    def bool_or(v1, v2):
        return v1 or v2
    def bool_not(self):
        stack = self._stack
        v1 = stack.pop()
        stack.append(not v1)
    def if_func(self):
        stack = self._stack
        pred = stack.pop()
        code = stack.pop()
        if pred:
            self.run(code)
    def ifelse_func(self):
        stack = self._stack
        pred = stack.pop()
        nocode = stack.pop()
        yescode = stack.pop()
        code = yescode if pred else nocode
        self.run(code)
    def store(self):
        stack = self._stack
        value = stack.pop()
        varname = stack.pop()
        self._vars[varname] = value
    def fetch(self):
        stack = self._stack
        varname = stack.pop()
        stack.append(self._vars[varname])
    def remove(self):
        varname = self._stack.pop()
        del self._vars[varname]
    # The default argument is because this is used internally as well.
    def run(self, code=None):
        if code is None:
            code = self._stack.pop()
        for tok in code:
            self.processToken(tok)
    def run_while(self):
        stack = self._stack
        pred = stack.pop()
        body = stack.pop()
        self.run(pred)
        should_go_on = stack.pop()
        while should_go_on:
            self.run(body)
            self.run(pred)
            should_go_on = stack.pop()
    def rot(self):
        stack = self._stack
        distance = int(stack.pop())
        if distance <= 0:
            return
        distance = -(distance + 1)
        save = stack[distance]
        stack[distance:] = stack[(distance + 1):]
        stack.append(save)
    def dup(self):
        self._stack.append(self._stack[-1])
    def swap(self):
        self._stack[-2:] = self._stack[-1:-3:-1]
    def pop(self):
        self._stack.pop()
    def showstack(self):
        print"%r" % (self._stack,)
    def showvars(self):
        print "%r" % (self._vars,)
    builtin_ops = {
        '+': add,
        '*': mul,
        '/': div,
        '-': sub,
        '%': mod,
        '^': Pow,
        '<': less,
        '<=': lesseq,
        '>': greater,
        '>=': greatereq,
        '==': isequal,
        '!=': isnotequal,
        '&&': bool_and,
        '||': bool_or,
        'not': bool_not,
        'if': if_func,
        'ifelse': ifelse_func,
        'while': run_while,
        '!': store,
        '@': fetch,
        'del': remove,
        'call': run,
        'dup': dup,
        'swap': swap,
        'rot': rot,
        'pop': pop,
        'stack': showstack,
        'vars': showvars
        }

def shell(interp):
    readline.read_init_file()
    readline.set_history_length(500)
    try:
        while True:
            x = raw_input("star>   ")
            msg = None
            try:
                interp.run(shlex.split(x))
            except KeyError:
                msg = "does not exist"
            except:
                sys.excepthook(*sys.exc_info())
                msg = "parse error!"
            if msg != None:
                print "   =>",msg,"\n"
            else:
                print "   => %r\n" % (interp.get_stack(),)
    except (EOFError, KeyboardInterrupt):
        print

interp = Interpreter()
if len(sys.argv) > 1:
    lex = shlex.shlex(open(sys.argv[1], 'r'), sys.argv[1])
    tok = shlex.get_token()
    while tok is not None:
        interp.processToken(tok)
        tok = lex.get_token()
shell(interp)
