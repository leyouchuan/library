from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from function import (
    admin_login, add_book, batch_add_books, query_books,
    add_library_card, delete_library_card,
    borrow_book, return_book, list_borrowed_books
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginReq(BaseModel):
    admin_id: str
    password: str

class AddBookReq(BaseModel):
    book_no: str
    category: str
    title: str
    publisher: str
    year: Optional[int] = None
    author: str
    price: float
    quantity: int

class CardReq(BaseModel):
    card_no: str
    name: str
    unit: str
    category: str

class BorrowReq(BaseModel):
    card_no: str
    book_no: str
    admin_id: str

class ReturnReq(BaseModel):
    card_no: str
    book_no: str


# ========== 管理员登录 ==========
@app.post("/admin/login")
def login(req: LoginReq):
    ok, result = admin_login(req.admin_id, req.password)
    if ok:
        return {"success": True, "admin": {"admin_id": result.admin_id, "name": result.name}}
    return {"success": False, "message": result}


# ========== 单本入库 ==========
@app.post("/books")
def create_book(req: AddBookReq):
    ok, msg = add_book(req.book_no, req.category, req.title, req.publisher,
                       req.year, req.author, req.price, req.quantity)
    return {"success": ok, "message": msg}


# ========== 批量入库（上传文件）==========
@app.post("/books/batch")
async def batch_books(file: UploadFile = File(...)):
    content = await file.read()
    lines = content.decode("utf-8").splitlines()
    book_list = []
    errors = []
    for i, line in enumerate(lines):
        line = line.strip().strip("()")
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 8:
            errors.append(f"第{i+1}行格式错误：{line}")
            continue
        try:
            book_no, category, title, publisher, year, author, price, quantity = parts
            book_list.append((book_no, category, title, publisher, int(year), author, float(price), int(quantity)))
        except Exception as e:
            errors.append(f"第{i+1}行解析失败：{e}")
    results = batch_add_books(book_list)
    return {"success": True, "results": results, "errors": errors}


# ========== 图书查询（支持全参数）==========
@app.get("/books")
def get_books(
    category: Optional[str] = None,
    title: Optional[str] = None,
    publisher: Optional[str] = None,
    year_start: Optional[int] = None,
    year_end: Optional[int] = None,
    author: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    order_by: Optional[str] = "title"
):
    books = query_books(
        category=category, title=title, publisher=publisher,
        year_start=year_start, year_end=year_end,
        author=author, price_min=price_min, price_max=price_max,
        order_by=order_by
    )
    return [
        {
            "book_no": b.book_no, "category": b.category, "title": b.title,
            "publisher": b.publisher, "year": b.year, "author": b.author,
            "price": float(b.price), "total_count": b.total_count, "stock": b.stock,
        }
        for b in books
    ]


# ========== 借书证管理 ==========
@app.post("/cards")
def create_card(req: CardReq):
    ok, msg = add_library_card(req.card_no, req.name, req.unit, req.category)
    return {"success": ok, "message": msg}

@app.delete("/cards/{card_no}")
def remove_card(card_no: str):
    ok, msg = delete_library_card(card_no)
    return {"success": ok, "message": msg}


# ========== 借书 ==========
@app.post("/borrow")
def borrow(req: BorrowReq):
    ok, msg = borrow_book(req.card_no, req.book_no, req.admin_id)
    return {"success": ok, "message": msg}


# ========== 还书 ==========
@app.post("/return")
def ret(req: ReturnReq):
    ok, msg = return_book(req.card_no, req.book_no)
    return {"success": ok, "message": msg}


# ========== 查询借书记录 ==========
@app.get("/borrowed/{card_no}")
def borrowed(card_no: str):
    records = list_borrowed_books(card_no)
    return [
        {
            "id": r.id,
            "book_no": r.book_no,
            "card_no": r.card_no,
            "borrow_time": str(r.borrow_time),
            "return_time": str(r.return_time) if r.return_time else None,
        }
        for r in records
    ]