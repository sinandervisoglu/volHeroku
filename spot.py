from binance.futures import Futures as futuresClient
from binance.spot import Spot as Client
import pandas as pd
from telegram import telegramBotSendText as sendMessage
import time
id=5675598221
spot_client=Client("apiKey","secretKey")
futures_client = futuresClient("apiKey", "secretKey")

#borsa verileri
def exchangeInfo(coinName:str ):
    exc=spot_client.exchange_info(symbol=str(coinName))
    return exc

#mum verileri:
def spotKlinesCoin(coinName:str ,period:str, limit: int=None):
    kline=spot_client.klines(symbol=str(coinName),interval=str(period),limit=limit)
    return kline

def spotAllSymbols():
    response=spot_client.exchange_info()
    return list(map(lambda symbol:symbol["symbol"],response["symbols"]))

spotUsdtList=[]
for coin in spotAllSymbols():
    if "USDT" in coin and "UP" not in coin and "DOWN" not in coin:
        spotUsdtList.append(coin)
    else:
        pass

def spotsymbolsData(coinName:str,period:str,limit:int):
    kline=spotKlinesCoin(coinName=coinName,period=period,limit=limit)
    converted=pd.DataFrame(kline,columns=['open_time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'nat',
                                      'tbbav', 'tbqav',
                                      'ignore'], dtype=float)
    return converted

def spotTarama(coinList):
    gucluSpotAlis = []
    zayifSpotAlis = []
    while True:
        try:
            for coin in coinList:
                data = spotsymbolsData(coinName=coin, period="15m", limit=21)
                avrg= sum(data["vol"])/ len(data["vol"])
                vol= data["vol"]
                open= data["open"]
                close= data["close"]
                low= data["low"]
                high= data["high"]

                if vol[len(data.index)-2]> (avrg*1.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    gucluSpotAlis.append(coin)
                #gucluSpotAlis.append(f"{coin} için tavsiye edilen TP = {(high[len(data.index)-2])+ (high[len(data.index)-2]*2.5)/100}\nTavsiye edilen SL= {(low[len(data.index) - 3])- (low[len(data.index)-3]*0.5)/100 }\n\n")

                if vol[len(data.index)-2]< (avrg*0.5) and close[len(data.index)-2]> open[len(data.index)-2] and open[len(data.index) - 2] == low[len(data.index) - 2] and open[len(data.index) - 3] > close[len(data.index) - 3]:
                    zayifSpotAlis.append(coin)
                    #zayifSpotAlis.append(f"{coin} için tavsiye edilen TP = {(high[len(data.index)-2])+ (high[len(data.index)-2]*3)/100}\nTavsiye edilen SL= {(lo+w[len(data.index) - 3])- (low[len(data.index)-3]*0.5)/100}\n\n ")

        except :
            pass
        if len(gucluSpotAlis)!=0:
            sendMessage(f"Güçlü Spot Alış Sinyali Olan Coinler 💵 : {gucluSpotAlis}", id)
        else:
            pass
        if len(zayifSpotAlis)!=0:
            sendMessage(f"Zayıf Spot Alış Sinyali Olan Coinler 💵 : {zayifSpotAlis}", id)
        else:
            pass
        gucluSpotAlis.clear()
        zayifSpotAlis.clear()
        time.sleep(900)

spotTarama(spotUsdtList)