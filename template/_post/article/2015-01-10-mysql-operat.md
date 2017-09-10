---
layout: post
title: MySQL(1):常用操作
category: 学习笔记
description: MySQL的常用操作
tag: MySQL
---

## MySQL的常用操作

1、DDL，数据定义语句

定义数据段、数据库、表、列、索引等数据库对象。
```
create
drop
alter
```

2、DML，数据操纵语句

添加、删除、更新、查询。
```
insert
delete
update
select
```
3、DCL，数据控制控制

定义安全和权限级别。
```
grant
revoke
```
### 一、DDL

1、查看数据库

```
SHOW DATABASES
```

2、查看表的列表

```
SHOW TABLES 
SHOW TABLES FROM db_name
```

3、创建数据库

```
CREATE DATABASE db_name
```

4、删除数据库

```
DROP DATABASE db_name	
```

5、选择操作的数据库

```
USE db_name
```

6、创建表

```
CREATE TABLE tb_name(
	column_name_1	column_type_1	constraints,
	 #项名称			项数据类型		约束条件
	 ...
	column_name_n	column_type_n	constraints
)
```

7、查看表的定义(项目)

```
DESC tb_name
```

8、删除表

```
DROP TABLE tb_name
```

9、重定义表项类型

```
ALTER TABLE tb_name MODIFY column column_define [FIRST / AFTER col_name]		
```

例如：将表user_info的user_name列的数据类型改为varchar(20)

```
ALTER TABLE user_info MODIFY user_name varchar(20)
```

10、增加表字段(项)

```
ALTER TABLE tb_name ADD col_name col_define [ FIRST / AFTER col_name ]
```

例如：在表 user_info 的 user_name 项之后，增加一项 user_age

```
ALTER TABLE user_info MODIFY user_age int(2) AFTER user_name
```

11、删除表字段(项)

```
ALTER TABLE tb_name DROP col_name
```

12、字段更名

```
ALTER TABLE tb_name CHANGE old_col_name new_col_name col_define
```

13、修改排序,参见“重定义表类型”

只要表项的名称、定义为变，通过最后一个可选参数[FIRST / AFTER col_name]来指定顺序。

```
ALTER TABLE tb_name MODIFY column column_define [FIRST / AFTER col_name]
```
14、更改表名称

```
ALTER TABLE tb_name RENAME new_tb_name
```

### 二、DML

1、查看记录

```
SELECT * FROM tb_name
```

2、插入记录

(1)插入一行

```
INSERT INTO tb_name(field_1,field_2...) VALUES(var_1,var_2...) 
```

例如，表main_info 插入一条记录。某些项允许为NULL时可以跳过。

```
INSERT INTO main_info(name,age,birthday) VALUES('caoliang',24,'1992-01-01');
```

不指定名称时，VALUES的序列要和表定义相匹配。
如表main_info:

```
mysql> desc main_info;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| name     | varchar(10) | YES  |     | NULL    |       |
| age      | int(2)      | YES  |     | NULL    |       |
| birthday | date        | YES  |     | NULL    |       |
| workyear | int(2)      | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
```

可以使用：
```
INSERT INTO main_info VALUES('zhangsan',30,'1992-01-01',5);
```

(2)插入多行

```
INSERT INTO tb_name(field_1,field_2...) 
VALUES
(recd_1_var_1,recd_1_var_2...),
(recd_2_var_1,recd_2_var_2...),
(recd_3_var_1,recd_3_var_2...),
...
```
每一条记录值后面有逗号分隔。

2、更新记录(更改记录的值)

```
UPDATE tb_name SET field_1=var_1,field_2=var_2 ... [ WHERE CONDITION]
```
WHERE CONDITION为更新的条件，如改变下面的数据库张三的id改为0

```
mysql> select * from main_info;
+------+----------+------+------------+----------+
| id   | name     | age  | birthday   | workyear |
+------+----------+------+------------+----------+
| NULL | zhangsan |   30 | 1992-01-01 |        5 |
|    1 | caoliang | NULL | 1993-01-01 |     NULL |
+------+----------+------+------------+----------+

mysql> update main_info set id=0 where name='zhangsan';
Query OK, 1 row affected (0.01 sec)

mysql> select * from main_info;                        
+------+----------+------+------------+----------+
| id   | name     | age  | birthday   | workyear |
+------+----------+------+------------+----------+
|    0 | zhangsan |   30 | 1992-01-01 |        5 |
|    1 | caoliang | NULL | 1993-01-01 |     NULL |
+------+----------+------+------------+----------+
```

update 命令可以改变多条记录的值。例如：

```
UPDATE main_info addi_info SET main_info.id = addi_info.cxid WHERE main_info.age = 12
```

3、删除记录

```
DELETE FROM tb_name WHERE condition
```

如上面的数据库，删除张三：

```
DELETE a FROM main_info a WHERE a.name='zhangsan';
```

a为main_info的别名。另外，如果不加附加条件去执行```DELETE FROM tb_name;```会清空整个表，此操作较为危险。

	




	
