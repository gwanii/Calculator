# -*- coding:utf-8 -*-

import re
import gmath as g

#函数映射
map_fun = {'sin': g.sin, 'cos': g.cos, 'tan': g.tan,
                         'arcsin': g.arcsin, 'arccos': g.arccos, 'arctan': g.arctan,
                         'sinh': g.sinh, 'cosh': g.cosh, 'tanh': g.tanh,
                         'log': g.log, 'log10': g.log10, 'ln': g.ln, 
                         'pow': g.pow, 'exp': g.exp, 'fact': g.fact, 'mod': g.mod, 
                         'sqrt': g.sqrt, 'cuberoot': g.cuberoot, 'yroot': g.yroot, 
                         'avg': g.avg, 'sum': g.sum, 
                         'var': g.var, 'varp': g.varp, 'stdev': g.stdev, 'stdevp': g.stdevp}
#一元运算映射
map_opr_1 = {'+': lambda x: x, '-': lambda x: -x}                     
#二元运算映射
map_opr_2 = {'+': lambda x,y: x+y, '-': lambda x,y: x-y, '*': lambda x,y: x*y, '/': lambda x,y: x/y,
                                   'mod': lambda x,y: x%y, '^': lambda x,y: x**y}
#各种符号优先级                             
pre = {'(': 0, ',': 1, '[': 2, ']': 2, '+': 3, '-': 3, '*': 4, '/': 4, '^': 5, 'mod':5, ')': 8}
#一元运算优先级
pre_opr_1 = 6
#函数优先级
pre_fun = 7
#操作数定义优先级为-1，便于区分
pre_opd = -1
#用于解析元素正则表达式，可解析小数，整数，函数，和各种符号
rex = re.compile(r'\d*\.\d+|\d+|[a-zA-Z][a-zA-Z0-9]*|\(|\)|\[|\]|\*|/|\+|\-|\^|,')
                   #小数 | 整数 | 函数 | 各种符号   
