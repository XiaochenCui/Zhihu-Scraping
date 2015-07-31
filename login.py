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

import ConfigParser
import requests
Zhihu = 'http://www.zhihu.com'
NON_LOGIN = False
email = None
password = None
cookie = None


def log_in():
    global cookie
    global email
    global password
    # print "Cookie is ",cookie
    # print "Email is ",email
    # print "Password is ",password
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    if email is None:
        email = cf.get('info', 'email')
    if password is None:
        password = cf.get('info', 'password')
    login_data = {'email': email, 'password': password}
    header = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
        'Host': "www.zhihu.com",
        'Referer': Zhihu,
        'X-Requested-With': "XMLHttpRequest",
        'Origin': Zhihu
    }
    final_session = requests.session()
    if cookie is None:
        cookie_stored = cf._sections['cookies']
        cookie_stored = dict(cookie_stored)
        cookie = cookie_stored
        response = final_session.post(Zhihu + '/login/email', data=login_data, headers=header, cookies=cookie)
    else:
        response = final_session.post(Zhihu + '/login/email', data=login_data, headers=header, cookies=cookie)
    if response.json()["r"] == 1:
        print "Login Failed, reason is:"
        print response.json()['msg']
        print "Use cookies"
        has_cookies = False
        for key in cookie:
            if key != '__name__' and cookie[key] != '':
                has_cookies = True
                break
        if has_cookies is False:
            raise ValueError("Please fill in config.ini.")
        else:
            raise ValueError("Automatic retrieve cookie failed, please fill in config.ini.")
    return final_session


def get_cookie():
    return cookie

