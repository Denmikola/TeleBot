import json
import requests
from app import app

def zapros_f(region, firstname, lastname):
    if 'TOKEN_PRISTAV' not in app.config or not app.config['TOKEN_PRISTAV']:
        return ('Ошибка: netu tokena dlia pristavov')
    token =  app.config['TOKEN_PRISTAV']
    req = requests.get('https://api-ip.fssprus.ru/api/v1.0'
                     '/search/physical?region={}&firstname={}&lastname={}&token={}'.format(
                         region, firstname, lastname,token))
    if 299 < req.status_code < 400 : return ('Какой-то глюк с маршрутизацией',req.status_code)
    elif 399 < req.status_code < 500 : return ('Ошибка в параметрах запроса',req.status_code)
    elif req.status_code >= 500 : return ('Нет ответа сервера',req.status_code)
    elif req.status_code == 200 : r=req.json()
    else : return (req.status_code)   
    if r['status'] == 'success' : 
        return (r['response']['task'])
    else : 
        return (r['exception'] )

def zapros_f_s(task):
    if 'TOKEN_PRISTAV' not in app.config or not app.config['TOKEN_PRISTAV']:
        return ('Ошибка: netu tokena dlia pristavov')
    token =  app.config['TOKEN_PRISTAV']
    req = requests.get('https://api-ip.fssprus.ru/api/v1.0/status?task={}&token={}'.format(
                         task,token))
    if req.status_code == 200 : 
       r=req.json()
       return (r['response']['progress'])
    else : return (' Ошибка ',req.status_code)
       
def zapros_f_r(task):
    if 'TOKEN_PRISTAV' not in app.config or not app.config['TOKEN_PRISTAV']:
        return ('Ошибка: netu tokena dlia pristavov')
    token =  app.config['TOKEN_PRISTAV']
    req = requests.get('https://api-ip.fssprus.ru/api/v1.0/result?task={}&token={}'.format(
                         task,token))
    if req.status_code == 200 : 
       r=req.json()
       return (r['response']['result'][0])
    else : return ('Ошибка ',req.status_code)

