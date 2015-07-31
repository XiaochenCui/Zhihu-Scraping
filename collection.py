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
import login
import answer
import user
import os
Zhihu = "http://www.zhihu.com"


class Collection:

    def __init__(self, url):
        # initiate a Collection class object
        if url[0:32] != "http://www.zhihu.com/collection/":
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
        # get the title of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            title = self.soup.head.title.text.split(" ")[0]
            return title

    def get_description(self):
        # get the description of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            description = str(self.soup.find("div", attrs={"id": "zh-fav-head-description"}).text)
            return description

    def get_follower_num(self):
        # get the number of follower of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            follower_url = self.url[20:] + "/followers"
            follower_num = int(self.soup.find("a", attrs={"href": follower_url}).text)
            return follower_num

    def get_author(self):
        # get the url of the author of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            author = Zhihu + self.soup.find("h2", class_="zm-list-content-title").a["href"]
            return author

    def save_questions_and_answers(self):
        # save all the answers of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            new_session = login.log_in()
            for i in xrange(100):
                collection_url = self.url + "?page={0}".format(i+1)
                r = new_session.get(collection_url)
                soup = BeautifulSoup(r.content, "lxml")
                items = soup.find_all("div", class_="zm-item")
                author = self.get_author()
                if items is None:
                    break
                title = self.get_title()
                try:
                    os.mkdir(user.User(author).get_id().replace("/", "") + "-" + title + "(collection)")
                    os.chdir(user.User(author).get_id().replace("/", "") + "-" + title + "(collection)")
                except OSError:
                    os.chdir(user.User(author).get_id().replace("/", "") + "-" + title + "(collection)")
                for item in items:
                    try:
                        answer_url = Zhihu + item.find("a", class_="answer-date-link last_updated meta-item")["href"]
                    except TypeError:
                        answer_url = Zhihu + item.find("a", class_="answer-date-link meta-item")["href"]
                    answer.Answer(answer_url).save_answer_to_file()
                os.chdir("..")
            return

    def get_hot_collections(self):
        # get the related hot collections
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            soup = self.soup.find("ul", class_="list hot-favlists")
            collection_url_list_raw = soup.find_all("div", class_="content")
            collection_url_list = []
            for collection_url in collection_url_list_raw:
                collection_url = Zhihu + collection_url.a["href"]
                collection_url_list.append(collection_url)
            return collection_url_list

    def get_last_activity_time(self):
        # get the last activity time of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            if self.soup is None:
                self.parser()
            time = self.soup.find("span", class_="time").text
            return time

    def save_all_followers_profile(self):
        # save the profile of all the followers of the collection
        if self.url is None:
            raise ValueError("Did not found url for the collection")
        else:
            self.parser()
            new_session = login.log_in()
            cookie = login.get_cookie()
            xsrf = cookie["_xsrf"]
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Origin': "http://www.zhihu.com",
                'Referer': self.url + "/followers",
            }
            title = self.get_title()
            text_file = open(title.replace("/", "") + " followers.txt(collection)", "w")
            follower_num = self.get_follower_num()
            for i in xrange((follower_num-1)/10):
                data = {'offset': 10*i,
                        '_xsrf': xsrf
                        }
                r = new_session.post(self.url + "/followers", headers=header, data=data, cookies=cookie)
                if r.status_code != 200:
                    raise ValueError("Error in retrieving collection's follower")
                soup = BeautifulSoup(r.text.decode('string_escape'), "lxml")
                soup = soup.find_all("a", class_="zg-link")
                for j in soup:
                    follower_id = j["title"].decode('unicode-escape')
                    follower_url = Zhihu + "/people/" + j["href"][32:]
                    text_file.write("Url: " + follower_url + "    ID: " + follower_id + "\n")
            text_file.close()
            return


