from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# import dev_settings as config
import numpy as np
import config

from calc import receive_data


app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Sino_trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    station = db.Column(db.String(50), nullable=False)
    article = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    sale = db.Column(db.Integer, default=0)
    rest = db.Column(db.Integer, default=0)
    month = db.Column(db.String(50), nullable=False)
    aroma_type = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, region, station, article, number, sale, rest, month, aroma_type):
    #     self.region = region
    #     self.station = station
    #     self.article = article
    #     self.number = number
    #     self.sale = 0
    #     self.rest = 0
    #     self.month = month
    #     self.aroma_type = aroma_type

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        # if db.engine.dialect.has_table(db.engine, 'Todo'):
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task_to_update)


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        month = request.form['month']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        data = receive_data(file, month)
        # data['jul_rest'].fillna(0, inplace=True)

        print(datetime.now())
        count = data['region'].count()
        # print(data.iloc[0]['region'])

        for item in range(count):
            pass

            # print('region - {} - {}'.format(item['region'], type(item['region'])))
            # print('station - {} - {}'.format(item['station'], type(item['station'])))
            # print('article - {} - {}'.format(item['article'], type(item['article'])))
            # print('number - {} - {}'.format(item['number'], type(item['number'])))
            # print('sale - {} - {}'.format(item['sale'], type(item['sale'])))
            # print('rest - {} - {}'.format(item['rest'], type(item['rest'])))
            # print('month - {} - {}'.format(item['month'], type(item['month'])))
            # print('aroma_type - {} - {}'.format(item['aroma_type'], type(item['aroma_type'])))

            # trade = Sino_trade(data.iloc[item]['region'],
            #                    data.iloc[item]['station'],
            #                    data.iloc[item]['article'],
            #                    data.iloc[item]['number'],
            #                    0, # np.int16(data.iloc[item]['sale']),
            #                    0, # np.int16(data.iloc[item]['rest']),
            #                    data.iloc[item]['month'],
            #                    data.iloc[item]['aroma_type']
            #                    )
            # trade = Sino_trade(region='', station='', article='', number='', sale=0, rest=0, month='', aroma_type='')
            # db.session.add(trade)
            # db.session.commit()

        data.to_sql('sino_trade', con=db.engine, if_exists='append',
                    # index_label='id',
                    index=False,
                    dtype={'region': db.String(50),
                           'station': db.String(50),
                           'article': db.Integer,
                           'number': db.String(50),
                           'sale': db.Integer,
                           'rest': db.Integer,
                           'month': db.String(50),
                           'aroma_type': db.String(50)
                           })

        print(datetime.now())

        return redirect('/')
    else:
        return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)

