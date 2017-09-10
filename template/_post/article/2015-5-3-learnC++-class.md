---
layout: post
title: 学习C++之八：类
category: 学习笔记
description: 组织数据的一种方式
---
##类
　　类即class，和结构体有很多共同的地方，主要区别在于类的成员分为三种类型：公共、私有和受保护的。相较于结构体，类严格定义了对成员的访问的权限，以及全新的数据复制等机制。可以像下面定义一个类,并声明一个具体的对象：

		class CBook
		{
			public:
				CBook();
				~CBook();
				...
			private:
				int m_Page;
				int m_Year;
				...
			protected:
				...
		};

		CBook MathBook;

　　成员函数不必定义在类的内部，如需定义在外部同时避免调用程序时跳转的开销，可以将函数定义为内联函数。这样，程序的代码块会直接嵌入到函数声明的地方，提高运行效率。假设上述的类中有成员函数```int GetPage();```,则在类外可以这样定义：

		inline int CBook::GetPage()
		{
			return m_Page;
		}
		
　　其中添加“::”的目的是告诉编译器，后面的函数归于前面的类。类内的函数可以访问类内的成员，但类外的函数只能访问public成员。可以使用inline关键字将普通的函数也定义为内联函数，只要函数体比较短小，就不会显著增加代码的体积。

##友元函数
　　在类中可以定义一类可以访问任何成员的函数，被称为友元函数。在类中声明友元函数和声明普通成员函数的唯一区别在于，需要给友元函数的原型前添加friend关键字。因为友元函数不是类的成员，所以友元函数在类中声明的位置不影响函数的访问权限。友元函数总是可以被访问的，它拥有和普通成员函数同等的特权。可以向下面这样声明友元函数：

		class CBook
		{
			public:
				CBook();
				~CBook();
				...
			private:
				int m_Page;
				int m_Year;
				...
			protected:
				...
			friend void showPage(CBook & book);
		};

		void showPage(CBook & book)
		{
			cout << book.m_Page << endl;
		}

##类构造函数
　　类构造函数是特殊的函数，没有返回值，它唯一的作用是在创建具体类对象的时候调用。上述的类中，```CBook()```就是一个构造函数。在命名上，没有任何商量的余地，一个类的构造函数必须和类的名字完全相同。如果我们不去定义类构造函数，那么编译器会提供一个默认的构造函数，但它什么也不做。我们最多可以定义两个类构造函数，一个不带参数，另一个带参数。如下定义构造函数，并在适当位置声明两个具体对象：

		CBook::CBook()
		{
			m_Page=0;
			m_Year=2015；
			...
		}

		CBook::CBook(int page,int year...)
		{
			m_Page=page;
			m_Year=year;
			...
		}

		CBook MathBook;
		CBook EnglishBook(200,2015...);

　　如果我们只提供了上面第二个类构造函数，当我们执行语句```CBook MathBook;```编译器就会报错。因为编译器不再提供默认的构造函数```CBook()```，所以为了解决报错的问题，可以给上述第二个函数带上默认的实参，比如```CBook::CBook(int page = 0, int year = 2015, ...)```。要注意只有一个构造函数时才能这么做，如果同时还提供了默认的构造函数```CBook()```，那么当声明一个不带参数的类对象时，编译器不知道应该调用哪个类构造函数而报错，因为两个都适用。

##避免隐式的类型装换
　　当有时只使用一个参数来定义一个类对象时，可能会进行隐式的数据类型转换，有时需要避免这样的情况，可以在构造函数前添加关键字explicit。如果在构造函数前添加explicit，则不能用“=”来给一个类对象初始化，比如：```
		CBook EnglishBook = 200;```,因为这样会涉及隐式的类型转换。这时只能使用函数表示法来为具体的类对象初始化,比如```CBook EnglishBook(200);```。当然此处举例限定的情况是：假定构造函数只有一个参数。

##this指针
　　类中的任何成员函数在执行时，都会包含一个隐藏的指针，名为this指针，它指向调用该函数时使用的对象。诸如上述的```CBook::GetPage()```函数，其实就是使用this->m_Page。

##类的const对象
　　如果需要创建固定的类对象，只需要在声明时添加const关键字。比如```const CBook EngBook( ...);```，其中“...”表示CBook类定义的所有实参。这样一来，如果此类中有任何尝试修改类中成员的函数，都不允许被调用，否则编译器将报错。

　　同样，如果不希望某个成员函数修改成员的值，也必须将其定义为const函数，方法是在该函数的后面写上const关键字，比如：```int CBook::GetPage() const```，此时它也被称作只读函数，因为该函数的this指针也同为const型，所以在函数内不能将类的数据成员写在赋值语句的左边。 const成员函数也不能调用非const成员函数。

##类的静态成员
　　和普通函数的静态成员一样，类的静态成员可以独立于本类的任何具体对象，适用于成员函数和数据成员。当定义一个静态的数据成员时，必须在类内声明成员，而在类外初始化，因为类内只是描绘类的特性，而不是具体的对象。下面是一个定义类静态数据成员和成员函数的实例：

		class CBook
		{
			public:
				CBook();
				~CBook();

				int m_Page;
				int m_Year;
				...				
				static void ShowObjectCount()
			private:
				...
				static int ObjectCount;
			protected:
				...
		};

		int CBook::ObjectCount = 0;
		void CBook::ShowObjectCount()
		{
			cout << ObjectCount << endl;
		}

　　使用static成员函数的优势是，即使没有一个具体的类对象，也能调用它，比如可以执行```CBook::ShowObjectCount();```。

