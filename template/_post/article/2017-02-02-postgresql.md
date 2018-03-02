---
title: PostgreSQL的分组查询和关联查询
category: 学习笔记
tag: MySQL, PostgreSQL
---

## PostgreSQL与MySQL对比

相较于M有SQL，PostgreSQL有以下优势：

* MySQL不支持“hash join”和“sort merge join”以及很多其他的SQL语法，子查询性能低
* 不支持sequence
* 在线操作功能性弱，如建立索引锁表，增加列基本上是新建表等
* 性能优化工具和度量信息不足

<!--more-->
### 分组查询

典型场景，对于一个2列选课表，分别为课程名称和学生id，需要统计选课人数最多的表，使用分组查询，关键字为“GROUP BY”。
```
postgres=# \d curriculum_schedule
                 Table "public.curriculum_schedule"
   Column   |         Type
------------+-----------------------
 class_name | character varying(20)
 student_no | integer

postgres=# select * from curriculum_schedule ;
 class_name | student_no
------------+------------
 a          |          1
 a          |          2
 a          |          3
 b          |          4
 c          |          5
 c          |          6
(6 rows)

postgres=# select class_name, count(class_name) from curriculum_schedule group by class_name order by count(class_name);
 class_name | count
------------+-------
 b          |     1
 c          |     2
 a          |     3
(3 rows)
```
### 关联查询

关联查询一般用于多张表联合查询。对于上述的例子，假如还有一张student的表，将学号映射到学生姓名上，需要查出学生姓名所选的课程，则使用关联查询。
```
postgres=# \d student
                     Table "public.student"
 Column |         Type
--------+-----------------------
 no     | integer
 name   | character varying(40)

postgres=# select * from student ;
 no | name
----+-------
  1 | a_stu
  2 | b_stu
  3 | c_stu
  4 | d_stu
  5 | e_stu
  6 | f_stu
(6 rows)

postgres=# select class_name, name from curriculum_schedule c, student s where c.student_no=s.no;
 class_name | name
------------+-------
 a          | a_stu
 a          | b_stu
 a          | c_stu
 b          | d_stu
 c          | e_stu
 c          | f_stu
(6 rows)

postgres=# select class_name, name from curriculum_schedule c left join student s on c.student_no=s.no;
 class_name | name
------------+-------
 a          | a_stu
 a          | b_stu
 a          | c_stu
 b          | d_stu
 c          | e_stu
 c          | f_stu
(6 rows)
```

PostgreSQL的join分为5种形式：

1. inner join   返回的结果：两个表的交集行
2. left join   是left outer join的简写，返回结果：左表的所有记录，右表中字段相等的行，不相等的部分为NULL
3. right Join  是 right outer Join的简写，返回结果：右表的所有记录，左表中字段相等的行，不相等的部分为NULL
4. full join  是 full outer join的简写，返回结果：两个表的并集 连接字段不相等的部分为NULL
5. cross join 返回结果：把两个表进行一个n*m的组合即笛卡尔积


