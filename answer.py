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
import xlwt
import login
import user

Zhihu = "http://www.zhihu.com"


class Answer:
    def __init__(self, url):
        # initiate a Answer class object
        if url[0:30] != "http://www.zhihu.com/question/":
            raise ValueError("\"" + url + "\"" + " : it isn't a answer url.")
        self.url = url
        self.soup = None
        self.session = None
        return

    def parser(self):
        # parse the information for other functions to use
        self.session = login.log_in()
        r = self.session.get(self.url)
        if r.status_code != 200:
            raise ValueError("\"" + self.url + "\"" + " : it isn't a answer url.")
        self.soup = BeautifulSoup(r.content, "lxml")
        return

    def get_author(self):
        # get the url of the author of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            author_raw = self.soup.find("a", class_="zm-item-link-avatar")
            try:
                author = Zhihu + author_raw["href"]
            except TypeError:
                author = "Anonymous user"
            return author

    def get_question_url(self):
        # get the url of the question that the answer belongs to
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            return self.url[:38]

    def get_question_text(self):
        # get the text of the question that the answer belongs to
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            try:
                question_text = self.soup.find("h2", class_="zm-item-title zm-editable-content").a.text
            except:
                question_text = self.soup.find("h2", class_="zm-item-title zm-editable-content").text
            return question_text

    def get_vote_num(self):
        # get the number of vote of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            soup1 = self.soup.find("div", class_="zm-votebar")
            try:
                vote_num = int(soup1.find("span", class_="count").text)
            except:
                vote_num = str(soup1.find("span", class_="count").text)
            return vote_num

    def get_content(self):
        # get the content of the answer
        h = html2text.HTML2Text()
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            content_raw = self.soup.find("div", class_=" zm-editable-content clearfix")
            content = h.handle(str(content_raw))
            return content

    def get_comment_num(self):
        # get the number of comment of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            comment_num_raw = self.soup.find("a", class_=" meta-item toggle-comment").text
            comment_num = int(comment_num_raw.split()[0])
            return comment_num

    def get_view_num(self):
        # get the number of view of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            try:
                view_num_raw = self.soup.find("div", class_="zm-side-section zh-answer-status")
                view_num = int(view_num_raw.div.p.next_sibling.next_sibling.strong.text)
            except:
                view_num = 0
            return view_num

    def get_collected_num(self):
        # get the number of time the answer is collected
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            if self.get_author() == "Anonymous user":
                print "Anonymous user, cannot get collected num"
                return 0
            try:
                collected_num = int(self.soup.find_all("div", class_="zm-side-section-inner")[3].h3.a.text)
            except:
                collected_num = 0
            return collected_num

    def get_created_time(self):
        # get the time that the answer is created
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            created_time = self.soup.find("span", class_="time").text
            return created_time

    def get_last_modified_time(self):
        # get the time the answer is last modified
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.soup is None:
                self.parser()
            last_modified_time = self.soup.find("span", class_="time").text
            return last_modified_time

    def save_answer_to_file(self):
        # save the answer
        h = html2text.HTML2Text()
        question_text = self.get_question_text()
        answer_file = open(question_text.replace('/', '') + user.User(self.get_author()).get_id() + ".txt", "w")
        answer_file.write(self.get_question_url() + "\n\n")
        answer_file.write(question_text + "\n\n")
        answer_file.write("Author is " + user.User(self.get_author()).get_id() + "   ")
        answer_file.write("Number of vote is " + str(self.get_vote_num()) + "\n\n")
        answer_file.write(h.handle(self.get_content()))
        answer_file.write("Answer url is " + self.url)

    def save_all_comments(self):
        # save all comments of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.session is None:
                self.session = login.log_in()
            if self.soup is None:
                self.parser()
            answer_id = self.soup.find("div", class_="zm-item-answer ")["data-aid"]
            comment_url_1 = "http://www.zhihu.com/node/AnswerCommentBoxV2?params=%7B%22answer_id%22%3A%22"
            comment_url_2 = "%22%2C%22load_all%22%3Atrue%7D"
            comment_url = comment_url_1 + answer_id + comment_url_2
            r = self.session.get(comment_url)
            soup = BeautifulSoup(r.content, "lxml")
            text_file = open(self.url[20:].replace("/", " ") + " comments.txt", "w")
            comment_list_raw = soup.find_all("div", class_="zm-item-comment")
            for comment_raw in comment_list_raw:
                like_num = int(comment_raw.find("span", class_="like-num").em.text)
                try:
                    author = Zhihu + comment_raw.find("a", class_="zm-item-link-avatar")["href"]
                    author_id = comment_raw.find("a", class_="zm-item-link-avatar")["title"]
                except TypeError:
                    author = "Anonymous user"
                    author_id = "Anonymous user"
                content = comment_raw.find("div", class_="zm-comment-content").text
                text_file.write(author_id + "    " + author)
                text_file.write(content)
                text_file.write("Number of vote: " + str(like_num) + "\n\n")
            text_file.close()
            return

    def save_all_voters_profile(self):
        # save the profile of all voters of the answer
        if self.url is None:
            raise ValueError("Did not found url for the answer")
        else:
            if self.session is None:
                self.session = login.log_in()
            if self.soup is None:
                self.parser()
            answer_id = self.soup.find("div", class_="zm-item-answer ")["data-aid"]
            voters_profile_url = Zhihu + "/answer/" + answer_id + "/voters_profile"
            cookie = login.get_cookie()
            header = {
                'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
                'Host': "www.zhihu.com",
                'Referer': self.url
            }
            book = xlwt.Workbook(encoding="utf-8")
            new_sheet = book.add_sheet("Voter_profile")
            new_sheet.write(0, 0, "url")
            new_sheet.write(0, 1, "id")
            new_sheet.write(0, 2, "agree_num")
            new_sheet.write(0, 3, "thanks_num")
            new_sheet.write(0, 4, "ask_num")
            new_sheet.write(0, 5, "answer_num")
            new_sheet.write(0, 6, "is_robot")
            total_vote = self.get_vote_num()
            row = 1
            robot_vote = 0
            for i in xrange((total_vote - 1) / 10 + 1):
                data = {"total": total_vote, "offset": 10 * i}
                r = self.session.get(voters_profile_url, headers=header, data=data, cookies=cookie)
                for j in r.json()["payload"]:
                    if row % 100 == 0 and row != 0:
                        print "Have saved {0} voter profiles".format(row)
                    soup = BeautifulSoup(j, "lxml")
                    try:
                        voter_url = soup.find("div", class_="author ellipsis").a["href"]
                    except:
                        voter_url = "Anonymous user"
                    new_sheet.write(row, 0, voter_url)
                    if voter_url != "Anonymous user":
                        voter_id = soup.find("div", class_="author ellipsis").a["title"]
                        new_sheet.write(row, 1, voter_id)
                        try:
                            voter_agree_num = int(soup.find("ul", class_="status").li.span.text.split()[0])
                        except ValueError:
                            voter_agree_num = soup.find("ul", class_="status").li.span.text.split()[0]
                        new_sheet.write(row, 2, voter_agree_num)
                        try:
                            voter_thanks_num = int(
                                soup.find("ul", class_="status").li.next_sibling.next_sibling.span.text.split()[0])
                        except ValueError:
                            voter_thanks_num = soup.find("ul", class_="status").li.next_sibling.next_sibling.span.text.split()[0]
                        new_sheet.write(row, 3, voter_thanks_num)
                        voter_ask_num = int(soup.find_all("li", class_="hidden-phone")[0].a.text.split()[0])
                        new_sheet.write(row, 4, voter_ask_num)
                        voter_answer_num = int(soup.find_all("li", class_="hidden-phone")[1].a.text.split()[0])
                        new_sheet.write(row, 5, voter_answer_num)
                        if voter_agree_num < 1 and voter_thanks_num < 1 and voter_ask_num < 1 and voter_answer_num < 2:
                            voter_is_robot = 1
                            robot_vote += 1
                        else:
                            voter_is_robot = 0
                        new_sheet.write(row, 6, voter_is_robot)
                    row += 1
            book.save(self.url[20:].replace("/", " ") + " voter profile(answer).xls")
            return robot_vote / (total_vote * 1.0)
