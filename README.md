Zhihu-Scraping：提取知乎信息
===============================

# 简介

本程序的目标是快速的提取知乎上的信息，包括问题、回答、专栏、收藏夹、关注列表等等。

本程序代码在 Mac OS X 10.10.4 上使用 python2.7.6 编写和测试通过，其他环境可能存在一定问题。

# 依赖

- 使用 Beautiful Soup 4 <http://www.crummy.com/software/BeautifulSoup/> 解析 html 文档
- 使用 requests <https://github.com/kennethreitz/requests> 处理 http 请求
- 使用 html2text <https://github.com/aaronsw/html2text> 进行格式转换
- 使用 xlwt <https://github.com/python-excel/xlwt> 将数据写入 excel 表格
- 使用 lxml parser 来对 html 内容进行梳理 
没有的话可以使用 pip 安装：

    $ pip install requests
    $ pip install beautifulsoup4
    $ pip install html2text
    $ pip install xlwt
    $ pip install lxml

# 文件概述

Zhihu-Scraping 主要文件共有8个，其中 zhihuScraping.py 是运行程序和测试的地方，其他七个文件含有不同模块的实现，另有一个配置文件为
config.ini , 将这九个文件下载到你的工作目录，并修改 config.ini 文件中的 email 为你的知乎账户邮箱，修改 password 为你的知乎账户密
来模拟登陆。由于可能涉及频繁登陆，本程序要求使用者修改并根据个人情况补充 config.ini 中的 cookie 项以避免频繁登陆后被要求输入验证码而无法登陆

**注意** ：一定记得修改 config.ini 文件，否则无法正常使用。

以下是不同文件的解析：

login.py:

模拟用户登录，并传递登陆后的 session ，要使用需要修改 config.ini

user.py:

user 文件里主要包含了 User 类，可以处理用户相关的信息。创建一个 User 类对象需要输入一个 url，比如

    import user

    user_url = "http://www.zhihu.com/people/talich"
    new_user = user.User(user_url)


**注意** ：如无特殊说明，本程序所有 url 都应该以 "http://" 开头

answer.py:

answer 文件里主要包含了 Answer 类, 可以处理回答相关的信息。 创建一个 Answer 类对象需要输入一个 url，比如

    import answer

    answer_url = "http://www.zhihu.com/question/33488763/answer/56619442"
    new_answer = answer.Answer(answer_url)

question.py:

question 文件里主要包含了 Question 类, 可以处理问题相关的信息。 创建一个 Question 类对象需要输入一个 url，比如

    import question

    question_url = "http://www.zhihu.com/question/33488763"
    new_question = question.Question(question_url)

column.py:

column 文件里主要包含了 Column 类, 可以处理专栏相关的信息。 创建一个 Column 类对象需要输入一个 url，比如

    import column

    column_url = "http://zhuanlan.zhihu.com/booooks"
    new_column = column.Column(column_url)

collection.py:

collection 文件里主要包含了 Collection 类, 可以处理收藏夹相关的信息。 创建一个 Collection 类对象需要输入一个 url，比如

    import collection

    collection_url = "http://www.zhihu.com/collection/19559479"
    new_collection = collection.Collection(colection_url)

topic.py:

topic 文件里主要包含了 Topic 类, 可以处理话题相关的信息。 创建一个 Topic 类对象需要输入一个 url，比如

    import topic

    topic_url = "http://www.zhihu.com/topic/19550429"
    new_topic = topic.Topic(topic_url)

# 快速开始
- 由于每一类对象都有很多 API 函数，这里将仅仅举一些非 API 的函数来作为例子。但每个函数的功能在对应的文件里都有注释，如果有不清楚的地方可以参考对应的文件。ZhihuScraping.py 里也有每个函数的测试例子。

User ---- 知乎用户操作类:

假设我们想要保存知乎用户 talich (http://www.zhihu.com/people/talich) 的所有问题、回答、专栏文章和收藏，我们可以

    import user

    user_url = "http://www.zhihu.com/people/talich"
    new_user = user.User(user_url)
    new_user.save_asks() (保存所有问题。在目录下会自动声称 .txt 文本，文本里有该用户的所有问题)
    new_user.save_answers() (保存所有回答。在目录下会自动生成文件夹，文件夹里有该用户的所有回答)
    new_user.save_column() (保存所有专栏文章。对于用户的每个专栏，在目录下会自动生成一个文件夹，文件夹里有该专栏的所有文章)
    new_user.save_collections() (保存所有收藏夹回答。对于用户的每个收藏夹，在目录下会自动生成一个文件夹，文件夹里有该收藏夹的所有文章)

假设我们想要保存知乎用户 talich (http://www.zhihu.com/people/talich) 的所有 follower (关注者) 和 followee (关注了) 资料，我们可以

    import user

    user_url = "http://www.zhihu.com/people/talich"
    new_user = user.User(user_url)
    new_user.save_followers_profile() (保存所有 follower 资料。在目录下会自动生成 .xls 的 excel 表格，里边有该用户所有 follower 的资料)
    new_user.save_followees_profile() (道理基本同上)

**注意** 当用户关注者很多时 save_followers_profile() 函数运行可能需要花一定时间

**注意** 建议不要提取用来登陆的账号的信息，可能会有bug；可以专门注册另一个账号来进行信息提取

Answer ---- 知乎答案操作类:

假设我们想要保存知乎回答 http://www.zhihu.com/question/33488763/answer/56619442 和所有点赞同的用户的资料，我们可以
    
    import answer

    answer_url = "http://www.zhihu.com/question/33488763/answer/56619442"
    new_answer = answer.Answer(answer_url)
    new_answer.save_answer_to_file() (保存回答。在目录下会自动生成一个 .txt 文本，文本里有回答的相关信息)
    new_answer.save_all_voters_profile() (保存点赞同的用户的资料。在目录下会自动生成一个 .xls excel 文件，文件里有用户资料)

[save_all_voters_profile() 效果实例] (http://www.zhihu.com/question/27297651/answer/56895614)

**注意** 当答案的赞同很多时 save_all_voters_profile() 函数运行可能需要花一定时间

Question ---- 知乎问题操作类:

假设我们想要保存知乎问题 http://www.zhihu.com/question/33488763 和所有回答和所有关注着的资料，我们可以

    import question

    question_url = "http://www.zhihu.com/question/33488763"
    new_question = question.Question(question_url)
    new_question.save_all_answers() (保存所有回答。在目录下会自动生成一个名为问题标题的文件夹，文件夹里有所有回答)
    new_question.save_all_followers_profile() (保存所有关注者资料。在目录下会自动生成一个 .xls excel 文件，文件里有所有关注者的资料)

**注意** 当问题的回答很多时 save_all_answers() 函数运行可能需要花一定时间

**注意** 当问题的关注者很多时 save_all_followers_profile() 函数运行可能需要花一定时间

Column ---- 知乎专栏操作类:

假设我们想要保存知乎专栏 http://zhuanlan.zhihu.com/booooks 的所有文章和所有关注者资料，我们可以

    import column

    column_url = "http://zhuanlan.zhihu.com/booooks"
    new_column = column.Column(column_url)
    new_column.save_all_posts() (保存专栏所有文章。在目录下会自动生成一个名为专栏标题的文件夹，文件夹里有所有文章)
    new_column.save_all_followers_profile (保存专栏所有关注者资料。在目录下会自动生成一个 .txt 文本，文本里有所有关注者资料)

**注意** 当专栏的关注者很多时 save_all_followers_profile() 函数运行可能需要花一定时间

Collection ---- 知乎收藏夹操作类:

假设我们想要保存知乎收藏夹 http://www.zhihu.com/collection/19559479 的所有回答和关注者资料，我们可以

    import collection

    collection_url = "http://www.zhihu.com/collection/19559479"
    new_collection = collection.Collection(colection_url)
    new_collection.save_questions_and_answers() (保存收藏夹所有回答。在目录下会自动生成一个名为收藏夹名的文件夹，文件夹里有所有回答)
    new_collection.save_all_followers_profile() (保存收藏夹所有关注者资料。在目录下会自动生成一个 .txt 文本，文本里有所有关注者资料)

**注意** 当收藏夹的回答很多时 save_questions_and_answers() 函数运行可能需要花一定时间

**注意** 当收藏夹的关注者很多时 save_all_followers_profile() 函数运行可能需要花一定时间

Topic ---- 知乎话题操作类:

假设我们想要保存知乎话题 http://www.zhihu.com/topic/19550429 的所有精华回答和最近动态，我们可以

import Topic

    topic_url = "http://www.zhihu.com/topic/19550429"
    new_topic = topic.Topic(topic_url)
    new_topic.save_top_answers() (保存话题所有精华回答。在目录下会自动生成一个文件夹，文件夹里有所有精华回答)
    new_topic.save_latest_feed() (保存话题最近动态。在目录下会自动生成一个文件夹，文件夹里有所有最近动态(回答))

**注意** 当话题的精华回答很多时 save_top_answers() 函数运行可能需要花一定时间

# 下一步

以这个程序为基础，一部分可能的下一步工作：

- 模拟用户操作，比如批量拉黑某个回答的赞同者，或批量关注某个问题下所有答案的作者

- 使用python的数据分析和绘图包对收集到的数据进行分析并可视化


# License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# 声明与感谢

- 本程序受到 @egrcc <https://github.com/egrcc> 的 zhihu-python <https://github.com/egrcc/zhihu-python> 程序的启发且本程序的一部分是在该程序基础上修改而得到的，该程序的LICENSE可以在Credits.txt里找到

- 特别感谢 @Zhang NS <https://github.com/zhangns> 在程序开发与测试过程中提供的帮助


# 关于作者

- github：@LiZifan <https://github.com/LiZifan>
- email：lizifanterry@gmail.com
