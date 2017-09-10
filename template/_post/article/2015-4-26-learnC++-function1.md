---
layout: post
title: 学习C++之四：让函数操作实参
category: 学习笔记
description: 让函数做更多的事情
---
##函数
　　当编写一个大型程序的时候，将不同的工作分配给不同的模块函数来完成，是一个明智的做法。当一个函数调用另一个函数的时候，如果被调用的函数声明需要传递一些参数才能工作，则传递给它的参数是某些变量、常量的副本，也就是说，函数的调用时传递数据是通过按值传递机制来进行的。实际的参数并没有传递给被调用的函数，这样一来可以有效的保护实参不被篡改。但有时确实要修改实参，这时，我们有以下几种办法让函数来操作实参。

##给函数传递指针实参和引用实参
　　一个经典的例子：

		#include<iostream>
		using std::cout;
		using std::endl;

		void exchange(int* a, int* b){
			int temp(0);
			temp = *b;
			*b = *a;
			*a = temp;
		}

		void main(void){
			int x(10),y(20);
			exchange(&x,&y);
			cout<<x << ','<<y
				<<endl;
		}

　　程序输出：20,10。程序的作用是给两个变量调换数值。同样，可以通过传递引用实参来使函数操作实参：	

		#include<iostream>
		using std::cout;
		using std::endl;

		void exchange(int& a, int& b){
			int temp(0);
			temp = b;
			b = a;
			a = temp;
		}

		void main(void){
			int x(10),y(20);
			exchange(x,y);
			cout<<x << ','<<y
				<<endl;
		}

　　两次运行程序结果相同。因为在我们给函数传递指针实参的时候，系统会给函数传递一个指针的副本，但这个指针副本指向的地址和实参指向的是同一区域，因为我们可以在函数中操作实参。

　　数组是唯一不能按值传递的数据类型，传递给函数的是该数组首个元素的指针的副本。因此，在函数中大可以随意操作指针副本，而不必担心数组的指针发生改变。运行下面程序：

		#include<iostream>
		using std::cout;
		using std::endl;

		void change(int a[])
		{
			a++;
			cout<<a
				<<endl;
		}

		void main(void)
		{
			int x[10];

			cout<<x
				<<endl;

			change(x);

			cout<<x
				<<endl;
		}

　　程序会输出三个地址，而第一行的值等于第三行，第二行的值等于第一行的值+4。虽然在函数change()中对数组的地址经行了递增操作，显然操作的只是传递给函数change的指针副本，因此实参数组x[]的地址并未改变。

##给函数传递不确定数量的实参
　　有时候，我们需要给函数传递不确定数量的实参，这时该怎么办呢？可以分析下面的程序：

		#include<iostream>
		#include<cstdarg>
		using std::cout;
		using std::endl;

		void sum(int count, ...){

			va_list pArgument;
			va_start(pArgument,count);

			int a = 0;
			for(int i=0;i<count;i++)
			{
				a = va_arg(pArgument,int);
				cout << a << endl;	
			}
			va_end(pArgument);
		}

		void main(void)
		{
			sum(7,1,2,3,4,5,7,6);
		}

　　应该注意到，此次在程序中包含了<cstdarg>头文件。其中，sum()函数的作用是，把传入的每个实参输出显示。程序运行结果：

		1
		2
		3
		4
		5
		7
		6

　　省略号代表可以传递任意多的实参到函数sum(),但使用时必须确定数量。上面用count来表示传入的实参数量，另一种确定传入实参数量的办法是，给最后一个实参打上特殊标记，在函数中检查和识别。

　　函数在运行时，首先创建了一个va_list型的指针pArguement，用来依次指向各个实参。然后调用va_start()函数来初始化pArguement，使其指向第一个实参。在for循环中，va_arg的宏返回pArguement指向的实参值，其中第二个参数int是返回实参值的类型。最后使用va_end来释放pArguement指针，使其指向一个空值，函数结束。

　　