import os

# for docker
#
# user = os.environ['POSTGRES_USER']
# password = os.environ['POSTGRES_PASSWORD']
# host = os.environ['POSTGRES_HOST']
# database = os.environ['POSTGRES_DATABASE']
# port = os.environ['POSTGRES_PORT']

# for local
#
host = '95.213.252.26'
port = 5432
database = 'postgres_db'
user = 'torn'
password = 'helicopter'

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.\
    format(user,
           password,
           host,
           port,
           database)