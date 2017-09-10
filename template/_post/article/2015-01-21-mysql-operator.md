---
layout: post
title: MySQL(3):运算符
category: 学习笔记
description: MySQL的运算符
tag: MySQL
---

## MySQL的运算符

一、算术运算

```
+			
-
*
/ 或 DIV		#除，若除数为0则返回NULL
% 或 MOD			#取余，MOD(12,3)相当于 12%3
```


二、比较运算符

```
=				#等于返回1
<> 或 !=		#不等于返回1
#上面两种运算符不能用于NULL的比较，操作数有NULL则返回NULL


<=>				#可用于NULL的比较

<
<=

>
>=

#上面四种大小比较运算符不能用于NULL的比较，操作数有NULL则返回NULL

BETWEEN			#存在于指定范围
#使用格式为 a BETWEEN min AND max; 判断时包含两端端点的值
#当三个操作数类型相同，相当于 a>=min and a<=max

IN				#存在于指定集合
#格式 a  in (var_1,var_2...) ; 列表中如果有a的值则返回1

IS NULL			
IS NOT NULL

LIKE			#统配符匹配
#格式 a LIKE %sub_str% ; 若a中含有sub_str则返回1
#例如：select 'hello_world' like '%llo%' ; 结果为1


REGEXP 或 RLIKE			#正则表达式
#格式 a REGEXP str_pat ;
```
三、逻辑运算符

```
NOT 或 !
#操作数为0返回1，为非零返回0，为NULL 则返回 NOT NULL

AND 或 &&
#有NULL 返回 NULL ,有0返回0 , 全部非零返回1

OR 或 ||
#有1返回1,  没1有NULL返回NULL ,没1没NULL 返回0

XOR 
#有NULL 返回NULL, 否则真假相同返回0，真假不同返回1
```

四、位运算符

```
&
|
^			#位异或
~			#位取反

>>			#移入补0，移出丢弃
<<
```

五、运算符的优先级
运算符优先级```由低到高```：

```
:=
||, OR, XOR
&&, AND
NOT
BETWEEN, CASE, WHEN, THEN, ELSE
=, <=>, >=, <=, <, >, !=, IS, LIKE, REGEXP, IN
|
&
<<, >>
-, +
*, /, %
^			#位异或
-, ~		#一元减号和一元比特翻转
!, NOT
```