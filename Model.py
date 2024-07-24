import configparser
import sqlalchemy
import os
import json
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import func

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length = 40), unique = True)

    def __str__(self):
        return f'{self.id}. {self.name}'
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

    def __str__(self):
        return f'{self.title}'
class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key = True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable = False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    shop = relationship(Shop, backref = "shops")
    book = relationship(Book, backref = "books")

    def __str__(self):
        return f'{self.count}'
class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key = True)
    price = sq.Column(sq.Numeric, nullable = False)
    date_sale = sq.Column(sq.Date, nullable = False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable = False)
    count = sq.Column(sq.Integer, nullable = False)

    stock = relationship(Stock, backref = "stocks")

    def __str__(self):
        return f'{self.price},{self.date_sale} '

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def insert_content():
    with open("tests_data.json") as f_json:
        json_data = json.load(f_json)
    # json_str = json_data
    # json_data = json.loads(f'{json_str}')
    for el in json_data:
        if el['model'] == 'publisher':
            publ_name = el['fields']['name']
            publisher = Publisher(name=publ_name)
            session.add(publisher)
        elif el['model'] == 'book':
            book_title = el['fields']['title']
            book_id_publ = session.query(Publisher).get(el['fields']['id_publisher'])
            book = Book(title=book_title, publisher=book_id_publ)
            session.add(book)
        elif el['model'] == 'shop':
            shop_name = el['fields']['name']
            shop = Shop(name=shop_name)
            session.add(shop)
        elif el['model'] == 'stock':
            book_id = session.query(Book).get(el['fields']['id_book'])
            shop_id = session.query(Shop).get(el['fields']['id_shop'])
            cnt_stock = el['fields']['count']
            stock = Stock(book=book_id, shop=shop_id, count=cnt_stock)
            session.add(stock)
        elif el['model'] == 'sale':
            price = el['fields']['price']
            date = el['fields']['date_sale']
            cnt_sale = el['fields']['count']
            st_id = session.query(Stock).get(el['fields']['id_stock'])
            sale = Sale(price=price, date_sale=date, stock=st_id, count=cnt_sale)
            session.add(sale)
    session.commit()
    session.close() #по аналогии с курсором нужно закрыть

def select_publishers():
    for p in session.query(Publisher).all():
        print(p)

def select_list(author):
    a = session.query(Book.title,Shop.name,Sale.price,Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if author.isdigit():
        query = a.filter(Publisher.id == author).all()
        cnt = a.filter(Publisher.id == author).count()
    else:
        query = a.filter(func.upper(Publisher.name).like(f'%{author}%')).all()
        cnt = a.filter(func.upper(Publisher.name).like(f'%{author}%')).count()
    print()
    print(f'По Вашему запросу "{author}" найдено {cnt} записей:')
    b="***"
    print(b.center(60,'-'))
    for el in query:
        print(f'{el[0].ljust(40)} | {el[1].ljust(15)} | {str(el[2]).ljust(5)} | {(el[3]).strftime('%d-%m-%Y')}')
    print()

    # for a in session.query(Publisher).join(Book).filter(Publisher.name.like(f'%{author}%')).all():
    #     print(a)
    # subq = session.query(Publisher).filter(Publisher.name.like(f'%{author}%')).subquery()
    # for a in (session.query(Book).
    #         join(subq, Book.id_publisher == subq.c.id)
    #         join(subq, Book.id_publisher == subq.c.id)
    #         .all()):
    #     print(a)
    # for a in session.query(Publisher).filter(Publisher.name.like(f'%{author}%')).all():


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    dsn = config.get('Settings', 'dsn1')

    DSN = dsn
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind = engine)
    session = Session()

    insert_content()
    question = input("Показать список авторов? Y/N\n")
    while question.lower() != "n":
        select_publishers()
        question2 = input("Вывести список произведений? Y/N\n")
        while question2.lower() != "n":
            if question2.lower() == "y":
                author = input("Введите автора или его ID:\n")
                select_list(author.upper())
            question2 = input("Вывести список произведений? Y/N\n")
        question = input("Показать список авторов? Y/N\n")
    print('Программа завершена')