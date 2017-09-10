---
layout: post
title: MySQL(4):常用查询方法
category: 学习笔记
description: MySQL的常用查询方法
tag: MySQL
---

## MySQL的常用查询方法

MySQL的查询语句主要以select为主。下面为主要的查询语句。

基本语法：

```
SELECT * FROM tb_name [WHERE CONDITION] 
```

1、将表的数据全部列出

```
SELECT * FROM tb_name
```

2、列出表的部分字段

```
SELECT field_1,field_2 ... FROM tb_name
```
例如：
```
mysql> desc main_info;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int(2)      | YES  |     | NULL    |       |
| name     | varchar(10) | YES  |     | NULL    |       |
| age      | int(2)      | YES  |     | NULL    |       |
| birthday | date        | YES  |     | NULL    |       |
| workyear | int(2)      | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+

mysql> select id,name from main_info;
+------+----------+
| id   | name     |
+------+----------+
|    1 | caoliang |
|    2 | liang    |
|    3 | zhangsan |
+------+----------+
```

3、查询不重复的记录
```
SELECT DISTINCT field FROM tb_name
```

4、排序和限制


```
SELECT * FROM tb_name [WHERE CONDITION] [ORDER BY field_1 [DESC/ASC],feild_2 [DESC/ASC] ... ]
```

其中DESC 为降序排列，ASC为升序排列，不指定则默认升序。后面可以跟多个字段，当有多条记录的第一个字段的值相同时，则按照语句规定的第二个字段的规则进行排序，否则这些记录将随机排序。例如：(注意id和workyear的排序)

```
mysql> select * from main_info ;                
+------+----------+------+------------+----------+
| id   | name     | age  | birthday   | workyear |
+------+----------+------+------------+----------+
|    1 | caoliang |   22 | 2015-09-16 |       10 |
|    2 | liang    |   21 | 2015-09-16 |       10 |
|    3 | zhangsan |   25 | 2015-09-16 |        9 |
|    4 | liang    |   21 | 2015-09-16 |       12 |
|    3 | lisi     |   25 | 2015-09-16 |       11 |
+------+----------+------+------------+----------+

mysql> select * from main_info order by id desc,workyear asc;
+------+----------+------+------------+----------+
| id   | name     | age  | birthday   | workyear |
+------+----------+------+------------+----------+
|    4 | liang    |   21 | 2015-09-16 |       12 |
|    3 | zhangsan |   25 | 2015-09-16 |        9 |
|    3 | lisi     |   25 | 2015-09-16 |       11 |
|    2 | liang    |   21 | 2015-09-16 |       10 |
|    1 | caoliang |   22 | 2015-09-16 |       10 |
+------+----------+------+------------+----------+

mysql> select * from main_info order by id desc,workyear desc;
+------+----------+------+------------+----------+
| id   | name     | age  | birthday   | workyear |
+------+----------+------+------------+----------+
|    4 | liang    |   21 | 2015-09-16 |       12 |
|    3 | lisi     |   25 | 2015-09-16 |       11 |
|    3 | zhangsan |   25 | 2015-09-16 |        9 |
|    2 | liang    |   21 | 2015-09-16 |       10 |
|    1 | caoliang |   22 | 2015-09-16 |       10 |
+------+----------+------+------------+----------+
```

5、隐藏部分记录

```
SELECT * FROM tb_name [LIMIT offset_start,row_count]
```
LIMIT的第一个参数为起始的行，默认为0，显示从起始行开始row_count行的记录。需要注意的是，它通常搭配ORDER BY命令一起使用，提供分页浏览的功能。

6、聚合操作
```
SELECT field_1,field_2 ... fun_name FROM tb_name
[WHERE CONDITION]
[GROUP BY field_1,field_2 ... [WITH ROLLUP] ]
[HAVING CONDITION]
```

上述的```fun_name```是聚合操作函数，例如求和操作```sum```，记录数```count```等。
"GROUP BY"表示分类的字段，比如统计相同姓名的人：
```
mysql> select  name,count(1) from main_info group by name WITH ROLLUP;
+----------+----------+
| name     | count(1) |
+----------+----------+
| caoliang |        1 |
| liang    |        2 |
| lisi     |        1 |
| zhangsan |        1 |
| NULL     |        5 |
+----------+----------+
```
而```WITH ROLLUP```表示在分类之后，将数据再聚合。可以看到上述最后一行，就是```WITH ROLLUP```输出的结果。

