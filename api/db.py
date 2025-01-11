import os
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}')
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.users_table = Table('users', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('username', String, unique=True, nullable=False),
                                 Column('password', String, nullable=False))
        self.metadata.create_all(self.engine)

    def get_db_session(self):
        session = self.Session()
        return session

    def register_user(self, username, password):
        session = self.get_db_session()
        try:
            new_user = self.users_table.insert().values(username=username, password=password)
            session.execute(new_user)
            session.commit()
            print('User registered successfully')
        except Exception as e:
            session.rollback()
            print(f'Error occurred: {e}')
        finally:
            session.close()