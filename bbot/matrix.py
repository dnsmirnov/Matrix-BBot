#!/usr/bin/env python
import json
class MatrixConfig(object):
    URL = "homeserver"
    USR = "username"
    TOK = "password"
    ADM = "admins"

    def __init__(self, homeserver, username, password, admins):
        self.username = username
        self.password = password
        self.homeserver = homeserver
        self.admins = admins

    @classmethod
    def from_file(cls, f):
        j = json.load(f)
        return MatrixConfig(
            homeserver=j[MatrixConfig.URL],
            username=j[MatrixConfig.USR],
            password=j[MatrixConfig.TOK],
            admins=j[MatrixConfig.ADM]
        )
