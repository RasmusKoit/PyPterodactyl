from pterodactyl import Base
import config
from pprint import pprint
if __name__ == '__main__':
    url = "https://panel.ialbhost.eu/api"
    user = Base(url, config.publicKey, config.privateKey)
    pprint(user.list_users())

    #pprint(user.create_user("arti.zirk@gmail.com", "Kalun", "Rasmus", "Zirk"))


