

def get_info_tovar          (message_info,status_input,setting_bot,id_list):                                                                 ### Получаем информацию по товару
    import iz_bot
    namebot     = message_info.setdefault('namebot','')
    answer = {}    
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,about,catalog,comment,currency,picture,pocket,price,quantity from service where id = {} limit 1".format (id_list)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,about,catalog,comment,currency,picture,pocket,price,quantity = rec.values()        
        answer['name']          = name 
        answer['about']         = about
        answer['catalog']       = catalog
        answer['comment']       = comment
        answer['currency']      = currency
        answer['picture']       = picture
        answer['pocket']        = pocket
        answer['price']         = price
        answer['quantity']      = quantity
    return answer


##################################################################################################################################################################################################    

def save_sql                (message_info,name,sql,limit,offset,back):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "INSERT INTO data_sql (name,data) VALUES (%s,%s)".format ()
    sql_save = (name,sql,limit,offset,back)
    result = cursor.execute(sql,sql_save)
    db.commit()    
    lastid = cursor.lastrowid
    return lastid

def get_sql                 (message_info,setting_bot,id_sql):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,sql,ask,limit,offset,back from data_sql where id = {}".format(id_sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,sql,ask,limit,offset,back = rec.values() 
    return sql,ask,limit,offset,back  

def save_message            (message_info,setting_bot,user_id,message_out):
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = iz_bot.connect (namebot)
    id = 0
    sql = "select id,name from message where name = 'Имя' and info = '{}' ;".format(message_out)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name = rec.values()     
    if id != 0:
        sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (0,message_out,'Имя')
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid
        sql = "UPDATE message SET data_id = '{}' WHERE id = {}".format(lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (lastid,message_out,'Текст')
        cursor.execute(sql)
        db.commit()    
    return ""    
        
def gets_message            (message_info,setting_bot,user_id,message_out):        
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = iz_bot.connect (namebot)
    message      = {}
    sql = "select id,name,info,data_id from message where name = 'Имя' and info = '{}' ;".format(message_out)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,info,data_id = rec.values() 
    sql  = "select id,name,info,data_id from message where data_id = {};".format(data_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,info,data_id = rec.values()
        message[name] = info
    if message.setdefault('Текст','') == '': 
        message['Текст'] = message_out 
    if message.setdefault('Меню','') == '': 
        message['Меню'] = ''        
    return message
    
    
def user_save_data          (message_info,status_input,save_data): 
    import iz_bot
    namebot     = message_info['namebot']
    user_id     = message_info['user_id']
    db,cursor   = iz_bot.connect (namebot)
    sql         = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' limit 1;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()   
    for row in results:
        id,name,info,data_id = row.values() 
        for line in save_data:
            name    = line[0]
            info    = line[1]
            sql     = "select id,name,info from users where data_id = {} and name = '{}';".format (data_id,name)
            cursor.execute(sql)
            results = cursor.fetchall()  
            id = 0
            for row in results:
                id,name,info = row.values() 
            if id != 0:
                sql         = "UPDATE users SET info = %s WHERE `name` = %s and data_id = %s "
                sql_save    = (info,name,data_id)
                cursor.execute(sql,sql_save)
                db.commit()    
            else:    
                sql         = "INSERT INTO users (data_id,info,name,status) VALUES (%s,%s,%s,'')".format ()
                sql_save    = (info,name,data_id)
                cursor.execute(sql)
                db.commit() 
            status_input[name] = info
    return status_input 
    
    
def key_type_message (key):
    line = []
    for number in range(30):
        line1  = []
        key11  = {}
        key11['text']          = key.setdefault('Кнопка ' +str(number+1)+'1','')
        key11['callback_data'] = key.setdefault('Команда '+str(number+1)+'1','')
        key12  = {}
        key12['text']          = key.setdefault('Кнопка ' +str(number+1)+'2','')
        key12['callback_data'] = key.setdefault('Команда '+str(number+1)+'2','')
        key13  = {}
        key13['text']          = key.setdefault('Кнопка ' +str(number+1)+'3','')
        key13['callback_data'] = key.setdefault('Команда '+str(number+1)+'3','')
        key14  = {}
        key14['text']          = key.setdefault('Кнопка ' +str(number+1)+'4','')
        key14['callback_data'] = key.setdefault('Команда '+str(number+1)+'4','')
        if key.setdefault('Кнопка ' +str(number+1)+'1','') != '':        
            line1.append(key11)
        if key.setdefault('Кнопка ' +str(number+1)+'2','') != '':
             line1.append(key12)
        if key.setdefault('Кнопка ' +str(number+1)+'3','') != '':        
            line1.append(key13)
        if key.setdefault('Кнопка ' +str(number+1)+'4','') != '':        
            line1.append(key14)
        line.append(line1)    
    array = {"inline_keyboard":line}  
    markup = json.dumps(array) 
    return markup     
       
def key_type_keybord (key):
    array  = {}        
    line   = []
    for number in range(10):
        line1   = []
        key11   = {}
        key11['text']       = key.setdefault('Кнопка '+str(number)+'1','')  
        if key.setdefault('Замена '+str(number)+'1','') != '':
            key11['text']   = key.setdefault('Замена '+str(number)+'1','')
        line1.append(key12)
        key12   = {}
        key12['text']       = key.setdefault('Кнопка '+str(number)+'2','')
        if key.setdefault('Замена '+str(number)+'2','') != '':
            key12['text']   = key.setdefault('Замена '+str(number)+'2','')
        line1.append(key12)    
        key13   = {}
        key13['text']       = key.setdefault('Кнопка '+str(number)+'3','')
        if key.setdefault('Замена '+str(number)+'3','') != '':
            key13['text']   = key.setdefault('Замена '+str(number)+'3','')
        line1.append(key13)
        line.append(line1)
    array       = {"keyboard":line,"resize_keyboard":True}  
    markup      = json.dumps(array)
    return markup    
 
def gets_key (message_info,setting_bot,user_id,menu):
    sql     = "select id,name,info,data_id from menu where name = 'Имя' and info = '{}' ;".format (menu)
    cursor.execute(sql)
    results = cursor.fetchall()    
    markup     = {}
    for row in results:
        id,name,info,data_id = row.values() 
        sql = "select id,name,info from menu where data_id = '{}' and status <> 'delete' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            key[name] = info
    if key.setdefault('Тип кнопки','') == 'Сообщение':
        markup = key_type_message (key)
    if key.setdefault('Тип кнопки','') == 'Клавиатура':    
        markup = key_type_keybord (key)
    return markup
    
def send_message            (message_info,setting_bot,user_id,message_out,markup):
    import requests
    token                   = setting.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup                
    url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage')
    resp                    = requests.post(url, params) 
    answer                  = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    print ('') 
    return answer 
       
def send_sendPhoto          (message_info,setting_bot,user_id,message_out,picture,markup):
    import requests
    token                   = setting.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    try:   
        file_path   = picture
        file_opened = open(file_path, 'rb')
    except:    
        file_path   = "/home/izofen/Main/Server/picture/file_2.jpg"
        file_opened = open(file_path, 'rb')
    files = {'photo': file_opened}    
    if markup != {}:
        params['reply_markup'] = markup                
    url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendPhoto')
    resp                    = requests.post(url, params,files=files) 
    answer                  = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ sendPhoto] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧[+]') 
    print ('') 
    return answer     
    
def editMessageText         (message_info,setting_bot,user_id,message_out,message_id,markup):
    import requests
    token                   = setting.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['message_id']    = message_id
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup                
    url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'editMessageText')
    resp                    = requests.post(url, params) 
    answer                  = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ editMessageText] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧[+]') 
    print ('') 
    return answer    
    
def editMessageCaption      (message_info,setting_bot,user_id,message_out,message_id,marku):
    import requests
    token                   = setting.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['message_id']    = message_id
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup                
    url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'editMessageCaption')
    resp                    = requests.post(url, params) 
    answer                  = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ token, 'editMessageCaption'] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧[+]') 
    print ('') 
    return answer     
    
def editMessageMedia        (message_info,setting_bot,user_id,message_out,message_id,picture,markup):
    import requests
    token                   = setting.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['message_id']    = message_id
    params['parse_mode']    = 'HTML'
    try:   
        file_path   = picture
        file_opened = open(file_path, 'rb')
    except:    
        file_path   = "/home/izofen/Main/Server/picture/file_2.jpg"
        file_opened = open(file_path, 'rb')
    files = {'photo': file_opened}    
    if markup != {}:
        params['reply_markup'] = markup                
    url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'editMessageMedia')
    resp                    = requests.post(url, params,files=files) 
    answer                  = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ editMessageMedia] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧[+]') 
    print ('') 
    return answer    
      
def complite_key            (message_info,id_sql,sql,ask,limit,offset,back,metka):                                                  ###  Формируем список из кнопок по переданным нам параметрам
    import iz_bot
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = iz_bot.connect (namebot)
    sql_save            = (limit,offset,ask)
    cursor.execute(sql,sql_save)
    data = cursor.fetchall()
    key_array = []
    for rec in data: 
        id,info = rec.values()  
        command =  iz_bot.build_jsom ({'o':metka,'i':id,'s':id_sql})
        key_array.append ([[info,command],['',''],['','']])  
    #command      =  iz_bot.build_jsom ({'o':'next','s':id_code})
    #name_key     = set_name_key (message_info,'Кнопка далее')        
    #key_array.append ([[name_key,command],['',''],['','']]) 
    if back != '':                                                                                                                  ### Если нам передали информацию как вернутся назад заносим ее
        name_key = set_name_key (message_info,'Кнопка назад') 
        command  = iz_bot.build_jsom ({'o':'back','s':id_sql,'b':back})
        key_array.append ([[name_key,command],['',''],['','']]) 
    return key_array   
  
def get_message             (message_info,name):
    namebot     = message_info.setdefault ('namebot')
    db,cursor   = connect (namebot) 
    data_message = {}
    sql = "select id,name,info from message where name = 'Имя' and info = '{}' ;".format (name)
    cursor.execute(sql)
    results = cursor.fetchall()    
    id = 0
    for row in results:
        id,name,info = row.values() 
        if id != 0:
            sql = "select id,name,info from message where data_id = {};".format (id)
            cursor.execute(sql)
            results = cursor.fetchall()    
            for row in results:
                id,name,info = row.values() 
                data_message[name] = info  
    return data_message 
  
def get_message_tovar       (message_info,status_input,setting_bot,id_list,info_tovar):                                             ###  Формируем карточку товара    
    message         = get_message (message_info,"Шаблон товара")                                                                    ###  Список значений исходящего сообщения
    message_text    = message['Текст']
    message_text    = message_text.replace('##name##'    ,str(name)) 
    message_text    = message_text.replace('##about##'   ,str(about)) 
    message_text    = message_text.replace('##catalog##' ,str(catalog)) 
    message_text    = message_text.replace('##comment##' ,str(comment)) 
    message_text    = message_text.replace('##currency##',str(currency)) 
    message_text    = message_text.replace('##picture##' ,str(picture)) 
    message_text    = message_text.replace('##pocket##'  ,str(pocket)) 
    message_text    = message_text.replace('##price##'   ,str(price))
    message_text    = message_text.replace('##quantity##',str(quantity)) 
    key             = {}
    return message_text,key
   
##################################################################################################################################################################################################    
   
def print_operator          (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                               ###  Печать команды оператор в json
    pass
   
def executing_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                               ###  Выполнение команды оператор в json
    
    if operation == 'catat':                                                                                                        ###  Нажата кнопка в списке
        ### id_list - id товара в списке
        ### id_sql  - id sql запроса
        ### Мы получили код товара и код запроса sql. Теперь нам нужно собрать информацию о товаре. 
        ### Шаг назад это возврашение в список, а именно id_sql.
        
        info_tovar = get_info_tovar (message_info,status_input,setting_bot,id_list)                                                 ###  Получаем библиотеку информации о товаре. Информация может собиратся из нескольких баз и таблиц.
        if info_tovar['catalog'] == 1:                                                                                              ###  Это каталог выводим. Выводим список всех товаров в который указан данный каталог 
            sql      = "select id,`info` from `service` where %s limit %s offset %s"
            ask      = "name_catalog = {} ".format (info_tovar['name_catalog'])
            limit    = 10
            offset   = 0            
            back     = id_sql                                                                                                       ###  Передаем номер сообщения для возврата из каталога
            id_sql   = save_sql     (message_info,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения            
            key_list = complite_key (message_info,id_sql,sql,ask,limit,offset,back,'catat')
        if info_tovar['catalog'] == 0:                                                                                              ###  Это товар выводим информацию о товаре
            message,key = get_message_tovar (message_info,status_input,setting_bot,id_list,info_tovar)
            
    if operation == 'back':                                                                                                         ###  Нажата кнопка вернутся назад 
        sql,ask,limit,offset,back = get_sql (message_info,id_sql)
        id_sql                    = id_sql         
        key_list                  = complite_key (message_info,id_sql,sql,ask,limit,offset,back,'catat')
        
def executing_program_json  (message_info,status_input,setting_bot):                                                                ###  Разбор команды оператор в json
    import iz_bot                                                                                                                   ###  Основные функции программы
    import json
    callback        = message_info.setdefault   ('callback','')                                                                     ###  Имя нажатой кнопки 
    json_string     = iz_bot.change_back        (callback.replace('i_',''))
    data_json       = json.loads                (json_string)
    operation       = data_json.setdefault      ('o','')                                                                            ###  Название команды переданной  в json
    id_list         = data_json.setdefault      ('i','')                                                                            ###  Параметр id переданной       в json    
    id_sql          = data_json.setdefault      ('s','')                                                                            ###  Параметр id_sql переданной   в json 
    id_back         = data_json.setdefault      ('b','')                                                                            ###  Параметр id_back переданной  в json
    print_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back)                                    ###  Печатаем команды полученные  в json
    executing_operator  (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back)                                    ###  Выполняем команды полученные в json
    
##################################################################################################################################################################################################   
   
def print_status            (message_info,status_input,setting_bot):
    print ('[+] Начальные настройки по текущиму пользователю.')
    for line in status_input:
        print ('        [+]',line,'-',status_input[line])
    status     = status_input.setdefault('status','')
    
def executing_admin         (message_info,status_input,setting_bot):
    if status_input.setdefault('Админ','') == 'Да':
        if message_in   == '/admin':
            user_id     = message_info.setdefault('user_id','') 
            message     = setting_bot .setdefault ("Сообщение администратору","Вы администратор бота")
            answer      = save_message (message_info,setting_bot,user_id,message)
            message_out = gets_message (message_info,setting_bot,user_id,message)
            markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
            answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
    
def testing_double          (message_info,status_input,setting_bot):
    message_in      =  message_info['message_in']
    if message_in   == setting_bot ['message_in']:
        user_id     = message_info.setdefault('user_id','') 
        message     = setting_bot .setdefault ("Сообщение повторное нажатие клавиши","Повторное нажатие клавиши")
        answer      = save_message (message_info,setting_bot,user_id,message)
        message_out = gets_message (message_info,setting_bot,user_id,message)
        markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
        answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
    save_data   = [['message_in',message_in]] 
    status_input = user_save_data (message_info,status_input,save_data)
    
def testing_blocking        (message_info,status_input,setting_bot):                                        ### Проверяем ввод оснавных параметров пользователя
    status      = user_save_data.setdefault('Статус','')                                                    ### Проверяем статус - возможно пользователь ввел значение
    db,cursor   = iz_bot.connect (namebot)
    sql  = "select id,name,answer from ask where name = '{}' ".format(status)
    cursor.execute(sql)
    data = cursor.fetchall()
    id   = 0 
    for rec in data:
        id,name,message_answer = rec.values()
    if id != 0:
        user_id         = message_info.setdefault('user_id','') 
        message         = setting_bot .setdefault (message_answer,message_answer)
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)
        markup          = gets_key       (message_info,setting_bot,user_id,message_out['Меню'])
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup)
        status_input    = user_save_data (message_info,status_input,[["Статус",""]])
    db,cursor = iz_bot.connect (namebot)                                                                    ### Задаем вопрос из списка вопросов. 
    sql = "select id,name from ask where 1=1 ".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name = rec.values()
        if status_input.setdefault (name,'') == '': 
            break
        name    = ''
    if name != '':      
        user_id         = message_info.setdefault('user_id','') 
        message         = setting_bot .setdefault (name,name)
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)
        markup          = gets_key       (message_info,setting_bot,user_id,message_out['Меню'])
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup)
        status_input    = user_save_data (message_info,status_input,[["Статус",name]])
    return answer
        
       
    
def save_info_refer         (message_info,status_input,setting_bot):
    pass
    
def save_info_user          (message_info,status_input,setting_bot):
    pass
    
def save_message_user       (message_info,status_input,setting_bot):
    pass
    
def executing_status        (message_info,status_input,setting_bot):
    if status_input.setdefault('Статус','') == 'Ввод города':                                                                       ###  Пример работы статусного сообщения
        pass
        
def executing_message       (message_info,status_input,setting_bot):
    if message_in   == 'Каталог':                                                                                                   ###  Пример работы тестового сообщения 
        sql      = "select id,`info` from `service` where %s limit %s offset %s"
        limit    = 10
        offset   = 0
        back     = ''
        id_sql   = save_sql     (message_info,"Список товаров",sql,limit,offset,back)                                               ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
        key_list = complite_key (message_info,id_sql,sql,ask,limit,offset,back,'catat')                                             ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки
        
def executing_program       (message_info,status_input,setting_bot):
    if callback.find ('i_') != -1:                                                                                                  ###  Кнопка которая передала в json информацию
        executing_program_json (message_info,status_input,setting_bot)
    if callback == 'save_message':                                                                                                  ###  Пример работы команды кнопки
        pass

def analis                  (message_info,status_input,setting_bot):
    pass

def save_out_message        (message_info,status_input,setting_bot):
    pass
   
##################################################################################################################################################################################################
   
def start_prog (message_info):                                                                                                      ###  Получение сигнала от бота. Расшифровка команды и сообщения
    status_input = iz_bot.user_get_data    (message_info,get_data)                                                                  ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    setting_bot  = iz_bot.get_setting      (message_info)                                                                           ###  Получение из базы информации по боту. Параметры и данные.
    status       = status_input.setdefault ('status','')                                                                            ###  Получаем основной статус пользователя например о том что он вводит данные и какие
    print_status            (message_info,status_input,setting_bot)                                                                 ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    executing_admin         (message_info,status_input,setting_bot)                                                                 ###  Выполнение команды администраторов бота 
    testing_double          (message_info,status_input,setting_bot)                                                                 ###  Проверка на повторно нажатые клавиши
    testing_blocking        (message_info,status_input,setting_bot)                                                                 ###  Проверка заполнения данных
    testing_time            (message_info,status_input,setting_bot)                                                                 ###  Проверка работы в определенное время суток
    save_info_refer         (message_info,status_input,setting_bot)                                                                 ###  Записываем информацию по полученной реферальной ссылке 
    save_info_user          (message_info,status_input,setting_bot)                                                                 ###  Обновляем информацию по текущему пользователю 
    save_message_user       (message_info,status_input,setting_bot)                                                                 ###  Записываем входяшие сообшение для протоколирования
    executing_status        (message_info,status_input,setting_bot)                                                                 ###  Выполняем на действие статуса бота. Например ввод данных
    executing_message       (message_info,status_input,setting_bot)                                                                 ###  Выполняем код прописанный в базе данных
    executing_program       (message_info,status_input,setting_bot)                                                                 ###  Выполняем код прописанный в этом файле
    analis                  (message_info,status_input,setting_bot)                                                                 ###  Выполнение кода если нет действия на сообщения
    save_out_message        (message_info,status_input,setting_bot)                                                                 ###  Протоколирование исходящего сообщения



