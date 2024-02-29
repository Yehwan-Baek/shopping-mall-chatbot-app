# run_shopping_mall.py
import sys
sys.path.append('/home/yehwan/Development/code/shopping-mall-chatbot-app/backend/')
from routes.user import user_blueprint
from config import create_app

app = create_app()

# Initialize MongoDB

app.register_blueprint(user_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
