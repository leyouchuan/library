from fastapi import FastAPI
from schemas import AdminLogin, BookCreate, CardCreate, BorrowCreate, ReturnCreate
from library_functions import (
    admin_login,
    add_book,
    batch_add_books,
    query_books,
    add_library_card,
    delete_library_card,
    list_borrowed_books,
    borrow_book,
    return_book
)

app = FastAPI(title="Library System API")


@app.post("/admin/login")
def login(data: AdminLogin):
    ok, result = admin_login(data.admin_id, data.password)
    if ok:
        return {"success": True, "admin": {"admin_id": result.admin_id, "name": result.name}}
    return {"success": False, "message": result}


@app.post("/books/add")
def books_add(data: BookCreate):
    ok, msg = add_book(
        data.book_no, data.category, data.title, data.publisher,
        data.year, data.author, data.price, data.quantity
    )
    return {"success": ok, "message": msg}


@app.post("/cards/add")
def cards_add(data: CardCreate):
    ok, msg = add_library_card(data.card_no, data.name, data.unit, data.category)
    return {"success": ok, "message": msg}


@app.delete("/cards/{card_no}")
def cards_delete(card_no: str):
    ok, msg = delete_library_card(card_no)
    return {"success": ok, "message": msg}


@app.get("/books/search")
def books_search(
    category: str = None,
    title: str = None,
    publisher: str = None,
    year_start: int = None,
    year_end: int = None,
    author: str = None,
    price_min: float = None,
    price_max: float = None,
    order_by: str = "title"
):
    books = query_books(
        category=category,
        title=title,
        publisher=publisher,
        year_start=year_start,
        year_end=year_end,
        author=author,
        price_min=price_min,
        price_max=price_max,
        order_by=order_by
    )
    return {"success": True, "data": [
        {
            "book_no": b.book_no,
            "category": b.category,
            "title": b.title,
            "publisher": b.publisher,
            "year": b.year,
            "author": b.author,
            "price": b.price,
            "total_count": b.total_count,
            "stock": b.stock
        } for b in books
    ]}


@app.post("/borrow")
def borrow(data: BorrowCreate):
    ok, msg = borrow_book(data.card_no, data.book_no, data.admin_id)
    return {"success": ok, "message": msg}


@app.post("/return")
def do_return(data: ReturnCreate):
    ok, msg = return_book(data.card_no, data.book_no)
    return {"success": ok, "message": msg}


@app.get("/cards/{card_no}/borrowed")
def borrowed(card_no: str):
    records = list_borrowed_books(card_no)
    return {
        "success": True,
        "data": [
            {
                "id": r.id,
                "book_no": r.book_no,
                "card_no": r.card_no,
                "borrow_time": r.borrow_time,
                "return_time": r.return_time
            } for r in records
        ]
    }