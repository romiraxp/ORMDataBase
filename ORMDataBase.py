import configparser
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 40), unique = True)

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 40), unique = True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key = True)
    title = sq.Column(sq.String, nullable = False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable = False)

    publisher = relationship(Publisher, backref = "publishers")

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    shop = relationship(Shop, backref = "shops")
    book = relationship(Book, backref = "books")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.Numeric, nullable = False)
    date_sale = sq.Column(sq.Date, nullable = False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    stock = relationship(Stock, backref = "stocks")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    dsn = config.get('Settings', 'dsn')

    DSN = dsn
    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind = engine)
    session = Session()

    #publisher1 = Publisher(name = "Пушкин")

    #session.add(publisher1)

    session.commit()
    session.close() #по аналогии с курсором нужно закрыть