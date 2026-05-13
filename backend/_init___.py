from connect import engine, SessionLocal
from tables import Base, Admin, Book, LibraryCard

def init_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 管理员
    if not db.query(Admin).filter_by(admin_id="admin01").first():
        db.add(Admin(
            admin_id="admin01",
            password="123456",
            name="系统管理员",
            contact="10086"
        ))

    # 图书
    books = [
        Book(
            book_no="B001",
            category="计算机",
            title="Python入门",
            publisher="机械工业出版社",
            year=2024,
            author="张三",
            price=59.8,
            total_count=5,
            stock=5
        ),
        Book(
            book_no="B002",
            category="数学",
            title="高等数学",
            publisher="高等教育出版社",
            year=2023,
            author="李四",
            price=45.0,
            total_count=3,
            stock=1
        ),
        Book(
            book_no="B003",
            category="文学",
            title="活着",
            publisher="作家出版社",
            year=2022,
            author="余华",
            price=39.0,
            total_count=2,
            stock=0
        ),
    ]

    for book in books:
        if not db.query(Book).filter_by(book_no=book.book_no).first():
            db.add(book)

    # 借书证
    if not db.query(LibraryCard).filter_by(card_no="C001").first():
        db.add(LibraryCard(
            card_no="C001",
            name="张三",
            unit="计算机学院",
            category="学生",
            is_active=True
        ))

    db.commit()
    db.close()
    print("初始化完成")

if __name__ == "__main__":
    init_data()