from datetime import datetime
from sqlalchemy import select, and_
from tables import Admin, Book, LibraryCard, BorrowRecord, Base
from connect import SessionLocal, engine

# 建表
def init_db():
    Base.metadata.create_all(bind=engine)


# ========== 管理员登录 ==========
def admin_login(admin_id: str, password: str):
    with SessionLocal() as db:
        admin = db.get(Admin, admin_id)
        if admin is not None and admin.password == password:
            return True, admin
        return False, "ID或密码错误"

 
# ========== 图书入库 ==========
def add_book(book_no, category, title, publisher, year, author, price, quantity):
    with SessionLocal() as db:
        book = db.get(Book, book_no)
        if book:
            book.total_count += quantity
            book.stock += quantity
        else:
            book = Book(
                book_no=book_no,
                category=category,
                title=title,
                publisher=publisher,
                year=year,
                author=author,
                price=price,
                total_count=quantity,
                stock=quantity
            )
            db.add(book)
        db.commit()
        return True, "入库成功"


# ========== 批量入库 ==========
def batch_add_books(book_list):
    """
    book_list格式：
    [
        (book_no, category, title, publisher, year, author, price, quantity),
        ...
    ]
    """
    results = []
    with SessionLocal() as db:
        for item in book_list:
            book_no, category, title, publisher, year, author, price, quantity = item
            book = db.get(Book, book_no)
            if book:
                book.total_count += quantity
                book.stock += quantity
                results.append((book_no, "更新成功"))
            else:
                book = Book(
                    book_no=book_no,
                    category=category,
                    title=title,
                    publisher=publisher,
                    year=year,
                    author=author,
                    price=price,
                    total_count=quantity,
                    stock=quantity
                )
                db.add(book)
                results.append((book_no, "新增成功"))
        db.commit()
    return results


# ========== 图书查询 ==========
def query_books(category=None, title=None, publisher=None,
                year_start=None, year_end=None,
                author=None, price_min=None, price_max=None,
                order_by="title"):
    with SessionLocal() as db:
        stmt = select(Book)

        if category:
            stmt = stmt.where(Book.category.like(f"%{category}%"))
        if title:
            stmt = stmt.where(Book.title.like(f"%{title}%"))
        if publisher:
            stmt = stmt.where(Book.publisher.like(f"%{publisher}%"))
        if year_start is not None:
            stmt = stmt.where(Book.year >= year_start)
        if year_end is not None:
            stmt = stmt.where(Book.year <= year_end)
        if author:
            stmt = stmt.where(Book.author.like(f"%{author}%"))
        if price_min is not None:
            stmt = stmt.where(Book.price >= price_min)
        if price_max is not None:
            stmt = stmt.where(Book.price <= price_max)

        if order_by == "category":
            stmt = stmt.order_by(Book.category)
        elif order_by == "publisher":
            stmt = stmt.order_by(Book.publisher)
        elif order_by == "year":
            stmt = stmt.order_by(Book.year)
        elif order_by == "author":
            stmt = stmt.order_by(Book.author)
        elif order_by == "price":
            stmt = stmt.order_by(Book.price)
        else:
            stmt = stmt.order_by(Book.title)

        books = db.execute(stmt).scalars().all()
        return books


# ========== 增加借书证 ==========
def add_library_card(card_no, name, unit, category):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if card:
            return False, "借书证已存在"
        card = LibraryCard(card_no=card_no, name=name, unit=unit, category=category, is_active=True)
        db.add(card)
        db.commit()
        return True, "借书证增加成功"


# ========== 删除借书证 ==========
def delete_library_card(card_no):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if not card:
            return False, "借书证不存在"
        card.is_active = False
        db.commit()
        return True, "借书证删除成功"


# ========== 查询该证未归还图书 ==========
def list_borrowed_books(card_no):
    with SessionLocal() as db:
        stmt = select(BorrowRecord).where(
            and_(
                BorrowRecord.card_no == card_no,
                BorrowRecord.return_time.is_(None)
            )
        )
        records = db.execute(stmt).scalars().all()
        return records


# ========== 借书 ==========
def borrow_book(card_no, book_no, admin_id):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if not card or not card.is_active:
            return False, "借书证无效"

        book = db.get(Book, book_no)
        if not book:
            return False, "图书不存在"

        if book.stock <= 0:
            stmt = select(BorrowRecord.return_time).where(
                BorrowRecord.book_no == book_no,
                BorrowRecord.return_time.is_not(None)
            ).order_by(BorrowRecord.return_time.desc())
            last_return = db.execute(stmt).first()
            return False, f"该书无库存，最近归还时间：{last_return[0] if last_return else '无'}"

        record = BorrowRecord(
            book_no=book_no,
            card_no=card_no,
            borrow_time=datetime.now(),
            return_time=None,
            admin_id=admin_id
        )
        book.stock -= 1
        db.add(record)
        db.commit()
        return True, "借书成功"


# ========== 还书 ==========
def return_book(card_no, book_no):
    with SessionLocal() as db:
        stmt = select(BorrowRecord).where(
            and_(
                BorrowRecord.card_no == card_no,
                BorrowRecord.book_no == book_no,
                BorrowRecord.return_time.is_(None)
            )
        )
        record = db.execute(stmt).scalars().first()

        if not record:
            return False, "没有找到未归还记录"

        book = db.get(Book, book_no)
        if book:
            book.stock += 1

        record.return_time = datetime.now()
        db.commit()
        return True, "还书成功"