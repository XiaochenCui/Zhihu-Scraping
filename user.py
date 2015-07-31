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

import requests
from bs4 import BeautifulSoup
import json
from ast import literal_eval
import html2text
import os
import login
import xlwt
import column
import collection

Zhihu = "http://www.zhihu.com"


class User:
    def __init__(self, user_url):
        # initiate a User class object
        if user_url is None or user_url == "Anonymous user":
            self.url = None
            return
        elif user_url[0:28] != "http://www.zhihu.com/people/":
            raise ValueError("\"" + user_url + "\"" + " : it isn't a user url.")
        else:
            self.url = user_url
            self.user_session = None
            self.soup = None
            return

    def parser(self):
        # parse the information for other functions to use
        if self.url is None:
            print "Anonymous user, parser failed"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            r = self.user_session.get(self.url)
            if r.status_code != 200:
                raise ValueError("\"" + self.url + "\"" + " : it isn't a user url.")
            self.soup = BeautifulSoup(r.content, "lxml")
            return

    def get_id(self):
        # get the id or name of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup = self.soup
            soup1 = soup.find("div", class_="title-section ellipsis")
            usr_id = soup1.find("span", class_="name").string
            return usr_id

    def get_sex(self):
        # get the sex of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("span", class_="item gender")
            try:
                usr_sex = soup1.i["class"][1][13:]
            except AttributeError:
                usr_sex = "unspecified"
            return usr_sex

    def get_followee_num(self):
        # get the number of followee of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="zm-profile-side-following zg-clear")
            followee_num = int(soup1.find_all("a")[0].strong.string)
            return followee_num

    def get_follower_num(self):
        # get the number of follower of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="zm-profile-side-following zg-clear")
            follower_num = int(soup1.find_all("a")[1].strong.string)
            return follower_num

    def get_agree_num(self):
        # get the number of agree of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="zm-profile-header-info-list")
            soup_agree = soup1.find("span", class_="zm-profile-header-user-agree")
            agree_num = int(soup_agree.strong.string)
            return agree_num

    def get_thanks_num(self):
        # get the number of thanks of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="zm-profile-header-info-list")
            soup_thanks = soup1.find("span", class_="zm-profile-header-user-thanks")
            thanks_num = int(soup_thanks.strong.string)
            return thanks_num

    def get_asks_num(self):
        # get the number of asks of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="profile-navbar clearfix")
            soup2 = soup1.find_all("span", class_="num")
            asks_num = int(soup2[0].string)
            return asks_num

    def get_answers_num(self):
        # get the number of answers of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="profile-navbar clearfix")
            soup2 = soup1.find_all("span", class_="num")
            answers_num = int(soup2[1].string)
            return answers_num

    def get_posts_num(self):
        # get the number of posts of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="profile-navbar clearfix")
            soup2 = soup1.find_all("span", class_="num")
            posts_num = int(soup2[2].string)
            return posts_num

    def get_collections_num(self):
        # get the number of collections of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="profile-navbar clearfix")
            soup2 = soup1.find_all("span", class_="num")
            collections_num = int(soup2[3].string)
            return collections_num

    def get_logs_num(self):
        # get the number of logs of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="profile-navbar clearfix")
            soup2 = soup1.find_all("span", class_="num")
            logs_num = int(soup2[4].string)
            return logs_num

    def get_column_followed_num(self):
        # get the number of columns that the user is following
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            column_followed_num_raw = self.soup.find("a", attrs={"href": self.url[20:] + "/columns/followed"})
            try:
                column_followed_num = int(column_followed_num_raw.strong.text.split()[0])
            except AttributeError:
                column_followed_num = 0
            return column_followed_num

    def get_topic_followed_num(self):
        # get the number of topics that the user is following
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            topic_followed_num_raw = self.soup.find("a", attrs={"href": self.url[20:] + "/topics"})
            topic_followed_num = int(topic_followed_num_raw.strong.text.split()[0])
            return topic_followed_num

    def get_view_num(self):
        # get the number of profile view of the user
        if self.url is None:
            return "Anonymous user"
        else:
            if self.soup is None:
                self.parser()
            view_num = int(self.soup.find_all("div", class_="zm-side-section-inner")[-1].span.strong.text)
            return view_num

    def get_columns_url(self):
        # get the list of urls of the user's columns
        if self.url is None:
            return "Anonymous user"
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            url = self.url + "/posts"
            r = self.user_session.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            column_url_list = []
            column_url_raw = soup.find_all("a", class_="avatar-link")
            for column_url in column_url_raw:
                column_url_list.append(column_url["href"])
            return column_url_list

    def get_collections_url(self):
        # get the list of urls of the user's collections
        if self.url is None:
            return "Anonymous user"
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            url = self.url + "/collections"
            r = self.user_session.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            collection_url_list = []
            collection_url_raw = soup.find_all("a", class_="zm-profile-fav-item-title")
            for collection_url in collection_url_raw:
                collection_url_list.append(Zhihu + collection_url["href"])
            return collection_url_list

    def save_followers_profile(self):
        # save the profile of all the user's followers
        if self.url is None:
            print "Anonymous user, cannot save followers profile"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            follower_num = self.get_follower_num()
            if follower_num == 0:
                print "No follower"
                return
            follower_url = self.url + "/followers"
            cookie = login.get_cookie()
            r = self.user_session.get(follower_url)
            soup = BeautifulSoup(r.content, "lxml")
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            soup1 = soup.find("div", class_="zh-general-list clearfix")
            string = soup1['data-init']
            params = literal_eval(string)['params']
            post_url = "http://www.zhihu.com/node/ProfileFollowersListV2"
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': follower_url,
            }
            book = xlwt.Workbook(encoding="utf-8")
            new_sheet = book.add_sheet("FollowerList")
            new_sheet.write(0, 0, "url")
            new_sheet.write(0, 1, "id")
            new_sheet.write(0, 2, "follower_num")
            new_sheet.write(0, 3, "asks_num")
            new_sheet.write(0, 4, "answers_num")
            new_sheet.write(0, 5, "agree_num")
            new_sheet.write(0, 6, "is_robot")
            row = 1
            for i in xrange((follower_num - 1) / 20 + 1):
                if i % 100 == 0 and i != 0:
                    print "Have recorded", i * 20, "followers"
                params['offset'] = i * 20
                data = {'_xsrf': _xsrf, 'method': "next", 'params': json.dumps(params)}
                response = self.user_session.post(post_url, data=data, headers=header, cookies=cookie)
                follower_list = response.json()["msg"]
                for j in follower_list:
                    main_soup = BeautifulSoup(j, "lxml")
                    followers_url = main_soup.find("h2", class_="zm-list-content-title").a["href"]
                    new_sheet.write(row, 0, followers_url)
                    followers_id = main_soup.find("h2", class_="zm-list-content-title").a["title"]
                    new_sheet.write(row, 1, followers_id)
                    info_list = main_soup.find_all("a", class_="zg-link-gray-normal")
                    follower_num = int(info_list[0].text.split()[0])
                    new_sheet.write(row, 2, follower_num)
                    asks_num = int(info_list[1].text.split()[0])
                    new_sheet.write(row, 3, asks_num)
                    answers_num = int(info_list[2].text.split()[0])
                    new_sheet.write(row, 4, answers_num)
                    agree_num = int(info_list[3].text.split()[0])
                    new_sheet.write(row, 5, agree_num)
                    if follower_num < 2 and asks_num < 1 and answers_num < 2 and agree_num < 2:
                        is_robot = 1
                    else:
                        is_robot = 0
                    new_sheet.write(row, 6, is_robot)
                    row += 1
            book.save(self.get_id() + " follower list.xls")
            return

    def save_followees_profile(self):
        # save the profile of all the user's followees
        if self.url is None:
            print "Anonymous user, cannot save followees profile"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            followee_num = self.get_followee_num()
            if followee_num == 0:
                print "No followee"
                return
            followee_url = self.url + "/followees"
            cookie = login.get_cookie()
            r = self.user_session.get(followee_url)
            soup = BeautifulSoup(r.content, "lxml")
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            soup1 = soup.find("div", class_="zh-general-list clearfix")
            string = soup1['data-init']
            params = literal_eval(string)['params']
            post_url = "http://www.zhihu.com/node/ProfileFolloweesListV2"
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': followee_url,
            }
            book = xlwt.Workbook(encoding="utf-8")
            new_sheet = book.add_sheet("FolloweeList")
            new_sheet.write(0, 0, "url")
            new_sheet.write(0, 1, "id")
            new_sheet.write(0, 2, "follower_num")
            new_sheet.write(0, 3, "asks_num")
            new_sheet.write(0, 4, "answers_num")
            new_sheet.write(0, 5, "agree_num")
            new_sheet.write(0, 6, "is_robot")
            row = 1
            for i in xrange((followee_num - 1) / 20 + 1):
                if i % 100 == 0 and i != 0:
                    print "Have recorded", i * 20, "followees"
                params['offset'] = i * 20
                data = {'_xsrf': _xsrf, 'method': "next", 'params': json.dumps(params)}
                response = self.user_session.post(post_url, data=data, headers=header, cookies=cookie)
                followee_list = response.json()["msg"]
                for j in followee_list:
                    main_soup = BeautifulSoup(j, "lxml")
                    followees_url = main_soup.find("h2", class_="zm-list-content-title").a["href"]
                    new_sheet.write(row, 0, followees_url)
                    followees_id = main_soup.find("h2", class_="zm-list-content-title").a["title"]
                    new_sheet.write(row, 1, followees_id)
                    info_list = main_soup.find_all("a", class_="zg-link-gray-normal")
                    follower_num = int(info_list[0].text.split()[0])
                    new_sheet.write(row, 2, follower_num)
                    asks_num = int(info_list[1].text.split()[0])
                    new_sheet.write(row, 3, asks_num)
                    answers_num = int(info_list[2].text.split()[0])
                    new_sheet.write(row, 4, answers_num)
                    agree_num = int(info_list[3].text.split()[0])
                    new_sheet.write(row, 5, agree_num)
                    if followee_num < 5 and asks_num < 2 and answers_num < 2 and agree_num < 2:
                        is_robot = 1
                    else:
                        is_robot = 0
                    new_sheet.write(row, 6, is_robot)
                    row += 1
            book.save(self.get_id() + " followee list.xls")
            return

    def save_asks(self):
        # save all the user's asks
        if self.url is None:
            print "Anonymous user, cannot save asks"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            asks_num = self.get_asks_num()
            if asks_num == 0:
                print "No asks"
                return
            total_page = (asks_num - 1) / 20 + 1
            text_file = open(self.get_id().replace('/', '') + " -Asks.txt", "w")
            for page in xrange(total_page):
                if page == 0:
                    asks_url = self.url + "/asks"
                else:
                    asks_url = self.url + "/asks" + "?page={0}".format(page + 1)
                r = self.user_session.get(asks_url)
                soup = BeautifulSoup(r.content, "lxml")
                ask_soup = soup.find_all("h2", class_="zm-profile-question")
                for asks in ask_soup:
                    asks_text = asks.a.text
                    asks_url = Zhihu + asks.a["href"]
                    text_file.write(asks_text)
                    text_file.write(asks_url + "\n\n")
            text_file.close()
            return

    def save_answers(self):
        # save all the user's answers
        if self.url is None:
            print "Anonymous user, cannot save answers"
            return
        else:
            h = html2text.HTML2Text()
            usr_id = self.get_id()
            answers_num = self.get_answers_num()
            if answers_num == 0:
                print "No answer"
                return
            new_session = login.log_in()
            total_page = (answers_num - 1) / 20 + 1
            try:
                os.mkdir(usr_id.replace("/", "") + "-Answers")
                os.chdir(usr_id.replace("/", "") + "-Answers")
            except OSError:
                os.chdir(usr_id.replace("/", "") + "-Answers")
            for page in xrange(total_page):
                if page == 0:
                    answers_url = self.url + "/answers"
                else:
                    answers_url = self.url + "/answers" + "?page={0}".format(page + 1)
                r = new_session.get(answers_url)
                soup = BeautifulSoup(r.content, "lxml")
                soup = soup.find("div", attrs={"id": "zh-profile-answer-list"})
                answer_text = soup.find_all("div", class_="zm-item-rich-text")
                vote_num = soup.find_all("a", class_="zm-item-vote-count")
                question_url = soup.find_all("a", class_="question_link")
                for i in xrange(len(answer_text)):
                    text_file = open(question_url[i].text.replace('/', '') + ".txt", "w")
                    text_file.write(Zhihu + question_url[i]["href"] + "\n\n")
                    text_file.write(question_url[i].text + "\n\n")
                    text_file.write("Author is : ")
                    text_file.write(usr_id + "    ")
                    text_file.write("Number of vote is:")
                    text_file.write(vote_num[i]["data-votecount"] + "\n\n")
                    text_file.write(h.handle(answer_text[i].textarea.text))
                    text_file.close()
            os.chdir("..")

        return

    def is_robot(self):
        # check if the user is likely to be robot
        if self.url is None:
            print "Anonymous user is tested for robot"
            return False
        else:
            follower_num = self.get_follower_num()
            followee_num = self.get_followee_num()
            answers_num = self.get_answers_num()
            asks_num = self.get_asks_num()
            if follower_num < 3 and followee_num < 5 and answers_num < 2 and asks_num < 2:
                return True
            else:
                return False

    def save_basic_info(self):
        # save the basic information of the user
        if self.url is None:
            print "Anonymous user, cannot get basic"
            return
        else:
            h = html2text.HTML2Text()
            if self.user_session is None:
                self.user_session = login.log_in()
            basic_info_url = self.url + "/about"
            r = self.user_session.get(basic_info_url)
            soup = BeautifulSoup(r.content, "lxml")
            usr_id = self.get_id()
            text_file = open(usr_id.replace("/", "") + " basic info.txt", "w")
            try:
                title = soup.find("span", class_="bio")["title"]
            except:
                title = "unspecified"
            try:
                location = soup.find("span", class_="location item")["title"]
            except:
                location = "unspecified"
            try:
                business = soup.find("span", class_="business item")["title"]
            except:
                business = "unspecified"
            try:
                education = soup.find("span", class_="education item")["title"]
            except:
                education = "unspecified"
            try:
                content = h.handle(soup.find("span", class_="content").text)
            except:
                content = "unspecified"
            try:
                weibo = soup.find("a", class_="zm-profile-header-user-weibo")["href"]
            except:
                weibo = "unspecified"
            text_file.write("Url: " + self.url + "\n")
            text_file.write("Id: " + usr_id + "\n")
            text_file.write("Biography title: " + title + "\n")
            text_file.write("Sina weibo: " + weibo + "\n")
            text_file.write("location: " + location + "\n")
            text_file.write("Business: " + business + "\n")
            text_file.write("Education: " + education + "\n")
            text_file.write("Content: " + content + "\n")
            text_file.close()
            return

    def get_column_followed(self):
        # get the list of urls of the columns that the user is following
        if self.url is None:
            print "Anonymous user, cannot get column followed"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            column_followed_url = self.url + "/columns/followed"
            column_followed_num = self.get_column_followed_num()
            if column_followed_num == 0:
                return []
            r = self.user_session.get(column_followed_url)
            soup = BeautifulSoup(r.content, "lxml")
            # print soup
            cookie = login.get_cookie()
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            soup1 = soup.find("div", class_="zh-general-list clearfix")
            string = soup1['data-init']
            params = literal_eval(string)['params']
            post_url = "http://www.zhihu.com/node/ProfileFollowedColumnsListV2"
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': column_followed_url
            }
            column_followed_list = []
            for i in xrange((column_followed_num - 1) / 20 + 1):
                params['offset'] = i * 20
                data = {'_xsrf': _xsrf, 'method': "next", 'params': json.dumps(params)}
                response = self.user_session.post(post_url, data=data, headers=header, cookies=cookie)
                column_followed_list_raw = response.json()["msg"]
                for column_followed_raw in column_followed_list_raw:
                    main_soup = BeautifulSoup(column_followed_raw, "lxml")
                    column_followed = main_soup.find("div", class_="zm-profile-section-main").a["href"]
                    column_followed_list.append(column_followed)
            return column_followed_list

    def get_topic_followed(self):
        # get the list of urls of the topics that the user is following
        if self.url is None:
            print "Anonymous user, cannot get topic followed"
            return
        else:
            if self.user_session is None:
                self.user_session = login.log_in()
            topics_followed_url = self.url + "/topics"
            topic_followed_num = self.get_topic_followed_num()
            if topic_followed_num == 0:
                return []
            r = self.user_session.get(topics_followed_url)
            soup = BeautifulSoup(r.content, "lxml")
            cookie = login.get_cookie()
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': topics_followed_url
            }
            topic_followed_list = []
            for i in xrange((topic_followed_num - 1) / 20 + 1):
                data = {'_xsrf': _xsrf, 'start': 0, 'offset': 20 * i}
                response = self.user_session.post(topics_followed_url, data=data, headers=header, cookies=cookie)
                topic_followed_raw = response.json()["msg"][1]
                main_soup = BeautifulSoup(topic_followed_raw, "lxml")
                topic_followed_raw = main_soup.find_all("div", class_="zm-profile-section-main")
                for topic in topic_followed_raw:
                    topic = Zhihu + topic.a.next_sibling.next_sibling["href"]
                    topic_followed_list.append(topic)
            return topic_followed_list

    def save_latest_activity(self):
        # save the latest activities of the user
        if self.url is None:
            print "Anonymous user, cannot save latest activity"
            return
        else:
            if self.soup is None:
                self.parser()
            usr_id = self.get_id()
            soup = self.soup.find("div", class_="zm-profile-section-list profile-feed-wrap")
            activities = soup.find_all("div", class_="zm-profile-section-main zm-profile-section-"
                                                     "activity-main zm-profile-activity-page-item-main")
            text_file = open(usr_id.replace("/", "") + "-latest activities.txt", "w")
            times = soup.find_all("span", class_="zm-profile-setion-time zg-gray zg-right")
            if len(times) != len(activities):
                raise ValueError("Bug in save_all_activities")
            for i in xrange(len(activities)):
                activity = activities[i]
                text_file.write(activity.text[:-1])
                text_file.write(times[i].text + "\n\n")
                try:
                    text_file.write("url is " + Zhihu + activity.a.next_sibling.next_sibling["href"] + "\n")
                except:
                    text_file.write(
                        "url is " + Zhihu + activity.a.next_sibling.next_sibling.next_sibling["href"] + "\n")

            text_file.close()
            return

    def save_all_activity(self):
        # save all activities of the user
        if self.url is None:
            print "Anonymous user, cannot save all activity"
            return
        else:
            if self.soup is None:
                self.parser()
            usr_id = self.get_id()
            text_file = open(usr_id.replace("/", "") + " all activities.txt", "w")
            temp_soup = self.soup.find("div", class_="zm-profile-section-list profile-feed-wrap")
            activities = temp_soup.find_all("div", class_="zm-profile-section-main zm-profile-section-"
                                                          "activity-main zm-profile-activity-page-item-main")
            times = temp_soup.find_all("span", class_="zm-profile-setion-time zg-gray zg-right")
            if len(times) != len(activities):
                raise ValueError("Bug in save_all_activities")
            for i in xrange(len(activities)):
                activity = activities[i]
                text_file.write(activity.text[:-1])
                text_file.write(times[i].text + "\n\n")
                try:
                    text_file.write("url is " + Zhihu + activity.a.next_sibling.next_sibling["href"] + "\n")
                except:
                    text_file.write(
                        "url is " + Zhihu + activity.a.next_sibling.next_sibling.next_sibling["href"] + "\n")
            if self.user_session is None:
                self.user_session = login.log_in()
            start_raw = self.soup.find_all("div", class_="zm-profile-section-item zm-item clearfix")
            try:
                start_raw[-1]
            except IndexError:
                print "No activity found"
                return
            start = start_raw[-1]["data-time"]
            _xsrf = self.soup.find("input", attrs={'name': '_xsrf'})["value"]
            data = {"start": start, "_xsrf": _xsrf}
            cookie = login.get_cookie()
            activities_url = self.url + "/activities"
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': self.url
            }
            info = 1
            while True:
                if info % 10 == 0 and info != 0:
                    print "Saved {0} pieces of activities".format(info * 10)
                r = self.user_session.post(activities_url, headers=header, data=data, cookies=cookie)
                if r.status_code != 200:
                    break
                new_soup = BeautifulSoup(r.json()["msg"][1], "lxml")
                activities = new_soup.find_all("div", class_="zm-profile-section-main zm-profile-section"
                                                             "-activity-main zm-profile-activity-page-item-main")
                times = new_soup.find_all("span", class_="zm-profile-setion-time zg-gray zg-right")
                if len(times) != len(activities):
                    raise ValueError("Bug in save_all_activities")
                for i in xrange(len(activities)):
                    activity = activities[i]
                    text_file.write(activity.text[:-1])
                    text_file.write(times[i].text + "\n\n")
                    try:
                        if activity.a.next_sibling.next_sibling["href"][0:3] != "http":
                            text_file.write("url is " + Zhihu + activity.a.next_sibling.next_sibling["href"] + "\n")
                        else:
                            text_file.write("url is " + activity.a.next_sibling.next_sibling["href"] + "\n")
                    except:
                        if activity.a.next_sibling.next_sibling.next_sibling["href"][0:3] != "http":
                            text_file.write(
                                "url is " + Zhihu + activity.a.next_sibling.next_sibling.next_sibling["href"] + "\n")
                        else:
                            text_file.write(
                                "url is " + activity.a.next_sibling.next_sibling.next_sibling["href"] + "\n")
                try:
                    start = new_soup.find_all("div", class_="zm-profile-section-item zm-item clearfix")[-1]["data-time"]
                except:
                    break
                data["start"] = start
                info += 1
            text_file.write("Approximately {0} pieces of activities".format(info * 10))
            text_file.close()
            return

    def save_columns(self):
        # save all the columns of the user
        if self.url is None:
            print "Anonymous user, cannot save columns"
            return
        else:
            column_url_list = self.get_columns_url()
            for column_url in column_url_list:
                column.Column(column_url).save_all_posts()
            return

    def save_collections(self):
        # save all the collections of the user
        if self.url is None:
            print "Anonymous user, cannot save collections"
            return
        else:
            collection_url_list = self.get_collections_url()
            for collection_url in collection_url_list:
                collection.Collection(collection_url).save_questions_and_answers()
            return
