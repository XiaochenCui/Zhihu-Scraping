# -*- coding: utf-8 -*-
__author__ = 'lizifan'

# Copyright (C) 2015 Zifan Li

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import time
from user import User
from answer import Answer
from question import Question
from column import Column
from collection import Collection
from topic import Topic
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def user_test():
    start = time.time()
    user = User("http://www.zhihu.com/people/talich")
    user.parser()
    print "User ID is ", user.get_id()
    print "User sex is ", user.get_sex()
    print "Number of followee is ", user.get_followee_num()
    print "Number of follower is ", user.get_follower_num()
    print "Number of agree is ", user.get_agree_num()
    print "Number of thanks is ", user.get_thanks_num()
    print "Number of asks is ", user.get_asks_num()
    print "Number of answers is ", user.get_answers_num()
    print "Number of posts is ", user.get_posts_num()
    print "Number of collections is ", user.get_collections_num()
    print "Number of log is ", user.get_logs_num()
    print "Number of columns followed is", user.get_column_followed_num()
    print "Number of topics followed is", user.get_topic_followed_num()
    print "Number of profile view is ", user.get_view_num()
    print "Column url is ", user.get_columns_url()
    print "Collection url is ", user.get_collections_url()
    print user.get_column_followed()
    print user.get_topic_followed()
    print "Robot test ", user.is_robot()
    user.save_basic_info()
    # user.save_followers_profile()  # might be time-consuming
    user.save_followees_profile()
    user.save_asks()
    user.save_answers()
    user.save_latest_activity()
    user.save_all_activity()  # might be time-consuming
    user.save_columns()  # might be time-consuming
    user.save_collections()  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


def answer_test():
    start = time.time()
    answer = Answer('http://www.zhihu.com/question/33488763/answer/56619442')
    answer.parser()
    print "Author is ", answer.get_author()
    print "Question url is ", answer.get_question_url()
    print "Question text is ", answer.get_question_text()
    print "Number of vote is ", answer.get_vote_num()
    print "Answer content is ", answer.get_content()
    print "Number of comment is ", answer.get_comment_num()
    print "Number of view is ", answer.get_view_num()
    print "Number of time being collected is ", answer.get_collected_num()
    print "Created time is ", answer.get_created_time()
    print "Last modified time is ", answer.get_last_modified_time()
    answer.save_answer_to_file()
    answer.save_all_comments()
    print "Answer robot vote rate is {0}".format(answer.save_all_voters_profile())  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


def question_test():
    start = time.time()
    question = Question("http://www.zhihu.com/question/33488763")
    question.parser()
    print "Title of the question is ", question.get_title()
    print "Tags of the question is ", question.get_tags()
    print "Details of the question is ", question.get_details()
    print "Number of answer of the question is ", question.get_answer_num()
    print "Number of collapsed answer of this question is ", question.get_collapsed_answer_num()
    print "Number of follower of this question is ", question.get_follower_num()
    print "Number of view of this question is ", question.get_view_num()
    print "Number of comment of this question is ", question.get_comment_num()
    print "Last activity time of this question is", question.get_last_activity_time()
    print "Number of follower of related tags is", question.get_related_tags_follower_num()
    print "First known follower of this question is ", question.get_first_known_follower()
    print "Related questions are ", question.get_related_questions()
    question.save_top_answers(3)
    question.save_all_answers()  # might be time-consuming
    question.save_all_followers_profile()  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


def column_test():
    start = time.time()
    column = Column("http://zhuanlan.zhihu.com/booooks")
    column.parser()
    print "Title of the column is ", column.get_title()
    print "Author of the column is ", column.get_author()
    print "Author id of the column is ", column.get_author_id()
    print "Number of follower of the column is ", column.get_follower_num()
    print "The description of the column is ", column.get_description()
    print "The number of posts of the column is ", column.get_post_count()
    column.save_all_posts()
    column.save_all_followers_profile()  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


def collection_test():
    start = time.time()
    collection = Collection("http://www.zhihu.com/collection/19559479")
    collection.parser()
    print "Title is ", collection.get_title()
    print "Description is ", collection.get_description()
    print "Number of follower is ", collection.get_follower_num()
    print "Author is ", collection.get_author()
    collection.save_questions_and_answers()  # might be time-consuming
    print "Hot collections are ", collection.get_hot_collections()
    print "Last activity time is ", collection.get_last_activity_time()
    collection.save_all_followers_profile()  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


def topic_test():
    start = time.time()
    topic = Topic("http://www.zhihu.com/topic/19550429")
    topic.parser()
    print "Title of the topic is ", topic.get_title()
    print "Introduction of the topic is ", topic.get_introduction()
    print "Number of follower of the topic is ", topic.get_follower_num()
    print "Parent topics are ", topic.get_parent_topic()
    print "Sample child topics are ", topic.get_sample_child_topic()
    print "Top answerers of this topic are ", topic.get_top_answerer()
    topic.save_latest_feed()
    topic.save_top_answers()  # might be time-consuming
    end = time.time()
    print "Time used is", end - start


user_test()
answer_test()
question_test()
column_test()
collection_test()
topic_test()

