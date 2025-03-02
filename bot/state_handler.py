from telebot import types

class StateHandlers:
    def __init__(self, bot, products, user):
        self.bot = bot
        self.products = products
        self.user = user
    def edit_product_price(self, message):
      price = message.text
      user_data = self.user.get_user_data(message.from_user.id)
      if price.isdigit():
          self.products.set_product("price", int(price), user_data['id'])
          self.bot.delete_state(message.from_user.id)
          self.bot.send_message(message.from_user.id, 'Цена на товар измена.')
      else:
          self.bot.send_message(message.from_user.id, 'Неверный формат цены. Пожалуйста, введите число.')

    def edit_product_photo(self, message):
      photo_id = message.photo[-1].file_id
      user_data = self.user.get_user_data(message.from_user.id)
      self.products.set_product("photo_id", photo_id, user_data['id'])
      self.bot.delete_state(message.from_user.id)
      self.bot.send_message(message.from_user.id, 'Фото товара измено.')

    def edit_product_name(self, message):
      name = message.text
      user_data = self.user.get_user_data(message.from_user.id)
      self.products.set_product("name", name, user_data['id'])
      self.bot.delete_state(message.from_user.id)
      self.bot.send_message(message.from_user.id, 'Название товара измено.')

    def edit_product_comment(self, message):
      comment = message.text
      user_data = self.user.get_user_data(message.from_user.id)
      self.products.set_product("comment", comment, user_data['id'])
      self.bot.delete_state(message.from_user.id)
      self.bot.send_message(message.from_user.id, 'Описание товара измено.')

    def edit_product_contact_user(self, message):
        contact_user = message.text
        user_data = self.user.get_user_data(message.from_user.id)
        self.products.set_product("contact_user", contact_user, user_data['id'])
        self.bot.delete_state(message.from_user.id)
        self.bot.send_message(message.from_user.id, 'Ваши данные для связи изменены.')

    def add_product_name(self, message):
        name = message.text
        user_data = self.user.get_user_data(message.from_user.id)
        self.products.set_product("name", name, user_data['id'])
        self.bot.send_message(message.from_user.id, 'Добавьте фото товара:')
        self.bot.set_state(message.from_user.id, "ADD-PHOTO")

    def add_product_photo(self, message):
        photo_id = message.photo[-1].file_id
        user_data = self.user.get_user_data(message.from_user.id)
        self.products.set_product("photo_id", photo_id, user_data['id'])
        self.bot.send_message(message.from_user.id, 'Укажите цену товара:')
        self.bot.set_state(message.from_user.id, "ADD-PRICE")

    def add_product_price(self, message):
        price = message.text
        user_data = self.user.get_user_data(message.from_user.id)
        if price.isdigit():
            self.products.set_product("price", int(price), user_data['id'])
            self.bot.delete_state(message.from_user.id)
            self.bot.send_message(message.from_user.id, 'Укажите описание товара:')
            self.bot.set_state(message.from_user.id, "ADD-COMMENT")
        else:
            self.bot.send_message(message.from_user.id, 'Неверный формат цены. Пожалуйста, введите число.')
    def add_product_comment(self, message):
        comment = message.text
        user_data = self.user.get_user_data(message.from_user.id)
        self.products.set_product("comment", comment, user_data['id'])
        self.bot.delete_state(message.from_user.id)
        self.bot.send_message(message.from_user.id, 'Укажите контакты для связи с вами:')
        self.bot.set_state(message.from_user.id, "ADD-CONTACT")

    def add_product_contact_user(self, message):
        contact_user = message.text
        user_data = self.user.get_user_data(message.from_user.id)
        self.products.set_product("contact_user", contact_user, user_data['id'])
        self.bot.delete_state(message.from_user.id)
        self.bot.send_message(message.from_user.id, 'Ваши данные для связи изменены.')

    def add_filter_minprice(self, message):
        price = message.text
        if price.isdigit():
            self.user.set_data_filters(message.from_user.id, 'min_price_filter', price)
            self.bot.delete_state(message.from_user.id)
            self.bot.send_message(message.from_user.id, 'Установлена min цена')
        else:
            self.bot.send_message(message.from_user.id, 'Неверный формат цены. Пожалуйста, введите число.')

    def add_filter_maxprice(self, message):
        price = message.text
        if price.isdigit():
            self.user.set_data_filters(message.from_user.id, 'max_price_filter', price)
            self.bot.delete_state(message.from_user.id)
            self.bot.send_message(message.from_user.id, 'Установлена max цена')
        else:
            self.bot.send_message(message.from_user.id, 'Неверный формат цены. Пожалуйста, введите число.')
