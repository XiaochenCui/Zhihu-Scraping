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
import os
import xlwt
Zhihu = "http://www.zhihu.com"


class Question:
    def __init__(self, url):
        # initiate a Question class object
        if url[0:30] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a question url.")
        self.url = url
        self.soup = None
        self.session = None
        return

    def parser(self):
        # parse the information for other functions to use
        self.session = login.log_in()
        r = self.session.get(self.url)
        if r.status_code != 200:
            raise ValueError("\"" + self.url + "\"" + " : it isn't a question url.")
        self.soup = BeautifulSoup(r.content, "lxml")
        return

    def get_title(self):
        # get the title of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            title = self.soup.find("h2", class_="zm-item-title zm-editable-content").text
            return title

    def get_tags(self):
        # get the tags of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            tags_raw = self.soup.find_all("a", class_="zm-item-tag")
            tags = []
            for tag_raw in tags_raw:
                tags.append(str(tag_raw.text).decode("utf-8"))
            return tags

    def get_details(self):
        # get the details of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            h = html2text.HTML2Text()
            if self.soup is None:
                self.parser()
            details = h.handle(self.soup.find("div", attrs={"id": "zh-question-detail"}).text)
            return details

    def get_answer_num(self):
        # get the number of answers of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            answer_num = self.soup.find("h3", attrs={"id": "zh-question-answer-num"})["data-num"]
            return answer_num

    def get_collapsed_answer_num(self):
        # get the number of collapsed answer of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            collapsed_answer_num = int(self.soup.find("span", attrs={"id": "zh-question-collapsed-num"}).text)
            return collapsed_answer_num

    def get_follower_num(self):
        # get the number of follower of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            follower_num = int(self.soup.find("div", class_="zh-question-followers-sidebar").div.a.strong.text)
            return follower_num

    def get_view_num(self):
        # get the number of view of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            view_num_raw = self.soup.find_all("div", class_="zm-side-section-inner")
            view_num = int(view_num_raw[-1].find_all("div", class_="zg-gray-normal")[-1].strong.text)
            return view_num

    def get_comment_num(self):
        # get the number of comment of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            try:
                comment_num = int(self.soup.find("a", class_="toggle-comment meta-item").text.split()[0])
            except UnicodeEncodeError:
                comment_num = 0
            return comment_num

    def get_last_activity_time(self):
        # get the last activity time of a question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            time = self.soup.find("span", class_="time").text
            return time

    def get_related_tags_follower_num(self):
        # get the number of followers of the related tags of the question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            num_raw = self.soup.find_all("div", class_="zm-side-section-inner")
            num = int(num_raw[-1].find_all("div", class_="zg-gray-normal")[-1].strong.text)
            return num

    def get_first_known_follower(self):
        # get the first un-anonymous follower of the question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            first_follower_raw = self.soup.find("div", class_="list zu-small-avatar-list zg-clear")
            first_follower = Zhihu + first_follower_raw.a["href"]
            return first_follower

    def get_related_questions(self):
        # get the related question urls of the question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            related_questions_raw = self.soup.find("div", class_="zh-question-related-questions clearfix")
            related_questions_raw = related_questions_raw.find_all("a", class_="question_link")
            related_questions = []
            for i in related_questions_raw:
                related_questions.append(Zhihu + i["href"])
            return related_questions

    def save_top_answers(self, num):
        # save the top i answers of the question
        #  if i is greater than the total number of answers, will save all answers
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            top_answers_url_raw = self.soup.find_all("span", class_="answer-date-link-wrap")
            title = self.get_title()[:-1]
            try:
                os.mkdir(title.replace("/", "") + "top {0} answers(question)".format(num))
                os.chdir(title.replace("/", "") + "top {0} answers(question)".format(num))
            except OSError:
                os.chdir(title.replace("/", "") + "top {0} answers(question)".format(num))
            if len(top_answers_url_raw) <= num:
                for answer_url in top_answers_url_raw:
                    answer.Answer(Zhihu + answer_url.a["href"]).save_answer_to_file()
            else:
                for j in xrange(num):
                    answer.Answer(Zhihu + top_answers_url_raw[j].a["href"]).save_answer_to_file()
            os.chdir("..")
            return

    def save_all_answers(self):
        # save all answers of the question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.soup is None:
                self.parser()
            top_answers_url_raw = self.soup.find_all("span", class_="answer-date-link-wrap")
            title = self.get_title()[:-1]
            try:
                os.mkdir(title.replace("/", "") + "all answers(question)")
                os.chdir(title.replace("/", "") + "all answers(question)")
            except OSError:
                os.chdir(title.replace("/", "") + "all answers(question)")
            for answer_url in top_answers_url_raw:
                answer.Answer(Zhihu + answer_url.a["href"]).save_answer_to_file()
            os.chdir("..")
            return

    def save_all_followers_profile(self):
        # save the profile of all followers of the question
        if self.url is None:
            raise ValueError("Did not found url for the question")
        else:
            if self.session is None:
                self.session = login.log_in()
            url = self.url + "/followers"
            follower_num = self.get_follower_num()
            r = self.session.get(url)
            soup = BeautifulSoup(r.content, "lxml")
            _xsrf = soup.find("input", attrs={'name': '_xsrf'})["value"]
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': url
            }
            book = xlwt.Workbook(encoding="utf-8")
            new_sheet = book.add_sheet("Follower_profile")
            new_sheet.write(0, 0, "url")
            new_sheet.write(0, 1, "id")
            new_sheet.write(0, 2, "follower_num")
            new_sheet.write(0, 3, "ask_num")
            new_sheet.write(0, 4, "answer_num")
            new_sheet.write(0, 5, "agree_num")
            new_sheet.write(0, 6, "is_robot")
            cookie = login.get_cookie()
            row = 1
            for i in xrange((follower_num-1)/20 + 1):
                data = {"offset": 20*i, "start": 0, "_xsrf": _xsrf}
                r1 = self.session.post(url, headers=header, data=data, cookies=cookie)
                temp_soup = BeautifulSoup(r1.json()["msg"][1], "lxml")
                user_list_raw = temp_soup.find_all("div", class_="zm-profile-card zm-profile-section-item zg-clear no-hovercard")
                for j in user_list_raw:
                    try:
                        user_url = j.h2.a["href"]
                        new_sheet.write(row, 0, user_url)
                        user_id = j.find("a", class_="zm-item-link-avatar")["title"]
                        new_sheet.write(row, 1, user_id)
                        sub_soup = j.find_all("a", class_="zg-link-gray-normal")
                        try:
                            user_follower = int(sub_soup[0].text.split()[0])
                        except:
                            user_follower = sub_soup[0].text.split()[0]
                        new_sheet.write(row, 2, user_follower)
                        user_asks = int(sub_soup[1].text.split()[0])
                        new_sheet.write(row, 3, user_asks)
                        try:
                            user_answers = int(sub_soup[2].text.split()[0])
                        except:
                            user_answers = sub_soup[2].text.split()[0]
                        new_sheet.write(row, 4, user_answers)
                        try:
                            user_agrees = int(sub_soup[3].text.split()[0])
                        except:
                            user_agrees = sub_soup[3].text.split()[0]
                        new_sheet.write(row, 5, user_agrees)
                        if user_follower < 2 and user_asks < 1 and user_answers < 2 and user_agrees < 3:
                            is_robot = 1
                        else:
                            is_robot = 0
                        new_sheet.write(row, 6, is_robot)
                    except:
                        user_url = "Anonymous user"
                        new_sheet.write(row, 0, user_url)
                    row += 1
            book.save(self.get_title().replace("/", "") + " followers profile(question).xls")
            return
