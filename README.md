# 哥白尼整体介绍

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7Dat.png"></div>

### 项目概况

**项目名为 Kopernik，哥白尼**。众所周知，开普勒是哥白尼的忠实维护者，那么哥白尼对开普勒来说是必不可少的存在，这个项目也是如此，对于用惯开普勒自动化的测试人员来说，哥白尼更是不可或缺的存在

**PS：Kopernik 源代码不涉及公司业务与数据！！并且我离职后此项目已重构！！因此本项目仅供参考**

### 使用哥白尼的好处
- 一键迭代全部用例，方便快捷且不会出错
- 只用维护两种表，方便后期批量修改
- 数据库中文检索，便于查看用例步骤细节

**PS：构建自动化整体的时间节省了 58%，详情看[设计思路](https://github.com/CourserLi/Kopernik/blob/main/%E8%AE%BE%E8%AE%A1%E6%80%9D%E8%B7%AF.md)和[开发日志](https://github.com/CourserLi/Kopernik/blob/main/%E5%BC%80%E5%8F%91%E6%97%A5%E5%BF%97.md)！！**

### 注意事项
1. 哥白尼暂时只能用于邮件项目，且一键迭代 webmail 下面的全部用例分组（不包括 webmail，webmail 是用于存放不放在表单中的用例，不进行迭代）
2. 主要的使用场景：场景用例，其他的场景暂未开发

# 下载

### 下载 MongoDB

[Mongodb](https://www.mongodb.com/try/download/community) 下载到 D 盘

`Custom -> Data Directory 和 Log Directory -> 去掉 Install MongoDB Compass 的勾`

[MongoDB Shell](https://www.mongodb.com/try/download/shell) 也下载到 D 盘

`安装包解压到 D 盘`

[MongoDB Compass](https://www.mongodb.com/try/download/compass) 默认下载到 C 盘

然后将 `D:\Software\MongoDB\bin` 和 `D:\Software\Mongosh\bin` 添加到 path

在 D 盘根目录创建文件夹 `D:\Mongo_data\db` 和 `D:\Mongo_data\log`

```cmd
# 以管理员方式运行
# 启动 Mongodb 服务（一直启动）
mongod --dbpath "D:\Mongo_data\db" --logpath "D:\Mongo_data\log\mongodb.log" --serviceName "mongodb" --serviceDisplayName "mongodb" --install
# 在 “服务” 程序中，手动启动 Mongodb 进程（需要关闭时停止即可）
# 查看服务 http://127.0.0.1:27017/
```
```cmd
# 另开一个终端（连接 Mongodb）
mongosh
```

### 下载 python 库

```cmd
pip install -r requirements.txt
```

# 全部功能介绍

### 零、需要填写的参数

文件位置：`Kopernik\base\info.py`

**需要填写的参数：`cookies`、`headers ` 与你所在的小组（ `project_id ` 、`teamid`）**

PS：这里的 `cookies`、`headers ` 可以任意抓取开普勒的包，然后在 [curl 转换网站](https://curlconverter.com/) 复制对应的 `python` 代码，然后粘贴到 `info.py` 文件中；而 `project_id ` 、`teamid` 可以在 URL 上面清晰的看到，其代指的分别是团队 ID 和项目 ID。

### 一、主体功能 -- 表单迭代

**演示：在已有的用例分组上，创建新的场景用例（比如我想创建“已发送邮件查看”）**

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS74Zn.png"></div>

1. 先在场景用例表单中填写步骤

文件位置：`Kopernik\scenario-test\processing\场景用例\邮件查看.txt`

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS75aq.png"></div>

2. 在用例步骤表单中查看所需的步骤是否存在

文件位置：`Kopernik\scenario-test\processing\用例步骤\xxx.txt`

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7TiV.png"></div>

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7HRU.png"></div>

注意：用例步骤文件夹中的全部文件，它们的用例步骤都是可以用的，相当于在一个文件中，我将它们分开到不同的文件，纯粹是为了方便查看

3. 如果所需的步骤不存在，确定测试的接口，在邮件上测试并抓包

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7LM4.png"></div>

4. 在开普勒的专用测试（哥白尼）中，导入 cURL，更改所需参数，Ctrl + S 保存，再抓包

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7XL9.png"></div>

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7vZR.png"></div>

如果是获取 body 参数，则复制字符串作为 JSON 字面量，粘贴至用例步骤表单中

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zS7zIx.png"></div>

如果是获取 Query 或 参数提取 等参数，不用抓包，可以参考其他步骤填写的，自行填写即可

诸如此类，直到所需的用例步骤全部填写完成

5. 确认场景用例表单中所需的，在用例步骤表单中都能找到

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHpi6.png"></div>

6. 运行表单迭代文件，一键迭代至开普勒

```bash
python Kopernik\scenario-test\表单迭代.py
```

**演示：创建新的用例分组**

1. 在开普勒中创建新分组（并记录 serviceid ）

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSH9JK.png"></div>

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHPzD.png"></div>

2. 在基类文件 demand 中添加新的用例分组

文件位置：`Kopernik\base\demand.py`

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHFQe.png"></div>

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHksH.png"></div>

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHVeA.png"></div>

在这三处地方的开头，按照规律填写新的 serviceid 即可

### 二、主体功能 -- 用例检索

直接运行用例检索文件即可

```bash
python Kopernik\用例检索.py
```

在浏览器打开 http://127.0.0.1:5000

<div align=center><img src="https://s1.ax1x.com/2022/11/09/zSHZdI.png"></div>

可根据关键字搜索对应用例

### 三、其他功能

具体看 设计思路 文件，包含了各种细化功能，也可以查阅代码理解

文件位置：`Kopernik\设计思路.md`