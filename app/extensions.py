import pyrebase, os

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

