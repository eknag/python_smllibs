import copy
import functools

#sequences as python lists
class Seq(object):
    def __init__(self, values):
        self.values = values
    
#functions
def length(s):
    return len(s)

def nth(s):
    def g(n):
        return copy.deepcopy(s[n])
    return g

def equal(f):
    def g(arg):
        (s1,s2) = arg
        if len(s1) != len(s2): return False
        for i in range(len(s1)):
            arg = (s1[i],s2[i])
            if not f(arg): return False
        return True
    return g

def empty(s):
    return []

def singleton(x):
    return [copy.deepcopy(x)]

def tabulate(f):
    def g(n):
        res = []
        for i in range(n):
            res.append(f(i))
        return res
    return g

def rev(s):
    s = copy.deepcopy(s)
    snew = [1 for i in range(len(s))]
    for i in range(len(s)):
        snew[len(s)-i-1] = s[i]
    return snew

def append(args):
    (s1,s2) = args
    s1 = copy.deepcopy(s1)
    s2 = copy.deepcopy(s2)
    return s1 + s2

def flatten(ll):
    res = []
    for row in ll:
        for value in row:
            res.append(copy.deepcopy(value))
    return res

def filter(p):
    def g(s):
        res = []
        for value in s:
            if p(value): res.append(copy.deepcopy(value))
        return res
    return g

def map(f):
    def g(s):
        s = copy.deepcopy(s)
        for (i,v) in enumerate(s):
            s[i] = f(v)
        return s 
    return g

def zip(arg):
    (s1,s2) = arg
    s1 = copy.deepcopy(s1)
    s2 = copy.deepcopy(s2)
    l = min(len(s1),len(s2))
    res = [(s1[i],s2[i]) for i in range(l)]
    return res

def zipWith(f):
    def g(arg):
        return map(f)(zip(arg))
    return g

def enum(s):
    s = copy.deepcopy(s)
    return [v for v in enumerate(s)]

def filterIdx(p):
    def g(s):
        s = copy.deepcopy(s)
        res = []
        for (i,v) in enum(s):
            if p((i,v)): res.append(v)
        return res
    return g

def mapIdx(f):
    def g(s):
        s = copy.deepcopy(s)
        return map(f)(enum(s))
    return g

def update(arg):
    (s,(i,x)) = arg
    s = copy.deepcopy(s)
    x = copy.deepcopy(x)
    s[i] = x
    return s

###TEST ME WHEN YOU WRITE ITERATE!!!!####
def inject(arg):
    (s, u) = arg
    s = copy.deepcopy(s)
    u = copy.deepcopy(u)
    return iterate(update)(s)(u)


def subseq(s):
    s = copy.deepcopy(s)
    def g(arg):
        (i,l) = arg
        if ((i+l > len(s)) or i < 0): raise ValueError('indexing array out of bounds in subseq')
        return s[i:i+l]
    return g

def take(s):
    def g(n):
        return subseq(s)((0,n))
    return g

def drop(s):
    def g(n):
        return subseq(s)((n,length(s)-n))
    return g

#using a tuple of (constructor, value) for return type
def splitHead(s):
    s = copy.deepcopy(s)
    if len(s) == 0: return ("NIL",None)
    return ("CONS",(nth(s)(0),splitHead(drop(s)(1))))

#using a tuple of (constructor, value) for return type
def splitMid(s):
    s = copy.deepcopy(s)
    if len(s) == 0: return ("EMPTY",None)
    if len(s) == 1: return ("ONE",s[0])
    l = subseq(s)((0,len(s)//2))
    r = subseq(s)((len(s)//2,len(s)-(len(s)//2)))
    l = splitMid(l)
    r = splitMid(r)
    return ("PAIR",(l,r))

def iterate(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            res = b
            for v in s:
                res = f((res,v))
            return res
        return h
    return g

#Don't Understand, probably incorrect!
def iteratePrefixes(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            return (tabulate(lambda i: iterate(f)(b)(take(s)(i)))(length(s)),iterate(f)(b)(s))
        return h
    return g

def iteratePrefixesInc1(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            return tabulate(lambda i: iterate(f)(b)(take(s)(i+1)))(length(s))
        return h
    return g

def reduce(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            if len(s) == 0: return b
            if len(s) == 1: return s[0]
            l = take(s)(len(s)//2)
            r = drop(s)(len(s)//2)
            return f((reduce(f)(b)(l),reduce(f)(b)(r)))
        return h
    return g

def scan(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            return iteratePrefixes(f)(b)(s)
        return h
    return g

def scanInc1(f):
    def g(b):
        b = copy.deepcopy(b)
        def h(s):
            s = copy.deepcopy(s)
            return iteratePrefixesInc1(f)(b)(s)
        return h
    return g

def sort(cmpf):
    def g(s):
        s = copy.deepcopy(s)
        return(sorted(s, key=functools.cmp_to_key(cmpf)))
    return g

def merge(cmpf):
    def g(arg):
        (s1,s2) = arg
        s1 = copy.deepcopy(s1)
        s2 = copy.deepcopy(s2)
        return (sort(cmpf)(append((s1,s2))))
    return g

#FINISH ME
def collect(cmpf):
    def g(s):
        s = copy.deepcopy(s)
        raise Exception("collect is not yet implemented")
    return g

#FINISH ME. Not sure how this behaves when one is empty and the other isn't!
def collate(cmpf):
    def g(args):
        (s1,s2) = args
        s1 = copy.deepcopy(s1)
        s2 = copy.deepcopy(s2)
        n1 = len(s1)
        n2 = len(s2)
        raise Exception("collate is not yet implemented")
        if (n1 == n2 and n1 == 0): return "EQUAL"
    return g

def argmax(cmpf):
    def g(s):
        s = copy.deepcopy(s)
        if len(s) == 0: raise ValueError("no argmax of length 0 sequence!")
        maxx = s[0]
        argmax = 0
        for i in range(1,len(s)):
            if cmpf(s[i],maxx) == 1:
                maxx = s[i]
                argmax = i
        return argmax
    return g


#Testing
s0 = []
s1 = [4]
s2 = [1,2,5]
s3 = [s1,s2,s1,s1]
s4 = ['a','b','c','d','e']
s5 = [[1,2],[3,4]]
s6 = [(1,'z'),(4,'q')]

def f(arg): 
    (a,b) = arg
    return a==b

def fID(arg):
    (i,v) = arg
    if i>0 and v != 'b': return True
    return False

def p(v):
    if v>1: return True
    return False

def zf(arg):
    (v1,v2) = arg
    return v1 + v2

def sf(arg):
    (x,y) = arg
    return x+y

def cmpf(item1, item2):
    if sum(item1) > sum(item2):
        return 1
    elif sum(item1) < sum(item2):
        return -1
    else:
        return 0

def cmpf2(a,b):
    if a>b:
        return 1
    elif a<b:
        return -1
    else:
        return 0
