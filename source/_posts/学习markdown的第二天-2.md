---
title: 学习markdown的第二天(2)
date: 2023-09-15 10:41:07
tags:
---



学习链接 [慕课网](https://www.imooc.com/wiki/markdownlesson/markdownparagraph.html)

<!--more-->

# 学习Markdown的第二天


<!-- ----------------------------分割线-------------------------- -->

## 1.markdown的前景色、背景色

<hr class="red">

### 1.1前景色
> 在 Markdown 文件中，建议使用 \<font> 标签的 color 属性修改文字颜色。
> 除了修改 color 属性外，还可以使用 style 样式属性修改文字颜色。

例子如下：
```
<font color="red">红色</font>
<font color="green">绿色</font>
<font color="blue">蓝色</font>

<font color="rgb(200, 100, 100)">使用 rgb 颜色值</font>

<font color="#FF00BB">使用十六进制颜色值</font>


#### 使用 `style` 的标签的修改文字前景色

<font style="color: red">红色</font>
<font style="color: green">绿色</font>
<font style="color: blue">蓝色</font>

<font style="color: rgb(200,100,100)">使用 rgb 颜色值</font>

<font style="color: #FF00BB">使用十六进制颜色值</font>

```
#### 使用 `style` 的标签的修改文字前景色
<font style="color: red">红色</font>  <font style="color: green">绿色</font><font style="color: blue">蓝色</font>

<font style="color: rgb(200,100,100)">使用 rgb 颜色值</font>

<font style="color: #FF00BB">使用十六进制颜色值</font>

### 1.2背景色
> Markdown 文档中定义文字背景色需要通过修改 style 样式实现。
```
#### 使用 `style` 属性修改文字的背景色

<font style="background: red">红色</font>
<font style="background: green">绿色</font>
<font style="background: blue">蓝色</font>

<font style="background: rgb(200,100,100)">使用 rgb 颜色值</font>

<font style="background: #FF00BB">使用十六进制颜色值</font>
```
#### 使用 `style` 属性修改文字的背景色

<font style="background: red">红色</font> <font style="background: green">绿色</font> <font style="background: blue">蓝色</font>

<font style="background: rgb(200,100,100)">使用 rgb 颜色值</font>

<font style="background: #FF00BB">使用十六进制颜色值</font>


<!-- --------------------------------分割线-------------------------- -->

## 2.markdown行内代码和代码块
<hr class="red">

>略


<!-- -------------分割线-------------------------- -->
## 3.markdown的超链接
<hr class="red">

### 3.1  介绍
>在 Markdown 文件中，使用 「中括号 [label]()」 声明超链接。
### 3.2 行内方式定义超链接细节
>当我们需要为超链接设置目标地址和标题时，可在中括号后增加小括号的形式实现 [text](url title)

### 3.3  介绍超链接细节的全局声明
```
#### 声明超链接的细节

[天坛][tiantan]公园，是明清两代皇帝每年祭天和祈祷五谷丰收的地方。[天坛][tiantan]以严谨的建筑布局、奇特的建筑构造和瑰丽的建筑装饰著称于世。

[tiantan]: http://www.tiantanpark.com 或者
[天坛]: http://www.tiantanpark.com
```
**声明超链接的细节**

[天坛][tiantan]公园，是明清两代皇帝每年祭天和祈祷五谷丰收的地方。[天坛][tiantan]以严谨的建筑布局、奇特的建筑构造和瑰丽的建筑装饰著称于世。

[tiantan]: http://www.tiantanpark.com

<!-- -------------分割线-------------------------- -->
## 4.markdown的图片
<hr class="red">

### 4.1  介绍
>在 Markdown 文件中，使用 \!\[替换文字](图片路径 "标题(可选)") 的形式定义图片

### 4.2 图片的全局声明
>当一张图片在文章中反复出现时，可以使用全局声明的形式，减少文章编写的工作量。方法同超链接

```
#### 插入一张图片

图片前的文字。

![](https://tva3.sinaimg.cn/crop.0.0.180.180.180/6d04a77djw1e8qgp5bmzyj2050050aa8.jpg?KID=imgbed,tva&Expires=1588529780&ssig=vNCcwnltm2)

图片后的文字
```
#### 插入一张图片

图片前的文字。

![](./学习markdown的第二天-2/download.jpg)

图片后的文字



<!-- ----------------------------样式设计------------------------------------------- -->
<style>
  h1{
    text-align:center;
  }
  h3{
    text-indent:1em;
  }

  h5,h6{
    text-align:center;
  }

p{
    text-indent:2em;
 }
 img{
    margin: 0 auto;
 }

hr.red {  
    margin:0;
    border: 1px;  
    height: 3px;  
    color: #333; /* 背景色 */  
    background-color: red; /* 线条颜色 */  
  }  
</style> 