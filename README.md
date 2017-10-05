## madliar.com

This is my personal blog, it's based on a tiny wsgi fremework which is written by myself and you can review it at the "madliar" repo. And this repo also contains some code snippets I have written to solve problems for myself.

## 简介

这是我的个人网站，构建于"nginx + uwsgi + madliar + redis"架构。其中madliar是我个人自制的Python后端web框架，使用类似Django的MVT视图，其他任何相关信息可以参见这个代码仓库：[https://github.com/cl-ei/madliar](https://github.com/cl-ei/madliar)。
这个网站分为三个主要模块，博客，音乐播放器，和一个允许第三方注册和使用的云笔记本。

![博客](/static/img/index.png)
![音乐](/static/img/music.png)

博客是一个单页面的网页，兼容移动端。交互逻辑几乎全部使用JavaScript处理。音乐播放器遵循简洁风格，访问地址：[https://www.madliar.com/music](https://www.madliar.com/music)

![笔记本](/static/img/notebook.png)

云笔记带有目录层级管理，支持markdown语法，支持为选中的文档创建分享链接。业务相关的逻辑代码在/application/notebook下，前端处理的逻辑在/static/notebook/main.js中定义。

## 其他

有任何的建议与批评，欢迎请给我发送邮件： i#caoliang.net。