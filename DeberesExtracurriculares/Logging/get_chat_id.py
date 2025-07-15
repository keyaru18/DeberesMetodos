import requests

TOKEN = '7782114763:AAG95EeBfC6Wd7rSEa88cidvMCTX9lkBQUE'
URL = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
response = requests.get(URL)
print(response.json())
#-1002513850512