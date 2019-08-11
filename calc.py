import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from functools import reduce
import re
import math


# def save_data(data):
#     for trade in data:
#         new_task = Todo(content=task_content)
#         db.session.add(new_task)
#         db.session.commit()


def receive_data(file, month):
    df = get_df_by_file(file)

    df['month'] = month
    df['number'] = df['article'].apply(get_aromaname)
    df['aroma_type'] = df['number'].apply(lambda x: x[0])

    groupped = df[['region', 'station', 'article', 'number', 'aroma_type', 'sale', 'rest', 'month']]

    return groupped.fillna(0)


def get_aromaname(article):
    names = {
        '330092830': 'man#01',
        '330092831': 'man#02',
        '330092832': 'man#03',
        '330092833': 'man#04',
        '330092834': 'man#05',
        '330092835': 'man#06',
        '330092836': 'man#07',
        '330092837': 'man#08',
        '330092838': 'man#09',
        '330092839': 'man#10',
        '330092840': 'woman#01',
        '330092841': 'woman#02',
        '330092842': 'woman#03',
        '330092843': 'woman#04',
        '330092844': 'woman#05',
        '330092845': 'woman#06',
        '330092846': 'woman#07',
        '330092847': 'woman#08',
        '330092848': 'woman#09',
        '330092849': 'woman#10'
    }
    return names[str(article)]


def get_df_by_file(file):
    try:
        return pd.read_excel(file)
    except FileNotFoundError:
        print('FileNotFoundError')

