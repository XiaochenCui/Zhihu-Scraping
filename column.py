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
import requests
import html2text
import os
import login

Zhihu = "http://www.zhihu.com"


class Column:
    def __init__(self, url):
        # initiate a Column class object
        if url[0:26] != "http://zhuanlan.zhihu.com/":
            raise ValueError("\"" + url + "\"" + " : it isn't a column url.")
        self.url = "http://zhuanlan.zhihu.com/api/columns/" + url[26:]
        self.soup = None
        return

    def parser(self):
        # parse the information for other functions to use
        user_session = login.log_in()
        r = user_session.get(self.url)
        if r.status_code != 200:
            raise ValueError("\"" + self.url + "\"" + " : it isn't a column url.")
        self.soup = r.json()
        return

    def get_title(self):
        # get the title of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            title = str(self.soup["name"])
            return title

    def get_author(self):
        # get the url of the author of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            author_url = self.soup["creator"]["profileUrl"]
            return author_url

    def get_author_id(self):
        # get the id of the author of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            author_id = self.soup["creator"]["name"]
            return author_id

    def get_follower_num(self):
        # get the number of followers of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            follower_num = self.soup["followersCount"]
            return follower_num

    def get_description(self):
        # get the description of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            description = self.soup["description"]
            return description

    def get_post_count(self):
        # get the number of posts of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            if self.soup is None:
                self.parser()
            post_count = int(self.soup["postsCount"])
            return post_count

    def save_all_posts(self):
        # save all the posts of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            h = html2text.HTML2Text()
            post_num = self.get_post_count()
            user_session = login.log_in()
            for i in xrange((post_num - 1) / 100 + 1):
                url = self.url + "/posts" + "/?limit={0}&offset={1}".format(100, 100 * i)
                r = user_session.get(url)
                title = self.get_title()
                author_id = self.get_author_id()
                try:
                    os.mkdir(author_id.replace("/", "") + "-" + title + "(column)")
                    os.chdir(author_id.replace("/", "") + "-" + title + "(column)")
                except OSError:
                    os.chdir(author_id.replace("/", "") + "-" + title + "(column)")
                for j in r.json():
                    text_file = open(j["title"].replace("/", "") + ".txt", "w")
                    text_file.write(j["title"] + "\n\n")
                    text_file.write("Author: " + author_id + "    Number of Like: " + str(j["likesCount"]) + "\n\n")
                    text_file.write(h.handle(j["content"]))
                    text_file.write("Published time: " + j["publishedTime"] + "\n\n")
                    text_file.write("url is " + Zhihu + j["url"])
                    text_file.close()
                os.chdir("..")
            return

    def save_all_followers_profile(self):
        # save the profile of all followers of the column
        if self.url is None:
            raise ValueError("Did not found url for the column")
        else:
            user_session = login.log_in()
            follower_num = self.get_follower_num()
            title = self.get_title()
            text_file = open(title.replace("/", "") + " followers.txt(column)", "w")
            for i in xrange((follower_num - 1) / 100):
                post_url = self.url + "/followers?limit={0}&offset={1}".format(100, i * 100)
                r = user_session.get(post_url)
                for j in xrange(len(r.json())):
                    text_file.write("Url: " + r.json()[j]["profileUrl"] + "    ID: " + r.json()[j]["name"] + "\n")
            text_file.close()
            return
