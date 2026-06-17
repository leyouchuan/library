from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Numeric, ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(String(50), primary_key=True)   # 管理员ID
    password = Column(String(255), nullable=False)     # 密码（建议存哈希）
    name = Column(String(100), nullable=False)        # 姓名
    contact = Column(String(100), nullable=True)      # 联系方式


class Book(Base):
    __tablename__ = "books"

    book_no = Column(String(50), primary_key=True)        # 书号
    category = Column(String(100), nullable=False)        # 类别
    title = Column(String(200), nullable=False)           # 书名
    publisher = Column(String(200), nullable=True)        # 出版社
    year = Column(Integer, nullable=True)                  # 年份
    author = Column(String(200), nullable=True)           # 作者
    price = Column(Numeric(10, 2), nullable=False)        # 价格
    total_count = Column(Integer, nullable=False, default=0)  # 总藏书量
    stock = Column(Integer, nullable=False, default=0)        # 库存


class LibraryCard(Base):
    __tablename__ = "library_cards"

    card_no = Column(String(50), primary_key=True)       # 借书证号
    password = Column(String(255), nullable=False, default="123456") #密码
    name = Column(String(100), nullable=False)           # 姓名
    unit = Column(String(200), nullable=True)            # 单位
    category = Column(String(50), nullable=False)        # 类别（教师/学生等）
    is_active = Column(Boolean, nullable=False, default=True)  # 是否有效


class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_no = Column(String(50), ForeignKey("books.book_no"), nullable=False)
    card_no = Column(String(50), ForeignKey("library_cards.card_no"), nullable=False)
    borrow_time = Column(DateTime, nullable=False, default=datetime.now)
    return_time = Column(DateTime, nullable=True)
    admin_id = Column(String(50), ForeignKey("admins.admin_id"), nullable=False)

    book = relationship("Book")
    card = relationship("LibraryCard")
    admin = relationship("Admin")