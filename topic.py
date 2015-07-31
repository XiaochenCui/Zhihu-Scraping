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

from bs4 import BeautifulSoup
import login
import os
import answer

Zhihu = "http://www.zhihu.com"


class Topic:

    def __init__(self, url):
        # initiate a Topic class object
        if url[0:27] != "http://www.zhihu.com/topic/":
            raise ValueError("\"" + url + "\"" + " : it isn't a collection url.")
        self.url = url
        self.soup = None
        return

    def parser(self):
        # parse the information for other functions to use
        user_session = login.log_in()
        r = user_session.get(self.url)
        if r.status_code != 200:
            raise ValueError("\"" + self.url + "\"" + " : it isn't a collection url.")
        self.soup = BeautifulSoup(r.content, "lxml")
        return

    def get_title(self):
        # get the title of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            title = str(self.soup.find("h1", class_="zm-editable-content").text)
            return title

    def get_introduction(self):
        # get the introduction of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            introduction = self.soup.find("div", attrs={"data-action": "/topic-introduction"}).div.text
            return introduction

    def get_follower_num(self):
        # get the number of follower of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            follower_num = int(self.soup.find("div", class_="zm-topic-side-followers-info").a.strong.text)
            return follower_num

    def get_parent_topic(self):
        # get the urls of the parent topics of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            temp = self.soup.find("div", class_="zm-side-section-inner parent-topic")
            parent_topics_list_raw = temp.find_all("a", class_="zm-item-tag")
            parent_topics_list = []
            for raw in parent_topics_list_raw:
                parent_topics_list.append(Zhihu + raw["href"])
            return parent_topics_list

    def get_sample_child_topic(self):
        # get the urls of the sample child topics of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            child_topic_raw = self.soup.find("div", class_="zm-side-section-inner child-topic")
            child_topics_raw = child_topic_raw.find_all("a", class_="zm-item-tag")
            child_topics = []
            for child_topic in child_topics_raw:
                child_topic = Zhihu + child_topic["href"]
                child_topics.append(child_topic)
            return child_topics

    def get_top_answerer(self):
        # get the urls of the top answerers of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            top_answerer_raw = self.soup.find_all("div", class_="zm-topic-side-person-item")
            top_answerers = []
            for top_answerer in top_answerer_raw:
                top_answerer = Zhihu + top_answerer.a["href"]
                top_answerers.append(top_answerer)
            return top_answerers

    def save_latest_feed(self):
        # save the latest feed of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            if self.soup is None:
                self.parser()
            title = self.get_title()
            try:
                os.mkdir(title.replace("/", "") + " latest feed(topic)")
                os.chdir(title.replace("/", "") + " latest feed(topic)")
            except OSError:
                os.chdir(title.replace("/", "") + " latest feed(topic)")
            feed_raw = self.soup.find("div", class_="zu-top-feed-list")
            question_links = []
            question_links_raw = feed_raw.find_all("a", class_="question_link")
            for question_link_raw in question_links_raw:
                question_link_raw = Zhihu + question_link_raw["href"]
                question_links.append(question_link_raw)
            answer_links = []
            answer_links_raw = feed_raw.find_all("span", class_="answer-date-link-wrap")
            for answer_link_raw in answer_links_raw:
                answer_link = Zhihu + answer_link_raw.a["href"]
                answer.Answer(answer_link).save_answer_to_file()
                answer_links.append(answer_link)
            os.chdir("..")
            return

    def save_top_answers(self):
        # save the top answers of the topic
        if self.url is None:
            raise ValueError("Did not found url for the topic")
        else:
            new_session = login.log_in()
            title = self.get_title()
            try:
                os.mkdir(title.replace("/", "") + " top answers(topic)")
                os.chdir(title.replace("/", "") + " top answers(topic)")
            except OSError:
                os.chdir(title.replace("/", "") + " top answers(topic)")
            for i in xrange(50):
                top_answer_url = self.url + "/top-answers?page={0}".format(i + 1)
                r = new_session.get(top_answer_url)
                if r.status_code != 200:
                    break
                soup = BeautifulSoup(r.content, "lxml")
                answer_links_raw = soup.find_all("span", class_="answer-date-link-wrap")
                for answer_link_raw in answer_links_raw:
                    answer_link_raw = Zhihu + answer_link_raw.a["href"]
                    answer.Answer(answer_link_raw).save_answer_to_file()
            os.chdir("..")
            return
