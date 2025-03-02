from telebot import types
from bot import create_message_data

class CallbackHandlers():
    def __init__(self, bot, products, user):
        self.bot = bot
        self.create_message = create_message_data.CreateMessage(products, user)
        self.products = products
        self.user = user

    def callback_set_details(self, call):
        command, id = tuple(call.data.split('_'))
        if command == 'setname':
            self.bot.send_message(call.message.chat.id, 'Введите новое имя продукта:')
            self.bot.set_state(call.from_user.id, "NAME")
        elif command == 'setprice':
             self.bot.send_message(call.message.chat.id, 'Введите новую цену продукта:')
             self.bot.set_state(call.from_user.id, "PRICE")

        elif command == 'setcomment':
            self.bot.send_message(call.message.chat.id, 'Введите новое описание продукта:')
            self.bot.set_state(call.from_user.id, "COMMENT")

        elif command == 'setcontact':
            self.bot.send_message(call.message.chat.id, 'Введите новое контакты для связи с вами:')
            self.bot.set_state(call.from_user.id, "CONTACT")

        elif command == 'setphoto':
            self.bot.send_message(call.message.chat.id, 'Добавьте новое фото:')
            self.bot.set_state(call.from_user.id, "PHOTO")
        self.user.set_id(call.from_user.id, id)

    def callback_page_creator(self, call):
        command, call_page_index = tuple(call.data.split('_'))
        page_index = int(call_page_index)
        promt, markup = self.create_message.mess_generate_page(command, page_index, filters=self.user.get_data_filters(call.from_user.id))
        self.user.set_data(call.from_user.id, 'prev_state', f"all-products_{page_index}")
        self.bot.edit_message_text(text=promt, reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

    def callback_get_info_product(self, call):
        command, id = tuple(call.data.split('_'))
        if command == 'edit-product':
            product = self.products.get_product_from_id(id)
            edit_buttons = types.InlineKeyboardMarkup()
            edit_buttons.add(types.InlineKeyboardButton(text="Удалить", callback_data=f"delete_{product['id']}"),
                types.InlineKeyboardButton(text='Редактировать', callback_data=f"edit_{product['id']}"),
                types.InlineKeyboardButton(text='Назад', callback_data="back"))

            text = f"{product['name']} Цена: {product['price']} руб. \n {product['comment']}\n Контакты: {product['contact_user']} \n Размещено: {product['date']}\n"
            if product['photo_id']!= "None":
                self.bot.edit_message_media(media=types.InputMediaPhoto(product['photo_id']), chat_id=call.message.chat.id, message_id=call.message.message_id)
                self.bot.edit_message_caption(text, reply_markup = edit_buttons, chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                self.bot.edit_message_text(text, reply_markup = edit_buttons, chat_id=call.message.chat.id, message_id=call.message.message_id)
        elif command =='info-product':
            product = self.products.get_product_from_id(id)
            edit_buttons = types.InlineKeyboardMarkup()
            edit_buttons.add(types.InlineKeyboardButton(text='Назад', callback_data="back"))
            text = f"{product['name']} Цена: {product['price']} руб. \n {product['comment']}\n Контакты: {product['contact_user']} \n Размещено: {product['date']}\n"
            if product['photo_id']!= "None":
                self.bot.edit_message_media(media=types.InputMediaPhoto(product['photo_id']), chat_id=call.message.chat.id, message_id=call.message.message_id)
                self.bot.edit_message_caption(text, reply_markup = edit_buttons, chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                self.bot.edit_message_text(text, reply_markup = edit_buttons, chat_id=call.message.chat.id, message_id=call.message.message_id)

    def callback_meny_keyboards(self, call):
        current_state_data = self.user.get_prev_state(call.from_user.id)
        current_state = current_state_data.split('_')[0]
        if current_state == "user-products":
            promt, markup = self.create_message.mess_list_users_ads(call.from_user.id)
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id, promt, reply_markup=markup)
        elif current_state == "all-products":
            page_index_str =current_state_data.split('_')[1]
            page_index = int(page_index_str)
            promt, markup = self.create_message.mess_generate_page('nextpage', page_index, filters=self.user.get_data_filters(call.from_user.id))
            self.user.set_data(call.from_user.id, 'prev_state', f"all-products_{page_index}")
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.send_message(call.message.chat.id, promt, reply_markup=markup)
        elif current_state == "settings":
            promt, markup= self.create_message.mess_settings(call.from_user.id)
            self.user.set_prev_state(call.from_user.id, "settings")
            self.bot.edit_message_text(text = promt, reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)
    def callback_sorted(self, call):
        setting, value = tuple(call.data.split('_'))
        if value == "reduce":
            self.user.set_data_filters(call.from_user.id, 'order_direction', 'DESC')
        elif value == "increase":
            self.user.set_data_filters(call.from_user.id, 'order_direction', 'ASC')
        elif value == "price":
            self.user.set_data_filters(call.from_user.id, 'order_by', 'price')
        elif value == "id":
            self.user.set_data_filters(call.from_user.id, 'order_by', 'id')
        text, keyboard = self.create_message.mess_settings_sorted(call.from_user.id)
        self.bot.edit_message_text(text = text, reply_markup = keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
    def callback_settings(self, call):
        setting, value = tuple(call.data.split('_'))
        if value == "price-range":
            price_filter = self.user.get_data_filters(call.from_user.id)
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Min цена", callback_data=f"filter_minprice"))
            keyboard.add(types.InlineKeyboardButton(text="Max цена", callback_data=f"filter_maxprice"))
            keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))

            text_price = f"Цена от {price_filter['min_price_filter']}"
            if price_filter['max_price_filter']:
                text_price += f" и до {price_filter['max_price_filter']}"
            self.bot.edit_message_text(text = text_price, reply_markup = keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)
            
        elif value =="sorted":
            text, keyboard = self.create_message.mess_settings_sorted(call.from_user.id)
            self.bot.edit_message_text(text = text, reply_markup = keyboard, chat_id=call.message.chat.id, message_id=call.message.message_id)

    def callback_settings_filters(self, call):
        command, value = tuple(call.data.split('_'))
        if value == 'maxprice':
            self.bot.send_message(call.message.chat.id, 'Введите max цену:')
            self.bot.set_state(call.from_user.id, "MAX-PRICE")
        elif value == 'minprice':
            self.bot.send_message(call.message.chat.id, 'Введите min цену:')
            self.bot.set_state(call.from_user.id, "MIN-PRICE")

    def callback_user_ads(self, call):
        command, id = tuple(call.data.split('_'))
        if command == "edit":
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Цена", callback_data=f"setprice_{id}"),
            types.InlineKeyboardButton(text="Фото", callback_data=f"setphoto_{id}"),
            types.InlineKeyboardButton(text=f'Название', callback_data=f"setname_{id}"),
            types.InlineKeyboardButton(text=f'Описание', callback_data=f"setcomment_{id}"),
            types.InlineKeyboardButton(text=f'Контакты', callback_data=f"setcontact_{id}"))
            self.bot.send_message(call.message.chat.id, f'Что хотите изменить?', reply_markup=keyboard)
        elif command == "delete":
            self.products.delete_product(id)
            self.callback_meny_keyboards(call)
