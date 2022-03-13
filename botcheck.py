from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import telebot
import requests
import os
import json
import yfinance as yf
import pandas
import numpy
import urllib.request
from ta.momentum import RSIIndicator
from datetime import date, timedelta

def start(update, context):
    
    name = update.message.chat.first_name
    chat_id = update.message.chat.id
    TOKEN = os.environ.get("TOKEN")
    bot = telebot.TeleBot(TOKEN)
    bot.config['api_key'] = TOKEN
    users = os.environ.get("Users") # allowed users.
    allowed_chat_ids = users.split(",")
    allowed_chat_ids = map(int, allowed_chat_ids)
    
    if chat_id in allowed_chat_ids:
        
        msg = "Hi " + name + " Welcome to crypto alerts. Please type cryptocurrency symbol and the target value of it's RSI e.g. for Bitcoin type as: BTCUSDT 50, where 50 is the target RSI value"
        context.bot.send_message(chat_id, msg)
        
    else:
        
        msg = "Hi " + yourname + " You are not registered..."
        context.bot.send_message(chat_id, msg)
        
def c_rsi(symbol, time_window):
    
    l = len(symbol)
    y_symbol = symbol[:l-4] + '-' + 'USD'
    window  = time_window
    today = date.today()
    st = today - timedelta(days=30)
    data = yf.download(y_symbol, start=st, end= today, interval = "1d")
    data = RSIIndicator(data["Close"], window)
    data = data.rsi()
    l = len(data)
    RSI = data.iloc[l-1]
    print(RSI)
    return RSI

def crypto_price(symbol):
    url = 'https://fapi.binance.com/fapi/v1/trades?symbol=' + symbol + '&limit=' + '1'
    data = requests.get(url).json()
    price = data[-1]['price']
    print(price)
       
    return price
      
def crypto(update,context):
    
    name = update.message.chat.first_name
    crypto_lst = [BTCUSDT, ETHUSDT, USDTUSDT, BNBUSDT, DOGEUSDT]
    TOKEN = os.environ.get("TOKEN")
    bot = telebot.TeleBot(TOKEN)
    bot.config['api_key'] = TOKEN
    reply = update.message.text
    chat_id = update.message.chat.id
    users = os.environ.get("Users") # allowed users.
    allowed_chat_ids = users.split(",")
    allowed_chat_ids = map(int, allowed_chat_ids)
    time_window = 14
    r = reply.split(" ")
    symbol = r[0]
    print(r)
    tRSI = float(r[1])
    print(tRSI)
    RSI = c_rsi(symbol, time_window)
    print(RSI)
        
        
    if chat_id in allowed_chat_id:
        if symbol in crypto_lst:
            price = crypto_price(symbol)
            context.bot.send_message(chat_id, " The Price of " + symbol + " is " + price)
            
            if float(RSI) > tRSI:
                
                context.bot.send_message(chat_id, " The value of RSI for " + symbol + " is greater than the target value. The current value of RSI is " + str(RSI))
                
            elif float(RSI) < tRSI:
                
                context.bot.send_message(chat_id, " The value of RSI for " + symbol + " is less than the target value. The current value of RSI is " + str(RSI))
                
            else:
                
                context.bot.send_message(chat_id, " The value of RSI for " + symbol + " is equal to the target value. The current value of RSI is " + str(RSI))
                
        else:
            
            context.bot.send_message(chat_id, " You have entered the wrong crypto_currency")
            
    else:
        
        context.bot.send_message(chat_id, "Hi " + name + " You are not registered...")
            
def details(update,context):
    
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, update.message)

def error(update,context):
    
    chat_id = update.message.chat.id
    context.bot.send_message(chat_id, "The bot has encountered an error")
    
def main():
    
    
    TOKEN = os.environ.get("TOKEN")
    updater = Updater(token = TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, crypto))
    dp.add_handler(CommandHandler("details", details))
    dp.add_error_handler(error)
    
    updater.start_webhook(listen = "0.0.0.0", port = os.environ.get("PORT", 443),
                      url_path = TOKEN,
                      webhook_url  = "https://checkbot1.herokuapp.com/" + TOKEN)
    updater.idle()
    
if __name__ == '__main__':
    
    main()
