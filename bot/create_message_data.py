from telebot import types

from datetime import datetime
from data import sql_data

class CreateMessage():
    def __init__(self, products, user):
        self.products = products
        self.user = user
        
    def mess_settings_sorted(self, user_id):
        keyboard = types.InlineKeyboardMarkup()
        filters = self.user.get_data_filters(user_id)

        text_reduce = "(+)По убыв." if filters['order_direction'] == "DESC" else "По убыв."
        text_increase = "(+)По возраст." if filters['order_direction'] == "ASC" else "По возраст."
        text_price = "(+)По цене." if filters['order_by'] == "price" else "По цене."
        text_id = "(+)По дате." if filters['order_by'] == "id" else "По дате."

        keyboard.add(types.InlineKeyboardButton(text=text_reduce, callback_data="sorted_reduce"), types.InlineKeyboardButton(text=text_increase, callback_data="sorted_increase"))
        keyboard.add(types.InlineKeyboardButton(text=text_price, callback_data="sorted_price"))
        keyboard.add(types.InlineKeyboardButton(text=text_id, callback_data="sorted_id"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))

        text_sorted = "Сортировка"
        if self.user.get_data_filters(user_id)['order_direction'] == 'ASC':
            text_sorted+=' по возраст.'
        elif self.user.get_data_filters(user_id)['order_direction'] == 'DESC':
            text_sorted+=' по убыв.'
        if self.user.get_data_filters(user_id)['order_by'] == 'price':
            text_sorted += " по цене"
        elif self.user.get_data_filters(user_id)['order_by'] == 'id':
            text_sorted += " по дате"

        text = text_sorted
        reply_markup = keyboard
        return text, reply_markup

    def mess_settings(self, user_id):
        setting_buttons = types.InlineKeyboardMarkup()
        setting_buttons.add(types.InlineKeyboardButton(text="Диапазон цены", callback_data=f"settings_price-range"))
        setting_buttons.add(types.InlineKeyboardButton(text="Параметры сортировки", callback_data=f"settings_sorted"))
        text = 'Настройте фильты поиска: '
        reply_markup=setting_buttons
        return text, reply_markup

    def mess_list_users_ads(self, user):
        user_id = user
        product_list = self.products.get_products_from_user(user_id, 0, 30)
        if product_list:
            promt = []
            product_keys = types.InlineKeyboardMarkup()
            for i in range(len(product_list)):
                product = product_list[i]
                text_message = f"{i+1}) {product['name']} за {product['price']} руб."
                product_keys.add(types.InlineKeyboardButton(text=text_message, callback_data=f"edit-product_{product['id']}"))
            text =  "Ваши объявления:"
            reply_markup = product_keys
        else:
            text =  "Нет доступных товаров."
            reply_markup = None
        return text, reply_markup

    def mess_generate_page(self, command, page_index, count=6, filters={}):
        product_list = self.products.get_products_from_user('%', page_index, page_index+count, filters)
        navigation = types.InlineKeyboardMarkup()
        product_buttons = types.InlineKeyboardMarkup()
        if product_list:
            for i in range(len(product_list)):
                product = product_list[i]
                text_message = f"{i+1+page_index}) {product['name']} за {product['price']} руб."
                product_buttons.add(types.InlineKeyboardButton(text=text_message, callback_data=f"info-product_{product['id']}"))
            text = "Список товаров:"
        else:
            text = "Нет доступных товаров."

        if command == "nextpage":
            if product_list==0 or len(product_list) < count:
                product_buttons.add(types.InlineKeyboardButton(text=f'<<', callback_data=f"prevpage_{page_index-count}"))
            elif page_index ==0:
                product_buttons.add(types.InlineKeyboardButton(text=f'>>', callback_data=f"nextpage_{page_index+count}"))
            else:
                product_buttons.add(types.InlineKeyboardButton(text=f'<<', callback_data=f"prevpage_{page_index-count}"),
                types.InlineKeyboardButton(text=f'>>', callback_data=f"nextpage_{page_index+count}"))
        elif command == "prevpage":
            if page_index < count:
                product_buttons.add(types.InlineKeyboardButton(text=f'>>', callback_data=f"nextpage_{page_index+count}"))
            else:
                product_buttons.add(types.InlineKeyboardButton(text=f'<<', callback_data=f"prevpage_{page_index-count}"),
                types.InlineKeyboardButton(text=f'>>', callback_data=f"nextpage_{page_index+count}"))

        reply_markup = product_buttons

        return text, reply_markup
