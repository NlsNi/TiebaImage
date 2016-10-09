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

实例化一个对象，调用**down_load()**方法即可，添加了简单的异常处理，针对url无效、帖子中没有图片等情况。

- **getTiebaImageWithGui.py**

  在前者的基础上添加了基于PyQt5的GUI支持。

  **bug**: 在下载线程中清空TextEdit会导致程序停止运行，待解决

To-do

- [x] 完成在GUI界面中显示log以及getTiebaImage.py类中的错误提示
- [x] 添加线程支持，防止图片下载时候界面假死
- [ ] 修复bug
- [ ] 界面美化









