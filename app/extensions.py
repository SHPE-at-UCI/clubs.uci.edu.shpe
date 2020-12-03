import pyrebase
import os
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
        self.is_admin = user_info['is_admin']
        self._raw_dict = user_info.copy()
        self._raw_dict['uid'] = uid

    def get_dict(self) -> dict:
        return self._raw_dict

    def print(self):
        print(' - email: {}'.format(self.email))
        print(' - firstname: {}'.format(self.firstname))
        print(' - lastname: {}'.format(self.lastname))
        print(' - major: {}'.format(self.major))
        print(' - year: {}\n'.format(self.year))

def promote_user(email:str, user) -> int:
    #print(email)
    #print(user.is_admin)
    try:
        if user.is_admin == 'False':
            #print("CANNOT PROMOTE USER, CURR USER IS NOT ADMIN")
            return 400

        users_dict = db.child('users').get().val()
        user_id = ''

        for id in users_dict:
            #print(id, users_dict[id]['email'])
            if users_dict[id]['email'] == email:
                #print("FOUND USER")
                user_id = id
        
        if user_id == '':
            return 400

        # gets the whole user on found id key
        user = db.child('users').child(user_id).get().val()

        # change is_admin value to True
        user['is_admin'] = 'True'

        # update values of user with new dictionary with 'is_admin' attribute set to 'True'
        db.child('users').child(user_id).set(user)


        return 200
    except: 
        return 400
    
    

    


class FBQuestion:
    def __init__(self, qid: str, question_info: dict):
        self.qid = qid
#        self.title = question_info['title']
