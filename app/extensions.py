import pyrebase, os
from urllib.parse import quote

config = {
  "apiKey": os.getenv("API_KEY"),
  "authDomain": "shpe-uci-tech.firebaseapp.com",
  "databaseURL": "https://shpe-uci-tech.firebaseio.com",
  "projectId": "shpe-uci-tech",
  "storageBucket": "shpe-uci-tech.appspot.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()


class FBUser:
    def __init__(self, uid: str, user_info: dict):
        self.uid = uid
        self.email = user_info['email']
        self.firstname = user_info['first_name']
        self.lastname = user_info['last_name']
        self.major = user_info['major']
        self.year = user_info['year']
        self._raw_dict = user_info.copy()
        self._raw_dict['uid'] = uid

    def get_dict(self) -> dict:
        return self._raw_dict

    def print(self):
        print(self.uid)
        print(' - email: {}'.format(self.email))
        print(' - firstname: {}'.format(self.firstname))
        print(' - lastname: {}'.format(self.lastname))
        print(' - major: {}'.format(self.major))
        print(' - year: {}\n'.format(self.year))
