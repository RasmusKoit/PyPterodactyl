import hmac
from base64 import b64encode
from hashlib import sha256
import config
import requests
from pprint import pprint
import json

public = config.publicKey

private = config.privateKey.encode('utf8')

url = 'https://panel.ialbhost.eu/api/admin/users'
# When you are sending data (i.e. POST), create a dict and pass it to `body`
# using json.dumps({"key": "value"})
values = {
    "email": "arti.zirk@gmail.com",
    "username": "arti",
    "name_first": "Arti",
    "name_last": "Zirk",
    "root_admin": False
}
body = json.dumps(values)

message = (url + body).encode('utf8')

hash = hmac.new(private, message, sha256)
hash_b64 = b64encode(hash.digest())

# 'Decoding' is simply bytes -> string in this case. The data
# is still in base64 format.
token = public + '.' + hash_b64.decode('utf8')
r = requests.post(url, json=values, headers={'Authorization': 'Bearer ' + token})
pprint(r.json())
