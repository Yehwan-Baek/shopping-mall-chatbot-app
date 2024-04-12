from flask import current_app
from datetime import datetime

class Review:
    def __init__(self, user_id, star, comment):
        self.user_id = user_id
        self.star = star
        self.comment = comment
        self.creation_date = datetime.now(pytz.timezone("Australia/Sydney"))

