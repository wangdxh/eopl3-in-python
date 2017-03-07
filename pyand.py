#!/usr/bin/python
#coding: utf-8
from pyparsing import *
from enviroments import init_env, apply_env, extend_env, funcdict, symboletofun

identifier = Word(alphas, alphanums+'_-?')
number = Combine( Optional('-') + Word(nums+'.')).setParseAction(lambda t:float(t[0]))

and_ = Literal("&&")
or_  = Literal("||")
not_ = Literal("!")

item = (identifier | number | quotedString)

bigger_, equal_, little_, be_, le_ = map(Literal, ['>', '==', '<', '>=', '<='])
bigger_exp = Group(item + bigger_ + item)
equal_exp = Group(item + equal_ + item)
little_exp = Group(item + little_ + item)
be_exp = Group(item + be_ + item)
le_exp = Group(item + le_ + item)

BoolTerm = (bigger_exp | equal_exp | little_exp | be_exp | le_exp)

BoolExpr = operatorPrecedence( BoolTerm,
       [
       (not_, 1, opAssoc.RIGHT),
       (and_, 2, opAssoc.LEFT),
       (or_, 2, opAssoc.LEFT),
       ])

let_exp = Group(Keyword('let') + Group( delimitedList( Group( identifier + '=' + item ))) \
          + "in" +  BoolExpr)

def value_of_compare(exp, env):
    # a > b  0, 2
    for i in range(0, len(exp), 2):
        if type(exp[i]) == str and exp[i][0] != '"':
            exp[i] = apply_env(env, exp[i])
    strexp = map(str, exp)
    print ' '.join(strexp)
    ret = eval(' '.join(strexp))
    return ret

def value_of_boolexp(exp, env):
    print 'boolexp',exp
    if exp[0] == '!':
        return not(value_of_boolexp(exp[1], env))     
    elif exp[1] == '&&' or exp[1] == '||':
        ret = False
        if (exp[1] == '||'):
            ret = True        
        for inx in range(0, len(exp), 2):
                if value_of_boolexp(exp[inx], env) == ret:
                    return ret
        return not ret
    else:
        return value_of_compare(exp, env)

def value_of_let(exp, env):
    name, identlist, in_symble, body = exp
    print name
    extendenv = env
    for (varname, equal_symble, varvalue) in identlist:        
        extendenv = extend_env(varname, varvalue, extendenv)
    return value_of_boolexp(body, extendenv)

#! x > 5 && 3 < 5 || (1 <= y && (z == b))
#       
tests1 = """

! 3 > 5 && 2 > 7 || 'abc1' == 'abc' || 3 < 5
    """

test2 = '''
 3 > 5
'''

tests = '''
let foo=5.2, ipcnt=24, function_Id="coupon",abc=24 in foo>5.1 &&ipcnt ==abc || function_Id=="coupon"   
        '''

print tests
print let_exp.parseString(tests)[0]

print tests1
print BoolExpr.parseString(tests1)[0]
print test2
print value_of_boolexp( BoolExpr.parseString(test2)[0], init_env())
#print value_of_let(let_exp.parseString(tests)[0], init_env())
