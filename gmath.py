# -*- coding:utf-8 -*-

from __future__ import division
import math


def sin(degree):
  radian = math.radians(degree)
  return math.sin(radian)
  
def cos(degree):
  radian = math.radians(degree)
  return math.cos(radian)
  
def tan(degree):
  radian = math.radians(degree)
  return math.tan(radian)
  
def arcsin(x):
  radian = math.asin(x)
  degree = math.degrees(radian)
  return degree
  
def arccos(x):
  radian = math.acos(x)
  degree = math.degrees(radian)
  return degree
  
def arctan(x):
  radian = math.atan(x)
  degree = math.degrees(radian)
  return degree
  
def sinh(x):
  return math.sinh(x)
  
def cosh(x):
  return math.cosh(x)
  
def tanh(x):
  return math.tanh(x)
  
def log(x, nBase):#当nBase<=0,x<=0时：ValueError
  return math.log(x, nBase)
  
def log10(x):#当x<=0时：ValueError
  return math.log10(x)

def ln(x):
  return math.log(x)
 
def pow(x, nPower):#当x<0,nPower为小数或分数时：ValueError 
  return math.pow(x, nPower)

def exp(x):
  return math.exp(x)
  
def fact(x):#当x<0或者x为小数分数时：ValueError
  return math.factorial(x)
 
def mod(x, y):#支持小数和负数，当y==0时: ValueError
  return math.fmod(x,y)

def sqrt(x):#当x<0时: ValueError
  return math.sqrt(x)
  
def cuberoot(x):
  if not x:
    return 0
  flag = -1 if x<0 else 1
  x = math.fabs(x)  
  return flag * math.exp(math.log(x)/3)

def yroot(x, y):
  if y and not x:
    return 0
  if x < 0 :
    if math.floor(y)==y and y%2:
      flag = -1
    elif math.floor(1/y)==1/y:
      flag = -1 if 1/y%2 else 1      
    else:
      raise ValueError    
  else:
    flag = 1
  x = math.fabs(x)
  return flag * math.exp(math.log(x)/y)
#对于yroot(x,y)的几点说明如下：
#  1.yroot(0,y)==0，其中y!=0
#  2.yroot(x,0)引发ZeroDivisionError 
#  3.当x>0时, yroot(x,y)必有解
#  4.当x<0时, 只考虑以下几种情况：
#      1> y为奇整数， 必有负数解  
#      2> 1/y为奇整数，必有负数解
#      3> 1/y为偶整数，必有正数解
#其他情况不予考虑，均视为表达式错误异常

def avg(*nums): 
   average = reduce(lambda x,y: x+y, nums, 0) / len(nums)
   return average

def sum(*nums):
  total = reduce(lambda x,y: x+y, nums, 0)
  return total

#此处为尽量降低各函数之间耦合性，var，varp，stdev，stdevp之间没有相互调用，也没有调用前面的avg和sum
def var(*nums):
  average = reduce(lambda x,y: x+y, nums, 0) / len(nums)
  square = map(lambda x: x*x, nums) 
  average_square = average ** 2
  square_sum = reduce(lambda x,y: x+y, square, 0)
  sample_variance = (square_sum - len(nums) * average_square) / (len(nums) - 1)
  return sample_variance
  
def varp(*nums):
  average = reduce(lambda x,y: x+y, nums, 0) / len(nums)
  square = map(lambda x: x*x, nums)
  average_square = average ** 2
  square_average = reduce(lambda x,y:x+y, square, 0) / len(nums) 
  overall_variance = square_average - average_square
  return overall_variance
  
def stdev(*nums):
  average = reduce(lambda x,y: x+y, nums, 0) / len(nums)
  square = map(lambda x: x*x, nums) 
  average_square = average ** 2
  square_sum = reduce(lambda x,y: x+y, square, 0)
  sample_variance = (square_sum - len(nums) * average_square) / (len(nums) - 1)
  sample_standard_deviation = math.sqrt(sample_variance) 
  return sample_standard_deviation
  
def stdevp(*nums):
  average = reduce(lambda x,y: x+y, nums, 0) / len(nums)
  square = map(lambda x: x*x, nums)
  average_square = average ** 2
  square_average = reduce(lambda x,y: x+y, square, 0) / len(nums) 
  overall_variance = square_average - average_square
  overall_standard_deviation = math.sqrt(overall_variance)
  return overall_standard_deviation
  
