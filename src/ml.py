# coding: utf-8

import sys
import requests
from workflow import Workflow, ICON_WARNING, PasswordNotFound
from workflow.notify import notify

USERNAME_KEY = 'alfred_mianliao_login_username'
PASSWORD_KEY = 'alfred_mianliao_login_password'

ML_URL = "https://wifi.52mianliao.com"
USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
ML_HEADERS = {
    'Connection': 'keep-alive',
    'Content-Length': 53,
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Origin': 'https://wifi.52mianliao.com',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': USERAGENT,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://wifi.52mianliao.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}


def login(wf, args):
    try:
        username = wf.get_password(USERNAME_KEY)
        password = wf.get_password(PASSWORD_KEY)
    except PasswordNotFound:
        notify(
            "Can't login",
            "You need to set your username and password before login",
        )
        return 1

    # Login code copied from
    # https://github.com/helloqiu/mianliao-login/blob/master/mianliao.py
    session = requests.Session()
    session.headers = ML_HEADERS
    session.verify = False  # SB Mianliao

    if session.get(ML_URL).status_code != 200:
        notify(
            "Can't login",
            "Can not connect to the Mianliao Auth Server!",
        )
        return 1

    session.post(
        ML_URL,
        data='username=%s&password=%s&action=login' % (username, password),
    )
    r = session.post(ML_URL, data={
        'ua': USERAGENT,
        'sw': 1280,
        'sh': 720,
        'ww': 1280,
        'wh': 720
    })
    wf.logger.debug(r.text)
    if u"登陆服务器响应异常" in r.text:
        notify(
            "Can't login",
            "Mianliao Auth Server is down."
        )
        return 1
    if u"登陆用户" in r.text:
        notify(
            "Login Success!",
        )
        return 0
    notify(
        "Can't login",
        "Maybe wrong username or password?"
    )


def config(wf, args):
    if len(args) != 2:
        notify(
            "Can't config",
            "type: ml config <username> <password>"
        )
        return 1
    wf.logger.debug(args)
    username = args.pop(0)
    password = args.pop(0)
    wf.save_password(USERNAME_KEY, username)
    wf.save_password(PASSWORD_KEY, password)
    notify(
        "Set success",
        "Username:%s Password: %s" % (username, password)
    )
    return 0


def main(wf):
    args = wf.args
    if not len(wf.args):
        wf.add_item('Login Mianliao', arg='login', valid=True)
        wf.add_item('Set Username and Password', arg='config', valid=True)
        wf.send_feedback()
        return 0
    else:
        action = args.pop(0)
        if action == 'login':
            return login(wf, args)
        if action == 'config':
            return config(wf, args)
        wf.add_item('Error', 'Unknown command: %s' % action)
        wf.send_feedback()
        return 0


if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
