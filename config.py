# url_base = "https://inviteme.ovh"
import json

with open('config.json', "r", encoding="utf8") as json_file:
    conf = json.load(json_file)


conf["url_login"] = f"{conf.get('url_base')}/auth/login"
conf["url_att_in"] = f"{conf.get('url_base')}/attendance/inside"
conf["url_att_out"] = f"{conf.get('url_base')}/attendance/outside"


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

conf = Struct(**conf)


