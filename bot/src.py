import telebot
import time
import logging

from data import sql_data
from telebot import types

from bot import callback_handler
from bot import message_handler
from bot import users
from bot import state_handler

class ProductBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.products = sql_data.sql_manager("data\products.db")
        self.user = users.User()
        self.CallbackHandlers = callback_handler.CallbackHandlers(self.bot, self.products, self.user)
        self.MessageHandlers = message_handler.MessageHandlers(self.bot, self.products, self.user)
        self.StateHandlers = state_handler.StateHandlers(self.bot, self.products, self.user)
        # Регистрация обработчиков команд
        self.bot.message_handler(commands=['start'])(self.MessageHandlers.start)
        self.bot.message_handler(commands=['add'])(self.MessageHandlers.add_product)
        self.bot.message_handler(func=lambda message:message.text =="Список объявлений")(self.MessageHandlers.list_products)
        self.bot.message_handler(func=lambda message:message.text =="Мои объявления")(self.MessageHandlers.list_users_ads)
        self.bot.message_handler(func=lambda message:message.text =="Разместить объявление")(self.MessageHandlers.add_user_product)
        self.bot.message_handler(func=lambda message:message.text =="Настройки")(self.MessageHandlers.settings)

        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "PRICE")(self.StateHandlers.edit_product_price)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "NAME")(self.StateHandlers.edit_product_name)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "COMMENT")(self.StateHandlers.edit_product_comment)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "CONTACT")(self.StateHandlers.edit_product_contact_user)
        self.bot.message_handler(content_types=['photo'],func=lambda message: self.bot.get_state(message.from_user.id) == "PHOTO")(self.StateHandlers.edit_product_photo)

        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "ADD-PRICE")(self.StateHandlers.add_product_price)
        self.bot.message_handler(content_types=['photo'], func=lambda message:self.bot.get_state(message.from_user.id) == "ADD-PHOTO")(self.StateHandlers.add_product_photo)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "ADD-NAME")(self.StateHandlers.add_product_name)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "ADD-COMMENT")(self.StateHandlers.add_product_comment)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "ADD-CONTACT")(self.StateHandlers.add_product_contact_user)

        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "MAX-PRICE")(self.StateHandlers.add_filter_maxprice)
        self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) == "MIN-PRICE")(self.StateHandlers.add_filter_minprice)

        self.bot.message_handler(func=lambda message:True)(self.MessageHandlers.check_text)
        #self.bot.message_handler(func=lambda message: self.bot.get_state(message.from_user.id) in ["USER_PRODUCTS"])(self.StateHandlers.open_page)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['back'])(self.CallbackHandlers.callback_meny_keyboards)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['info-product', 'edit-product'])(self.CallbackHandlers.callback_get_info_product)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['nextpage', 'prevpage'])(self.CallbackHandlers.callback_page_creator)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['delete', 'edit'])(self.CallbackHandlers.callback_user_ads)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['setprice','setname', 'setcomment', 'setcontact', 'setphoto'])(self.CallbackHandlers.callback_set_details)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['settings'])(self.CallbackHandlers.callback_settings)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['filter'])(self.CallbackHandlers.callback_settings_filters)
        self.bot.callback_query_handler(func=lambda call:call.data.split('_')[0] in ['sorted'])(self.CallbackHandlers.callback_sorted)
    def run(self):
        #self.bot.polling(none_stop=True)
        while True:
            try:
                #self.bot.polling(none_stop=True)
                self.bot.infinity_polling(timeout=10, long_polling_timeout = 10)
            except Exception as e:
                logging.error(e)
                time.sleep(1)
