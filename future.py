from binance.futures import Futures
import pandas as pd
from telegram import telegramBotSendText as sendMessage
import time
id=5675598221
futuresClient = Futures("apiKey", "secretKey")

def futuresGetAllSymbols():
    response= futuresClient.exchange_info()
    return list(map(lambda symbol:symbol["symbol"],response["symbols"]))

futureUsdtList=[]
for coin in futuresGetAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin:
        futureUsdtList.append(coin)
    else:
        pass

def futuresKlinesCoin(coinName, period, limit=None):  #2 getting kline data
    kline = futuresClient.klines(symbol=str(coinName), interval=str(period), limit=str(limit))
    return kline

def futuresSymbolData(coinName:str,period:str,limit:int): #1 We entering coinName, period and interval.
    kline=futuresKlinesCoin(coinName=coinName,period=period,limit=limit)
    converted= pd.DataFrame(kline,columns=['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat', 'tbbav', 'tbqav',
                 'ignore'],dtype=float) #kline data is converting to dataframe.
    return converted




def futureTarama(coinList):
    gucluFutureAlis = []
    zayifFutureAlis = []
    while True:
        try:
            for coin in coinList:
                data = futuresSymbolData(coinName=coin, period="15m", limit=21)
                avrg= sum(data["vol"])/ len(data["vol"])
                vol= data["vol"]
                open= data["open"]
                close= data["close"]
                low= data["low"]
                high= data["high"]
                if vol[len(data.index)-2]> (avrg*1.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    gucluFutureAlis.append(coin)
                    #{ low[len(data.index) - 4]}")

                if vol[len(data.index)-2]< (avrg*0.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    zayifFutureAlis.append(coin)

        except :
            pass
        if len(gucluFutureAlis)!=0:
            sendMessage(f"Güçlü Future Alış Sinyali olan Coinler 💵 : {gucluFutureAlis}", id)
        else:
            pass
        if len(zayifFutureAlis)!=0:
            sendMessage(f"Zayıf Future Alış Sinyali Olan Coinler zort💵 : {zayifFutureAlis}", id)
        else:
            sendMessage("yok",id)
        gucluFutureAlis.clear()
        zayifFutureAlis.clear()
        time.sleep(900)

futureTarama(futureUsdtList)

