import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from api.models.user import Base, User

load_dotenv()

class Database:

    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_db_session(self):
        session = self.Session()
        return session

    def register_user(self, username, password, role):
        session = self.get_db_session()
        try:
            new_user = User(username=username, password=password, role=role)
            session.add(new_user)
            session.commit()
            print('User registered successfully')
        except Exception as e:
            session.rollback()
            print(f'Error occurred: {e}')
        finally:
            session.close()

    def login_user(self, username, password):
        session = self.get_db_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and user.password == password:
                print(f'User {username} logged in successfully')
                return True
            else:
                print('Invalid username or password')
                return False
        except Exception as e:
            print(f'Error occurred: {e}')
            return False
        finally:
            session.close()

    def add_product(self, username, product_name, product_price, product_quantity, product_description):
        session = self.get_db_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user.add_product(session, product_name, product_price, product_quantity, product_description):
                return True
            return False
        except Exception as e:
            print(f'Error occurred: {e}')
        finally:
            session.close()

    def remove_product(self, username, product_id):
        session = self.get_db_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user.remove_product(session, product_id):
                return True
            return False
        except Exception as e:
            print(f'Error occurred: {e}')
        finally:
            session.close()

    def view_sell_summary(self, username):
        session = self.get_db_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                return user.view_order_summary(session)
            return []
        except Exception as e:
            print(f'Error occurred: {e}')
        finally:
            session.close()