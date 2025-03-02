from telebot import types
import re
from datetime import datetime
from data import sql_data
from bot import create_message_data
class MessageHandlers():
    def __init__(self, bot, products, user):
        self.bot = bot
        self.create_message = create_message_data.CreateMessage(products, user)
        self.products = products
        self.user = user

    def start(self, message):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        list = types.KeyboardButton("Список объявлений")
        my_ads = types.KeyboardButton("Мои объявления")
        add_ads = types.KeyboardButton("Разместить объявление")
        settings = types.KeyboardButton("Настройки")
        menu.add(list,my_ads, add_ads, settings)
        self.bot.reply_to(message, 'Привет! Я бот для размещения товаров. ', reply_markup=menu)

    def settings(self, message):
        promt, markup= self.create_message.mess_settings(message.from_user.id)
        self.user.set_prev_state(message.from_user.id, "settings")
        self.bot.reply_to(message, text = promt, reply_markup = markup)

    def add_product(self, message):
      match = re.match(r'/add\s+(.+?)\s+(\d+(\.\d+)?)$', message.text)
      if match:
          product_name = match.group(1)
          product_price = int(match.group(2))
          message_date = datetime.fromtimestamp(message.date)
          product = {
               'user': message.from_user.id,
               'name': product_name,
               'comment': 'Нет описания',
               'price': product_price,
               'date': str(message_date.strftime('%Y-%m-%d %H:%M:%S')),
               'contact_user': "Нет контактных данных",
               'photo_id':'None'
          }
          id = self.products.add_new_product(product)
          keyboard = types.InlineKeyboardMarkup()
          keyboard.add(types.InlineKeyboardButton(text="Цена", callback_data=f"setprice_{id}"),
          types.InlineKeyboardButton(text="Фото", callback_data=f"setphoto_{id}"),
          types.InlineKeyboardButton(text=f'Название', callback_data=f"setname_{id}"),
          types.InlineKeyboardButton(text=f'Описание', callback_data=f"setcomment_{id}"),
          types.InlineKeyboardButton(text=f'Контакты', callback_data=f"setcontact_{id}"))
          self.bot.reply_to(message, f'Товар "{product_name}" добавлен! Если хотите добавить или изменить информацию о нем, то воспользуйтесь кнопками:', reply_markup=keyboard)
      else:
          self.bot.reply_to(message, 'Пожалуйста, укажите название товара и его цену. Пример: /add Товар1 100')
    def check_text(self, message):
        print(message.from_user.id, message.text)
    def add_user_product(self, message):
        message_date = datetime.fromtimestamp(message.date)
        product = {
             'user': message.from_user.id,
             'name': "Нет имени",
             'comment': 'Нет описания',
             'price': 0,
             'date': str(message_date.strftime('%Y-%m-%d %H:%M:%S')),
             'contact_user': "Нет контактных данных",
             'photo_id':'None'
        }
        id = self.products.add_new_product(product)
        self.user.set_id(message.from_user.id, id)
        self.bot.reply_to(message, 'Введите название товара: ')
        self.bot.set_state(message.from_user.id, "ADD-NAME")

    def list_products(self, message):
        page_index = 0
        promt, markup= self.create_message.mess_generate_page('nextpage',page_index, filters=self.user.get_data_filters(message.from_user.id))
        self.user.set_prev_state(message.from_user.id, f"all-products_{page_index}")
        self.bot.reply_to(message, text = promt, reply_markup = markup)

    def list_users_ads(self, message):
        promt, markup= self.create_message.mess_list_users_ads(message.from_user.id)
        self.bot.reply_to(message, text=promt, reply_markup=markup)
        self.user.set_prev_state(message.from_user.id, "user-products_0")
