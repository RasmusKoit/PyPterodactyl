import hmac
from base64 import b64encode
from hashlib import sha256
import requests
import json
from pprint import pprint

class Base():

    def __init__(self, hostname, public_key, private_key):

        self.hostname = hostname
        self.public_key = public_key
        self.private_key = private_key.encode('utf8')

    def auth(self, url, body=''):
        """
        :param url: Full API path
        :param body: Json dump message
        :return: Auth bearer
        """

        message = (url + body).encode('utf8')
        hash = hmac.new(self.private_key, message, sha256)
        hash_b64 = b64encode(hash.digest())

        return self.public_key + '.' + hash_b64.decode('utf8')

    def list_users(self, id=None):

        url = self.hostname + "/admin/users"
        if id:
            url += "/" + str(id)
        r = requests.get(url, headers={'Authorization': 'Bearer ' + self.auth(url)})
        json_raw = r.json()

        if id:
            return User.from_json(json_raw['data'])

        users = []
        for user_raw in json_raw['data']:
            users.append(User.from_json(user_raw))  # User klassi instance on täidetud andmetega
        return users

    def create_user(self, user):

        url = self.hostname + "/admin/users"
        values = {
            "email": user.email,
            "username": user.username,
            "name_first": user.name_first,
            "name_last": user.name_last,
            "root_admin": user.root_admin
        }
        if user.password:
            values["password"] = user.password
        #  wut ?
        if user.id:
            values["custom_id"] = user.id
        body = json.dumps(values)
        r = requests.post(url, json=values, headers={'Authorization': 'Bearer ' + self.auth(url, body)})

        return r.json()


class User():

    def __init__(self, email=None, username=None, name_first=None,
                 name_last=None, password=None, root_admin=None, id=None, uuid=None):

        self.email = email
        self.username = username
        self.name_first = name_first
        self.name_last = name_last
        self.password = password
        self.root_admin = root_admin
        self.uuid = uuid
        self.id = id

    @classmethod
    def from_json(cls, data):
        user = cls()  # tühi User klassi instance mis ei tea veel sittagi
        user.email = data['attributes']['email']
        user.username = data['attributes']['username']
        user.name_first = data['attributes']['name_first']
        user.name_last = data['attributes']['name_last']
        user.root_admin = data['attributes']['root_admin']
        user.uuid = data['attributes']['uuid']
        # user.password = user_raw['attributes']['password']
        user.id = data['id']
        return user

    def __str__(self):
        return "<pterodactyl.User id={} username={} email={}>".format(self.id, self.username, self.email)

    def __repr__(self):
        return self.__str__()


class Server():

    def __init__(self, name=None, user_id=None, location_id=None, node_id=None, allocation_id=None,
                 allocation_additional=None, memory=None, swap=None, disk=None, cpu=None, io=None,
                 service_id=None, option_id=None, startup=None, auto_deply=None, pack_id=None,
                 custom_id=None, custom_container=None):

        self.name = name
        self.user_id = user_id
        self.location_id = location_id
        self.node_id = node_id
        self.allocation_id = allocation_id
        self.allocation_additional = allocation_additional
        self.memory = memory
        self.swap = swap
        self.disk = disk
        self.cpu = cpumc
        self.io = io
        self.service_id = service_id
        self.option_id = option_id
        self.startup = startup
        self.auto_deply = auto_deply
        self.pack_id = pack_id
        self.custom_id = custom_id
        self.custom_container = custom_container
