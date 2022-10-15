import requests
import telegram
import json
from telegram.forcereply import ForceReply
from telegram.ext import Updater
from telegram.ext import CommandHandler
import apitelegram as api
import telebot
import ccxt

print("Bot Running ....")
updater = Updater(token=api.telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    """Send a message when the command /start is issued."""
    global first
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    update.message.reply_text('**** Selamat Datang! '+str(first_name)+' **** \n----------------------------------------------- \n          Informasi Penggunaan! \n----------------------------------------------- \n\n Untuk Melihat Harga di Indodax \n /pi + Token \n Contoh /pi doge \n\n Untuk Melihat Harga di Binance \n /pb + Token \n Contoh /pb doge \n\n Untuk Melihat Semua Harga /all \n\n /help untuk info lebih lanjut \n\n\n Developer By : @Jambal_co')


def help(update, context):
    update.message.reply_text('\n----------------------------------------------- \n          Informasi Penggunaan! \n----------------------------------------------- \n\n Untuk Melihat Harga di Indodax \n /pi + Token \n Contoh /pi doge \n\n Untuk Melihat Harga di Binance \n /pb + Token \n Contoh /pb doge \n\n Untuk Melihat Semua Harga /all \n\n /help untuk info lebih lanjut \n\n\n Developer By : @Jambal_co')


def price(update, context):
    if len(context.args) > 0:
        market = context.args[0].upper()
        cryptoname = context.args[1]
        ticker2 = 'USDT'  # second ticker of the crypto pair

    # retrieving the # method from ccxt whose name matches the given exchange name
        method_to_call = getattr(ccxt, market.lower())
        exchange_obj = method_to_call()  # defining an exchange object
        pair_price_data = exchange_obj.fetch_ticker(
            cryptoname.upper()+'/'+ticker2)
        closing_price = pair_price_data['close']
        c = pair_price_data['percentage']
        if float(c) > 0 :
            icon = "💚"
        else:
            icon = "❤️"
        # print(pair_price_data)
        msg = f""" 
{icon} {icon} {icon}

Pair = {cryptoname.upper()}/{ticker2}
Market = {market}
Price = {closing_price}
Change = {c} %
    """
    else:
        msg = f"{cryptoname} Itu Koin apa ya ?!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def marketinfo(update, context):
    update.message.reply_text('\n--------------------------------------------------------- \n         AVAILABLE MARKET COMMANDS! \n--------------------------------------------------------- \n\n aax | alpaca | ascendex | bequant | bibox | bigone | binance | binancecoinm | binanceus | binanceusdm | bit2c | bitbank | bitbay | bitbns | bitcoincom | bitfinex | bitfinex2 | bitflyer | bitforex | bitget | bithumb | bitmart | bitmex | bitopro | bitpanda | bitrue | bitso | bitstamp | bitstamp1 | bittrex | bitvavo | bkex | bl3p | blockchaincom | btcalpha | btcbox | btcex | btcmarkets | btctradeua | btcturk | buda | bw | bybit | bytetrade | cex | coinbase | coinbaseprime | coinbasepro | coincheck | coinex | coinfalcon | coinmate | coinone | coinspot | crex24 | cryptocom | currencycom | delta | deribit | digifinex | eqonex | exmo | flowbtc | fmfwio | ftx | ftxus | gate | gateio | gemini | hitbtc | hitbtc3 | hollaex | huobi | huobijp | huobipro | idex | independentreserve | indodax | itbit | kraken | kucoin | kucoinfutures | kuna | latoken | lbank | lbank2 | liquid | luno | lykke | mercado | mexc | mexc3 | ndax | novadax | oceanex | okcoin | okex | okex5 | okx | paymium | phemex | poloniex | probit | qtrade | ripio | stex | therock | tidebit | tidex | timex | tokocrypto | upbit | wavesexchange | wazirx | whitebit | woo | yobit | zaif | zb | zipmex | zonda')


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("price", price))
dispatcher.add_handler(CommandHandler("market", marketinfo))

dispatcher.add_handler(CommandHandler("help", help))

updater.start_polling()
updater.idle()

if __name__ == '__main__':
    main()
