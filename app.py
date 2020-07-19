from datetime import datetime
from random import choice

from flask import render_template, redirect, request, Flask

from db import db, migrate
from models import Restaurant, History


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('local.cfg')

# Setup DB Connection
db.init_app(app)

# Setup Flask-Migrate
migrate.init_app(app, db)


@app.route('/')
def start():
    now = datetime.utcnow()
    return render_template('start.html', nav='start', now=now)


@app.route('/draw/')
def draw():
    restaurant_list = Restaurant.query.all()
    if not restaurant_list:
        return redirect('/restaurant/create/')

    restaurant = choice(restaurant_list)
    restaurant.draw += 1
    db.session.add(restaurant)

    history_obj = History(restaurant_id=restaurant.id)
    db.session.add(history_obj)

    db.session.commit()

    now = datetime.utcnow()
    return render_template('draw.html', restaurant=restaurant, now=now)


@app.route('/restaurant/list/', methods=['GET'])
def restaurant_list():

    restaurant_list = Restaurant.query.all()

    return render_template('restaurants.html', nav='restaurant', restaurant_list=restaurant_list)


@app.route('/restaurant/create/', methods=['GET', 'POST'])
def create_restaurant():

    if request.method == 'POST':
        req_data = request.form
        name = req_data.get('name')
        desc = req_data.get('desc')
        site_url = req_data.get('site_url')

        restaurant_obj = Restaurant(name=name, desc=desc, site_url=site_url)
        db.session.add(restaurant_obj)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print('Exception: ', e)

        return redirect('/restaurant/list/')

    return render_template('create_restaurant.html')


@app.route('/restaurant/edit/', methods=['GET', 'POST'])
def edit_restaurant():
    req_data = request.args

    restaurant = Restaurant.query.filter_by(id=req_data['id']).first()

    if request.method == 'POST':
        req_data = request.form
        restaurant.name = req_data['name']
        restaurant.desc = req_data['desc']
        restaurant.site_url = req_data['site_url']

        db.session.add(restaurant)
        db.session.commit()

        return redirect('/restaurant/list/')

    return render_template('edit_restaurant.html', restaurant=restaurant)


@app.route('/restaurant/delete/')
def delete_restaurant():
    req_data = request.args

    if req_data['id']:
        restaurant = Restaurant.query.filter_by(id=req_data['id']).first()

        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()

    return redirect('/restaurant/list/')


@app.route('/top')
def top():
    restaurant_list = Restaurant.query.order_by(
        db.desc(Restaurant.draw)).limit(5)

    return render_template('top.html', nav='top', restaurant_list=restaurant_list)


@app.route('/history')
def history():
    history_list = History.query.order_by(
        db.desc(History.create_at)).limit(20)

    return render_template('history.html', nav='history', history_list=history_list)


def mealformat(value):
    if value.hour in [4, 5, 6, 7, 8, 9]:
        return 'Breakfast'
    elif value.hour in [10, 11, 12, 13, 14, 15]:
        return 'Lunch'
    elif value.hour in [16, 17, 18, 20, 21]:
        return 'Dinner'
    else:
        return 'Supper'


def datetimeformat(value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


app.jinja_env.filters['meal'] = mealformat
app.jinja_env.filters['datetime'] = datetimeformat
