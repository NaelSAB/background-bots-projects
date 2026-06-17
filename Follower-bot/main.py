import os
from dotenv import load_dotenv
from instafollower import InstaFollower


load_dotenv()
USERNAME = os.getenv("user")
PASSWORD = os.getenv("password")
ACCOUNT_FOLLOWER = os.getenv("account_follower")
LOGIN_URL = os.getenv("login_URL")


insta = InstaFollower()

insta.login(LOGIN_URL, USERNAME, PASSWORD)
insta.find_followers(ACCOUNT_FOLLOWER)
insta.follow()