---
layout: post
title: 自己动手做极简风音乐播放器
category: 学习笔记
tags: 编程
---
 
<img src="/static/blog/img/project/20160826/0.jpg" style="width:100%;"/>

　　我打算在博客里添加上这些音乐。没有适合本页风格的js插件可以使用，所以手动实现了。
<!--more-->

　　最开始的那一版是初学js的时候做的，由于对js的不熟练，遇到问题了总是各种百度，导致最后逻辑混乱、jQuery和js原生方法胡乱交织一起，显得十分拙劣（虽然现在也很拙劣）。而最近对其进行了重新整理，较之前有一些改观，现在发布出来欢迎拍砖。

## 一、简介

　　这是一个无后台的简易的音乐播放器，点击这里查看全部代码<a target="_blank" href="https://github.com/cl-ei/music_player">https://github.com/cl-ei/music_player</a>。你可以按照下述方式把这个播放器嵌入到任意html中：

```
<iframe src="https://music.caoliang.net/ref/"
        frameborder="0" 
        scrolling="no"
        marginheight="0"
        marginwidth="0"     
        width="350px"  
        height="150px"
        style=" border: 1px solid #000;">
</iframe>
```

　　效果如下：
<center>
<iframe name="frame" 
        src="https://music.caoliang.net/ref/"
        frameborder="0" 
        scrolling="no"
        marginheight="0"
        marginwidth="0"     
        width="350px"  
        height="150px"
        style=" border: 1px solid #000;">
</iframe>
</center>

　　如果你部署在自己的服务器上，将src替换为```src="/ref/index.html"```。所有音乐存放在```/music```目录下，同时将音乐文件名写到```/ref/index.html```文件中的```<script>```标签里即可。如下：

```
<script type="text/javascript">
music_list = [
    "Nightingale - Yanni.mp3",
    "暮色苍然 はちみつれもん.mp3",
    "Comtine D'un Autre Ete L'apres Midi  Yann Tiersen.mp3",
    "夜的钢琴曲(五) 石进.mp3",
    "さよならの夏 手嶌葵.mp3",
    ... ...
];
</script>
</body>
```
## 二、页面结构
　　HTML页面主要分为两层。第一层是标题和按钮，第二层是列表和3个按钮。列表的滚动其实是调整margin-top属性，外加一个list_border的div将列表超出的部分隐藏掉。除了UI简陋以外，目前依然有很多做的不够好的地方，例如点击进度条不能直接将滑块置于点击位置、必须拖动，还有列表滑动不能支持触控等。这些希望以后慢慢改进。

　　标题“CL's 疯言疯语”在最初是```<p>```标签，使用的是Microsoft YaHei UI Light字体，但很多电脑没有内置此字体，所以常会显示很low的宋体，偶尔会格式错乱，所以在后来改为了图片。但chrome浏览器对图片的缩放会使用优化算法处理图像的边缘，这使得字体边缘变得模糊，所以在chrome浏览器上的体验反而会更差。如下图，左右分别为chrome浏览器、Edge浏览器的效果。后续依然会解决这个问题。当然，欢迎高手告知我解决办法，不胜感激。

![虚化](/static/blog/img/project/20160826/1.bmp)

　　另外，有的网页背景音乐关不掉，每次一打开页面就会烦人的播放音乐，这是非常令人反感的。这里使用了三个cookie，分别记录播放位置和播放状态。如果第一次打开页面，它会自动播放第一首歌。而之后的一个月内再次打开页面，它会记录关闭前的状态，如果之前是暂停的，此时也会暂停；如果之前在播放，此时会断点续播。
