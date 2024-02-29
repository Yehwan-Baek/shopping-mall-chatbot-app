from flask import Flask, render_template
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/shopping_mall'
    mongo = PyMongo(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        return render_template('error.html', error=str(e)), 500

    return app, mongo

if __name__ == '__main__':
    app, mongo = create_app()

    def seed_data():
        try:
            # 시딩 전에 users 컬렉션이 비어 있는지 확인
            mongo.db.users.delete_many({})

            # 샘플 유저 데이터
            admin = {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': generate_password_hash('admin123'),
                'user_type': True
            }
            # 필요에 따라 더 많은 유저 데이터 추가

            # 데이터베이스에 유저 데이터 삽입
            mongo.db.users.insert_one(admin)
            print("데이터 씨딩 성공.")

        except Exception as e:
            print(f"에러: {e}")

    seed_data()
    app.run(debug=True)
