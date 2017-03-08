#!/usr/bin/python
#coding: utf-8
def empty_env_record():
    return list()

def is_empty_env_record(x):
    return not len(x)


def extended_env_record(sym, val, old_env):    
    return [[sym, val]] + old_env

def extended_env_record2(pname, pargs, pbody, old_env):
    return [[pname, pargs, pbody]] + old_env

# 
def is_first_a_proc_rec(r):
    if len(r[0]) == 2:
        return False
    elif len(r[0]) == 3:
        return True
    else:
        raise 'is_first_a_proc_rec error'



def extract_extended_env_record(r):
    # symble, value, oldenv    
    if len(r[0]) == 2:
        return r[0][0], r[0][1], r[1:]
    elif len(r[0]) == 3:
        return r[0][0], r[0][1], r[0][2], r[1:]



###########################################################

def empty_env():    
    return empty_env_record()

def isempty_env(x): 
    return is_empty_env_record(x)

def extend_env(sym, val, old_env):
    print 'extend env ', sym, val
    return extended_env_record(sym, val, old_env)
    

def extend_env_rec(pname, pargs, pbody, old_env):
    return extended_env_record2(pname, pargs,pbody, old_env)


def init_env():
    return extend_env('zzz', 'new zzz', extend_env('zzzc', 'aaa', extend_env('abcxxx', 12345, empty_env())))

def apply_env(env, search_sym):
    print 'apply env ', search_sym
    if isempty_env(env):
        raise Exception('apply-env "No binding for %s" ' % search_sym)
    else:
        if is_first_a_proc_rec(env):
            print 'proc rec', len(env), env
            pname, pargs, pbody, old_env = extract_extended_env_record(env)
            if pname == search_sym:
                return [pargs, pbody, env]
            else:
                return apply_env(old_env, search_sym)
            pass
        else:
            sym, val, old_env = extract_extended_env_record(env)
            print 'env:', sym, search_sym
            if sym == search_sym:
                print 'end:', val, type(val)
                return [val]
            else:
                return apply_env(old_env, search_sym)


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
    
    for a, b in [['aa', 'b'], ['cc', 'd']]:
        print a, b 