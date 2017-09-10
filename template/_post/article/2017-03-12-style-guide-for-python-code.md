---
layout: post
title: Pythonic
category: 学习笔记
tags: 编程， Python
---
<img src="/static/blog/img/blog/20161211/0.jpg" style="width: 100%">

### 代码规范
　　谈及Python编程，《PEP 8》总是说不过去的，它是比较官方的代码风格的规范和建议。除此之外，还有《Google编程风格指导》之类的文档等，都是非常不错的文档。代码规范的重要性不言而喻，但这也是人们学习编程时最常忽略的章节。

　　在我读过的入门Python书籍里，中这部分的内容都比较少。但在进阶的书籍中，有的不惜用上两个章节专门讲述，如何写出遵循PEP 8规范的Python代码，并介绍各种工具来审查代码、管理项目结构和文档。当然，事情也没这么复杂，很多时候只要配置一个顺手的IDE就够了。这里我非常推荐PyCharm，它是一款非常优秀的IDE，而且提供免费的社区版。
<!--more-->
<img src="https://www.caoliang.net/static/thrdfiles/i@caoliang.netQQ%E6%88%AA%E5%9B%BE20170311233522.png" style="width:100%;"/>

　　PyChram安装之时就自带PEP 8检查，但不应把代码格式化依赖于快捷键和autopep8之类的工具进行。合格的程序员能潜移默化、自然而然的写出规整的代码。当他成为习惯时你会发现，这不是所谓的细枝末节，而且并不会拖累写代码的速度，相反，带有这种习惯会使码代码这件事更加惬意。

### 变量的命名
　　除了基本的代码规范，比如Java推荐的驼峰式命名法，Python推荐小写字母加下划线的命名法则之外，一个同样重要的原则就是，让看这份代码的人读出变量名就能知道它的含义。

* 尽量使用明确含义的变量名

 除非是特别抽象的库和公用方法，变量命名要就事论事，带上要处理的数据的含义。这样在维护起来，看到变量名就知道其代表的什么，脑海里不会有一个“翻译过程”。例如：
		def find_target_screen(query, spec):
		    for element in query:
		        if element.specifications == spec:
		            return element
		        else:
		            pass
 它显然不如下面：
		def find_target_screen(screen_list, spec):
		    for screen in screen_list:
		        if screen.specifications == spec:
		            return screen
		        else:
		            pass
 另外，有些人喜欢用数字2代表英文的“to”，数字4代表英文的“for”，比如```link2screen```、```ready4play```，这些都是很恶劣的习惯。且不说阿拉伯数字混淆在拉丁字母里很难辨认，即使英文水平很高的人，看到这样的变量名往往也需要停顿思考一下，这样就打断了分析代码者的思绪。所以，时刻谨记“效率第一”的原则，不要写这样的劣化代码。
* 不要害怕过长的变量名

 为了方便阅读，长的变量名是必要的。在Nginx源码中，有非常多的超过40个字符的变量名，所以完全没有必要单纯因为长度的原因而过分缩写。其次，如果不得不缩写，Python建议的原则是去掉单词的元音部分的字母，比如“count”缩写为“cnt”。一定要确认缩写后的单词是否会造成混淆，比如有人把“direction”缩写为“dire”，这绝对会让后来维护这份代码的人感到莫名其妙。


### 编程方法

 * 不要滥用“奇技淫巧”

 编写代码不仅要考虑简洁，更要可维护性。有些奇技淫巧确实能使你用简短的代码实现某些功能，但也要权衡是否值得这么做，因为它有时会带来的可阅读性下降。比如：```example_list[::-1]```这样的操作，好多老鸟有时也要百度一下才知道什么含义，而它等同于```example_list.reverse()```，后者其实是一种更好的方法。

* 不要滥用“assert”

 Python中提供了断言语句，当条件不为真时抛出AssertionError的异常。很多人使用它作为输入参数的检查、用户输入的检查等，但这是不合适的。assert最初的目的用于调试，典型的场合就是单元测试。它的原则是检查用户定义的约束，而不是程序运行时错误，所以在使用assert时谨记以下几点：
	* 断言失败代表程序存在bug

		这是最基本的原则。如果你认为断言引发的错误不是bug，应该使用if等语句替换断言的逻辑

	* Python本身的异常能够捕获相关错误，就无须断言

		比如数组越界、除数为0、类型不匹配等，能够在操作时抛出Python自带的ValueError、TypeError等异常，就不要再操作前用assert。

	* 不要用于检查用户输入
		应当使用if等条件判断来检测用户输入。否则与第一点相违背。

 断言适用的典型场景如下：
	* 检查函数返回值是否合理时
	* 当条件是业务逻辑继续下去的先决条件时
		比如业务进行下去需要两个list完全相等，而由于不可控的因素可能导致两个list不等，此时业务进行下去必然会造成错误。这时，可以使用断言。

* 不要滥用\*args和**kwargs

 对于Python的位置参数和关键字参数，很多人都会用这么用：
		def func(*args):
		    if isinstance(args[0], ExampleClassA):
		        # do something
		        pass
		    if isinstance(args[1], ExampleClassB):
		        # do something
		        pass
		    ...

		def func_b(**kwargs):
		    if key_a in kwargs:
		        param_a = kwargs[key_a]
		    else:
		        return False

		    if key_b in kwargs:
		        param_b = kwargs[key_b]
		    else:
		        return False
		    ...

 但这么做事不合理的。它违背了Pythonic原则，把参数传入到函数当中，不应该因为无名参数和关键字参数的引入而增加解析参数包的负担。如果每个函数都要对传入参数再检查，只能说明函数栈的设计存在缺陷。编写代码应该把参数检查放在一两个层级之内，而其他层级如果产生错误，应该从代码逻辑入手，而不是强制检查传入参数。

 所以，位置参数和关键字参数更适合下面的场合：
		def func(*args):
		    for object in args:
		        object.do_some_thing()
		    ...

		def func_b(**kwargs):
		    direction = kwargs.get("direction", "h")
		    user_group = kwargs.get("user_group", "normal")
		    ...
* 优化代码分支

 Python使用缩进替代大括号来区分代码块，所以，代码分支不合理，会使得Python代码混乱不堪，毫无优美可言。比如：
		if some_case:
		    ...
		    if some_case_2:
		        ...
		        if some_case_3:
		           ...
		    else:
		        ....
		else:
		    ....
 上述的代码存在的问题是，用省略号代替的代码块比较长，而且实际的分支肯定多于上面的示例，这种情况下，当阅读者把代码滚动到下面查看else时，他可能忘记了代码块所在层。所以，他不得不滚动到开始的位置，来寻找对应的if的层级。事实上，多数情况下都可以优化成下面的结构：
		if some_case:
		    ...
		else:
		    ...
		    if some_case_2:
		        ...
		    else:
		        ...
		        if some_case_3:
		            ...
		        else:
		            ....

		return
 或者：
		if not some_case:
		    ...
		    return
		...

		if not some_case_2:
		    ...
		    return
		...

		if not some_case_3:
		    ...
		    return
		...
		return
 一个很典型的例子是，刚学编程时老师让我们写一个程序，用户输入三个数代表三角形的三条边，系统输出这三条边能组成什么三角形，比如直角三角形、钝角三角形等。有的人if条件嵌套的了很多层，前面有N多个判定的条件来确定这是什么三角形，但却在最后一层处理不能组成三角形的case。老师告诉我们，应当首先判断这个条件，如果不能组成三角形，就直接返回；如果满足，再按照优先级逐一判断，这样的程序条理清晰、层级分明。所以，上述两个实例就是这一编程思想的体现。

 当然有些情况不能优化成2的结构，不论哪个分之下都有复杂的流。这时，就应该把这个大的函数切分成小函数。要时刻谨记同一个方法缩进的层级不能太深，哪怕函数的行数并不长，也应当保持简洁。
