import sqlalchemy as master
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import String


Base = declarative_base()
engine = master.create_engine('sqlite:///data.db?check_same_thread=False')
Session = sessionmaker(bind=engine)


class Database:
    def __init__(self):
        self.session = Session()
        Base.metadata.create_all(bind=engine)

    class frequency(Base):
        __tablename__ = 'frequency'

        id = master.Column(master.Integer, primary_key=True)
        owner = master.Column(master.Text, default="")
        reallocable = master.Column(master.Integer, default=0)
        occuped = master.Column(master.Integer, default=0)

        def __repr__(self):
            return f'<Frequency #{self.id}>'

    class admin(Base):
        __tablename__ = 'admin'

        id = master.Column(master.Integer, primary_key=True)
        username = master.Column(master.Text)
        password = master.Column(master.Text)

        def __repr__(self):
            return f'<Admin #{self.id}>'
