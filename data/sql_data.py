import sqlite3
class sql_manager:
    def __init__(self, path):
        self.path = path
        self.name = path.split("\\")[-1].replace(".db", "", 1)
        self.connection = sqlite3.connect(f'{self.path}', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER,
            name TEXT,
            comment TEXT,
            price INTEGER,
            date TEXT,
            contact_user TEXT,
            photo_id TEXT
        ) """)
        self.connection.commit()
    def add_new_product(self, product):
        self.cursor.execute(f'INSERT INTO {self.name} (user, name, comment, price, date, contact_user, photo_id) VALUES (?, ?, ?, ?, ?, ?, ?)', tuple(map(lambda x: x[1], product.items())))
        id = self.cursor.lastrowid
        self.connection.commit()
        return id

    def set_product(self, name_val, val, id):
        self.cursor.execute(f"UPDATE {self.name} SET {name_val} = ? WHERE id LIKE ?", (val, id, ))
        self.connection.commit()

    def get_product_from_id(self, id):
        self.cursor.execute(f'SELECT id, name, comment, price, date, contact_user, photo_id FROM {self.name} WHERE id LIKE ?', (id, ))
        item = self.cursor.fetchone()
        if item:
            product = {
                'id':item[0],
                'name': item[1],
                'comment': item[2],
                'price': item[3],
                'date': item[4],
                'contact_user': item[5],
                'photo_id' : item[6]
            }
            return product
        return 0

    def get_products_from_user(self, user, start, end, filters={}):
        count = end - start
        query = f'SELECT id, name, comment, price, date, contact_user, photo_id FROM {self.name} WHERE user LIKE ?'
        params = [user]
        where_clause = ""
        order_by_clause = ""

        if filters:
            where_condition_list = []
            if filters['min_price_filter'] != 0:
                where_condition_list.append('price >= ?')
                params.append(filters['min_price_filter'])

            if filters['max_price_filter'] is not None:
                where_condition_list.append('price <= ?')
                params.append(filters['max_price_filter'])

            if where_condition_list:
                where_clause = ' AND ' + ' AND '.join(where_condition_list)

            if filters['order_by'] is not None:
                order_by_clause = f" ORDER BY {filters['order_by']} {filters['order_direction']}"

        query += where_clause + order_by_clause + ' LIMIT ? OFFSET ?'
        params.append(count)
        params.append(start)
        self.cursor.execute(query, params)
        products = self.cursor.fetchmany(count)
        if products:
            product_list = []
            for item in products:
                product = {
                    'id': item[0],
                    'name': item[1],
                    'comment': item[2],
                    'price': item[3],
                    'date': item[4],
                    'contact_user': item[5],
                    'photo_id': item[6]
                }
                product_list.append(product)
            return product_list
        return 0
    def delete_product(self, id):
        self.cursor.execute(f"DELETE FROM {self.name} WHERE id LIKE ?", (id,))
        self.connection.commit()
