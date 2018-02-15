---
layout: post
title: How Jekyll Works
category: 学习笔记
description: Jekyll-bootstrap入门文档的翻译
---
## 学习Jekyll
　　最近开始学习jekyll和bootstrap，这就必须要学习一堆英文技术文档，虽然英文不是晦涩难懂，但看的多了便眼花缭乱，看了下句忘了上句。还是彻底翻译成中文再彻头彻尾看吧。  	

## 文档
　　以下将完整但简洁的介绍是Jekyll如何工作的。注意核心内容是介绍没有代码的快速替换. 这些信息并不打算明确教你做任何事,而是告诉你Jekyll世界的全貌.

　　学习这些核心内容（core concepts）将帮你避免一些常见挫折，并且帮你更好的理解包含在Jekyll-Bootstrap里面的代码示例.

## 初始设置
　　安装jekyll之后，你需要依照jekyll期望的方式来格式化你的网页目录，Jekyll-bootstrap合理地提供基本的目录格式。 

　　The Jekyll 应用程序的基本格式
Jekyll 希望你的网页目录按照下面这样建立:

		.
		|-- _config.yml
		|-- _includes
		|-- _layouts
		|   |-- default.html
		|   |-- post.html
		|-- _posts
		|   |-- 2011-10-25-open-source-is-good.markdown
		|   |-- 2011-04-26-hello-world.markdown
		|-- _site
		|-- index.html
		|-- assets
		    |-- css
		        |-- style.css
		    |-- javascripts


　　_config.yml 存储配置设置.

　　_includes 这个文件夹是局部视图.

　　_layouts 这个文件夹存放你的内容将要插入的主模板.你可以建立更多不同的layouts来存放不同的页面.

　　_posts 这个文档包含你的动态内容和公告. 需要按照这样的格式命名 @YEAR-MONTH-DATE-title.MARKUP@.

　　_site 一旦Jekyll完成转换，将会把生成的网页放置在这个目录.

　　assets 这个文件夹不是标准的jekyll结构.你创建根文件夹后，assets文档代表任何通用文件夹. 目录和文件不正确格式化将导致Jekyll不能正常为您服务.

　　(了解更多: https://github.com/mojombo/jekyll/wiki/Usage)

　　Jekyll 配置

　　Jekyll 这里列出完全支持各种配置选项: (https://github.com/mojombo/jekyll/wiki/Configuration)

## Jekyll 的内容
　　Jekyll内的内容是一个 post 或者一个 page. 这些内容 “objects” 将插入到若干个模板来来建立一个静态页面.

## Posts and Pages

　　posts 和 pages 可以使用 markdown, textile, or HTML 等标记语言. 它们都可以使用元数据分配title, url path, 甚至任意自定义元数据.

## Posts是如何工作的

　　建立Posts需要正确的格式化文件并将它放置_post文件夹.

　　格式化一个Post必须有一个有效的文件名，如：YEAR-MONTH-DATE-title.MARKUP .并且要放置到_posts文件夹中. 如果格式不正确，Jekyll将无法识别这是一篇Post. 借助正确的文件名，日期和标题会自动解析. 此外，每个文件必须含有YAML Front-Matter来返回它的前页. YAML Front-Matter 是一个有效的YAML语法，来指定给定文件的meta-data.

## Order
　　排序是Jekyll的重要组成部分，但很难指定一个自定义的排序策略. Jekyll只支持按时间倒序排序.

　　由于日期是硬编码到文件名格式, 所以改变时序,你必须改变文件名中的日期.

## Tags Posts
　　可以有标签作为它们的meta-data关联它们 . 通过提供posts的YAML前页，标签可以放置到posts里面 . 你可以访问发布具体标签的模板. 这些标签也会添加到 sitewide collection.

## Categories Posts
　　在YAML的前页可以被归类为一个或多个类别. 类别提供更多的意义在标记,它们可以反映在给定的URL路径. Note categories in Jekyll work in a specific way. 如果你定义一个以上的类别，你需要定义一个类别层次结构“set”.

　　示例：

		---
		title :  Hello World
		categories : [lessons, beginner]
		---
		
　　This defines the category hierarchy “lessons/beginner”. Note this is one category node in Jekyll. You won’t find “lessons” and “beginner” as two separate categories unless you define them elsewhere as singular categories.




		
