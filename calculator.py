# -*- coding:utf-8 -*-

import re 
import inspect
from global_variables import map_fun, map_opr_1, map_opr_2, pre, pre_fun, pre_opr_1, pre_opd, rex 
import pdb


class ExpressionError(Exception):
  def __init__(self):
    Exception.__init__(self)

    
def extract(expr):
  """extract(...)
         extract(expr) -> list
         
         Usage:
           extract every element from the string 'expr', including numbers, operators, brackets, and functions
           
         Return:
           a list of elements extracted from the input string 'expr'"""
  expr = expr.lstrip()
  if not expr:
    raise ExpressionError
  elems = []
  while expr:
    matched = rex.match(expr)
    if matched:
      m = matched.group().lower()      
      if m[0] in 'abcdefghijklmnopqrstuvwxyz' and m not in map_fun:
        if m.startswith('mod'):###以'mod'开头的解析处理(如'modsin', 'modmod', 'mod2'等)
          elems.append('mod')
          expr = expr[3:].lstrip()
        else:
          raise ExpressionError
      else:
        elems.append(m)
        expr = expr[matched.end():].lstrip()
    else:
      raise ExpressionError
  return elems
  
def pretreat(elems):
  """pretreat(...)
         pretreat(elems) -> list
         
         Usage:
           1.Distinguish the unitary and the dual for operator '+' and '-'(inclued 'mod' 
             as a function, especially)
           2.Construct a tuple list with precedence and map of elements in list 'elems'
           
         Return: 
           a list of tuple like (pre, map)"""
  pre_map = []
  elems.insert(0, '(')
  elems.append(')')
  #在表达式左右添加'('和')'，一方面是防止一元运算判断中elems[i-1]的索引错误，二来适应爬山算法
  for i in xrange(len(elems)):
    cur = elems[i]
    if cur[0] in '.0123456789':#数字由字符串转化为浮点型
      pre_map.append((pre_opd, float(cur)))
    elif cur in pre:#对于所有出现的符号分一元运算（函数mod也抽象在内），二元运算和其他符号
      if cur in ['+', '-', 'mod'] and elems[i-1] in ['+', '-', '*', '/', '^', '(', '[', ',', 'mod']:
      #cur为一元运算或者函数mod
        if cur in ['+', '-']:
          pre_map.append((pre_opr_1, map_opr_1[cur]))
        else:
          pre_map.append((pre_fun, map_fun[cur]))
      elif cur in map_opr_2:
        pre_map.append((pre[cur], map_opr_2[cur]))
      else:
        pre_map.append((pre[cur], cur))
    elif cur in  map_fun:#函数的情况（函数mod已在上面的elif中被处理）
        pre_map.append((pre_fun, map_fun[cur]))
  return pre_map

def position_of_parentheses(d):
  """position_of_parentheses(...)
         position_of_parentheses(d) -> (l, r)
         
         Usage:
           find the position of the innermost parentheses
         
         Return:
           the position of left and right parenthesis"""
  l, r = 0, 0
  while d[r][1] != ')':
    if d[r][1] == '(':
      l = r
    r += 1
    if r >= len(d):#找不到匹配的右括号
      raise ExpressionError 
  if not(d[l][1] == '(' and d[r][1] == ')'):#左右圆括号不匹配
    raise ExpressionError
  if l+1 == r:#圆括号内容为空
    raise ExpressionError
  return l, r

def number_of_parameters(func):
  """number_of_parameters(...)
         number_of_parameters(func) -> int
         
         Usage:
           get the number of parameters for distinguishing different functions
           
         Return:
           a number of "func"' parameters(for multi-function, return -1)"""
  t = inspect.getargspec(func)
  if t[0]:
    num = len(t[0])
  else:
    num = -1
  return num    
    
def calculate(pre_map):
  """calculate(...)
         calculate(elems) -> float
         
         Usage: 
           calculate the expression with the climbing algorithm
         
         Return: 
           the calculated result of expression"""
  while len(pre_map) > 1:#直到计算结果为一个数
    lft, rgt = position_of_parentheses(pre_map)
    #每次找最靠左的最内层括号位置， 对括号内运算
    sublist = pre_map[lft+1:rgt] 
    while 1:
    #反复做括号内的子表达式进行计算，直到剩下一个值或元组
      highest, k = 0, 0#选取最高优先级并记录位置
      for i in xrange(len(sublist)):
        if sublist[i][0] > highest:
          highest, k = sublist[i][0], i     
      if highest == pre_fun:
        if k+1 >= len(sublist) or sublist[k+1][0] != pre_opd:
          raise ExpressionError#越界、参数不存在、参数不合法
        n = number_of_parameters(sublist[k][1])
        if n == 1:
          if type(sublist[k+1][1]) not in (float, int, long):
            raise ExpressionError#一元函数参数错误
          sublist[k] = (pre_opd, sublist[k][1](sublist[k+1][1]))
        elif n == 2:
          if type(sublist[k+1][1]) != tuple or len(sublist[k+1][1]) != 2:
            raise ExpressionError#二元函数参数错误
          sublist[k] = (pre_opd, sublist[k][1](*sublist[k+1][1]))
        else:
          if type(sublist[k+1][1]) in (int ,long, float):
            sublist[k+1] = (pre_opd, (sublist[k+1][1],))
          #多元函数只有一个参数情况时转化为元组形式
          sublist[k] = (pre_opd, sublist[k][1](*sublist[k+1][1]))               
        sublist.pop(k+1)
      elif highest == pre_opr_1:###一元运算
        pos = k 
        #按照一元运算右结合性从右至左运算
        while sublist[pos][0]==highest and pos<len(sublist):
          pos += 1
        pos -= 1
        if pos+1 >= len(sublist) or sublist[pos+1][0] != pre_opd:
        #sublist[k+1]的操作数判断；越界、不存在、存在但不为数
          raise ExpressionError
        while pos >= k:
          sublist[pos] = (pre_opd, sublist[pos][1](sublist[pos+1][1]))
          sublist.pop(pos+1)
          pos -= 1
      elif highest >= pre['+']:###二元运算
        if k < 1 or k+1 >= len(sublist) or sublist[k-1][0] != -1 or sublist[k+1][0] != -1:
          raise ExpressionError
        #sublist[k-1]和sublist[k+1]的操作数判断；k+1，k-1越界、不存在、存在但不为数
        sublist[k] = (-1, sublist[k][1](sublist[k-1][1], sublist[k+1][1]))
        sublist.pop(k-1)
        sublist.pop(k)
      elif highest == pre['[']:#()中包含[],则[]的正确位置必与()相邻, 其他出现位置判断为表达式错误
        if not(sublist[0][1] == '[' and sublist[len(sublist)-1][1] == ']'):
          raise ExpressionError
        sublist.pop(0)
        sublist.pop(len(sublist)-1)        
      else:
        break
    
    if highest == pre[',']:#逗号
      t = tuple([ s[1] for s in sublist if s[0] == -1])#二元或多元函数参数构成元组 
      if not t:
        raise ExpressionError
      sublist = [(pre_opd, t)]
    else:
      if len(sublist) > 1:
        raise ExpressionError
    pre_map = pre_map[:lft] + sublist + pre_map[rgt+1:] 

  if type(pre_map[0][1]) in [tuple, list]:
    raise ExpressionError      
  return pre_map[0][1]  

def main(): 
  try:
    expr = raw_input("Please input a valid expression:\n")
    elems = extract(expr)
    pre_map = pretreat(elems)
    result = calculate(pre_map)  
    print "The calculated result of expression is:\n%r" % result  
  except ExpressionError:
    print "ExpressionError:\n  Oops! A wrong expression was inputed!"
  except ZeroDivisionError, e:
    print "ZeroDivisionError:\n  ", e
  except ValueError, e:
    print "ValueError:\n  ", e
  except TypeError, e:
    print "TypeError:\n  type error(operand or parameter for function)!"
  except OverflowError, e:
    print "OverflowError:\n  Oh my god! The result is too large!"
    
if __name__ == '__main__':
  main()