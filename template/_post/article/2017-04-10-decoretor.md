---
layout: post
title: Pythonic - 装饰器正解
category: 学习笔记
tags: 编程， Python
---
<img src="/static/blog/img/blog/20161231/0.jpeg" style="width: 100%">

　　Python装饰器是Python高级特性中相当重要的一部分，但由于涉及函数式编程、闭包等概念，所以相对难以理解。包括廖雪峰的教程在内，很多教程讲述的都十分晦涩，甚至有很多帖子只是贴出大量没有意义的代码，完完全全是电子垃圾。关于编程，__我们的目的是理解它的原理而写出代码，而不是通过看代码来推敲它的原理__，可偏就有很多人喜欢反其道而行。

<!--more-->
## 两种装饰器，一个本质
　　对于装饰器，我觉得官方文档用了简短的2、30行就已经描述的非常详尽明了了，有意思的一段是下面：
```
@dec2
@dec1
def func(arg1, arg2, ...):
    pass

# This is equivalent to:

def func(arg1, arg2, ...):
    pass
func = dec2(dec1(func))

# ----------------------------------------------

@decomaker(argA, argB, ...)
def func(arg1, arg2, ...):
    pass
    
# This is equivalent to:

def func(arg1, arg2, ...):
    pass
func = decomaker(argA, argB, ...)(func)
```
　　可以知道，装饰器只是一种语法糖的存在，装饰器的代码会在被装饰的函数定义的时候执行，也就是被import后载入内存时生效。装饰器分两种，具体如下：
1. __不带参数的装饰器：接收一个函数f作为参数，返回另一个函数fd，在调用函数f的地方，用fd取而代之。__
1. __带参数的装饰器：接收设定的参数，返回一个装饰器。返回这个装饰器可以是带参数的，也可以不带参数。但如果它带参数，这个返回的装饰器就必须再返回一个装饰器。直到最后返回的装饰器是不带参数的，也就是上面这种装饰器，就进入1的逻辑。__

　　先说第一种。由于Python没有switch……case……的支持，所以可以借助装饰器来实现类似的作用。
```
_case_map = {}

def supported_case(f):
    _case_map[f.__name__] == f
    return f

@supported_case
def load_data():
    return "load"

@supported_case
def parse_data():
    return "parse"

def switch(case):
    proc_func = _case_map.get(case)
    if proc_func:
        result = proc_func()
    else:
        result = None

    return result

if __name__ == "__main__":
    case = "load_data"
    print switch(case)

运行结果：
[out]: load
```
这是最常见的用法了：supported_case接收一个函数，将它的名字注册到_case_map字典中，然后原封不动的把这个函数返回（暂时先不对接受到的这个函数做魔改，以简化问题。对其魔改的事宜，稍后再论）。也就是说，这里选择的依据，是函数名。如果不根据函数名而指定case，那就要用到第二种装饰器——带参数的装饰器：
```
def supported_case(case):
    def non_param_decoretor(f):
        _case_map[case] = f
        return f

    return non_param_decoretor

@supported_case(case="load")
def load_data():
    return "load"

...
```
如上，装饰器supported_case中返回了一个不带参数的装饰器non_param_decoretor，对load_data函数的装饰工作（注册到_case_map）就是由这个不带参数的装饰器进行的。而外层的装饰器supported_case，它的存在就是接收case参数，再通过局部变量的方式，传递给内层。

可以猜想，如过内层的装饰器可以通过某种方式接收case参数，是不是它就不用在supported_case中定义了呢？是的，根据总结的第二点，带参数的装饰器只要它最终返回一个I类装饰器就OK，而不必要关心它在哪里定义。所以上面的```supported_case```装饰器可以改写成下面的样子：
```
__current_case = None


def non_param_decoretor(f):
    _case_map[_current_case] = f
    return f


def supported_case(case):
    global __current_case
    __current_case = case

    return non_param_decoretor

```
这段代码与上一段代码作用完全相同，但展示了一点，__装饰器完全可以不用嵌套很多层，一层足矣__。新手惧怕装饰器的重要原因之一就是，装饰器往往嵌套很多层，让人摸不着头脑。事实上，嵌套多层显著的优点是可以自然而然的向内层的代码块传送变量，因为变量的作用域就是嵌套的，而这段代码只要有一个地方修改了\__current_case，那么程序就会出错，因为它共享了__current_case变量，变得不安全。

所以，搞懂了装饰器中每一层定义的函数的功用，就算真正理解了装饰器了。所以下面可以对函数进行魔改了，比如做参数检查等。这一步总结起来如下：
1. 已经知道了要魔改的函数名，假设为function_watting_to_be_modified
2. 已经知道要魔改的参数（如果不知道或者为不定参数，则使用\*args替代位置参数，\**kwargs代替键值参数，当然args和kwargs的名字可以自定义）
3. 定义一个函数，函数名随意（假定为modified_function），但是和要魔改的函数接收相同的参数
4. 首先对参数做一些操作，比如参数检查、预先打印日志等，然后用操作之后的参数来调用要魔改的函数，记录结果，并对结果做一些操作，比如合理性检查、打印日志等，再返回魔改的结果

那么可以这么写：
```
def modified_function(*args, **kwargs):
    # 做参数检查，log等
    if kwargs.get("data_langth", 0) <= ……
        ……

    # 记录结果
    result = function_watting_to_be_modified(*args, **kwargs)

    # 对结果检查等 
    if not result...

    return result
```

那么， 依照之前的思路，再用一个全局变量来保存要魔改的函数，完成最终的魔改。假设有前面定义的“load_data”、“parse_data”这两个函数，不接受任何参数，返回它们的函数名，我们要把它魔改成这样：在它们返回的结果追加字符串“decoretor”。然后根据指定的case来选择执行哪个函数，那么完整的代码如下：
```
_case_map = {}
__current_case = None
__function_watting_to_be_modified = None

def modified_function():
    result = __function_watting_to_be_modified()
    return str(result) + "decoretor"

def non_param_decoretor(f):
    global __function_watting_to_be_modified
    __function_watting_to_be_modified = f
    _case_map[__current_case] = modified_function
    return modified_function

def supported_case(case):
    global __current_case
    __current_case = case
    return non_param_decoretor

@supported_case(case="load")
def load_data():
    return "load_data"

@supported_case(case="parse")
def parse_data():
    return "parse_data"

def switch(case):
    proc_func = _case_map.get(case)

    return proc_func() if proc_func else None

if __name__ == "__main__":
    case = "load"
    print switch(case)
```
注意，这里使用了三个函数来完成一个装饰器，这三个函数由上到下分别的作用是：
* 魔改原函数，在其结果后追加“decoretor”字符串
* 将魔改后的函数注册到_case_map中，以便后续的switch搜索
* 接收指定的case参数，将其传递给一个无法接受参数的装饰器

那么，这个实例的目的，就是为了说明一点__无论多么复杂的装饰器，都可以写在一层。而付出的代价是，失去了函数式编程优点，重度依赖的变量的作用域无法完全把控，从而带来极大的安全风险，也使得代码失去了简洁性__。所以，用标准的装饰器写法改写上述的三个函数：
```
def supported_case(case):  # 接收指定的case参数，将其传递给一个无法接受参数的装饰器
    def non_param_decoretor(f):  # 将魔改后的函数注册到_case_map中，以便后续的switch搜索
        def modified_function(*args, **kwargs):  # 魔改原函数，在其结果后追加“decoretor”字符串
            result = f(*args, **kwargs)
            modified_result = str(result) + "decoretor"
            return modified_result

        _case_map[case] = modified_function
        return modified_function

    return non_param_decoretor
```
以上就是精彩的Python装饰器，关于函数被装饰后，内置属性__name__、__doc__等发生改变所造成的一些问题的解决方法，网络上教程众多，在此不赘述。Python装饰器的强大，远不止于此。总的来讲，OOP的装饰模式需要通过继承和组合来实现，而Python的decorator直接从语法层次支持装饰模式。Python的decorator可以用函数实现，也可以用类实现。

## 用类实现的装饰器
　　参见一个高水平的装饰器，这是Django的一段源代码：
```
class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res

```
这段代码看doc就知道，是将一个类实例的一个只接受self的方法，转换成该实例的属性并缓存。这段代码用途广泛，典型的就是服务器收到一个http请求之后缓存request的cache、GET的QUERY_STRING、POST的文件流等。使用方法如下：
```
class Test(object):
    @cached_property
    def test_property(self):
        print "calc"
        return 1

a = Test()
a.test_property
[out]: calc
1

a.test_property
[out]: 1
```
可以看到，只要被装饰的方法运行过一次，就再也不调用它，而是直接读取缓存的结果。神奇的代码在这一句```res = instance.__dict__[self.name] = self.func(instance)```，它用被装饰的函数的运行结果，替换实例的内置属性\__dict\__中的“test_property”的值。所以在之后访问这个属性，就直接取\__dict\__中缓存的结果，访问不到test_property函数。所以，用类实现的装饰器与用函数实现的装饰器的区别，就是前者可以借助类的属性来保存一些中间变量，虽然实现起来更加繁琐，但功能也更加强大。