---
layout: post
title: 学习C++之一：数据类型和转换
category: 学习笔记
description: 了解C++中的数据类型
---
##C++中的基本类型
　　在C++中基本数据类型除了最常用的int型，还有占用字节数为1的bool、char型，占用2个字节的wchar_t、short型，占用4个字节的int、long、float型，还有占8个字节的long long、double和long double型。从下图可得知visual C++中各种基本类型变量所支持的值域。

##bool类型
　　bool类型的变量只具有两个值，为true或者false。在C++中引入bool类型之前，常用int型变量来表示逻辑0和逻辑1，此时数值0为真，非零为假。如果尝试输出true和false所代表的数值，可以看到true代表1，false代表0，这样就统一了逻辑真的表示（如果用非零整数来表示真，则可以使用各种各样的非零值，这有时是不利的）。

　　在编译器中输入这两个值时，true和false显示为关键字。而TRUE和FALSE是MFC定义的符号，并不是关键字，也不是合法的bool值，因此不能混淆大小写。

##类型的确定
　　typeid操作符可以确定表达式的类型。运行下面程序：

		#include<iostream>
		using namespace std;

		void main(void)
		{
	
			bool n = true;
			float pi = 3.14;			

			cout<<typeid(n).name()
				<<endl
				<<typeid(pi).name()
				<<endl;
		}

　　可以看到，程序在第一行输出“bool”，在第二行输出“float”。typeid操作符产生的结果是一个对象，因此只可以按照上述操作方式来使用。在后述章节来详细学习这种操作方法。

##auto关键字
　　可以在变量定义时使用auto关键字作为变量的类型，如```auto n = 10;``` ``` auto pi = 3.14;```等，这种情况下，变量类型是根据字面值来确定的，这时n为int型，pi为float型。这也就意味着，每次给auto型变量定义时，就要为其赋予初始值，否则无法编译通过。运行下面程序：

		#include<iostream>
		using namespace std;

		void main(void)
		{
	
			auto e = 2.71828L;			

			cout<<typeid(e).name()
				<<endl;
		}

　　可以看到，程序输出“long double”，这是因为字面值2.71828的后面附加了L，代表此字面值的数据类型为long double型。

##类型的转换　　
　　C++中的计算只能在相同类型的值中进行，如果一个表达式中使用不同类型的变量，则编译器会把某个操作数的类型转换为与另一个操作数相匹配的数据类型之后再行计算。整个过程是隐式进行的，因此有时候将发生意想不到的效果。

　　将一种类型的变量转换为另一种类型，有可能造成信息丢失。为了避免这种危险情况的发生，应该避免数据类型的转换，或者在确定数据类型转换不会发生危险时，执行转换。在任何时候，都要尽量避免使用编译器来自动安排类型转换，因为编译器不能完全知晓编程者的意图，所以在需要转换某个数据类型时，尽量使用显示的类型转换，也叫强制类型转换。

　　老式的强制类型转换的操作方式是，在表达式之前使用圆括号来指明强制转换后的数据类型，如：``` int a = 0; float pi = 3.14f; a = (int) pi;``` 。这时，变量a的值为3，即pi的整数部分。

　　实际上，强制类型转换有很多种不同的情况，但老式的强制类型转换涵盖了所有情况，所以更容易出错。因此，新的C++标准定义了新的数据类型转换：```static_cast<要转换的数据类型>(表达式)```。用static_cast关键字是指明此强制类型转换在编译时检查，同样还有dynamic_cast，指在执行程序的时候检查转换，另外还有删除const属性的const_cast等。执行下面程序：

		#include<iostream>
		using namespace std;

		void main(void)
		{
	
			double f1=1.5;
			double f2=2.0;
			int number = static_cast<int>(f1) + static_cast<int>(f2);

			cout<<number
				<<endl;
		}

　　可以看到，程序输出3,恰好是f1和f2的整数部分。

##lvalue和rvalue
　　C++中每个表达式的结果，都是“lvalue”和“rvalue”中的一种，它们以不同的形式存贮在的计算机的内存当中，通常也写作“l-value”或“r-value”。“l”代表“左”的英文“left”，是因为所有产生lvalue的表达式都可以出现在赋值语句“=”的左边，它的结果会放置在内存中持续存储。与之相反的是rvalue，它只会被临时存储。例如：

		int a(0), b(1), c(2);
		a = b + c ;
		b = ++a;
		c = a++;

　　其中第一句是定义三个整形变量a、b、c，并赋予初始值。第二条语句中“b+c”的结果被临时存储在内存的一个区域中，它的结果是一个rvalue，当把它的值赋予a之后，存储“b+c”结果的内存位置便被丢弃。需要注意的是，第三条语句中“++a”是一个lvalue，因为它的结果是递增之后的a，而第四条语句中的“a++”是rvalue。只包含一个命名变量的表达式永远是lvalue。