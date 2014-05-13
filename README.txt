This is Calculator version 1.2
=============================== 
Copyright (c) 2014 Gwanwlw & 越崖 & 晓云. All rights reserved.


Development Language
------------
  Python

Development Environment
------------ 
  -Windows 8.1 Build 9600
  -Python 2.7.6
  -Notepad++

Development Cycle
------------
  2014/3/26--2014/4/13

How to run it ?
------------
  由于没有exe文件，需要在控制台下运行
  以我的电脑运行情况为例，win8.1控制台
  控制台下从键盘输入命令"python calculator.py"，然后按照提示输入表达式，回车显示运算结果
  前提是需要设置好pytohn.exe的环境变量
  注意：开发环境为python2.7.6，主运行程序为calculator.py
  
This Beta contains the following files
------------  
  calculator.py			  -calculating module
  calculator.pyc          -compiled roduct from calculator.py
  global_varibles.py      -global varibles
  global_varibles.pyc     -compiled product from global_varibles.py
  gmath.py                -math function library
  gmath.pyc               -compiled product from gmath.py
	
  case.xlsx               -passed datas for testing 
  README.txt              -this file

Exceptions
------------
  1.空表达式
  2.解析出错误符号或者数字或者函数
  3.括号内内容为空或者括号不匹配
  4.方括号的错误出现形式
  5.函数参数为空或者函数参数形式不匹配（一元函数与多元函数要求不一样）
  6.一元运算右操作数不存在或者形式不匹配
  7.二元运算左右操作数不存在或者形式不匹配
  8.缺少操作符或者函数
  9.运算错误如ZeroDivisionError、ValueError、TypeError、OverFlowError等
   
 其中对于1-8扔出自定义异常ExpressionError，并在main()中捕获
 
The file "gmath.py" contains
------------
  一元函数：sin,cos,tan,arcsin,arccos,arctan,sinh,cosh,tanh,log10,ln,exp,fact,sqrt,cuberoot
  二元函数：log,pow,mod,yroot
  统计函数：avg,sum,var,varp,stdev,stdevp
  
The file "global_varibles.py" contains
------------
  map_fun: 数学函数映射
  map_opr_1: 一元函数映射
  map_opr_2: 二元函数映射
  pre: 各种符号优先级规定（包括运算符，圆括号，方括号，分隔符）  
  pre_opr_1: 一元运算优先级
  pre_opd: 操作数标记
  
The file "calculator.py" contains
------------
  这个文件主要分为以下三大模块：
    1.解析表达式；extract(expr)；将表达式中数，符号，函数解析出来
	2.预处理；pretreat(elems)；指定优先级并建立运算映射
	3.计算；calculate(pre_map)；基于爬山算法对表达式计算
  另外有：
    1.main()；输入输出，对不同模块调用，并进行异常处理
	2.position_of_parentheses(d)；寻找当前表达式中最左内侧的圆括号位置
  	3.number_of_parameters(func)；统计函数参数个数，在函数计算时基于此分配不同的参数表并进行参数表检查
	
Algorithm 
------------  
  -表达式解析部分运用正则表达式：
    rex = re.compile(r'\d*\.\d+|\d+|[a-zA-Z][a-zA-Z0-9]*|\(|\)|\[|\]|\*|/|\+|\-|\^|,')  
    运用该正则解析出来的元素可能会出现一种不合理情况，比如将'mod2mod2sin','modsin',
  'modmod'等解析为一个函数，故在extract中对此情况特殊处理，详见extract(expr)
  
  
  -计算部分运用爬山算法:
    按照常规来说，括号内的应该优先计算，而此算法正是基于此。
	1.每次找最左内侧的一对圆括号，将括号内的内容视作一个子表达式。
	2.对于子表达式按照优先级从高到低，一元运算和函数右结合，二元运算左结合
  的原则依次运算，直至括号内运算结果为一个数或者元组，然后用运算结果代替
  子表达式构成新的表达式
    3.对新的表达式重复步骤1、2，直到最终表达式计算结果变为一个数
  
  -其中需要特别说明的是：
    1.对于分隔符','的处理；','主要出现在函数参数列表中，在此将','抽象为构建
  参数表的一种运算，即对','分隔的操作数构建元组作为多元函数参数表
    2.对于方括号'['和']'的处理；由于'['和']'只出现在统计函数中，并且紧挨圆括号，
  实际上并起不了太大作用；故在程序中处理时直接删掉'['和']'并无影响
    3.对于+，-，mod可能出现二义性的处理；
	   1>  +-可以是正负号，这时视为一元运算；可以是加减，这时视为二元运算  
	   2>  mod可以作为二元运算符，也可以是右结合的函数
	 因此，在pretreat预处理模块中对+-mod三者特别加以区分，然后按函数，一元运算，
  二元运算分配不同优先级和运算映射
     区分的原则是：+-mod左边出现'+', '-', '*', '/', '^', '(', '[', ',', 'mod'
	 对于一元运算应遵循右结合性，对于二元运算遵循左结合性

------------
End of Document