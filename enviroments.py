#!/usr/bin/python
#coding: utf-8

def empty_env_record():
    return list()

def is_empty_env_record(x):
    return not len(x)

def ispair(x):
    for item in x:
        if len(item) != 2:
            return False
    return True

def extended_env_record(sym, val, old_env):    
    return [[sym, val]] + old_env

def extract_extended_env_record(r):
    # symble, value, oldenv    
    return r[0][0], r[0][1], r[1:]


# wait for anded
def issymbol(x):
    return True
def isexpval(x):
    return True

def isenvironment(x):
    if is_empty_env_record(x):
        return True
    elif ispair(x) and issymbol(x[0][0]) and \
         isexpval(x[0][1]) and isenvironment(x[1:]):
        return True
    else:
        return False

###########################################################

def empty_env():    
    return empty_env_record()

def isempty_env(x): 
    return is_empty_env_record(x)

def extend_env(sym, val, old_env):
    print 'extend env ', sym, val
    return extended_env_record(sym, val, old_env)

def apply_env(env, search_sym):
    print 'apply env ', search_sym
    if isempty_env(env):
        raise Exception('apply-env "No binding for %s" ' % search_sym)
    else:
        sym, val, old_env = extract_extended_env_record(env)
        print 'env:', sym, search_sym
        if sym == search_sym:
            print 'end:', val, type(val)
            return val
        else:
            return apply_env(old_env, search_sym)	

def init_env():
    return extend_env('zzz', 'new zzz', extend_env('zzzc', 'aaa', extend_env('abcxxx', 12345, empty_env())))

def changelist(lista):
    c = lista
    c = ['c']+lista

funcdict = {}
def symboletofun(originalname):
    def decorator(func):
        funcdict[originalname] = func
        def wrap(*args, **kw):
            return func(*args, **kw)
        return wrap
    return decorator

if __name__ == "__main__":
    a = init_env()
    print a
    print 'isenvironment', isenvironment(a)
    print apply_env(a, 'abcxxx')
    print apply_env(a, 'zzz')
    
    for a, b in [['aa', 'b'], ['cc', 'd']]:
        print a, b 