---
layout: post
title: 学习C++之六：异常的处理
category: 学习笔记
description: 处理程序运行错误
---
##异常
　　在某些特定的情况下，程序的运行会难免产生错误，而标志程序中产生错误或者意外状态，叫做异常。之前用new操作符来申请内存时，也有可能返回异常，但我们编写程序时将其忽略。下面我们学习如何捕获这种异常，并且在异常发生后做一些挽救。

　　运行下面程序：

``` 
#include<iostream>
#include<new>

using	std::bad_alloc;
using	std::cout;
using	std::endl;

void main(void)
{
	char* pdata(nullptr);

	while(1)
	{
		try
		{
			pdata = new char[static_cast<size_t>(100)];
		}
		catch(bad_alloc &ex)
		{
			cout << "memory allocation failed !" << endl
				 << "the information from the exception object is :" << ex.what() <<endl;
			break ;
		}
	}
}
```

　　上面的程序使用new操作符反复申请一个长度为100的char型数组，直到系统资源被消耗殆尽，最终导致内存申请失败，new抛出一个异常。在try标示的可能出现异常的代码块下方的catch代码块中，捕获new操作抛出的bad_alloc类型的异常，并执行信息输出操作。可以看到，程序输出：

		memory allocation failed !
		the information from the exception object is :bad allocation

　　需要注意到，当不能申请到内存时，new抛出一个bad_alloc类型的异常，bad_alloc是new标准头文件中定义的类类型，所以需要包含<new>头文件。

##异常机制
　　异常机制使用三个关键字，```try```、 ```throw```和```catch```。把可能发生异常的代码包含在try的代码块内，其中的代码会按照顺序正常执行。try代码块中，使用throw或者包含throw操作的函数来抛出一个异常，此时程序立即跳转到与抛出的异常相匹配的catch代码块中。此时仍可在catch块中使用没有操作数的throw来重新抛出异常，这样就会把抛出的异常转交给调用函数，以执行某些附加的操作。运行下面程序：

```
#include<iostream>
using	std::cout;
using	std::endl;

void main(void)
{
	int sum[]={1,2,3,4,5};

	for(int i = 0; i < 5; i++)
	{
		try{
			if(sum[i] == 1) throw 1;
			if(sum[i] == 2) throw "sum[i] is 2.";
			if(sum[i] == 3) throw 'x';
		}
		catch(const char* a){
			cout << a << endl;
		}
		catch(const int a){
			cout << a << endl;
		}
		catch(...){
			cout << "error !" << endl;
		}
	}
	cout << "program has been terminated."
		 << endl;
}
```

　　运行结果：

		1
		sum[i] is 2.
		error !
		program has been terminated.

　　程序在for循环中判断sum数组中元素的值，如果为1，则抛出一个const int类型的异常，然后用第二个catch代码块来捕获，将const int输出。因此第一行输出数字1。当sum某个元素值等于2时，抛出一个字符串，实质上是抛出一个字符数组类型的异常，被第一个catch代码块捕获，输出这个字符数组。第三个catch的括号中是三个点，它可以处理任何异常，在前两个catch代码块中无法处理的异常，都在这里处理。因此，在一个try中可以抛出多个不同类型的异常，后可跟多个catch分别捕获不同类型的异常。而且，如果有```catch(...) {... ...}```，则必须放在最后。