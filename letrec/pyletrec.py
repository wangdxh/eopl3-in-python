#!/usr/bin/python
#coding: utf-8
from pyparsing import *
from enviroments import init_env, apply_env, extend_env, funcdict, symboletofun, extend_env_rec

identifier = Word(alphas, alphanums+'_-?')
number = Combine( Optional('-') + Word(nums)).setParseAction(lambda t:int(t[0]))

var_exp = Group( identifier )
const_exp = Group( number)
expression = Forward()
LPAREN, RPAREN, COMMA = map(Suppress, '(),')

diff_exp = Group( '-' + LPAREN + expression + COMMA + expression + RPAREN)
zero_exp = Group( Keyword('zero?') + LPAREN + expression + RPAREN) 
if_exp = Group( Keyword('if') + expression + Keyword('then') + expression + Keyword('else') + expression)
let_exp = Group(Keyword('let') + Group( delimitedList( Group( identifier + '=' + expression ))) + "in" +  expression)

proc_exp = Group(Keyword('proc') + LPAREN + identifier + RPAREN + expression)
call_exp = Group('(' + expression + expression + ')' )

let_rec_exp = Group(Keyword('letrec') + identifier + LPAREN + identifier + RPAREN + '=' + expression + 'in' + expression)


expression << (diff_exp | zero_exp | if_exp | call_exp | proc_exp | let_exp  | let_rec_exp | const_exp | var_exp)


def value_of(exp, env):
    name = exp[0]
    print 'valueof', exp
    if type(name) == int:
        return name

    func = funcdict.get(name, var_fun)
    return func(exp, env)



def var_fun(exp, env):
    retlist = apply_env(env, exp[0])
    if len(retlist) == 1:
        return retlist[0]
    elif len(retlist) == 3:
        #varname, body, the closet env that close letrec proc name
        return proceduer(retlist[0], retlist[1], retlist[2])
    else:
        raise 'var fun bad return apply_env'

@symboletofun('let')
def let(exp, env):    
    name, identlist, in_symble, body = exp
    print name
    extendenv = env
    for (varname, equal_symble, varvalue) in identlist:
        extendenv = extend_env(varname, value_of(varvalue, env), extendenv)
    return value_of(body, extendenv)

@symboletofun('letrec')
def letrec(exp, env):    
    name, procname, procarg, equals, procbody, in_symble, body = exp
    print name

    extendenv = extend_env_rec(procname, procarg, procbody, env)
    return value_of(body, extendenv)

@symboletofun('-')
def diff(exp, env):
    name, left, right = exp
    print 'diff', name
    x = value_of(left, env)
    y = value_of(right, env)
    print x, type(x)
    print y, type(y)
    return  x - y

@symboletofun('zero?')
def iszero(exp, env):
    name, param = exp
    print name
    return not(bool(value_of(param, env)))

@symboletofun('if')
def if_fun(exp, env):
    name, boolfun, then, thenfun, elsename, elsefun = exp
    print name
    if value_of(boolfun, env):
        return value_of(thenfun, env)
    else:
        return value_of(elsefun, env)

def proceduer(var, body, env):
    def fun(val):
        return value_of(body, extend_env(var, val, env)) 
    return fun

@symboletofun('proc')
def proc_fun(exp, env):
    name, ident, body = exp
    print 'in proc', name, ident, exp
    return proceduer(ident, body, env)

@symboletofun('(')
def call_fun(exp, env):
    left, rator, rand, right = exp
    print left
    return value_of(rator, env)(value_of(rand, env))

def value_of_program(program):
    print funcdict
    return value_of(expression.parseString(program)[0], init_env())

inputstr = '''
             let xx = 0, bb = 24 in
                if zero? ( xx )
                then -(bb,3)
                else - (xx , 5 )
            '''
inputstr = '''
             let xx = 0, bb = 24 in
                if zero? ( xx )
                then -(bb,3)
                else
                   let zz = 300 in -(zz, 10)
            '''
            #( proc(x) -(3,1)  30 )'
            #let f = proc (x) -(x,1) in (f 30)
            #(proc(f)(f 30)  proc(x)-(x,1))
            #((proc (x) proc (y) -(x,y)  5) 6)
            #let f = proc(x) proc (y) -(x,y) in ((f -(10,5)) 6)
 
            #let times4 = (fix t4m)
                            #in (times4 3)
inputstr2 = '''
                let fix =  proc (f)
                    let d = proc (x) proc (z) ((f (x x)) z)
                    in proc (n) ((f (d d)) n)
                in let
                    t4m = proc (f) proc(x) if zero?(x) then 0 else -((f -(x,1)),-4)
                    in let times4 = (fix t4m)
                        in (times4 5)
                
           '''

inputstr = '''

letrec even(odd)  = proc(x) if zero?(x) then 1 else (odd -(x,1))
   in letrec  odd(x)  = if zero?(x) then 0 else ((even odd) -(x,1))
       in (odd 15)

           '''
inputstr3 = '''
letrec f(x) = if zero?(x)  then 0 else -((f -(x,1)), -2) in (f 6)
           '''           
#letrec f(x) = if zero?(x)  then 0 else -((f -(x,1)), -2) in (f 4)

print value_of_program(inputstr)
print 'now1'
#print diff_exp.parseString('- ( -1, -123)')