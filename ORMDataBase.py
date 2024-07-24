import configparser
import sqlalchemy
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
    publisher1 = Publisher(name = "Пушкин")
    publisher2 = Publisher(name = "Гоголь")
    publisher3 = Publisher(name = "Бажов")
    publisher4 = Publisher(name = "Булгаков")
    #session.add(publisher1)
    session.add(publisher2)
    session.add(publisher3)
    session.add(publisher4)

    shop1 = Shop(name = "Читай- город")
    shop2 = Shop(name = "Лабиринт")
    shop3 = Shop(name = "Буквоед")
    shop4 = Shop(name = "Книжный дом")
    shop5 = Shop(name = "Живое слово")

    session.add(shop1) # Читай- город
    session.add(shop2) # Лабиринт
    session.add(shop3) # Буквоед
    session.add(shop4) # Книжный дом
    session.add(shop5) # Живое слово

    book1 = Book(title = "Капитанская дочка", publisher = publisher1)
    book2 = Book(title = "Руслан и Людмила", publisher = publisher1)
    book3 = Book(title = "Евгений Онегин", publisher = publisher1)
    book4 = Book(title = "Мертвые души", publisher = publisher2)
    book5 = Book(title = "Вий", publisher = publisher2)
    book6 = Book(title = "Серебрянное копытце", publisher = publisher3)
    book7 = Book(title = "Хозяйка медной горы", publisher = publisher3)
    book8 = Book(title = "Мастер и Маргарита", publisher = publisher4)

    session.add(book1) # Капитанская дочка
    session.add(book2) # Руслан и Людмила
    session.add(book3) # Евгений Онегин
    session.add(book4) # Мертвые души
    session.add(book5) # Вий
    session.add(book6) # Серебрянное копытце
    session.add(book7) # Хозяйка медной горы
    session.add(book8) # Мастер и Маргарита

    stock1 = Stock(book = book1, shop = shop3, count = 2)
    stock2 = Stock(book = book2, shop = shop3, count = 4)
    stock3 = Stock(book = book1, shop = shop2, count = 2)
    stock4 = Stock(book = book3, shop = shop4, count = 6)
    stock5 = Stock(book = book6, shop = shop5, count = 2)
    stock6 = Stock(book = book6, shop = shop1, count = 2)
    stock7 = Stock(book = book8, shop = shop1, count = 5)
    stock8 = Stock(book = book7, shop = shop4, count = 2)
    stock9 = Stock(book = book5, shop = shop2, count = 2)
    stock10 = Stock(book = book4, shop = shop5, count = 2)

    session.add(stock1)
    session.add(stock2)
    session.add(stock3)
    session.add(stock4)
    session.add(stock5)
    session.add(stock6)
    session.add(stock7)
    session.add(stock8)
    session.add(stock9)
    session.add(stock10)

    sale1 = Sale(price = 600, date_sale = "09-11-2022", stock = stock1, count = 1)
    sale2 = Sale(price = 500, date_sale = "08-11-2022", stock = stock2, count = 1)
    sale3 = Sale(price = 580, date_sale = "05-11-2022", stock = stock3, count = 1)
    sale4 = Sale(price = 490, date_sale = "02-11-2022", stock = stock4, count = 1)
    sale5 = Sale(price = 600, date_sale = "26-10-2022", stock = stock1, count = 1)
    sale6 = Sale(price = 700, date_sale = "10-11-2022", stock = stock7, count = 1)
    sale7 = Sale(price = 650, date_sale = "09-11-2022", stock = stock5, count = 1)
    sale8 = Sale(price = 600, date_sale = "15-11-2022", stock = stock6, count = 1)
    sale9 = Sale(price = 1300, date_sale = "14-11-2022", stock = stock10, count = 1)
    sale10 = Sale(price = 830, date_sale = "09-11-2022", stock = stock9, count = 1)

    session.add(sale1)
    session.add(sale2)
    session.add(sale3)
    session.add(sale4)
    session.add(sale5)
    session.add(sale6)
    session.add(sale7)
    session.add(sale8)
    session.add(sale9)
    session.add(sale10)

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
        print(f'{el[0].ljust(20)} | {el[1].ljust(15)} | {str(el[2]).ljust(5)} | {(el[3]).strftime('%d-%m-%Y')}')
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
    dsn = config.get('Settings', 'dsn')

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