from bardapi import Bard
import requests
import configparser

conf = configparser.ConfigParser()
conf.read("config.ini", encoding="UTF-8")

session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", conf["cookies"]["__Secure-1PSID"])
session.cookies.set("__Secure-1PSIDTS", conf["cookies"]["__Secure-1PSIDTS"])
# session.cookies.set("__Secure-1PSIDCC", conf["cookies"]["__Secure-1PSIDCC"])

bard = Bard(
    token=conf["cookies"]["__Secure-1PSID"],
    session=session,
    timeout=30,
    conversation_id=conf["conversation"]["id"],
    language="zh-TW"
)

while True:
    s = input()
    s = s.split("~")
    if len(s) == 1:
        o = bard.get_answer(s[0])
    else:
        o = bard.ask_about_image(s[0], open(s[1].replace("\"", ""), "rb").read())

    audio = bard.speech(o["content"])
    with open("speech.ogg", "wb") as f:
        f.write(bytes(audio["audio"]))

    print(bard.conversation_id, conf["conversation"]["id"])
    print(o["content"])

    if bard.conversation_id != conf["conversation"]["id"]:
        conf.set("conversation", "id", bard.conversation_id)
        conf.write(open("config.ini", "w"))
        bard = Bard(
            token=conf["cookies"]["__Secure-1PSID"],
            session=session,
            timeout=30,
            conversation_id=conf["conversation"]["id"],
            language="zh-TW"
        )
