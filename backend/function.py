from datetime import datetime
from sqlalchemy import select, and_
from tables import Admin, Book, LibraryCard, BorrowRecord, Base
from connect import SessionLocal, engine

# 建表 drop if exists
def init_db(drop=False):
    if drop:
        Base.metadata.drop_all(bind=engine)
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
        # 联合查询 BorrowRecord 和 Book 表
        stmt = select(
            Book.book_no,
            Book.category,
            Book.title,
            Book.publisher,
            Book.year,
            Book.author,
            Book.price,
            BorrowRecord.borrow_time
        ).join(
            BorrowRecord, Book.book_no == BorrowRecord.book_no
        ).where(
            and_(
                BorrowRecord.card_no == card_no,
                BorrowRecord.return_time.is_(None)
            )
        )
        records = db.execute(stmt).all()
        
        # 返回包含完整图书信息的列表
        result = []
        for row in records:
            result.append({
                'book_no': row[0],
                'category': row[1],
                'title': row[2],
                'publisher': row[3],
                'year': row[4],
                'author': row[5],
                'price': float(row[6]) if row[6] else 0,
                'borrow_time': row[7].strftime('%Y-%m-%d %H:%M:%S') if row[7] else None
            })
        return result


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

        # ===== 新增：检查该证是否已借该书且未归还 =====
        existing_stmt = select(BorrowRecord).where(
            and_(
                BorrowRecord.card_no == card_no,
                BorrowRecord.book_no == book_no,
                BorrowRecord.return_time.is_(None)
            )
        )
        existing = db.execute(existing_stmt).scalars().first()
        if existing:
            return False, "该借书证已借阅此书，请先归还"

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

# ========== 用户登录（使用借书证号） ==========
def user_login(card_no: str, password: str):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if card and card.is_active and card.password == password:
            return True, card
        return False, "借书证号或密码错误"

# ========== 获取用户信息 ==========
def get_user_info(card_no: str):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if not card:
            return None
        return {
            'card_no': card.card_no,
            'name': card.name,
            'unit': card.unit,
            'category': card.category,
            'is_active': card.is_active
        }

# ========== 更新用户信息 ==========
def update_user_info(card_no: str, name: str = None, unit: str = None, category: str = None):
    with SessionLocal() as db:
        card = db.get(LibraryCard, card_no)
        if not card:
            return False, "借书证不存在"
        if not card.is_active:
            return False, "借书证已失效"
        
        if name is not None:
            card.name = name
        if unit is not None:
            card.unit = unit
        if category is not None:
            card.category = category
            
        db.commit()
        return True, "用户信息更新成功"

# ========== 查询用户借书历史（包含已归还的） ==========
def get_user_borrow_history(card_no: str, include_returned: bool = False):
    with SessionLocal() as db:
        stmt = select(
            BorrowRecord.id,
            Book.book_no,
            Book.category,
            Book.title,
            Book.publisher,
            Book.year,
            Book.author,
            Book.price,
            BorrowRecord.borrow_time,
            BorrowRecord.return_time
        ).join(
            Book, BorrowRecord.book_no == Book.book_no
        ).where(
            BorrowRecord.card_no == card_no
        )
        
        if not include_returned:
            stmt = stmt.where(BorrowRecord.return_time.is_(None))
        
        records = db.execute(stmt).all()
        
        result = []
        for row in records:
            result.append({
                'id': row[0],
                'book_no': row[1],
                'category': row[2],
                'title': row[3],
                'publisher': row[4],
                'year': row[5],
                'author': row[6],
                'price': float(row[7]) if row[7] else 0,
                'borrow_time': row[8].strftime('%Y-%m-%d %H:%M:%S') if row[8] else None,
                'return_time': row[9].strftime('%Y-%m-%d %H:%M:%S') if row[9] else None
            })
        return result