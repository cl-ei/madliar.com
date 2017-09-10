---
layout: post
title: MySQL(2):常用数据类型
category: 学习笔记
description: MySQL的常用数据类型
tag: MySQL
---

## MySQL的数据类型

一、整数：

```
#类型				字节数
TINYINT			1
SMALLINT			2
MEDIUMINT			3
INT				4
BIGINT			8
```


二、实数（带小数）：

```
#浮点数类型			字节数
FLOAT				4
DOUBLE				8

#定点数
DEC,DECIMAL(M,D)	M+2			

#decimal(20,2):小数点前18位，小数点后2位

#位类型				字节数
BIT(M)				1~8
```

三、字符串：

```
CHAR(M)				#定长,M,M的范围0~255
VARCHAR(M)				#长度可变,0~65535,值的长度加1


TEXT				#字符字符集
	TINYTEXT
	TEXT
	MEDIUMTEXT
	LONGTEXT

BLOB			#二进制数据流
	TINYBLOB
	BLOB
	MEDIUMBLOB
	LONGBLOB
BINARY(M)			# 0~M个字节的定长字符串
```

四、日期：

```	
DATE 			4B
#只表示日期，1000-01-01 ~ 9999-12-31

DATETIME 		8B		
#1000-01-01 00:00:00 ~9999-12-31 23:59:59 精确到秒

TIMESTAMP		4B		
#1970~2038，时间戳，格林威治标准时间以来经历的秒数

TIME 			3B
#-838:59:59 ~ 838:59:59

YEAR			1B
#1901 ~ 2155
```

使用```now()```函数何以获得当前日期，例如插入一条当前时间的记录:

```
INSERT INTO tb_name(date,time,date_time) VALUES (now(),now(),now());
```

*选择原则

1、最小原则
2、简单原则
3、避免索引列上的NULL