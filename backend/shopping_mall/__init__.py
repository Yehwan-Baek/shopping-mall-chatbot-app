# shopping_mall/__init__.py
from flask import Flask

app = Flask(__name__)

# 여기에 필요한 초기화 및 구성을 추가할 수 있습니다.
# ...

# 라우트 및 모델 등을 여기에 추가할 수도 있습니다.
# 예를 들어, 라우트를 추가하려면:
# from shopping_mall.routes import product, user, order, cart, review

# app.register_blueprint(product.bp)
# app.register_blueprint(user.bp)
# app.register_blueprint(order.bp)
# app.register_blueprint(cart.bp)
# app.register_blueprint(review.bp)
