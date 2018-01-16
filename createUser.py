import requests
import config
url = 'https://panel.ialbhost.eu/api/admin/users'

response = requests.request("POST", url)

print(response.text)
