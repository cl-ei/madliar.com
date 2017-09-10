---
layout: post
title: 学习C++之五：函数的指针
category: 学习笔记
description: 让函数做更多的事情
---
##函数的指针
　　在我们使用指针时，通常使用的是另一个变量的地址值，这样可以在不同的时间使用同一个指针来访问不同的变量。除此之外，指针还可以指向函数的地址，这也就意味着，我们也可以通过指针来调用函数。指针是不是很强大？

　　我们可以这样声明一个函数，并声明一个函数的指针来指向这个函数,并通过调用函数的指针来调用该函数：

		#include<iostream>
		using std::cout;
		using std::endl;

		double sum(int a, double b)
		{
			return (static_cast<double>(a) + b) ;
		}

		void main(void)
		{
			double (*psum)(int , double) = sum;

			cout<<psum(3,6)
				<<endl;
		}


　　程序输出结果9。需要注意的是，声明函数sum的指针psum时，用圆括号把*psum包含起来。如果不这么做，则实际上是在声明一个函数的原型，而不是在声明指针。还可以利用一个更简单的方法来声明函数指针，就是利用auto关键字，如：```auto psum = sum ;```只要之前定义了sum的函数原型，编译器就能够理解编程者的意图，自动将psum设定为sum函数的指针类型。另外，如果给函数指针赋予一个与声明时的函数原型不相同的函数，编译将不会通过，所以函数指针的声明要和指向函数的原型保持一致。

##为什么要用函数的指针
　　如同使用变量的指针一样，使用函数的指针可以利用一个函数指针，在不同的时候调用不同的函数。假如要编写这样一个函数：在某些情况下，该函数要产生数组中所有元素的平方和，而另一些情况下需要产生它们的立方和。一种实现方法是，利用函数的指针来作为实参。程序如下：

		#include<iostream>
		using std::cout;
		using std::endl;

		double squared(double a){
			return (a*a);
		}

		double	cubed(double a){
			return (a*a*a);
		}

		double sumarray(double count[], int length, double (*pfunction)(double)){
			double	total(0);

			for (int i = 0; i<length; i++)
				total += pfunction(count[i]) ;

			return	total;
		}

		void main(void){
			double	data[]={2.0, 4.0, 6.0, 8.0};
			int len = (sizeof(data) / sizeof(data[0]));

			cout<<"squared:"<<sumarray(data,len,squared)<<endl
				<<"cubed:"<<sumarray(data,len,cubed)<<endl;
		}

　　其中```int len = (sizeof(data) / sizeof(data[0]));```的作用是计算出数组data[]中元素的个数，给sizeof操作符传递数组名作为实参，则它会返回该数组占用的所有内存，再除以单个元素占用的空间，便不难得出数组元素的个数。程序的结果是在第一行输出squared:120，在第二行输出cubed:800。这恰好分别是数组data各元素的平方和和立方和。这里把函数的指针作为实参来传递给另一个函数供其调用，传递不同函数指针来执行不同的函数。当然可以用更简单的办法来实现，但在某些非常复杂的情况下，使用函数指针来处理事情显得更加方便。

##函数指针的数组
　　如同常规指针一样，可如下来使用函数指针数组：

		double fun1(double );
		double fun2(double );
		double fun3(double );

		double (*pfun[])(double ) = {fun1, fun2, fun3};

　　此时不能通过auto关键字来推测数组的类型，所以必须向上述一样声明函数指针的数组。数组的各个元素分别初始化为大括号里对应的函数的地址，数组长度由列表中的初始值的个数来决定。此时如果要调用数组中第二个元素，可以这样写：```pfun[1](a);```，其中a为double型的实参。

##为函数形参设定默认值
　　在声明函数时，可以给括号内的形参赋予初始值。如果在调用函数时没有填入参数，则函数按照默认值来执行，如果填入参数，则默认值将丢弃。例如 ```int sum(int a=30, int b=20){return (a+b);}```,如果执行```sum();```,则能得到返回值50。

　　如果在调用时省略形参，则只可以从右往左省略。例如，```int do(int a=1, int b=2, int c=3)```,如果要省略c，则只可以省略最后一个c，```do(4,5,)；```是一个正确的使用方法；如果要省略b，则c也必须省略，```do(3,,8);```是错误的使用方法，应该改写为：```do(3,,);```。