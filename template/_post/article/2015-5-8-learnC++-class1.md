---
layout: post
title: 学习C++之九：对象复制问题
category: 学习笔记
description: 组织数据的一种方式
---
##复制构造函数
　　构造函数是在创建一个类对象的时候，由系统自动调用的，复制构造函数也可以理解为构造函数一种，因为他们不仅有共同的函数名，而且他们的目的也十分相似。而复制构造函数是在复制一个对象时调用的。如果不去手动编写复制构造函数，系统会自动提供一个，但只是简单的复制类的各个成员。下面是一个实例：

		class CMassage
		{
		private:
			char* pMassage;
		public:
			CMassage(const char* text = "some massage."){
				pMassage = new char[strlen(text) + 1];
				strcpy_s(pMassage, strlen(text) + 1, text);
			}

			CMassage(const CMassage & aMsg){
				pMassage = new char [strlen(aMsg.pMassage) + 1];
				strcpy_s(pMassage,strlen(aMsg.pMassage) + 1,aMsg.pMassage);
			}

			~CMassage(){
				delete [] pMassage;
			}

			void Show() const {
				cout << pMassage << endl;
			}
		};


　　其中第一个函数是带有默认形参值的构造函数，初始化具体类对象时，如果不带形参就会把对象初始化为“some massage.”。第二个是复制构造函数，需要注意的是实参类型为const的类对象的引用。使用const是因为复制构造函数不需要修改类对象的值，如果不这么做，则在复制const型的类对象时，编译无法通过；使用引用的目的是，防止在给函数传递实参时，为了复制实参而对复制构造函数无休止的调用。

　　上述最后一个函数是该类的析构函数。在类对象到达作用域的结束位置时，系统调用析构函数释放为成员分配的内存空间。通常析构函数也做一些收尾工作，在程序结束后由系统调用。如果析构函数发生异常错误，有可能导致程序崩溃，所以我们也曾遇到过这种情况，在关闭某个软件后，还会弹出一个错误提示。

　　大多数人都知道，当类中含有指针或者数组类型的数据成员时，如果使用系统提供的默认复制构造函数就会发生潜在的危险。因为默认的构造函数会把两个对象的数据成员，也就是两个指针赋成同一个值，当其中一个类对象被析构后，如果还要使用另一个对象，就会发生一些异常状况，因为它的指针指向的空间已经被释放，可能是别的程序正在使用的一块空间。那么，如果在程序中不去复制两个同类的对象时，是否不再需要编写复制构造函数呢？看下面的实例：

		void DisplayMsg(CMassage X){
			X.Showit();
		};

		CMassage aMsg("hello world !");
		DisplayMsg(aMsg);

　　当没有编写复制构造函数时，上述函数在调用CMassage的具体对象X作为实参时，编译器会复制一个X的副本，因为实参的传递是按值传递进行的。当```DisplayMsg()```函数执行完毕后，系统会调用CMassage的析构函数，来释放副本的指针。需要注意的是，X的副本和X本身的成员指针都指向同一区域，因此只是调用了显示的函数```DisplayMsg()```，就同时把X的空间给删除掉了。

　　所以，当动态的给类中的成员分配内存时，必须编写复制构造函数。

##重载赋值运算符“=”
　　记得在之前的类构造函数中有提到，如果构造函数只有一个参数，而且没有指定为explicit方式来构造类对象，则可以使用“=”来初始化类的成员，但需要注意的是，在此过程中有可能涉及隐式的类型转换。可以运行下面的程序：

		#include<iostream>
		#include<cstring>

		using namespace std;

		class CMassage
		{
		private:
			char* pMassage;
		public:
			CMassage(const char * text = "some massage."){
				cout << "Construstor ... ";
				pMassage = new char[strlen(text) + 1];
				strcpy_s(pMassage, strlen(text) + 1, text);
				cout << "called !" << endl;
			}

			CMassage(const CMassage & aMsg){		
				if (pMassage != nullptr)  delete[] pMassage;
				pMassage = new char[strlen(aMsg.pMassage) + 1];
				strcpy_s(pMassage, strlen(aMsg.pMassage) + 1, aMsg.pMassage);
				cout << "Copy construstor called !" << endl;
			}

			~CMassage(){		
				cout << "Disconstrustor ... ";
				delete[] pMassage;
				pMassage = nullptr;
				cout << "called !" << endl;
			}

			void Showit() const {
				cout << pMassage << endl;
			}
		};
		void main()
		{
			{
				const char* const  p = "how are you?";
				CMassage aMsg = p;
				CMassage bMsg;
				bMsg = p;
				aMsg.Showit();
				bMsg.Showit();
			}
				while (true);
		}

　　先来分析一下上面的程序：先定义了指向常量字符串数组的常量指针p，然后用p来初始化aMsg，接着初始化bMsg，然后使bMsg等于p，最后显示输出。程序的构造函数中，一开始就输出“Construstor ...”，结束时输出“called!”，这有利于直观的观察构造函数执行的情况——如果函数执行到一半，就不会输出“called!”。析构函数也以同样的方式编写。如果按照我们的所想象的，程序应该输出：

		Construstor ... called !
		Construstor ... called !
		how are you?
		how are you?
		Disconstrustor ... called !
		Disconstrustor ... called !

但事实上，程序的输出是这样的：

		Construstor ... called !
		Construstor ... called !
		Construstor ... called !
		Disconstrustor ... called !
		how are you?
		[乱码]
		Disconstrustor ...

其中“[乱码]”表示程序在此处输出的是一串乱码。伴随而来的是，弹出一个debug的错误。而程序编译并没有任何错误和警告，在运行时却发生错误，为什么呢？

　　仔细分析程序的输出，发现有两点可疑的地方：一是，在整个过程中竟然调用了三次构造函数，在第三次构造函数调用完成后，紧接着又调用了一次析构函数；二是，程序在第二次调用析构函数的时候，崩溃了，此时析构函数尚未执行完毕。

　　首先说第一个可疑的地方。我们在main()函数中只声明了两个类对象实例，而第三次调用构造函数是什么作用呢？可能是用来给bMsg的pMassage来实现赋值。通过调试发现第三次的构造函数发生在语句```bMsg = p;```，因此这么推测貌似有一定道理。但是，为什么接着又调用一次析构函数呢？如果仅仅是给bMsg来赋值的话，是没有必要调用析构函数的——析构函数仅仅在一个类实例完成作用域后使用的，而此处的aMsg和bMsg显然没有到达作用域的结尾。没有新的对象产生，就不会调用析构函数。所以，此处的解释就是：在执行```bMsg = p;```的时候，一定产生了一个新的类对象，而且在这一句运行结束之后，新的对象的作用域也就结束了。

　　此时不难想到，在函数调用的时候，是“按值传递”的，它会创建一个实参的副本。所以，此处一定是创建了类对象的副本，恰好在```bMsg = p;```执行完毕后，副本的作用域也结束，正好符合上述的情况。但此处创建的副本，是谁的副本呢？显然，是指针p的副本，只不过在创建p的副本之后，系统又进行了一次隐式的类型转换，将“cont char *”转化为“CMassage”类型，第三次调用构造函数也就发生在此时。为了验证类型的转换也会调用类构造函数，可以运行下面的程序：

		void main()
		{
			{
				const char* const  p = "how are you?";
				static_cast<CMassage>(p);
			}
				while (true);
		}

可以看到，程序输出：

		Construstor ... called !
		Disconstrustor ... called !

　　接着分析。这时```bMsg = p;```并未执行完毕。它不去调用复制构造函数，而是调用赋值运算符“=”，来使得副本p的类实例的pMassage的值与bMsg的pMassage的值相等。此时，这两个指针指向同一块区域，内容是“how are you?”。然后副本p的类实例完成使命，调用析构函数将其删除。而此时，悲剧发生，因为bMsg.pMassage指向的空间也被释放了。

　　到了此时，第二个问题也迎刃而解，报告的错误是：


<img style ="max-width: 90%;display: block;margin: 20px auto;border: 1px solid #E2E2E2;padding: 5px;" src="/images/project/cpp1.jpg" alt="error1">


错误类型为_BLOCK_TYPE_IS_VAILD(pHead->nBlockUse)，可能正是因为一块内存在被释放的时候，它的头部里面的信息已经被改掉了，和预期的不一样。内存分配的程序往往在被分配出的内存块头部放上一些校验信息。这个信息内存的用户是不知道也不应该修改的。这样，在内存被释放的时候，内存分配程序就可以验对这个头部信息是否被改过了。若被改过，就说明发生了内存corruption. 这种corruption有两种可能性：要么是有人在内存越界写东西；要么就是这块内存已经被释放了，又被重复释放了一次。这与之前的推论非常吻合。

　　根据先创建的类对象后析构的原则，第二次调用析构函数显然是析构bMsg对象，正式因为它的内存已经被释放掉了，此处报告错误。到此为止，一切水落石出。

　　总结起来就是：

　　1、单独使用“=”为类对象赋值，就不会调用复制构造函数，而是调用赋值运算符来操作。

　　2、当一个实例转换为一个类类型实例时，会调用该类的构造函数。

　　3、函数按值传递时，会复制实参的副本。如果副本是一个类对象，在函数结束后，又会调用析构函数删除副本。

　　避免这种错误应该怎么做呢？前面说到，可以在构造函数钱添加“explicit”关键字，这样可以阻止运行```CMassage aMsg = p;```这样的语句，而只能使用函数表示法来初始化一个类对象（因为这时调用的不是赋值操作，而是类构造函数），如```CMassage aMsg(p);```。而使用```bMsg = p;```也同样非法，错误信息是“没有与这些操作数相匹配的运算符‘=’”。使用explicit会阻止隐式的转换，所有涉及隐式转换的语句都需要显示的指定，否则编译器报告为错误。

　　但这样做只能阻止```CMassage aMsg = p;```这样的语句，当程序中出现的时候报告为错误。有时候确实需要使用“=”来进行赋值，应该怎么做呢？此时，可以编写重载赋值运算符的成员函数，在类中添加：

		CMassage& operator=(const CMassage& xMsg)
			{
				if (this != &xMsg)
				{
					delete[] pMassage;
					pMassage = new char[strlen(xMsg.pMassage) + 1];
					strcpy_s(pMassage, strlen(xMsg.pMassage) + 1, xMsg.pMassage);
				}
				return *this;
			}

　　这样就定义了重载赋值运算符的函数，其中operator是关键字。这样一来，可以执行下面的语句：

		CMassage bMsg;
		bMsg = p;

　　如果还指定explicit的调用构造函数，则需要把```bMsg = p;```替换成```bMsg = static_cast<CMassage>(p);```，这样显式的将p转化为CMassage的类对象。否则，编译器告知没有与之匹配的操作符“=”。


##其他运算符的重载
　　。
