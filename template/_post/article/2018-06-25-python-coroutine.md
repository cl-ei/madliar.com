---
title: Python生成器与协程
category: 学习笔记
tags: 编程， Python
---
<!--more-->

### 生成器与协程
　　当一个函数中包含yield关键字时，调用这个函数就会返回一个生成器。将这个生成器传入next()函数，就会获取一次yield产生的值，直到生成器结束，抛出StopIteration异常。例如下面就是一个生成器：

```
>>> def g():
    for _ in "abc":
        yield _
        
>>> s = g()
>>> s
<generator object g at 0x00000253B98B8F68>

>>> next(s)
'a'

>>> next(s)
'b'

>>> next(s)
'c'

>>> next(s)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```

　　在Python2.5的版本以后，yield 关键字可以在表达式中使用，而且生成器 API 中增加了```.send(value)```方以接收变量，使得生成器可以当做协程来使用。下面就是一个简单的协程：
```
>>> def simple_coroutine():
    print('-> coroutine started')
    x = yield "ok"
    print('-> coroutine received:', x)

>>> my_coro = simple_coroutine()
>>> my_coro
<generator object simple_coroutine at 0x10

>>> next(my_coro)
-> coroutine started
ok

>>> my_coro.send(42)
-> coroutine received: 42
Traceback (most recent call last): # ➏
 ...
StopIteration
```

　　得到一个生成器s之后，应调用一次next(s)或s.send(None)来激活它，此时生成器代码会运行到yield处挂起。之后调用者每发送一个值，都会使这个生成器重新从yield处往下执行。每次都要给一个初始化的生成器施以next函数，显得太过繁琐，有人实现了一个装饰器，作用在一个初始化的生成器上，可以不用再调用next()就能立即使用：
```
from functools import wraps

def coroutine(func): 
    """装饰器：向前执行到第一个`yield`表达式，预激`func`"""
    @wraps(func)
    def primer(*args,**kwargs):
        gen = func(*args,**kwargs)
        next(gen)
        return gen
    return primer
```

　　用作的协程的生成器s如果发生异常，则会抛给调用者。同时，s还有两个方法，.throw()和.close()。前者用来给生成器传入一个异常，如果生成器处理了异常，则会顺利运行到下一次的yield处；反之，会重新抛出给调用者，进而协程结束。后者是用来显式的关闭一个生成器。

　　用作的协程的生成器return了一个值，则会抛一个StopIteration的异常给调用者，而这个异常的value属性就是return的值。

### yield from
　　yield from功能强大，在生成器 gen 中使用 yield from subgen() 时，subgen 会获得控制权，把产出的值传给gen 的调用方，即调用方可以直接控制 subgen。与此同时，gen 会阻塞，等待 subgen 终止。

　　所以yield from 的主要功能是打开双向通道，把最外层的调用方与最内层的子生成器连接起来， 这样二者可以直接发送和产出值，还可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的样板代码。


