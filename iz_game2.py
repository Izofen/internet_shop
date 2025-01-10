

def connect_postgres ():  
    import psycopg2
    db = psycopg2.connect(dbname='main', user='postgres', password='podkjf4', host='localhost')
    cursor = db.cursor()       
    return db,cursor 


def gos_avto (message_info):
    import iz_bot
    message_in  = message_info.setdefault('message_in','')
    user_id     = message_info.setdefault('user_id','')
    setting     = iz_bot.get_setting (message_info)
    token       = setting.setdefault ('Токен','')
    setting     = iz_bot.get_setting_prog  ('Гос. номер')
    print ('[+] setting:',setting)
    message_out = setting['message_out']
    db,cursor  = connect_postgres ()
    sql = "SELECT id,info,about FROM master_gosnomer WHERE name = '{}'".format(message_in)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records: 
        import requests    
        id,info,about = row
        print ('[+] origin:',id,info)
        message_out = message_out.replace ('##Ответ##',str(info))
        method = "sendMessage"
        params = {}
        params['chat_id'] = user_id                  
        params['text'] = message_out
        params['parse_mode'] = 'HTML'
        url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
        resp = requests.post(url, params) 
        answer = resp.json()
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ( answer)
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ('')
        
        if about != None:
            message_out = about
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
            print ( answer)
            print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
            print ('')
                
        
        