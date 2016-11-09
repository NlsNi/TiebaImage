## Python爬虫小项目

**Python 版本 ： 3.5 **

- **getTiebaImage.py**

**功能描述:**

自动获取贴吧某个帖子中的所有**回复图片**（签名档以及其他网页中的图片不会获取到）

**参数说明:**

- url : 要爬取的帖子地址
- header: 浏览器头部信息，简单的反爬虫策略
- path: 本地保存路径
  ​

**使用:**

实例化一个对象，调用**download_image()**方法即可，添加了简单的异常处理，针对url无效、帖子中没有图片等情况。

- **getTiebaImageWithGui.py**

  在前者的基础上添加了基于PyQt5的GUI支持。

  ~~**bug**: 在下载线程中清空TextEdit会导致程序停止运行，待解决~~

  **bug**修复：bug产生的原因是在子线程中操作主UI导致程序crash,修复的方式是利用PyQt的信号和槽机制，当需要操作UI的时候，发射信号交给主线程的槽函数进行处理

**界面：**

添加了程序的icon和背景图片，效果如图(icon和背景请根据自己的审美和实际的现实效果进行调整)：

![gui](http://odh8qadsk.bkt.clouddn.com/20161026_225718.png)

设置icon和背景的PyQt代码如下，icon.jpg和bg.jpg与程序放在同一个目录下：

```python
# 设置Icon 和背景图片
icon = QIcon()
# C++ reference
# void QIcon::addPixmap(const QPixmap &pixmap, Mode mode = Normal, State state = Off)
icon.addPixmap(QPixmap('icon.jpg'), mode=QIcon.Normal, state=QIcon.On)
self.setWindowIcon(icon)
palette = QPalette()
palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))
self.setPalette(palette)
```

To-do

- [x] 完成在GUI界面中显示log以及getTiebaImage.py类中的错误提示
- [x] 添加线程支持，防止图片下载时候界面假死
- [x] 修复bug
- [x] 界面美化









