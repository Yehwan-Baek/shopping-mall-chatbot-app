from flask import current_app
from datetime import datetime

class Review:
    def __init__(self, review_id, star, comment):
        self.review_id = review_id
        self.star = star
        self.comment = comment

