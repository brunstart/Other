# -*- coding: utf-8 -*-
import sqlite3
from prettytable import PrettyTable

## 데이터베이스를 연결하는 코드
conn = sqlite3.connect("sqlite3.db")
c = conn.cursor()
table = PrettyTable()

## 상품과 주문 테이블을 생성하는 코드
def create_table():
    create_item = """
        CREATE TABLE IF NOT EXISTS item(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INT NOT NULL, 
            quantity UNSIGNED INT NOT NULL
        )
    """
    create_cart = """
        CREATE TABLE IF NOT EXISTS cart(
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            quantity INT UNSIGNED NOT NULL,
            item_id INT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            price INT NOT NULL,
            FOREIGN KEY(item_id) REFERENCES item(id)
        )
    """
    c.execute(create_item)
    c.execute(create_cart)

## 상품 데이터를 추가하는 코드
# c.execute("INSERT INTO ...
def insert():

    search_q = c.execute("""
                            select *
                            from item
    """)

    search = search_q.fetchall()
    
    if len(search) == 0:
        c.execute("""
            INSERT INTO item (name, price, quantity) 
            VALUES ('A', 21500, 3),
                    ('B', 500, 190),
                    ('C', 1000, 20),
                    ('D', 9000, 15),
                    ('E', 3800, 100),
                    ('F', 2000, 10),
                    ('G', 15000, 10)
        """)
        
        conn.commit()

## 상품 목록을 표시하는 코드
def view_item():
    print('')
    item_list = """
        SELECT id, name, price, quantity
        FROM item
        WHERE quantity > 0
    """
    c.execute(item_list)
    stock = c.fetchall()
    table.title = "상품 목록"
    table.field_names = ["번호", "제품명", "가격", "수량"]
    table.add_rows(stock)

create_table()
insert()
view_item()


def stock_check(order, stock):
    if order > stock:
        return True
    else:
        return False


while True:
    print(table)
    ## 상품 번호와 주문 수량을 입력받는 코드
    while True:
        try:

            print()
            buy_item_id = int(input("제품 번호 입력: "))
            print()
            buy_item_quantity = int(input("구매 수량 입력: "))

            oq = c.execute(f"""
                select quantity
                from item
                where id = {buy_item_id}
            """)

            stock_quantity = oq.fetchall()[0][0]

            if stock_check(buy_item_quantity, stock_quantity):
                print('\n재고 부족')
                continue

        except:
            print("\n잘못된 입력")
        else:
            break


    ## 주문 데이터를 db에 추가하는 코드
    # c.execute("INSERT INTO ...

    total_price_q = f"""
        SELECT price * {buy_item_quantity}
        from item
        where id = {buy_item_id} 
    """

    tqp = c.execute(total_price_q)

    total_price = tqp.fetchall()[0][0]

    insert_cart = f"""
        INSERT INTO cart (item_id, quantity, price) 
        VALUES ({buy_item_id}, {buy_item_quantity}, {total_price})
    """
    c.execute(insert_cart)
    conn.commit()

    ## 현재까지 주문 내역을 출력하는 코드
    print()
    print("주문 내역")
    print()

    cart_list_table = """
        SELECT number, cart.item_id, item.name, cart.quantity, cart.price
        from cart, item
        where cart.item_id = item.id
    """
    c.execute(cart_list_table)

    cart_list = c.fetchall()
    cart = PrettyTable()
    cart.title = "나의 주문 내역"
    cart.field_names = ["주문 번호", "제품 번호", "제품명", "개수", "가격"]
    cart.add_rows(cart_list)

    print(cart)

    clear_cart = """
        delete from cart;
    """
    clear_sequence = """
        delete from sqlite_sequence;
    """

    order_confirm = input("\n주문을 완료하시겠습니까? [Y/N] \n")
    
    if order_confirm == "Y":
        
        c.execute(clear_cart)
        c.execute(clear_sequence)
        conn.commit()
        
        exit = input("\n주문이 완료되었습니다. 계속 쇼핑하시겠습니까? [Y/N] \n")

        if exit == 'Y':
            print()
        elif exit == 'N':
            print('\n쇼핑을 종료합니다')
            conn.close()
            break
        else:
            print('잘못된 입력, 쇼핑 종료')
            conn.close()
            break
    else:
        print()