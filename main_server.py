#!/usr/bin/python
# -*- coding: utf-8

from flask import Flask
from flask import request
app = Flask(__name__)

from threading import Thread

def connect ():
    import psycopg2
    db = psycopg2.connect(dbname='main', user='postgres', password='podkjf4', host='127.0.0.1')
    cursor = db.cursor()
    return db,cursor

def connect_mysql (namebot): 
    import pymysql
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()  
    return db,cursor
       
def update_key (name_key1,name_key2,key11,data_id,namebot):
    db,cursor = connect (namebot)     
    id = 0
    sql = "select id,data_id from menu  where name = '{}' and data_id = {} limit 1;".format (name_key1,data_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name  =  rec.values()    
    if id == 0:
        sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format (name_key1,data_id,key11,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit()            
    else:    
        sql = "UPDATE menu SET `info` = '{}' WHERE name = '{}' and data_id = {} ".format (key11,name_key1,data_id)
        sql_save = ()
        cursor.execute(sql,sql_save)  
        db.commit()      
    id = 0
    sql = "select id,data_id from menu  where name = '{}' and data_id = {} limit 1;".format (name_key2,data_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name  =  rec.values()    
    if id == 0:
        sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format (name_key2,data_id,key11,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit()            
    else:    
        sql = "UPDATE menu SET `info` = '{}' WHERE name = '{}' and data_id = {} ".format (key11,name_key2,data_id)
        sql_save = ()
        cursor.execute(sql,sql_save)  
        db.commit()      

def connect_postgs ():
    import psycopg2
    db = psycopg2.connect(dbname='main', user='postgres', password='podkjf4', host='localhost')
    cursor = db.cursor()       
    return db,cursor

class start_bot (Thread):
    def __init__(self,message_info):
        Thread.__init__(self)
        self.message_info            = message_info
        
    def run(self):
        message_info                 = self.message_info
        namebot    = message_info.setdefault('namebot','')
        namebot    = namebot.replace("@","")
        #print ('[+] namebot:',namebot)
        mycode = 'import start_{}'.format (namebot)
        exec(mycode)        
        mycode = 'start_{}.start_prog (message_info)'.format(namebot)
        exec(mycode)

class grup_bot (Thread):
    def __init__(self,username,message_info):
        Thread.__init__(self)
        self.message_info        = message_info
        self.username            = username
        
    def run(self):
        message_info                 = self.message_info
        username                     = self.username
        namebot    = message_info.setdefault('namebot','')
        namebot    = namebot.replace("@","")
        try:
            print ('[+] username:',username)
            mycode = 'import start_{}'.format (username)
            exec(mycode)        
            mycode = 'start_{}.start_prog (message_info)'.format(username)
            exec(mycode)
        except:
            pass            

def get_id ():
    import iz_bot
    db,cursor = iz_bot.connect_postgres ()
    sql = "select id,name,text,picture,chat,file from public_news where 1=1 order by id desc limit 1".format ()
    cursor.execute(sql)
    results = cursor.fetchall() 
    db.close ()   
    id = 0
    for row in results:
        id,name,text,picture,user_id,filesend = row
    return id
                     
@app.route('/telegram/<access_code>/<namebot>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def telegram (access_code,namebot):     ### 
    import iz_general
    import iz_bot
    import time
    print ('[+] namebot:',namebot)
    if namebot == '@VK314_bot':
        return {"ok": False}
    if request.method == "POST":
        parsed_string = request.json        
        message_info = iz_general.parsed_string (parsed_string)  
        if message_info.setdefault('sender_chat_username','')  != '':  
            import requests
            import json
            user_id = -1001644105615
            message_out = 'Проверка работы системы'
            token       = '6422168947:AAGy4pzndN1WYgMyFRf_mVXF6gEptDpzLz0'
            method      = "editMessageText"
            import iz_bot
            db,cursor = iz_bot.connect ('bot_main') 
            sql = "select id,key01,key02,key03,key_press01,key_press02,key_press03 from key_message where name = 'Тестовая кнопка' limit 1"
            cursor.execute(sql)
            results = cursor.fetchall()        
            for row in results: 
                id,key01,key02,key03,key_press01,key_press02,key_press03 = row.values()            
            if str(message_info['callback'].find ('i_')) != -1:
                import json
                import requests
                json_string  = iz_bot.change_back(message_info['callback'].replace('i_',''))
                data_json = json.loads(json_string)
                operation = data_json.setdefault('o','')
                nomer     = data_json.setdefault('p','')  
                key_pres  = data_json.setdefault('k','') 
                print ('    [+] operation:',operation)    
                print ('    [+] nomer    :',nomer)    
            if operation == 'grup':
                if key_pres == 1:
                    sql = "UPDATE key_message SET key_press01 = key_press01 + 1 WHERE name = 'Тестовая кнопка' ".format ()
                    sql_save = ()
                    cursor.execute(sql,sql_save)
                    db.commit()
                if key_pres == 2:
                    sql = "UPDATE key_message SET key_press02 = key_press02 + 1 WHERE name = 'Тестовая кнопка' ".format ()
                    sql_save = ()
                    cursor.execute(sql,sql_save)
                    db.commit()
            sql = "select id,key01,key02,key03,key_press01,key_press02,key_press03 from key_message where name = 'Тестовая кнопка' limit 1"
            cursor.execute(sql)
            results = cursor.fetchall()        
            for row in results: 
                id,key01,key02,key03,key_press01,key_press02,key_press03 = row.values()
                line = []
                line1  = []
                key11  = {}
                key11['text']          =  str(key01) + ' ' + str(key_press01)
                key11['callback_data'] =  iz_bot.build_jsom({"o":'grup',"p":id,"k":1})
                key12  = {}
                key12['text']          =  str(key02) + ' ' + str(key_press02)
                key12['callback_data'] =  iz_bot.build_jsom({"o":'grup',"p":id,"k":2})
                key13  = {}
                line1.append(key11)
                line1.append(key12)
                #line1.append(key13)
                line.append(line1)    
                array = {"inline_keyboard":line}  
                markup = json.dumps(array)            
                params = {}
                params['chat_id'] = user_id                  
                params['text'] = message_out
                params['parse_mode'] = 'HTML'
                params['message_id'] = message_info['message_id']
                #if menu_name != '' or key_array != '':
                params['reply_markup'] = markup      
                #    print ('[markup]:',markup)                
                url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
                resp = requests.post(url, params) 
                answer = resp.json()
                print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
                print ( answer)
                print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
                print ('')        
        db,cursor   = iz_bot.connect (namebot)         
        message_in   = message_info.setdefault('message_in')
        message_new  = message_info.setdefault('message_in',message_in)        
        message_in   = message_in.replace('\\','')
        sql = 'select id,name,info,data_id from menu where name like %s and info = %s ;'.format ()
        sql_save = ('Замена%',message_in)
        cursor.execute(sql,sql_save)
        results = cursor.fetchall()    
        for row in results:
            id,name,info,data_id = row.values()
            name_new = name.replace("Замена ","")
            sql = "select id,name,info from menu where  data_id = {} and name = 'Кнопка {}';".format (data_id,name_new)
            cursor.execute(sql)
            results = cursor.fetchall()    
            for row in results:
                id,name,info = row.values() 
            message_new = info
        message_info['message_in']   = message_new 
        message_info['message_old']  = message_in 
        message_info['namebot']      = namebot 
        if message_in == '/message_test':
            print ('[+]                         [+]')
            send_data = {'Text':'Отправка проверочного сообщения'}
            iz_bot.send_message (message_info,send_data)        
        print ('[+]🌹--------------------------------------------------------------- [message_info] -------------------------------------------------------🌹[+]')
        print (message_info)
        print ('[+]🌹--------------------------------------------------------------- [message_info] -------------------------------------------------------🌹[+]')
        print ('')
        #db,cursor = connect ()
        #sql = "INSERT INTO log_bot (namebot,user_id,unixtime,message_in,message_out,status,data_in,data_out) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format ()
        #from datetime import datetime
        #str_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #sql_save = (namebot,user_id,int(time.time ()),str(message_in),'','',str(str_date),'')
        #result = cursor.execute(sql,sql_save)
        #db.commit()    
        #lastid = cursor.lastrowid
        #message_info['data_id'] = lastid
        
        
        
        FIO_id = iz_bot.save_FIO (message_info)
        send_data = {'Автомат':'Да'}
        iz_bot.send_message (message_info,send_data) 
        my_thread = start_bot (message_info)
        my_thread.start()
        print ('[+] --------------------------------------------------- [Запуск отдельного потока] ---------------------------------------------------------')    

        callback_query  = parsed_string.setdefault('callback_query','')
        if callback_query != '':
            message         = callback_query.setdefault('message',{})
            chat            = message.setdefault('chat',{})
            chat            = message.setdefault('chat',{})
            username        = chat.setdefault('username',{})
            my_thread = grup_bot (username,message_info)
            my_thread.start()
            
        if message_new == '/about':
            db,cursor = connect ()
            sql = "select id,name,info from about where 1=1 limit 1;".format ()  #### and status <> 'resolved'       
            cursor.execute(sql)
            results = cursor.fetchall() 
            info = ""
            for row in results:
                id,name,info = row
                
            send_data = {"Text":info,'Запись в базу':'Не записывать'}
            iz_bot.send_message (message_info,send_data)
            
        
        
    return {"ok": True}

@app.route('/vk_crisp/', methods=["GET", "POST"])   ### 
def vk_crisp ():   ### 
    print ('[vk_crisp]:',vk_crisp)
    namebot = "TEST"
    user_id = "TEST"
    message = "TEST"
    #import iz_func
    #import iz_vk
    from flask import request
    if request.method == "POST":
        print ('[+]----vk_crisp 1.100--------------------------------------------------------------[+]')
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')        
        parsed_string   = request.json
        website_id_main   = parsed_string.setdefault('website_id','')
        event_main        = parsed_string.setdefault('event','')
        if event_main == 'message:send':
             return 'ok'
        data_main         = parsed_string.setdefault('data','')    
        website_id        = data_main.setdefault('website_id','')
        type_t            = data_main.setdefault('type','')
        from_t            = data_main.setdefault('from','')
        origin            = data_main.setdefault('origin','')
        content           = data_main.setdefault('content','')
        fingerprint       = data_main.setdefault('fingerprint','')
        user              = data_main.setdefault('user','')
        nickname_user     = ''
        nickname_user_id  = ''
        if user != '':
            nickname_user     = user.setdefault('nickname','')
            nickname_user_id  = user.setdefault('user_id','')        
        mentions          = data_main.setdefault('mentions','')
        timestamp         = data_main.setdefault('timestamp','')
        stamped           = data_main.setdefault('stamped','')
        session_id        = data_main.setdefault('session_id','')
        print ('[+] website_id_main:',website_id_main)
        print ('[+] event_main:',event_main)
        print ('[+] data_main',data_main)
        print ('[+] data_main',type(data_main))
        print ('[+] user:',user)
        print ('[+] nickname_user:',nickname_user)
        print ('[+] nickname_user_id:',nickname_user_id)
        print ('[+] session_id:',session_id)
        print ('[+] content:',content)
        message_out = content;
        base = "crisp"
        import pymysql
        db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
        cursor = db.cursor()   
        sql = "select id,name,user_id,mesage_in from session where session_id = '{}'  limit 1;".format (session_id)  #### and status <> 'resolved'       
        cursor.execute(sql)
        results = cursor.fetchall()    
        user_id_i = 0
        id_i = 0
        for row in results:
            id_i,name_i,user_id_i,mesage_in_i = row.values() 
            print ('[+] id_i',id_i,name_i,user_id_i,mesage_in_i)
        user_id = user_id_i
        if str(message_out).find ('state:resolved') != -1:
            sql = "UPDATE session SET status = '{}' WHERE id  = '{}'".format ('resolved',id_i)
            cursor.execute(sql)
            db.commit()
        if message_out != '' and user_id != 0 and str(message_out).find ('state:resolved') == -1 :
            print ('    [+] message_out:',message_out)    
            print ('    [+] user_id:',user_id)    
            import vk_api
            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
            from vk_api.utils import get_random_id  
            apikey_avtor = 'vk1.a.2mtlxCdi94HCl_o58vujcLqJEqn4bRamn8LJ4h-eJaVqtllvkfIg8ngj0AJX6OMrNVBn0w0ggFNGAB--JmPz0oYJ4hf4n48P91oM2KOb86st1cPE7jqOqE5HW0sO5d0JJtlhXlmG0oTHG3xRqJvj06oXqqf006nluEfj3pu3NrGSA1boxVtHUoNX8d-ytjPvrIWRUKspSrvBn5aiyreQnw'
            vk_session = vk_api.VkApi(token=apikey_avtor)
            vk = vk_session.get_api() 
            vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out)
            sql = "UPDATE session SET message_out = '{}' WHERE id  = '{}'".format (message_out,id_i)
            cursor.execute(sql)
            db.commit()
    return 'ok'

@app.route('/vkmessage/', methods=["GET", "POST"])   ### 
def vkmessage ():   ### 
    namebot = "TEST"
    user_id = "TEST"
    message = "TEST"
    import iz_vk
    from flask import request
    if request.method == "POST":
        print ('[+]----VK 1. 224--------------------------------------------------------------[+]')
        print (request.json)
        print ('[+]--------------------------------------------------------------------------[+]')        
        parsed_string   = request.json
        type_message = parsed_string['type']
        group_id     = parsed_string['group_id']
        event_id = parsed_string.setdefault('event_id','')  
        try:
            message  = parsed_string['object']['message']['text']        
        except:    
            message  = ''
        try:
            user_id  = parsed_string['object']['message']['peer_id']        
        except:    
            user_id  = ''
        print ('[+] user_id:',user_id)
        print ('[+] message:',message)
        print ('[+] event_id:',event_id)
        print ('[+] group_id:',group_id)
        print ('[+] type_message:',type_message)
        import pymysql 
        connect_info = {'host':'127.0.0.1','user':'izofen','password':'podkjf4','database':'vk_'+str(group_id)}
        print ('[+] connect_info:',connect_info)
        try:
            db = pymysql.connect(host=connect_info['host'],user=connect_info['user'],password=connect_info['password'],database=connect_info['database'],charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
            cursor = db.cursor() 
        except:
            return 'error'
        sql = "select id from event where name = '{}' limit 1".format (event_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        id = 0
        for row in results:
            id = row['id']
        if id == 0:
            sql = "INSERT INTO event (`name`) VALUES ('{}')".format (event_id)
            cursor.execute(sql)
            db.commit()
        event_id = id
        if type_message == 'message_new' and id == 0: 
            import vk_api
            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
            from vk_api.utils import get_random_id  
            info = ""    
            sql = "select id,info,data_id from setting where name = 'Токен' "
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,info,data_id = rec.values() 
            if info != "":
                apikey_avtor = info
            vk_session = vk_api.VkApi(token=apikey_avtor)
            vk = vk_session.get_api()  
            info = "нет сообщения"    
            sql = "select id,info,data_id from setting where name = 'Нет сообщения' "
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,info,data_id = rec.values() 
                message_out_min = info
                message_out     = info
            kb = ''    
            if message != '': 
                sql = "select id,info,data_id from message where name = 'Имя' and info = '{}' ".format (message)
                cursor.execute(sql)
                data = cursor.fetchall()
                data_id = 0
                for rec in data: 
                    id,info,data_id = rec.values() 
                message_info = {}    
                if data_id != 0:    
                    sql = "select id,name,info,data_id from message where data_id = {} ".format (data_id)
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    for rec in data: 
                        id,name,info,data_id = rec.values() 
                        message_info[name] = info                    
                    message_out  = message_info.setdefault('Текст',message_out_min)                    
                    message_menu = message_info.setdefault('Меню','')
                    if message_menu != '':
                        sql = "select id,info,data_id from menu where name = 'Имя' and info = '{}' ".format (message_menu)
                        cursor.execute(sql)
                        data = cursor.fetchall()
                        data_id = 0
                        for rec in data: 
                            id,info,data_id = rec.values() 
                        menu_info = {}    
                        if data_id != 0:    
                            sql = "select id,name,info,data_id from menu where data_id = {} ".format (data_id)
                            cursor.execute(sql)
                            data = cursor.fetchall()
                            for rec in data: 
                                id,name,info,data_id = rec.values() 
                                menu_info[name] = info 
                            kb = 'Ok'
                            from vk_api.keyboard import VkKeyboard, VkKeyboardColor
                            keyboard = VkKeyboard(one_time=True)
                            if menu_info.setdefault('Кнопка 11','') != '':        
                                if menu_info.setdefault('Цвет 11','') == 'Белый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 11',''), color=VkKeyboardColor.SECONDARY)
                                if menu_info.setdefault('Цвет 11','') == 'Зеленый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 11',''), color=VkKeyboardColor.POSITIVE)
                            if menu_info.setdefault('Кнопка 12','') != '' :                                             
                                if menu_info.setdefault('Цвет 12','') == 'Белый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 12',''), color=VkKeyboardColor.SECONDARY)
                                if menu_info.setdefault('Цвет 12','') == 'Зеленый':                             
                                    keyboard.add_button(menu_info.setdefault('Кнопка 12',''), color=VkKeyboardColor.POSITIVE)
            if kb != '':
                vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out,keyboard=keyboard.get_keyboard()) 
            else:    
                vk.messages.send(peer_id=user_id,random_id=get_random_id(),message=message_out) 
    return 'ok'
 
@app.route('/cripta_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def cripta_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)
        
        if command == 'Крипта : Получить билет fetchOHLCV':
            import iz_exchanges
            exchange    = info.setdefault('exchange','')
            pair        = info.setdefault('pair','') 
            timeframes  = info.setdefault('timefraim','') 
            limit       = info.setdefault('limit',1) 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+] timeframes :',timeframes)
            print ('[+] limit      :',limit)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchOHLCV (exchange,pair,timeframes,limit)
            print ('    [answer]',answer)
            return answer
            
        if command == 'Крипта : Получить список криптобирж':
            import iz_exchanges
            answer = iz_exchanges.exchanges_myexchange ()
            print ('    [answer]',answer)
            return answer
            
        if command == 'Крипта : Получить список инструментов fetchMarkets':    
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchMarkets (exchange)
            print ('    [answer]',answer)
            return answer            

        if command == 'Крипта : Получить баланс':  
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            spot     = info.setdefault('spot','spot')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] spot       :',spot)
            print ('[+]-----------------------------------[+]')
            answer = iz_exchanges.exchanges_fetchBalance (exchange,apiKey,secret,spot)
            print ('    [answer]',answer)                 
            return answer     
            
        if command == 'Крипта : Создать фьючерный ордер на покупку': ##long
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            amount   = info.setdefault('amount','')
            pair     = info.setdefault('pair','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] amount     :',amount)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')            
            answer = iz_exchanges.create_market_order_long (exchange,apiKey,secret,pair,amount)
            print ('    [answer]',answer)                   
            return answer  
            
        if command == 'Крипта : Создать фьючерный ордер на продажу': ##short
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')   
            amount   = info.setdefault('amount','')
            pair     = info.setdefault('pair','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] amount     :',amount)
            print ('[+] pair       :',pair)   
            print ('[+]-----------------------------------[+]')            
            answer = iz_exchanges.create_market_order_short (exchange,apiKey,secret,pair,amount)
            print ('    [answer]',answer)                    
            return answer  
            
        if command == 'Крипта : Выставить плечо':  
            import iz_exchanges
            exchange  = info.setdefault('exchange','')
            apiKey    = info.setdefault('apiKey','')
            secret    = info.setdefault('secret','')   
            leverage  = info.setdefault('leverage',0)  
            pair      = info.setdefault('pair','')
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+] leverage   :',leverage)
            print ('[+] pair       :',pair)   
            print ('[+]-----------------------------------[+]')                        
            answer = iz_exchanges.set_leverage (exchange,apiKey,secret,pair,leverage)
            print ('    [answer]',answer)
            return answer     

        if command == 'Крипта : Получить позиции':  
            import iz_exchanges
            exchange  = info.setdefault('exchange','')
            apiKey    = info.setdefault('apiKey','')
            secret    = info.setdefault('secret','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetch_positions (exchange,apiKey,secret)
            print ('    [answer]',answer)
            return answer     
           
        if command == 'Крипта : Получить load_markets':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+]-----------------------------------[+]')                         
            answer = iz_exchanges.exchanges_loadMarkets (exchange)
            print ('    [answer]',answer)
            return answer      
                        
        if command == 'Крипта : Получить OrderBook':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')                         
            answer = iz_exchanges.exchanges_fetchOrderBook (exchange,pair)
            print ('    [answer]',answer)
            return answer  
            
        if command == 'Крипта : Получить OrderBook':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')          
            answer = iz_exchanges.exchanges_fetchOrderBook (exchange,pair)
            print ('    [answer]',answer)
            return answer  

        if command == 'Крипта : Создать лимитный ордер на покупку':
            import iz_exchanges
            exchange    = info.setdefault('exchange','')  
            apiKey      = info.setdefault('apiKey','')
            secret      = info.setdefault('secret','')  
            pair        = info.setdefault('pair','')              
            amount      = info.setdefault('amount','')
            price       = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_createLimitBuyOrder (exchange,apiKey,secret,pair,amount,price)
            print ('    [answer]',answer)
            return answer  

        if command == 'Крипта : Создать лимитный ордер на продажу':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')              
            amount   = info.setdefault('amount','')
            price    = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_createLimitSellOrder (exchange,apiKey,secret,pair,amount,price)
            print ('    [answer]',answer)
            return answer  
         
        if command == 'Крипта : Список выставленных ордеров':
            import iz_exchanges
            exchange   = info.setdefault('exchange','')  
            apiKey     = info.setdefault('apiKey','')
            secret     = info.setdefault('secret','')  
            pair       = info.setdefault('pair','')              
            amount     = info.setdefault('amount','')
            price      = info.setdefault('price','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] amount     :',amount)
            print ('[+] price      :',price)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetchOpenOrders (exchange,apiKey,secret,pair)
            print ('    [answer]',answer)
            return answer  
            
        if command == 'Крипта : Показать статус ордера':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')              
            ID       = info.setdefault('ID','')             
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] ID         :',ID)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_fetchOrder (exchange,apiKey,secret,pair,ID)
            print ('    [answer]',answer)
            return answer             
              
        if command == 'Крипта : Удалить выставленный ордер':
            import iz_exchanges
            exchange = info.setdefault('exchange','')  
            apiKey   = info.setdefault('apiKey','')
            secret   = info.setdefault('secret','')  
            pair     = info.setdefault('pair','')    
            ID       = info.setdefault('ID','')            
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] apiKey     :',apiKey)
            print ('[+] secret     :',secret)            
            print ('[+] pair       :',pair)
            print ('[+] ID         :',ID)
            print ('[+]-----------------------------------[+]')             
            answer = iz_exchanges.exchanges_cancelOrder (exchange,apiKey,secret,ID,pair)
            print ('    [answer]',answer)
            return answer             
                  
        if command == 'Крипта : Цена покупки':
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')              
            answer = iz_exchanges.exchanges_ask (exchange,pair)
            print ('    [answer]',answer)
            return answer    

        if command == 'Крипта : Цена продажи': 
            import iz_exchanges
            exchange = info.setdefault('exchange','')
            pair     = info.setdefault('pair','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] exchange   :',exchange)
            print ('[+] pair       :',pair)
            print ('[+]-----------------------------------[+]')              
            answer = iz_exchanges.exchanges_bid (exchange,pair)
            print ('    [answer]',answer)
            return answer            
        return 'API'    

@app.route('/vk_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def vk_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)

        if command == 'Боты : Получить users':
            import pymysql
            import json
            where    = info.setdefault('Условия','')                
            namebot = 'vk'            
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "select * from user_vk where "+str(where)+"".format ()
            cursor.execute(sql)
            data = cursor.fetchall()  
            json_string = json.dumps(data)
            return json_string
            
@app.route('/site_command/<access_code>/<command>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def site_command (access_code,command):     ###
    import iz_bot
    import pymysql
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = 'A123_site',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    info = "Нет данных"
    id = 0
    sql = "select id,name,info from A_service where name = 'Задание' ORDER BY id DESC limit 1;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values() 
    element = {}    
    sql = "select id,name,info from A_service where data_id = {};".format (id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values()
        element[name] = info    
        print ('[+] id,name,info',id,name,info)    
    answer = 'OK'
    namebot = '@'+str(element['Отправитель'])
    user_id = str(element['Получатель'])
    text    = str(element['Текст отправки'])
    send_data = {"Text":text,'Замена':[]}
    message_info = {'namebot':namebot,'user_id':user_id}
    answer = iz_bot.send_message (message_info,send_data)      
    return str(answer)

@app.route('/send_1c/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def send_1c (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        print ('[parsed_string]:',parsersring) 
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('[+] command:',command)

        if command == '1С : Информация':
            import requests
            user_id     = info.setdefault('user_id','399838806')
            token       = info.setdefault('token','6988761810:AAHsyODYS5qrJSmjbxaJs6JuAR0y2auZaYQ')
            message_out        = info.setdefault('message_out','test')  
            print ('[+] user_id',user_id)
            print ('[+] text',message_out)
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            return str(answer)
            
        if command == '1С : Старт системы':
            import requests
            user_id     = info.setdefault('user_id','399838806')
            token       = info.setdefault('token','6988761810:AAHsyODYS5qrJSmjbxaJs6JuAR0y2auZaYQ')
            message_out         = info.setdefault ('message_out','test')  
            message_name        = info.setdefault('message_name','test')  
            print ('[+] user_id',user_id)
            print ('[+] text',message_out)
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            return str(answer)            

@app.route('/bot_command/<access_code>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def bot_command (access_code):     ### 
    if request.method == "POST":
        parsersring = request.json 
        print ('[parsersring]',parsersring)
        info     = parsersring.setdefault('Информация','')
        command  = parsersring.setdefault('Команда','')        
        print ('    [Команда]    :',command)
        print ('    [Информация] :',info)
 
 
        if command == "Управление : Создать telegraph Сайт":
            html_content = info.setdefault('html_content','')
            title        = info.setdefault('title','')
            short_name   = info.setdefault('short_name','')
            name         = info.setdefault('name','site')
            #import requests
            from telegraph import Telegraph
            telegraph = Telegraph()
            result=telegraph.create_account(short_name=short_name)
            print (result)
            ##{'short_name': '1337', 
            ##'author_name': '', 
            ##'author_url': '', 
            ##'access_token': 'ec647c3494b4178ef303db3f9b5b6f5a55f38aec6fa4eab209e5a7c5fc00', 
            ##'auth_url': 'https://edit.telegra.ph/auth/TssMFEMezFTLTleCRfu9ZmvAEYbhHNuydUkQx644KV'}
            telegraph = Telegraph(result['access_token']) # передаём токен доступ к страницам аккаунта
            response = telegraph.create_page(title,html_content=html_content) # ставим параметр html_content, добавляем текст страницы
            print ('[response]',response)
            print('https://telegra.ph/{}'.format(response['path'])) # распечатываем адрес страницы
            answer = 'https://telegra.ph/{}'.format(response['path'])
            db,cursor = connect_postgs ()
            sql = "INSERT INTO telegraph (name,response,result,status,html_content,title,short_name) VALUES (%s,%s,%s,%s,%s,%s,%s)".format ()
            sql_save = (name,str(response),str(result),'',html_content,title,short_name)
            cursor.execute(sql,sql_save)
            db.commit()
            return answer 
 
        if command == 'Управление : Записать текстовое сообщение':
            name1 = info.setdefault('name1','')
            name2 = info.setdefault('name2','')
            message1 = info.setdefault('message1','')
            message2 = info.setdefault('message2','')
            menu1 = info.setdefault('menu1','')
            menu2 = info.setdefault('menu2','')
            namebot  = info.setdefault('namebot','')
            picture  = info.setdefault('picture','нет')
            status1 = ""
            status2 = "Дополнительное"
            namebot1  = 'orenlkip_bot'
            namebot2  = 'orenlkip_bot'
            db,cursor = connect ()
            sql         = "INSERT INTO send_message (answer,menu,message,message_id,name,namebot,picture,status,task,user_id,wait) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            sql_save    = ("",menu1,message1,0,'Первое сообщение',namebot,picture,'',0,'',5)            
            cursor.execute(sql,sql_save)
            db.commit()
            lastid = cursor.lastrowid
            sql         = "INSERT INTO send_message (answer,menu,message,message_id,name,namebot,picture,status,task,user_id,wait) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            sql_save    = ("",menu2,message2,lastid,'Второе сообщение',namebot,'','Дополнительное',lastid,'',5)
            cursor.execute(sql,sql_save)
            db.commit()
            json_string = "OK"
            return str(json_string) 
            
        if command == 'Управление : Получить ссылки на картинки':  
            db,cursor = connect_postgs ()
            sql = "select id,url_picture,code,name from torrent where url_picture <> '';".format ()
            cursor.execute(sql)
            data = cursor.fetchall()
            import json
            json_string = json.dumps(data)
            print ('[+] json_string:',json_string)
            print (json_string)
            return str(json_string)             
            
        if command == 'Оренклип : Пользователь по user_id':
            name        = info.setdefault('name','')
            user_id     = info.setdefault('user_id','')
            db,cursor = connect_mysql ("orenlkip_bot")
            sql = "select id,name,data_id,info from `users` where name = 'user_id' and info = '{}'  limit 1".format (user_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            data_id = 0
            for rec in data: 
                id,name,data_id,info = rec.values()
            answer = ''  
            print ('[data_id] : ',data_id)    
            sql = "select id,name,info from `users` where name = 'Имя cотрудника' and data_id = '{}'  limit 1".format (data_id)
            print ('sql',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,name,info = rec.values() 
                answer = answer + info + '\n'
            print ('[+] answer',answer)    
            #import json
            #json_string = json.dumps(result)
            #print (json_string)
            return str(answer) 
 
        if command == 'ОренКлип : Получить заказы':
            name        = info.setdefault('name','')
            db,cursor = connect_mysql ("orenlkip_bot")
            sql = "select * from `order` where id > 3616  order by id desc ".format ()
            cursor.execute(sql)
            result = cursor.fetchall()
            import json
            json_string = json.dumps(result)
            print (json_string)
            return str(json_string)    
 
        if command == 'ОренКлип : Проставить баланс':
            name        = info.setdefault('name','')
            user_id     = info.setdefault('user_id','')
            summ        = info.setdefault('summ','')
            import iz_bot
            message_info = {}
            message_info['user_id'] = user_id
            message_info['namebot'] = 'orenlkip_bot'
            save_data = [['1С',str(name)],['Баланс',str(summ)]]
            iz_bot.user_save_data (message_info,save_data)
            return str('ok')   

        if command == 'ОренКлип : Записать услугу':
            name_S      = info.setdefault('name','')
            data_id     = info.setdefault('data_id','')
            info_m      = info.setdefault('info','')
            summ        = info.setdefault('summ','')
            currency    = info.setdefault('currency','')
            amount      = info.setdefault('amount','')
            user_id     = info.setdefault('user_id','')
            nomer       = info.setdefault('nomer',0)
            db,cursor = connect_mysql ("orenlkip_bot")
            sql = "select id,name from balans where data_id = {} limit 1".format (data_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            id = 0
            for rec in data: 
                id,name = rec.values()
            if id == 0:
                sql = "INSERT INTO balans (`name`,`info`,`data_id`,`summ`,`currency`,`user_id`,`amount`,`nomer`) VALUES ('{}','{}',{},{},'{}','{}',{},{})".format(name_S,info_m,data_id,summ,currency,user_id,amount,nomer)
                cursor.execute(sql)
                db.commit()  
            else:
                sql = "UPDATE `balans` SET nomer    = {}    WHERE id = {} ".format (nomer,id)
                cursor.execute(sql)
                sql = "UPDATE `balans` SET amount   = {}    WHERE id = {} ".format (amount,id)
                cursor.execute(sql)
                sql = "UPDATE `balans` SET name     = '{}'  WHERE id = {} ".format (name_S,id)
                cursor.execute(sql)
                sql = "UPDATE `balans` SET summ     = '{}'  WHERE id = {} ".format (summ,id)
                cursor.execute(sql)
                db.commit()
            return str('ok')            
 
        if command == 'Телеграмм бот : Отправить файл':  
            bot_token       = info.setdefault('token','')
            bot_chatId      = info.setdefault('bot_chatId','')
            file_location   = info.setdefault('file_location','')
            caption         = info.setdefault('caption','')
            import requests
            url = 'https://api.telegram.org/bot' + bot_token +'/sendDocument?'
            data = {'chat_id': bot_chatId,'parse_mode':'HTML','caption':caption}
            files = {'document': open(file_location, 'rb')}
            resp = requests.post(url, data=data, files=files, stream=True)
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(json_string)             
            
        if command == 'Инфостарт : Получить данные':
            id     = info.setdefault('id','')
            db,cursor = connect_mysql ("a123_site")
            sql = "select id,name,accounting,category,configuration,whom,short,info,url  from infostart where id > {} limit 1000".format (id)
            cursor.execute(sql)
            result = cursor.fetchall()
            import json
            json_string = json.dumps(result)
            print (json_string)
            return str(json_string)                
               
        if command == 'Клиент : Получить список клиентов':
            db,cursor = connect_mysql ("telegram")
            sql = "select accound1.name,accound1.info,accound2.name,accound2.info  from accound as accound1, accound as accound2 where accound1.data_id = accound2.data_id and accound1.name = 'Имя' and accound2.name = 'Токен'".format ()
            cursor.execute(sql)
            result = cursor.fetchall()
            import json
            json_string = json.dumps(result)
            print (json_string)
            return str(json_string)  
            
        if command == 'ВК : Создать шапку': 
            name     = info.setdefault('name','')
            kod      = info.setdefault('kod','')
            grup     = info.setdefault('grup','')
            color01  = info.setdefault('color01','')
            color02  = info.setdefault('color02','') 
            color03  = info.setdefault('color03','')
            color04  = info.setdefault('color04','')
            color05  = info.setdefault('color05','') 
            db,cursor = connect_postgs ()
            sql = "select id,name from vk_hat where l1c = '{}';".format (kod)
            cursor.execute(sql)
            result = cursor.fetchall()
            id = 0
            for rec in result: 
                id,name_sql = rec
            if id == 0:
                sql = "INSERT INTO vk_hat (name,color01,color02,color03,color04,color05,font,font_size,grup,l1c,picture,text01,text02,text03,text04,text05,token,x01,x02,x03,x04,x05,y01,y02,y03,y04,y05) VALUES ('"+str(name)+"','"+str(color01)+"','"+str(color02)+"','"+str(color03)+"','"+str(color04)+"','"+str(color05)+"','7',8,'"+str(grup)+"','"+str(kod)+"','11','12','13','14','15','16','17',18,19,20,21,22,23,24,25,26,27)".format ()
                cursor.execute(sql)
                db.commit()
                lastid = cursor.lastrowid
            else:  
                sql = "UPDATE vk_hat SET name = '{}' WHERE l1c = '{}'".format (name,kod)
                cursor.execute(sql)
                db.commit()                
            #import json
            #json_string = json.dumps(data)
            #print (json_string)
            return str("ok")                  
               
        if command == 'orenlkip_bot Новое меню':  
            date     = info.setdefault('date','')            
            menu01   = info.setdefault('menu01','')
            menu02   = info.setdefault('menu02','')
            menu11   = info.setdefault('menu11','')
            menu12   = info.setdefault('menu12','')
            status   = info.setdefault('status','')
            menu21   = info.setdefault('menu21','')
            menu22   = info.setdefault('menu22','')
            namebot  = "orenlkip_bot"
            db,cursor = connect_mysql (namebot)
            sql = "INSERT INTO food (date,menu01,menu02,menu11,menu12,status,menu21,menu22) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format (date,menu01,menu02,menu11,menu12,status,menu21,menu22)
            cursor.execute(sql)
            db.commit()
            sql = "select id,name from order where 1=1  ORDER BY id desc limit 1".format()   
            cursor.execute(sql)
            results = cursor.fetchall()  
            for row in results:
                id,name = row.values() 
            sql = "UPDATE setting SET info = '{}' WHERE name = 'Последний ID' ".format (id)
            cursor.execute(sql)
            db.commit()    

            sql = "UPDATE setting SET info = '{}' WHERE name = 'Шапка' ".format (date)
            cursor.execute(sql)
            db.commit()    

            
            return 'ok'

        if command == 'Управление : Создать задачу на отправку файлов':
            db,cursor = connect_postgs ()
            name    = info.setdefault('name','')
            text    = info.setdefault('text','')
            picture    = info.setdefault('picture','')
            chat    = info.setdefault('chat','')
            file    = info.setdefault('file','')
            date    = info.setdefault('date','нет')
            rating    = info.setdefault('rating',0)
            sql = "INSERT INTO send_news (name,text,picture,start,file,chat,rating,like_s,dislike,answer) VALUES ('{}','{}','{}','{}','{}','{}',{},{},{},'{}')".format (name,text,picture,str(date),file,chat,rating,1,1,'')
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            return 'ok'        
        
        if command == 'Управление : Создать новое сообшение':
            namebase   = info.setdefault('namebase','')
            name   = info.setdefault('Имя','')
            text   = info.setdefault('Текст','')
            menu   = info.setdefault('Меню','')
            import pymysql
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebase,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor() 
            sql = "INSERT INTO message (`name`,data_id,info,status) VALUES ('{}',0,'{}','')".format ('Имя',name)
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            sql = "UPDATE message SET data_id = '{}' WHERE id = {}".format (lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO message (`name`,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Текст',lastid,text)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO message (`name`,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Меню',lastid,menu)
            cursor.execute(sql)
            db.commit()
            return 'ok'

        if command == 'Управление : Создать динамический список':
            namebase   = info.setdefault('namebase','')
            name       = info.setdefault('name','')
            data       = info.setdefault('info','')
            rating     = info.setdefault('rating','')
            import pymysql
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebase,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor() 
            sql = "INSERT INTO service (`name`,data_id,info,status,rating) VALUES ('{}',{},'{}','',{})".format (name,0,data,rating)
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            #sql = "UPDATE setting SET data_id = '{}' WHERE id = {}".format (lastid,lastid)
            #cursor.execute(sql)
            #db.commit()
            #try:
            #cursor_main.execute(sql_main)
            #except Exception as e:
            #    print ('    [+] Ошибка создания базы данных:',e)  
            #db_main.commit() 
            return 'ok'  
            
        if command == 'Управление : Создать задание ping':
            namebot     = info.setdefault('namebot','')
            message_in  = info.setdefault('message_in','')
            message_out = info.setdefault('message_out','')
            status      = info.setdefault('status','')
            data_id     = info.setdefault('data_id','')
            db,cursor = connect_postgs ()
            sql = "select id,name from ping_task where name = '{}' and data_id = '{}' ".format (namebot,data_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            id = 0
            for rec in result: 
                id,name_sql = rec               
            
            sql = "INSERT INTO ping_task (name,message_in,message_out,status,data_id) VALUES ('{}','{}','{}','{}','{}') ".format (namebot,message_in,message_out,status,data_id)
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            return str(lastid)
                        
        if command == 'Управление : Созранить телеграмм клиента в базе':
            name     = info.setdefault('name','')
            token    = info.setdefault('token','')
            status   = info.setdefault('status','')
            phone_number  = info.setdefault('phone_number','')
            db,cursor = connect_postgs ()  
            sql = "select id,name from ping_accound where phone_number = '{}' ".format (phone_number)
            cursor.execute(sql)
            result = cursor.fetchall()
            id = 0
            for rec in result: 
                id,name_sql = rec             
            if id == 0:
                sql = "INSERT INTO ping_accound (name,token,status,phone_number) VALUES ('{}','{}','{}','{}') ".format (name,token,status,phone_number)
                cursor.execute(sql)
                db.commit()
            else:
                print ('[ok] Обновление')
                
                
                
                
            return str("ok")
            
        if command == 'Управление : Создать команду ping':
            name     = info.setdefault('name','')
            info_d   = info.setdefault('info','')
            status   = info.setdefault('status','')
            data_id  = info.setdefault('data_id','')
            delete   = info.setdefault('delete','')
            db,cursor = connect_postgs ()
            sql = "select id,name from ping_master where name = '{}' and data_id = '{}' ".format (name,info_d,data_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            id = 0
            for rec in result: 
                id,name_sql = rec            
            if id == 0:
                print ('[+] Ввод новых данных') 
                sql = "INSERT INTO ping_master (name,info,status,data_id) VALUES ('{}','{}','{}','{}') ".format (name,info_d,status,data_id)
                cursor.execute(sql)
                db.commit()
                lastid = cursor.lastrowid
            else:
                print ('Обновление данных')                
            return str("ok")
            
        if command == 'Управление : Создать новую настройку':
            namebase   = info.setdefault('namebase','')
            data       = info.setdefault('Значение','')
            name       = info.setdefault('Парметр','')
            import pymysql
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebase,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor() 
            sql = "INSERT INTO setting (`name`,data_id,info,status) VALUES ('{}',{},'{}','')".format (name,0,data)
            cursor.execute(sql)
            db.commit()
            lastid = cursor.lastrowid
            sql = "UPDATE setting SET data_id = '{}' WHERE id = {}".format (lastid,lastid)
            cursor.execute(sql)
            db.commit()
            #try:
            #cursor_main.execute(sql_main)
            #except Exception as e:
            #    print ('    [+] Ошибка создания базы данных:',e)  
            #db_main.commit() 
            return 'ok'              
        
        if command == 'Управление : Создать исполняемый файл':
            filename    = info.setdefault('filename','')
            text        = info.setdefault('text','')
            f= open("C:/Main/Server/{}".format(filename),"w+")
            f.write(text)
            f.close()
            #print ("C:\Main\{}".format(filename))
            #import pymysql
            #db_main = pymysql.connect(host='localhost',user='izofen',password='podkjf4',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            #cursor_main = db_main.cursor() 
            #sql_main = 'CREATE DATABASE '+str(namebase)
            #try:
            #cursor_main.execute(sql_main)
            #except Exception as e:
            #    print ('    [+] Ошибка создания базы данных:',e)  
            #db_main.commit() 
            return 'ok'                        
        
        if command == 'Управление : Создать таблицу':
            namebase   = info.setdefault('namebase','')
            sql        = info.setdefault('SQL','нет')
            import pymysql
            db_main = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebase,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor_main = db_main.cursor() 
            print ('    [+] Создаем таблицы SQL:',sql)
            cursor_main.execute(sql)
            db_main.commit() 
            return 'ok'         
               
        if command == 'Управление : Создать базу данных':
            namebase        = info.setdefault('namebase','')
            import pymysql
            db_main = pymysql.connect(host='localhost',user='izofen',password='podkjf4',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor_main = db_main.cursor() 
            sql_main = 'CREATE DATABASE '+str(namebase)
            #try:
            cursor_main.execute(sql_main)
            #except Exception as e:
            #    print ('    [+] Ошибка создания базы данных:',e)  
            db_main.commit() 
            return 'ok'    
              
        if command == 'Получить webhook':
            db,cursor = connect_postgs ()
            sql = "select * from setting where name = 'Текущий webhook';".format ()
            cursor.execute(sql)
            data = cursor.fetchall()
            import json
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)             
                 
        if command == 'DLE создать новость':
            db,cursor = connect_mysql ("news")
            allow_br        = info.setdefault('allow_br',0)
            allow_comm      = info.setdefault('allow_comm',1)
            allow_main      = info.setdefault('allow_main',1)
            alt_name        = info.setdefault('alt_name','')
            approve         = info.setdefault('approve',1)
            autor           = info.setdefault('autor','')
            category        = info.setdefault('category','7')
            comm_num        = info.setdefault('comm_num',0)
            date            = info.setdefault('date','2024-07-16 21:12:07.000')
            descr           = info.setdefault('descr','')
            fixed           = info.setdefault('fixed',0)
            full_story      = info.setdefault('full_story','')
            keywords        = info.setdefault('keywords','')
            metatitle       = info.setdefault('metatitle','')
            short_story     = info.setdefault('short_story','')
            symbol          = info.setdefault('symbol','')
            tags            = info.setdefault('tags','')
            title           = info.setdefault('title','')
            xfields         = info.setdefault('xfields','')
            
            sql = "INSERT INTO dle_post (`allow_br`,`allow_comm`,`allow_main`,`alt_name`,`approve`,`autor`,`category`,`comm_num`,`date`,`descr`,`fixed`,`full_story`,`keywords`,`metatitle`,`short_story`,`symbol`,`tags`,`title`,`xfields`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format ()
            sql_save = (allow_br,allow_comm,allow_main,alt_name,approve,autor,category,comm_num,date,descr,fixed,full_story,keywords,metatitle,short_story,symbol,tags,title,xfields)
            cursor.execute(sql,sql_save)
            db.commit()
            return str("OK")  
        
        if command == 'Торрент список новостей':
            id      = info.setdefault('id',0)
            limit   = info.setdefault('limit',100)
            offset  = info.setdefault('offset',0)
            db,cursor = connect_postgs ()
            #print ('[+] Тестовый пример ...')
            sql = "select id,code,name,picture,text,title02,title03,magnet from torrent where (pic_type = 'jpeg' or pic_type = 'png' or pic_type = 'webp' ) and id > {} order by id asc limit {} offset {} ".format (id,limit,offset)
            #print ('[sql]',sql)
            cursor.execute(sql)
            data = cursor.fetchall()   
            import json
            json_string = json.dumps(data)
            #print (json_string)
            return str(json_string)          
        
        if command == '1С Создать задание для шапки':
            print ('[+] Тестовый пример ...')
            import sqlite3 as sl
            db  = sl.connect('C:\\Main\\templat.db')  
            cursor = db.cursor() 
            id          = info.setdefault('id','')   ##12
            name        = info.setdefault('name','')  ## 'Научная и техническая литература'
            L1C         = info.setdefault('L1C','')  ## '000000017'
            grup        = info.setdefault('grup','')  ## '225150934'
            
            
            color01     = '#ecec53'
            color02     = '#1C0606'
            color03     = '#1C0606'
            color04     = ''
            color05     = '#ecec53'
            font        = '20851.ttf'    
            font_size   = 50
            
            picture     = 'logo001.jpeg'
            text01      = '%d-%m-%Y %H:%M'
            text02      = 'Вступил в группу последний'
            text03      = ''
            text04      = ''
            text05      = ''
            token       = 'vk1.a.d2wvmWi-seEeSRLnMhTfK_83m7gZRt-KqJrwK4rpK2cEH0RBZefL1ia3ouyciY-cxDJilYhmIn5UId2VQWATLY-QUXEEP2gVeWtm6R44ucEo8hufAxVwCC8053_flUTRnNVpkFj8XqRTyV8kAzWn0-Q-8ZjPfC9VdYSKONY8tkxu1SPuXDkfQ0VXzQ97-3xw_ir5ZF6wa6DGzhFjaNqAhg'
            x01         = 1300
            x02         = 1000
            x03         = 1300
            x04         = 1040
            x05         = 1200
            y01         = 400
            y02         = 330
            y03         = 545
            y04         = 210
            y05         = 240
            #sql = "INSERT INTO vk_hat (id,name,L1C,color01,color02,color03,color04,color05,font,font_size,grup,picture,text01,text02,text03,text04,text05,token,x01,x02,x03,x04,x05,y01,y02,y03,y04,y05) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format ()
            sql = "INSERT INTO vk_hat (id,token,name,font,font_size,grup,picture,text01,text02,text03,text04,text05,x01,x02,x03,x04,x05,y01,y02,y03,y04,y05,color01,color02,color03,color04,color05,L1C) VALUES ({},'{}','{}','{}',{},'{}','{}','{}','{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{},'{}','{}','{}','{}','{}','{}')".format (id,token,name,font,font_size,grup,picture,text01,text02,text03,text04,text05,x01,x02,x03,x04,x05,y01,y02,y03,y04,y05,color01,color02,color03,color04,color05,L1C)
            print ('sql',sql)
            sql_save = (id)
            cursor.execute(sql)
            db.commit()             
            return 'ok'
               
        if command == 'a123bot.ru : Информацию о новости':
            import json
            db,cursor = connect ("A123_site")
            id     = info.setdefault('Номер','')            
            sql = "select * from news  where id = {};".format (id)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)         
        
        if command == 'a123bot.ru : Получить список новостей':
            import json
            db,cursor = connect ("A123_site")
            data_id     = info.setdefault('Номер','')            
            sql = "select id,name from news  where 1=1;".format ()
            print ('[sql]',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)         
        
        if command == 'password_save_bot : Получить информацию':
            import json
            db,cursor = connect ("password_save_bot")
            data_id     = info.setdefault('Номер','')            
            sql = "select id,name,info,user_id from password  where info <> '' and status <> 'delete';".format (data_id)
            print ('[sql]',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)         

        if command == 'audiobooks_314_bot : Записать информационную':
            namebot = "audiobooks_314_bot"
            db,cursor = connect_mysql (namebot)
            name      = info.setdefault('name','')
            data      = info.setdefault('info','')
            status    = info.setdefault('status','')
            data_id   = info.setdefault('data_id',0)             
            id = 0 
            sql = "select id,name from service where data_id = {} and name = '{}' ".format(data_id,name)
            cursor.execute(sql)
            result = cursor.fetchall()
            for rec in result: 
                id,name_del = rec.values()
            if id == 0: 
                sql = "INSERT INTO service (name,info,data_id,status) VALUES ('{}','{}',{},'{}')".format (name,data,data_id,status)
                print ('[+] sql:',sql)
                cursor.execute(sql)
                db.commit() 
            else:
                sql = "UPDATE service SET info = '{}' WHERE data_id = {} and name = '{}'".format(data,data_id,name)
                cursor.execute(sql)
                db.commit()
            return str("ok") 
            
        if command == 'audiobooks_314_bot : Записать чат':
            namebot = "audiobooks_314_bot"
            db,cursor = connect_mysql (namebot)
            name      = info.setdefault('name','')
            data      = info.setdefault('info','')
            status    = info.setdefault('status','')
            data_id   = info.setdefault('data_id',0)             
            id = 0 
            sql = "select id,name from service where data_id = {} and name = '{}' and info = '{}' ".format(data_id,name,data)
            cursor.execute(sql)
            result = cursor.fetchall()
            for rec in result: 
                id,name_del = rec.values()
            if id == 0: 
                sql = "INSERT INTO service (name,info,data_id,status) VALUES ('{}','{}',{},'{}')".format (name,data,data_id,status)
                print ('[+] sql:',sql)
                cursor.execute(sql)
                db.commit() 
            else:
                sql = "UPDATE service SET status = '{}' WHERE data_id = {} and name = '{}' and info = '{}'  ".format(status,data,data_id,name,data)
                cursor.execute(sql)
                db.commit()
            return str("ok")            
        
        if command == 'audiobooks_314_bot : Получить информацию по номеру': ### Удалить
            import json
            db,cursor = connect ("audiobooks_314_bot")
            data_id     = info.setdefault('Номер','')            
            sql = "select id,name,info from service  where data_id = {};".format (data_id)
            print ('[sql]',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string) 
            
        if command == 'audiobooks_314_bot : Обновить информацию по номеру': ### Удалить
            import json
            db,cursor = connect ("audiobooks_314_bot")
            
            name        = info.setdefault('name','')
            data_id     = info.setdefault('Номер','')
            picture     = info.setdefault('Картинка','')
            change      = info.setdefault('Замена','')
            text        = info.setdefault('Текст','')
            katalog     = info.setdefault('Каталог','')
            url         = info.setdefault('url','')
            type_send   = info.setdefault('Тип_рассылки','')

            files         = info.setdefault('Файлы','')
            silcts        = info.setdefault('ЧатФайлов','')



            
            lastid = data_id
            if data_id == '': 
                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Имя книги',0,name,'')
                cursor.execute(sql)
                db.commit() 
                lastid = cursor.lastrowid    
                sql = "UPDATE service SET data_id = {} WHERE id = {}".format (lastid,lastid)
                cursor.execute(sql)
                db.commit()
            
                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Картинка',lastid,picture,'')
                cursor.execute(sql)
                db.commit() 
        
                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Замена',lastid,change,'')
                cursor.execute(sql)
                db.commit() 

                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Текст',lastid,text,'')
                cursor.execute(sql)
                db.commit() 

                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Каталог',lastid,katalog,'')
                cursor.execute(sql)
                db.commit() 

                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('url',lastid,url,'')
                cursor.execute(sql)
                db.commit() 
                
                sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Тип рассылки',lastid,type_send,'')
                cursor.execute(sql)
                db.commit()                 
                
                for file in files: 
                    sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Файл',lastid,file,'')
                    cursor.execute(sql)
                    db.commit()                 
                
                for file in silcts: 
                    sql = "INSERT INTO service (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format('Чат',lastid,file,'')
                    cursor.execute(sql)
                    db.commit()                 
                
                
                
            else:
                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(name,'Имя книги',data_id)
                cursor.execute(sql)
                db.commit()

                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(picture,'Картинка',data_id)
                cursor.execute(sql)
                db.commit()

                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(change,'Замена',data_id)
                cursor.execute(sql)
                db.commit()

                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(text,'Текст',data_id)
                cursor.execute(sql)
                db.commit()

                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(katalog,'Каталог',data_id)
                cursor.execute(sql)
                db.commit()

                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(url,'url',data_id)
                cursor.execute(sql)
                db.commit()
                
                sql = "UPDATE service SET info = '{}' WHERE name = '' and data_id = {}".format(type_send,'Тип рассылки',data_id)
                cursor.execute(sql)
                db.commit()
                
            #json_string = json.dumps(data)
            #print (json_string)
            #return str(json_string) 
            return str(lastid)

        if command == 'ping314_bot : Записать задание':
            import json
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            db,cursor = connect ("ping314_bot")
            sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`,`type`) VALUES ('{}',{},'{}','{}','{}')".format('Имя',0,namebot,'','')
            cursor.execute(sql)
            db.commit()  
            lastid = cursor.lastrowid    
            sql = "UPDATE task SET data_id = {} WHERE id = {}".format (lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`,`type`) VALUES ('{}',{},'{}','{}','{}')".format('user_id',lastid,user_id,'','')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (`name`,`data_id`,`info`,`status`,`type`) VALUES ('{}',{},'{}','{}','{}')".format('Проверка',lastid,'Ожидание начала','','')
            cursor.execute(sql)
            db.commit()  
            data = {'answer':'ok'}
            json_string = json.dumps(lastid)
            print ('    [answer]',json_string)
            return str(json_string)             

        if command == 'ping314_bot : Получить задание':
            import json
            db,cursor = connect ("ping314_bot")
            sql = "select id,info from task  where name = '{}';".format ('Имя')
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)  
              
        if command == 'Телеграм : Получить информацию по токену': 
            import json
            from telethon.sync import TelegramClient
            from telethon.sessions import StringSession          
            token = info.setdefault('token','')
            print ('[+]-----------------------------------[+]')
            print ('[+] token   :',token)
            print ('[+]-----------------------------------[+]')

            api_id = 192804
            api_hash = '1b40d1d01f8922b384d44e29d32f6acf'
            session = token
            client = TelegramClient(StringSession(session),api_id=api_id,api_hash=api_hash)
            client.connect()        
            #if not await client.is_user_authorized():
            #    answer = 'Отсутствует подключение к телеграмм серверу'
            #    return 'Отсутствует подключение к телеграмм серверу'    
            #else:
            #    answer = 'Подключение к телеграмм серверу успешно'        
            answer = client.get_me()
            #try:
            #    print ('[+] user',answer.stringify())        
            #    first_name  = answer.first_name #'Petr',
            #    last_name   = answer.last_name  #'Menshikov',
            #    username    = answer.username   #'petrmenshikoff',
            #    phone       = answer.phone      #'447985193730',
            #    id          = answer.id      #'447985193730',
            #    answer      = first_name + " " + last_name + "("+str(id)+","+str(phone)+")"
            #    print ('[+] answer:',answer)
            #except:    
            #answer = "No"            
            return str(answer)         
               
        if command == 'Бот : Анкетирование':
            import json
            import pymysql
            namebot  = info.setdefault('namebot','Serofim_anketa_bot')
            name     = info.setdefault('name','')
            info_s   = info.setdefault('info','')
            data_id  = info.setdefault('data_id','')
            id       = info.setdefault('id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] id      :',id)
            print ('[+] namebot :',namebot)
            print ('[+] name    :',name)
            print ('[+] info    :',info)
            print ('[+] data_id :',data_id)
            print ('[+]-----------------------------------[+]')
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor   = db.cursor()
            sql = "INSERT INTO `service` (`name`,`data_id`,`info`,`status`,`rating`) VALUES ('{}',{},'{}','{}',{})".format (name,data_id,info_s,'',0)
            print ('[sql] : ',sql)
            sql_save = ()
            cursor.execute(sql,sql_save)
            lastid = cursor.lastrowid 
            db.commit() 
            sql = "UPDATE service SET data_id = {} WHERE id = {} ".format (lastid,lastid)
            print ('[sql] : ',sql)
            cursor.execute(sql)
            db.commit()
            data = {'answer':lastid}
            json_string = json.dumps(lastid)
            print ('    [answer]',json_string)
            return str(answer)        
        
        if command == 'Бот : Список пользователей':
            import json
            namebot     = info.setdefault('namebot','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+]-----------------------------------[+]')            
            db,cursor = connect_mysql (namebot)            
            sql = "select id,name,info,data_id,status from users where name = 'user_id' ;".format ()
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('[answer]',json_string)
            return str(json_string)                           
        
        if command == 'Бот : Информация о пользователе':
            import json            
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')            
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect_mysql (namebot)            
            sql = "select id,name,info,data_id,status from users where name = 'user_id' and info = '{}' ;".format (user_id)
            #print ('[sql] : ',sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            data_id = 0
            for rec in results:
                id,name,info,data_id,status = rec.values()                
            sql = "select id,name,info,data_id,status from users where data_id = {} ;".format (data_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)        
               
        if command == 'Бот : Отправить сообщение':
            import json
            import requests
            user_id     = info.setdefault('user_id','')
            token       = info.setdefault('token','')
            message_out = info.setdefault('message_out','')
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id :',user_id)
            print ('[+] token   :',token)
            print ('[+] text    :',message_out)
            print ('[+]-----------------------------------[+]')
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(json_string)   

        if command == 'Бот : Отправить сообщение с картинкой':
            import json
            import requests
            user_id     = info.setdefault('user_id','')
            token       = info.setdefault('token','')
            message_out = info.setdefault('message_out','')
            picture      = info.setdefault('picture','')
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id :',user_id)
            print ('[+] token   :',token)
            print ('[+] text    :',message_out)
            print ('[+] picture    :',picture)
            print ('[+]-----------------------------------[+]')
            
            method = "sendPhoto"
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['parse_mode'] = 'HTML'
            file_path = picture
            file_opened = open(file_path, 'rb')
            #try:
            file_opened = open(file_path, 'rb')
            files = {'photo': file_opened}
            #        except:       
            #            file_path = "/home/izofen/Main/Server/picture/file_2.jpg"
            #            file_path = "c:/Main/Server/picture/file_2.jpg"
            #            file_opened = open(file_path, 'rb')            
            # 
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params, files=files) 
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(json_string) 

        if command == 'Телеграм : Создать меню':
            import pymysql
            import json
            namebot     = info.setdefault('namebot','')
            text        = info.setdefault('Текст','')
            name_menu   = info.setdefault('Имя','')
            menu        = info.setdefault('Меню','') 
            type_m      = info.setdefault('Тип_кнопки','')            
            key11       = info.setdefault('Кнопка_11','')
            key12       = info.setdefault('Кнопка_12','')
            key13       = info.setdefault('Кнопка_13','')
            key21       = info.setdefault('Кнопка_21','')
            key22       = info.setdefault('Кнопка_22','')
            key23       = info.setdefault('Кнопка_23','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot   :',namebot)
            print ('[+] name_menu :',name_menu)
            print ('[+] text      :',text)
            print ('[+]-----------------------------------[+]')            
            db,cursor = connect (namebot)  
            data_id = 0
            sql = "select id,data_id from menu  where name = 'Имя' and info = '{}' limit 1;".format (name_menu)
            print ('[sql] : ',sql)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,data_id  =  rec.values()
            #data = 'OK'    
            #json_string = json.dumps(data)
            #print ('    [answer]',json_string)
            #return str(json_string)     
            ########################################################################################################################################
            id = 0
            sql = "select id,name from menu  where name = 'Имя' and data_id = '{}' limit 1;".format (data_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,name  =  rec.values()    
            if id == 0:
                sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format ('Имя',data_id,name_menu,'')
                sql_save = ()
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid 
                db.commit()            
            else:    
                sql = "UPDATE menu SET `info` = '{}' WHERE name = 'Имя' and data_id = {} ".format (name_menu,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()      
            update_key ('Кнопка 11','Замена 11',key11,data_id,namebot)   
            update_key ('Кнопка 21','Замена 21',key21,data_id,namebot)            
            update_key ('Кнопка 22','Замена 22',key22,data_id,namebot)            
            update_key ('Кнопка 23','Замена 23',key23,data_id,namebot)            
            data = {'answer':'OK'}
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)
        
        if command == 'Телеграм : Записать сообшение':
            import json
            namebot     = info.setdefault('namebot','')
            text        = info.setdefault('Текст','')
            name        = info.setdefault('Имя','')
            menu        = info.setdefault('Меню','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot   :',namebot)
            print ('[+] name      :',name_menu)
            print ('[+] text      :',text)
            print ('[+] menu      :',menu)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)            
            data_id = 0
            sql = "select id,data_id from message  where name = 'Имя' and info = '{}' limit 1;".format (name)
            cursor.execute(sql)
            data = cursor.fetchall()
            for rec in data: 
                id,data_id  =  rec.values()
            if data_id == 0: 
                sql = "INSERT INTO message (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Имя',0,name,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid   
                db.commit()
                data_id = lastid
                sql = "UPDATE message SET `data_id` = {} WHERE id = {} ".format (data_id,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()  
                sql = "INSERT INTO message (name,data_id,info,status) VALUES (%s,%s,%s,%s)".format ()
                sql_save = ('Текст',data_id,text,'')
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid   
                db.commit()
            else:
                sql = "UPDATE message SET `info` = '{}' WHERE name = 'Текст' and data_id = {} ".format (text,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit()  
                sql = "UPDATE message SET `info` = '{}' WHERE name = 'Меню' and data_id = {} ".format (menu,data_id)
                sql_save = ()
                cursor.execute(sql,sql_save)  
                db.commit() 
                data = {'answer':'OK'}
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)    

        if command == 'Телеграм : Сменить пароль':
            import random
            db,cursor = connect ("A123_site")
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+]-----------------------------------[+]')            
            ps = ''
            strSM = "01234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvnm"
            for number1 in range(5):
                for number2 in range(4):
                    rn = random.randint(0,len(strSM))
                    ps = ps + strSM[rn:rn+1]
                ps = ps + '-' 
                for number2 in range(4):
                    rn = random.randint(0,len(strSM))
                    ps = ps + strSM[rn:rn+1]   
            password = ps
            sql = "UPDATE access SET `pass` = '{}' WHERE namebot = '{}' and user_id = '{}' ".format (password,namebot,user_id)
            sql_save = ()
            cursor.execute(sql,sql_save)  
            db.commit()  
            data = {'answer':password}            
            json_string = json.dumps(data)
            print (json_string)
            return str(json_string)     
                            
        if command == 'Телеграм : Получить пароль':
            import json
            import pymysql
            import random
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+]-----------------------------------[+]')              
            db,cursor = connect ("A123_site")
            sql = "select id,pass from access  where namebot = '{}' and user_id = '{}' limit 1;".format (namebot,user_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            elements = []
            password = ''
            for rec in data: 
                id,password  =  rec.values()
            if password == '':
                ps = ''
                strSM = "01234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvnm"
                for number1 in range(5):
                    for number2 in range(4):
                        rn = random.randint(0,len(strSM))
                        ps = ps + strSM[rn:rn+1]
                    ps = ps + '-' 
                    for number2 in range(4):
                        rn = random.randint(0,len(strSM))
                        ps = ps + strSM[rn:rn+1]   
                password = ps
                sql = "INSERT INTO `access` (`name`,`user_id`,`table`,`namebot`,`pass`) VALUES (%s,%s,%s,%s,%s)"
                sql_save = ('Администрирование',user_id,'info',namebot,password)
                cursor.execute(sql,sql_save)
                lastid = cursor.lastrowid
                db.commit()
            data = {'answer':password}            
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string)             

        if command == 'Телеграм : Открыть доступ':
            import json
            namebot     = info.setdefault('namebot','')
            user_id     = info.setdefault('user_id','')
            name        = info.setdefault('name','')
            acces       = info.setdefault('Доступ','')
            name_eng    = info.setdefault('name_end','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot :',namebot)
            print ('[+] user_id :',user_id)
            print ('[+] name    :',name)
            print ('[+] acces   :',acces)
            print ('[+]-----------------------------------[+]')             
            db,cursor = connect ("A123_site")
            sql = "INSERT INTO security (`name`,`user_id`,`status`,`menu`,`namebot`) VALUES (%s,%s,%s,%s,%s)"
            sql_save = (name_eng,user_id,acces,name,namebot)
            cursor.execute(sql,sql_save)
            lastid = cursor.lastrowid
            db.commit()
            data = {'answer':lastid}            
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string) 
        
        if command == 'Телеграм : Список ботов':
            import json
            namebot = 'bot_main'
            print ('[+]-----------------------------------[+]')
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)
            sql = "select id,name from bot_bots  where 1=1;".format ()
            cursor.execute(sql)
            data = cursor.fetchall()
            elements = []
            for rec in data: 
                id,name  =  rec.values()
                elements.append ([id,name])
            json_string = json.dumps(elements)
            print ('    [answer]',json_string)
            return json_string
        
        if command == 'Телеграм : Отправить сообщение по токену':
            import requests
            user_id     = info.setdefault('user_id','')
            token       = info.setdefault('token','')
            message_out = info.setdefault('message_out','')  
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id    :',user_id)
            print ('[+] token      :',name)
            print ('[+] message_out:',message_out)
            print ('[+]-----------------------------------[+]')   
            method = "sendMessage"
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            json_string = resp.json()
            print ('    [answer]',json_string)
            return str(answer)
                       
        if command == 'Боты : Отправить сообщение':
            import pymysql
            import iz_bot
            namebot     = info.setdefault('namebot','')                
            id_message  = info.setdefault('data_id','')
            text        = info.setdefault('text','')  
            menu        = info.setdefault('menu','')
            user_id     = info.setdefault('user_id','')
            no_save     = info.setdefault('no_save','')           
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id    :',user_id)
            print ('[+] menu       :',menu)
            print ('[+] text       :',text)
            print ('[+]-----------------------------------[+]')               
            db,cursor = connect (namebot)
            zamena = {}
            send_data = {"Text":text,'Замена':zamena}
            if no_save == 'Yes':
                send_data['Запись в базу '] = 'Не записывать'
            message_info = {'namebot':namebot,'user_id':user_id,'Меню':'Кнопка запуска меню'}
            json_string  = iz_bot.send_message (message_info,send_data) 
            print ('    [answer]',json_string)            
            return str(answer)
               
        if command == 'Боты : Создать service':
            import pymysql
            namebot    = info.setdefault('namebot','')                
            data_id    = info.setdefault('data_id','')
            name       = info.setdefault('name','')  
            info       = info.setdefault('info','')   
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot    :',namebot)
            print ('[+] data_id    :',data_id)
            print ('[+] name       :',name)
            print ('[+] info       :',info)
            print ('[+]-----------------------------------[+]')    
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "INSERT INTO service (name,data_id,info,status,rating) VALUES (%s,%s,%s,%s,%s)".format ()
            sql_save = (name,data_id,info,'',0)
            cursor.execute(sql,sql_save)
            db.commit()
            lastid = cursor.lastrowid 
            data = {'answer':lastid} 
            json_string = json.dumps(data)
            print ('    [answer]',json_string)
            return str(json_string) 
        
        if command == 'Боты : получить FTP':
            import ftplib
            import json
            NameFile    = info.setdefault('Имя','')
            print ('[+]-----------------------------------[+]')
            print ('[+] NameFile    :',NameFile)
            print ('[+]-----------------------------------[+]')    
            host            = "192.168.1.237"
            ftp_user        = "admin"
            ftp_password    = "podkjf4"
            server= ftplib.FTP(host, ftp_user, ftp_password)
            print("[+] ... CONNECTED TO FTP")
            files = server.nlst(NameFile)  #"/Public/bot_data/audiobooks_314_bot/Best/MDS/mBooks/"
            json_string = json.dumps(files)
            print ('    [answer]',json_string)
            return json_string
                    
        if command == 'Боты : получить размер':
            import ftplib
            import json
            NameFile    = info.setdefault('Имя','')
            print ('[+]-----------------------------------[+]')
            print ('[+] NameFile    :',NameFile)
            print ('[+]-----------------------------------[+]')   
            host            = "192.168.1.237"
            ftp_user        = "admin"
            ftp_password    = "podkjf4"
            filename        = NameFile
            server= ftplib.FTP(host, ftp_user, ftp_password)
            print("[+] ... CONNECTED TO FTP")
            try:
                files = str (server.size(NameFile)) 
            except :
                files = str ("Каталог")
            json_string = json.dumps(files)
            print ('    [answer]',json_string)
            return json_string    
                
        if command == 'Боты : Создать сообшение отправки':
            import pymysql
            import json
            namebot = info.setdefault('namebot','')                
            name    = info.setdefault('Имя','')
            text    = info.setdefault('Текст','')            
            menu    = info.setdefault('Меню','') 
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot    :',namebot)
            print ('[+] Имя        :',name)
            print ('[+] Меню       :',menu)
            print ('[+] Текст      :',text)
            print ('[+]-----------------------------------[+]')   
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                                        
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Имя',0,'{}','')".format (name)
            cursor.execute(sql)
            db.commit() 
            lastid = cursor.lastrowid
            sql = "UPDATE message SET data_id = '{}' WHERE id = {}  ".format(lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Текст',{},'{}','')".format (lastid,text)
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO message (name,data_id,info,status) VALUES ('Меню',{},'{}','')".format (lastid,menu)
            cursor.execute(sql)
            db.commit() 
            data = {'answer':lastid}
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)

        if command == 'Боты : Создать обеденное меню':
            import pymysql
            namebot     = info.setdefault('namebot','')
            Assortment  = info.setdefault('Aссортимент','')
            Date        = info.setdefault('Дата','')
            name        = info.setdefault('Наименование','')
            menu01 = info.setdefault('Меню01','')
            menu11 = info.setdefault('Меню11','')
            menu02 = info.setdefault('Меню02','')
            menu21 = info.setdefault('Меню21','')
            menu03 = info.setdefault('Меню03','')
            menu31 = info.setdefault('Меню31','')
            menu04 = info.setdefault('Меню04','')
            menu41 = info.setdefault('Меню41','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] Aссортимент :',name)
            print ('[+] Дата        :',Date)
            print ('[+] Наименование:',name)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('Aссортимент',0,'{}','')".format (Assortment)
            cursor.execute(sql)
            db.commit() 
            lastid = cursor.lastrowid
            sql = "UPDATE task SET data_id = '{}' WHERE id = {}  ".format(lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Дата',lastid,Date,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('Наименование',lastid,name,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu01',lastid,menu01,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu11',lastid,menu11,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu02',lastid,menu02,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu21',lastid,menu21,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu03',lastid,menu03,'')
            cursor.execute(sql)
            db.commit() 
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu31',lastid,menu31,'')
            cursor.execute(sql)
            db.commit()             
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu04',lastid,menu04,'')
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO task (name,data_id,info,status) VALUES ('{}',{},'{}','')".format ('menu41',lastid,menu41,'')
            cursor.execute(sql)
            db.commit() 
            data = {'answer':lastid}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)            

        if command == 'Боты : Удалить сообщение':
            import pymysql
            namebot = info.setdefault('namebot','')
            data_id = info.setdefault('data_id','0')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] data_id     :',data_id)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "UPDATE message SET status = 'delete' WHERE  data_id = '{}' ".format (data_id)
            cursor.execute(sql)
            db.commit()
            data = {'answer':'API'}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)            

        if command == 'Боты : Записать настройки':
            import pymysql
            namebot = info.setdefault('namebot','')
            data_id = info.setdefault('data_id','0')
            name    = info.setdefault('name','')
            info    = info.setdefault('info','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] data_id     :',data_id)
            print ('[+] name        :',name)
            print ('[+] info        :',info)
            print ('[+]-----------------------------------[+]')             
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()                
            sql = "UPDATE setting SET info = '{}' WHERE  name = '{}' ".format (info,name)
            cursor.execute(sql)
            db.commit()
            data = {'answer':'API'}  
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)        
                        
        if command == 'Сайты : Получить Title':
            import pymysql
            import json
            sql = info.setdefault('sql','')
            print ('[+]-----------------------------------[+]')
            print ('[+] sql     :',sql)
            print ('[+]-----------------------------------[+]')              
            base = "site_rus"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            cursor.execute(sql)            
            data = cursor.fetchall()    
            json_string = json.dumps(data)
            print ('    [answer]',json_string)   
            return json_string    
   
        if command == 'Боты : Выполнить запрос':
            import pymysql
            import json
            namebot = info.setdefault('namebot','')
            sql     = info.setdefault('sql','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] sql     :',sql)
            print ('[+]-----------------------------------[+]')                          
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)            
            cursor = db.cursor() 
            cursor.execute(sql)
            data = cursor.fetchall()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)   
            return json_string
            
        if command == 'Боты : Записать параметр пользователя':
            import pymysql
            import json
            namebot     = info.setdefault('namebot','')
            name_save   = info.setdefault('name','')
            info_save   = info.setdefault('info','')
            user_id     = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] namebot     :',namebot)
            print ('[+] name_save   :',name_save)
            print ('[+] info_save   :',info_save)
            print ('[+] user_id     :',user_id)
            print ('[+]-----------------------------------[+]')              
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database = namebot,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)            
            cursor = db.cursor() 
            sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}'".format (user_id)
            cursor.execute(sql)
            data = cursor.fetchall()  
            data_id = 0            
            for rec in data:
                id,name,info,data_id = rec.values()
                sql = "select id,name,info,data_id from users where name = '{}' and data_id = '{}'".format (name_save,id)
                cursor.execute(sql)
                data_find = cursor.fetchall()  
                id_find = 0            
                for rec_find in data_find:
                    id_find,name_find,info_find,data_id_find = rec_find.values()
                if id_find == 0:
                    sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'{}')".format(name_save,info_save,id,'')
                    cursor.execute(sql)
                    db.commit()
                sql = "UPDATE users SET info = '{}' WHERE name = '{}' and data_id = '{}' ".format (info_save,name_save,id)
                cursor.execute(sql)
                db.commit()
            json_string = json.dumps(data)
            print ('    [answer]',json_string)            
            return str(json_string)                  
      
        if command == 'Телеграмм боты : Получить список анкет':
            import pymysql
            import json
            print ('[+]-----------------------------------[+]')
            print ('[+]-----------------------------------[+]')              
            base = "TemplateIzBot"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            sql = "select id,user_id,name01,name02,name03,name04,name05,name06,name07,name08,name09,name10,name11,name12,name13 from anketa where 1=1 "
            cursor.execute(sql)
            results = cursor.fetchall()   
            json_string = json.dumps(results)
            print ('    [answer]',json_string)   
            return str(json_string)   
               
        if command == 'Телеграмм боты : Получить информацию пользователя':
            print ('[+] Телеграмм боты : Получить информацию пользователя')
            import pymysql
            import json
            user_id = info.setdefault('user_id','')
            print ('[+]-----------------------------------[+]')
            print ('[+] user_id     :',user_id)
            print ('[+]-----------------------------------[+]')              
            base = "TemplateIzBot"
            db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
            cursor = db.cursor()                    
            sql = "select u1.id,u2.name,u2.info from users as u1, users as u2  where (u1.name = 'user_id' and u1.info = '{}') and u2.data_id = u1.id;".format(user_id)
            cursor.execute(sql)
            results = cursor.fetchall()   
            json_string = json.dumps(results)
            print ('    [answer]',json_string)   
            return json_string   
         
@app.route('/platon/<access_code>/', methods=["GET", "POST"])   ### Для Маруси навыки
def platon (access_code):     ###       
    import json
    if request.method == "POST":
        request_message = request.json 
        derived_session_fields = ['session_id', 'user_id', 'message_id']
        response_message = {
            "response": {
            "text": 'Платон молодец',
            "tts": 'Люба самый красивый человек на свете. Высылаем ей игрушки которые она заказала. А так же вкусняшки и подарки. Люба молодец',
            "end_session": False
            },
            "session": {derived_key: request_message['session'][derived_key] for derived_key in derived_session_fields},
            "version": request_message['version']
        }    
    json_string = response_message
    return json_string   
       
@app.route('/proxy/<name>/', methods=["GET", "POST"])   ### <access_code>/<namebot>/
def proxy (name):     ### 
    import pymysql
    import time
    base = 'nnmclub314_bot'
    db = pymysql.connect(host='localhost',user='izofen',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)        
    cursor = db.cursor()                    
    sql = "select id,line from proxy where line = '{}' limit 1".format (name)
    cursor.execute(sql)
    results = cursor.fetchall()   
    id = 0
    for row in results:
        id,line = row.values()   
        print ('[line]',line)
    if id == 0:
        answer = 'save'    
        datatime = int(time.time())
        sql = "INSERT INTO proxy (`ip`,`port`,`type`,`status`,`line`,`datatime`) VALUES ('',0,'','','{}',{})".format (name,datatime)
        cursor.execute(sql)
        db.commit()
    else:
        answer = 'no'    
    return answer

@app.route('/')
def hello_world():
    return 'API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3140)
    app.run(host='0.0.0.0', port=80)

