import requests, telegram, json
from bs4 import BeautifulSoup
from telegram.forcereply import ForceReply
from telegram.ext import Updater
from telegram.ext import CommandHandler
import apitelegram as api
import telebot

print("Bot Running ....")
updater = Updater(token=api.telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update,context):
    """Send a message when the command /start is issued."""
    global first
    first_name=update.message.chat.first_name
    last_name=update.message.chat.last_name
    update.message.reply_text('**** Selamat Datang! '+str(first_name)+' **** \n----------------------------------------------- \n          Informasi Penggunaan! \n----------------------------------------------- \n\n Untuk Melihat Harga di Indodax \n /pi + Token \n Contoh /pi doge \n\n Untuk Melihat Harga di Binance \n /pb + Token \n Contoh /pb doge \n\n Untuk Melihat Semua Harga /all \n\n /help untuk info lebih lanjut \n\n\n Developer By : @Jambal_co')
def help(update,context):
    update.message.reply_text('\n----------------------------------------------- \n          Informasi Penggunaan! \n----------------------------------------------- \n\n Untuk Melihat Harga di Indodax \n /pi + Token \n Contoh /pi doge \n\n Untuk Melihat Harga di Binance \n /pb + Token \n Contoh /pb doge \n\n Untuk Melihat Semua Harga /all \n\n /help untuk info lebih lanjut \n\n\n Developer By : @Jambal_co')
def indodax(update, context):
    chat_id = update.effective_chat.id
    pair = context.args[0]
    url_idx = "https://indodax.com/api/ticker"
    coin = f"{url_idx}/{pair}idr"
    response = requests.get(coin)

    if response.json().get("ticker"):
        price_idr = response.json().get("ticker").get("last")
        price_idr = "{:0,}".format(float(price_idr))
        high_idr = response.json().get("ticker").get("high")
        high_idr = "{:0,}".format(float(high_idr))
        low_idr = response.json().get("ticker").get("low")
        low_idr = "{:0,}".format(float(low_idr))
        text = f""" 
{pair.upper()}/IDR

❇️ Harga Di INDODAX (idr)

▶️ Harga Sekarang   : {price_idr} IDR

🕡 Harga Tertinggi : {high_idr} USDT

🕡 Harga Terendah  : {low_idr} USDT
    """
    else:
        text = f"{pair} Itu Koin apa ya ?!"
    context.bot.send_message(chat_id=chat_id, text=text)


def binance(update, context):
    chat_id = update.effective_chat.id
    koin = context.args[0]
    url_binance = "https://www.binance.com/fapi/v1/ticker/24hr?symbol="
    url_fix = url_binance + koin.upper() + "USDT"
    respons = requests.get(url_fix)

    if respons.json():
        symbol = respons.json().get("symbol")
        price = respons.json().get("lastPrice")
        change = respons.json().get("priceChangePercent")
        high = respons.json().get("highPrice")
        low = respons.json().get("lowPrice")
        kirim = f""" 
{koin.upper()}/USDT

❇️ Harga Di BINANCE (usdt)

▶️ Harga Sekarang   : {price} USDT

🕡 Presentase 24h    : {change} %

🕡 Harga Tertinggi   : {high} USDT

🕡 Harga Terendah  : {low} USDT
    """
    else:
        kirim = f"{koin} Itu Koin apa ya ?!"
    context.bot.send_message(chat_id=chat_id, text=kirim)


def get_prices():
    coins = ["BTC", "ETH", "XRP", "LTC", "BCH", "ADA", "DOT", "LINK", "BNB", "XLM"]

    crypto_data = requests.get(
        "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(",".join(coins))).json()["RAW"]

    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["USD"]["PRICE"],
            "change_day": crypto_data[i]["USD"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["USD"]["CHANGEPCTHOUR"]
        }

    return data

def all(update, context):
    chat_id = update.effective_chat.id
    message = ""

    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"""
❇️ Coin: {coin}/USD

▶️ Harga Sekarang: ${price:,.2f} USD

   Hour Change: {change_hour:.3f}%
   Day Change: {change_day:.3f}%
--------------------------------------------------
"""
    context.bot.send_message(chat_id=chat_id, text=message)






dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("pi", indodax))
dispatcher.add_handler(CommandHandler("pb", binance))


dispatcher.add_handler(CommandHandler("all", all))

dispatcher.add_handler(CommandHandler("help", help))

updater.start_polling()
updater.idle()

if __name__ == '__main__':
    main()