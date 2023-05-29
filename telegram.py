import requests

def telegramBotSendText(botMessage,id):
    botToken="6070522686:AAEtYoImDUpyOyWl2JiHrWD6GsuDdg2qEZQ" #BotFather'!
    url="https://api.telegram.org/bot"+botToken+"/sendMessage?chat_id="+str(5675598221)+"&parse_mode=Markdown&text="+botMessage
    response=requests.get(url)
    return response.json()