from flask import current_app
from datetime import datetime
import pytz

class Review:
    def __init__(self, user_id, product_id, star, comment):
        self.user_id = user_id
        self.product_id = product_id
        self.star = star
        self.comment = comment
        self.creation_date = datetime.now(pytz.timezone("Australia/Sydney"))

    # change to dictionary
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'product_id': self.product_id,
            'star': self.star,
            'comment': self.comment,
            'creation_date': self.creation_date
        }

    # save data
    def save_to_db(self):
        current_app.mongo.db.reviews.insert_one(self.to_dict())

    # update review
    def update(self, star, comment):
        self.star = star
        self.comment = comment
        current_app.mongo.db.reviews.update_one({'user_id': self.user_id, 'product_id': self.product_id}, {'$set': self.to_dict()})


    # remove review
    def delete(self):
        current_app.mongo.db.reviews.delete_one({'user_id': self.user_id, 'product_id': self.product_id})

    # find review by user id
    @classmethod
    def get_reviews_by_user(cls, user_id):
        review_data = current_app.mongo.db.reviews.find({'user_id': user_id})
        return [cls(**review) for review in review_data]

    # find review by product id
    @classmethod
    def get_reviews_by_product(cls, product_id):
        review_data = current_app.mongo.db.reviews.find({'product_id': product_id})
        return [cls(**review) for review in review_data]