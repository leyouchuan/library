from function import (
    admin_login,
    add_book,
    batch_add_books,
    query_books,
    add_library_card,
    delete_library_card,
    borrow_book,
    return_book,
    list_borrowed_books
)


def print_books(books):
    if not books:
        print("没有查到图书")
        return

    print("-" * 100)
    for book in books:
        print(
            f"书号: {book.book_no} | "
            f"类别: {book.category} | "
            f"书名: {book.title} | "
            f"出版社: {book.publisher} | "
            f"年份: {book.year} | "
            f"作者: {book.author} | "
            f"价格: {book.price} | "
            f"总藏书量: {book.total_count} | "
            f"库存: {book.stock}"
        )
    print("-" * 100)


def print_records(records):
    if not records:
        print("没有未归还记录")
        return

    print("-" * 100)
    for r in records:
        print(
            f"记录ID: {r.id} | "
            f"书号: {r.book_no} | "
            f"借书证号: {r.card_no} | "
            f"借书时间: {r.borrow_time} | "
            f"归还时间: {r.return_time}"
        )
    print("-" * 100)


def main():
    current_admin = None

    while True:
        print("\n========== 图书管理系统 ==========")
        print("1. 管理员登录")
        print("2. 图书入库")
        print("3. 批量入库")
        print("4. 图书查询")
        print("5. 增加借书证")
        print("6. 删除借书证")
        print("7. 借书")
        print("8. 还书")
        print("9. 查询某借书证未归还图书")
        print("0. 退出")
        choice = input("请选择：").strip()

        if choice == "1":
            admin_id = input("管理员ID：").strip()
            password = input("密码：").strip()
            ok, result = admin_login(admin_id, password)
            if ok:
                current_admin = result
                print(f"登录成功，欢迎：{current_admin.name}")
            else:
                print(f"登录失败：{result}")

        elif choice == "2":
            book_no = input("书号：").strip()
            category = input("类别：").strip()
            title = input("书名：").strip()
            publisher = input("出版社：").strip()
            year = input("年份：").strip()
            author = input("作者：").strip()
            price = input("价格：").strip()
            quantity = input("入库数量：").strip()

            year = int(year) if year else None
            price = float(price)
            quantity = int(quantity)

            ok, msg = add_book(book_no, category, title, publisher, year, author, price, quantity)
            print(msg)

        elif choice == "3":
            n = int(input("请输入批量入库条数：").strip())
            book_list = []
            for i in range(n):
                print(f"\n第 {i+1} 条：")
                book_no = input("书号：").strip()
                category = input("类别：").strip()
                title = input("书名：").strip()
                publisher = input("出版社：").strip()
                year = input("年份：").strip()
                author = input("作者：").strip()
                price = input("价格：").strip()
                quantity = input("入库数量：").strip()

                year = int(year) if year else None
                price = float(price)
                quantity = int(quantity)

                book_list.append((book_no, category, title, publisher, year, author, price, quantity))

            results = batch_add_books(book_list)
            for book_no, msg in results:
                print(f"{book_no}: {msg}")

        elif choice == "4":
            category = input("类别（可空）：").strip() or None
            title = input("书名（可空）：").strip() or None
            publisher = input("出版社（可空）：").strip() or None
            year_start = input("起始年份（可空）：").strip()
            year_end = input("结束年份（可空）：").strip()
            author = input("作者（可空）：").strip() or None
            price_min = input("最低价格（可空）：").strip()
            price_max = input("最高价格（可空）：").strip()
            order_by = input("排序字段(title/category/publisher/year/author/price)，默认title：").strip() or "title"

            year_start = int(year_start) if year_start else None
            year_end = int(year_end) if year_end else None
            price_min = float(price_min) if price_min else None
            price_max = float(price_max) if price_max else None

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
            print_books(books)

        elif choice == "5":
            card_no = input("借书证号：").strip()
            name = input("姓名：").strip()
            unit = input("单位：").strip()
            category = input("类别：").strip()
            ok, msg = add_library_card(card_no, name, unit, category)
            print(msg)

        elif choice == "6":
            card_no = input("借书证号：").strip()
            ok, msg = delete_library_card(card_no)
            print(msg)

        elif choice == "7":
            if current_admin is None:
                print("请先登录管理员")
                continue
            card_no = input("借书证号：").strip()
            book_no = input("书号：").strip()
            ok, msg = borrow_book(card_no, book_no, current_admin.admin_id)
            print(msg)

        elif choice == "8":
            card_no = input("借书证号：").strip()
            book_no = input("书号：").strip()
            ok, msg = return_book(card_no, book_no)
            print(msg)

        elif choice == "9":
            card_no = input("借书证号：").strip()
            records = list_borrowed_books(card_no)
            print_records(records)

        elif choice == "0":
            print("退出系统")
            break

        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main()