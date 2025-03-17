
### message         - Список данных сообщение полученный из базы данных
### message_out     - Текст отправленного сообшения 
### message_name    - Название текстового сообшения
### message_text    - Текст сообщения для обработки

### informanion     - Список информации о товаре

### Узко специализированные программы ###


def connect_postgres        (namebot):  
    import psycopg2
    db = psycopg2.connect(dbname = namebot, user='postgres', password='podkjf4', host='localhost')
    cursor = db.cursor()       
    return db,cursor 

def list_find_menu  (message_info,status_input,setting_bot):
    user_id         = message_info['user_id']
    sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
    limit           = 20
    offset          = 0
    back            = ''
    ask             = "name = 'Поиск'"
    id_sql          = save_sql     (message_info,status_input,setting_bot,"Список поиска",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
    markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'find')                                                      ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
    return markup_list 

def change_simvol   (message_out):
    message_out = message_out.replace ('<','#')
    message_out = message_out.replace ('>','#')
    #message_out = message_out.replace ('/','.')
    message_out = message_out.replace ('#b#','<b>')
    message_out = message_out.replace ('#/b#','</b>')
    message_out = message_out.replace ('#.b#','</b>')
    message_out = message_out.replace ('#code#','<code>')
    message_out = message_out.replace ('#/code#','</code>')
    #message_out = message_out.replace ('<b>','')
    #message_out = message_out.replace ('</b>','')
    return message_out

def change_word     (message_text,new):
    #message_text  = message_out
    message_text = message_text.replace('%%code%%'      ,str(new['ID']))  
    message_text = message_text.replace('%%title%%'     ,str(new['title']))  
    message_text = message_text.replace('%%url%%'       ,str(new['url']))
    message_text = message_text.replace('%%title02%%'   ,str(new['title02']))
    message_text = message_text.replace('%%title03%%'   ,str(new['title03']))
    message_text = message_text.replace('%%magnet%%'    ,str(new['magnet']))
    message_text = message_text.replace('%%main%%'      ,str(new['text']))
    message_text = message_text.replace('%%rek%%'       ,str('https://t.me/nnm_a123_bot'))
    #message_out = message_text; 
    return message_text

def message_slip_tg (message_info,new,setting):
    import iz_bot
    #info_data    = {'Имя':'Главное сообщение телеграмм','Сохранить':'Да'}
    #message_out  = iz_bot.get_message (message_info,info_data)['Текст']
    message_out = setting['message01']
    message_out = change_word (message_out,new)
    dl = len (message_out)
    if dl > 800:
        message_out_01 = setting['message02']
        message_out_01 = change_word (message_out_01,new)        
        message_out_02 = setting['message03']
        message_out_02 = change_word (message_out_02,new)        
    else:    
        message_out_01 = message_out
        message_out_02 = ''
        
    message_out_01 = change_simvol (message_out_01)
    message_out_02 = change_simvol (message_out_02)
        
    return [message_out_01,message_out_02]

def message_send_tg (chat_id,token_avtor,message_out,picture):
    import requests
    message_out_01 = message_out[0]
    message_out_02 = message_out[1]
    params = {}
    method = "sendPhoto"
    params['chat_id'] = int(chat_id) ##-1001644105615
    params['caption'] = str(message_out_01)
    params['parse_mode'] = 'HTML'
    parsed_string = ''
    print ('[+] picture:',picture)
    if picture != '':
        file_path = 'W:/Picture/'+picture
        try:
            file_opened = open(file_path, 'rb')
        except:    
            file_path = 'W:/Picture_9/'+picture
            file_opened = open(file_path, 'rb')
        files = {'photo': file_opened}
        token_tg = token_avtor #'6422168947:AAGy4pzndN1WYgMyFRf_mVXF6gEptDpzLz0'
        url='https://api.telegram.org/bot{0}/{1}'.format(token_tg, method)   
        response = requests.post(url, params, files=files)
        parsed_string = response.json() 
    else:
        method = "sendMessage"
        params['text'] = str(message_out_01)
        token_tg = token_avtor
        url  = 'https://api.telegram.org/bot{0}/{1}'.format(token_tg, method)
        resp = requests.post(url, params) 
        answer = resp.json()
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ( answer)
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ('')  
    #parsed_print   ('Отправка сообщения в группу',parsed_string)
    print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
    print ( parsed_string)
    print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
    print ('')       
    if message_out_02 != '':
        method = "sendMessage"
        params = {}
        params['chat_id'] = int(chat_id)                  
        params['text'] = str(message_out_02)
        params['parse_mode'] = 'HTML'
        url  = 'https://api.telegram.org/bot{0}/{1}'.format(token_tg, method)
        try:
            resp = requests.post(url, params) 
        except:    
            print ('[+] Ожидание перед повторным отправлением телеграмм каталоги 10 сек.')
            time.sleep (10)
            resp = requests.post(url, params) 
        answer = resp.json()
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ( answer)
        print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
        print ('')        
    return parsed_string

def send_telegram_message (message_info,status_input,setting_bot,list_answer):
    import iz_bot
    namebot = message_info.setdefault ('namebot','')
    setting = iz_bot.get_setting_prog ('nnm-club')
    user_id = message_info['user_id']
    for rec in list_answer: 
        id,code,name,text,title02,title03,magnet,picture  =  rec
        new = {}
        new['ID']               = code
        new['url']              = ''
        new['title']            = name.strip()
        new['text']             = text.strip()
        new['picture_url']      = ''    
        new['picture']          = picture.strip()
        new['title_page']       = ''
        new['magnet']           = magnet.strip()
        new['title02']          = title02.strip()
        new['title03']          = title03.strip()
        message_info = {'namebot':namebot}
        token_avtor = setting_bot.setdefault ('Токен','')
        message_out = message_slip_tg (message_info,new,setting) 
        answer      = message_send_tg (user_id,token_avtor,message_out,picture)   
    return answer

def execution_procedure (message_info,status_input,setting_bot,word):
    import iz_bot
    db,cursor       = iz_bot.connect_postgres ()
    sql             = "select id,code,name,text,title02,title03,magnet,picture from torrent where (name like '%{}%' or text like '%{}%' ) and picture <> 'Нет картинки' and pic_type <> 'Файл не найден ' order by id desc limit 10;".format (word,word)
    cursor.execute(sql)
    data            = cursor.fetchall()
    answer          = []
    for rec in data:
        id,code,name,text,title02,title03,magnet,picture = rec
        answer.append ([id,code,name,text,title02,title03,magnet,picture])        
    return answer
    
def execution_procedure_sql (message_info,status_input,setting_bot,sql):
    import iz_bot
    db,cursor       = iz_bot.connect_postgres ()
    cursor.execute(sql)
    data            = cursor.fetchall()
    answer          = []
    for rec in data:
        id,code,name,text,title02,title03,magnet,picture = rec
        answer.append ([id,code,name,text,title02,title03,magnet,picture])        
    return answer    
    
def history_order (message_info,status_input,setting_bot,answer):
    if answer.setdefault('name','') == 'Поиск торрент':
        namebot     = message_info.setdefault('namebot','')
        user_id     = message_info['user_id']
        ask_info    = get_active_ask (message_info,status_input,setting_bot,'Новое сообщение в боте')
        active1     = answer.setdefault('active1','')
        active2     = answer.setdefault('active2','')
        active3     = answer.setdefault('active3','')
        active4     = answer.setdefault('active4','')
        active5     = answer.setdefault('active5','')
        from iz_bot import connect as connect
        db,cursor   = connect (namebot)
        import time
        unixtime    = int(time.time ())
        sql         = "INSERT INTO history (`name`,`user_id`,`active1`,`active2`,`active3`,`active4`,`active5`,unixtime) VALUES ('{}','{}','{}','{}','{}','{}','{}',{})".format (answer['name'],user_id,active1,active2,active3,active4,active5,unixtime)
        cursor.execute(sql)
        db.commit()

def get_order_psg (message_info,status_input,setting_bot,answer,id_list):
    namebot     = message_info.setdefault('namebot','')
    user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
        
    sql = "select id,info,name,master,service from order_master where id = {} ;".format (id_list)
    cursor.execute(sql)
    results  = cursor.fetchall()
    #data_id  = 0
    #for row in results:
    #    id,name,info,data_id = row.values()
    cursor.execute(sql)
    db.commit()
    return results 

def update_order_psg (message_info,status_input,setting_bot,answer,id,name,info):
    namebot     = message_info.setdefault('namebot','')
    user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
    sql = "UPDATE order_master SET {} = '{}' WHERE id = {}".format(name,info,id)
    cursor.execute(sql)
    db.commit()
    return id 

def create_order_psg (message_info,status_input,setting_bot,answer):
    namebot     = message_info.setdefault('namebot','')
    user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
    sql         = "INSERT INTO order_master (name,info,user_id,status) VALUES ('','','{}','')  RETURNING id".format (user_id)
    cursor.execute(sql)
    result = cursor.fetchone()
    lastid = result[0]
    db.commit()
    return lastid 

def create_order (message_info,status_input,setting_bot,answer):

    
    if answer.setdefault('name','') == 'Новое сообщение в боте':
        ask_info    = get_active_ask (message_info,status_input,setting_bot,'Новое сообщение в боте')
        namebot     = message_info.setdefault('namebot','')
        active1     = answer.setdefault('active1','')
        active2     = answer.setdefault('active2','')
        active3     = answer.setdefault('active3','')
        active4     = answer.setdefault('active4','')
        active5     = answer.setdefault('active5','')
        from iz_bot import connect as connect
        db,cursor   = connect (namebot)
        sql         = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES (0,'','{}','Имя')".format (active1)
        cursor.execute(sql)
        db.commit()
        lastid      = cursor.lastrowid 
        sql         = "UPDATE message SET data_id = {} WHERE id = {}".format (lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql         = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES ({},'','{}','Текст')".format (lastid,active2)
        cursor.execute(sql)
        db.commit()
        sql         = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES ({},'','{}','Меню')".format (lastid,active3)
        cursor.execute(sql)
        db.commit()
        user_id     = message_info['user_id']
        message     = setting_bot.setdefault ("Сообщение ввод итоговое",ask_info['message'])                           ###  Выводим текст информированный что создано задание
        nswer_null  = save_message (message_info,setting_bot,user_id,message)
        message_out = gets_message (message_info,setting_bot,user_id,message)
        answer_null = send_message (message_info,setting_bot,user_id,message_out['Текст'],{})
        
##################################################################################################################################################################################################
def complite_key_for_name (name):
    if name == 'Ввести данные':
        key                 = {}
        key['Кнопка 11']    = 'Ввести данные' 
        key['Команда 11']   = 'Ввести данные' 
    return key    

def get_message_in_id       (message_info,status_input,setting_bot,id_list):
    informanion = {}
    namebot     = message_info.setdefault('namebot','')
    from iz_bot import connect as connect
    db,cursor = connect (namebot)
    sql = "select id,name,info,data_id from message where id = {} ;".format (id_list)
    cursor.execute(sql)
    results  = cursor.fetchall()
    data_id  = 0
    for row in results:
        id,name,info,data_id = row.values() 
    sql = "select id,name,info,data_id from message where data_id = {} ;".format (data_id)
    cursor.execute(sql)
    results = cursor.fetchall()  
    for row in results:
        id,name,info,data_id = row.values() 
        informanion[name] = info
    return informanion  

def get_message_text        (message_info,status_input,setting_bot,informanion):  
    user_id         = message_info.setdefault('user_id','') 
    message_name    = setting_bot .setdefault ("Шаблон выводимого сообщения","Шаблон выводимого сообщения")
    answer          = save_message (message_info,setting_bot,user_id,message_name)
    message         = gets_message (message_info,setting_bot,user_id,message_name)
    list            = get_list_change  (message_info,status_input,setting_bot,message.setdefault('Текст',''))                                                                      ###  Список значений исходящего сообщения
    message_text    = message.setdefault('Текст','')
    message_text    = complite_message_add_list (message_info,status_input,setting_bot,message_text,informanion,list)
    #markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
    #answer          = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),"")
    ##status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",""]])
    return message_text

######################################################################### Получение всех данных по настройкам data_id #########################################################################################################################

def get_message_setting     (message_info,status_input,setting_bot,info_service):  ### Вывод сообщения у которого заполнены все переменные. В данном случаи настройки  
    
    user_id             = message_info.setdefault('user_id','')
    message             = setting_bot.setdefault  ("Вывести настройки","Вывести настройки")
    answer              = save_message            (message_info,setting_bot,user_id,message)
    message_in          = gets_message            (message_info,setting_bot,user_id,message)
    message_out = ""
    list_change         = get_list_change         (message_info,status_input,setting_bot,message_in['Текст'])
    for change in list_change:
        message_out = message_out.replace (change,info_service.setdefault (change,""))
    message_out     = message_out.replace ("##","")    
    markup          = complite_list_key (message_info,status_input,setting_bot,"Настройка")                                                 ####
    return message,markup
    
def get_message_main_menu   (message_info,status_input,setting_bot,info_service):
    message             = setting_bot.setdefault  ("Вывести список меню","Вывести список меню")
    answer              = save_message            (message_info,setting_bot,user_id,message)
    message_out         = gets_message            (message_info,setting_bot,user_id,message)
    list_change         = get_list_change         (message_info,status_input,setting_bot,message_out)
    for change in list_change:
        message_out = message_out.replace (change,info_service.setdefault (change,""))
    message_out     = message_out.replace ("##","")
    key = {}
    key['Кнопка 11']  = "Кнопка 11"
    key['Кнопка 12']  = "Кнопка 12"
    key['Кнопка 21']  = "Кнопка 21"
    key['Кнопка 22']  = "Кнопка 22"
    key['Команда 11'] = "Команда 11"
    key['Команда 12'] = "Команда 12"
    key['Команда 21'] = "Команда 21"
    key['Команда 22'] = "Команда 22"
    markup = key_type_keybord (key)
    return message,markup

def get_info_product        (message_info,status_input,setting_bot,id_list):                                                                                    ###  Получаем информацию по товару
    from iz_bot import connect as connect
    namebot     = message_info.setdefault('namebot','')
    answer  = {}    
    db,cursor = connect (namebot)
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
       
def get_info_product_time   (message_info,status_input,setting_bot,date_time):                                                                                  ###  Получаем информацию по товару в указанное время
    from iz_bot import connect as connect
    namebot     = message_info.setdefault('namebot','')
    answer  = {}    
    db,cursor = connect (namebot)
    sql = "select id,name,about,catalog,comment,currency,picture,pocket,price,quantity from service where date_time > {} limit 1".format (date_time)
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

def get_info_tovar          (message_info,status_input,setting_bot,id_list):
    info_tovar = {'Имя':'Пробный товар'}
    info_tovar['catalog'] = 0
    return info_tovar

##################################################################################################################################################################################################

def send_user_message_v1    (message_info,status_input,setting_bot,name_message):
    user_id     = message_info.setdefault('user_id','') 
    message     = setting_bot .setdefault (name_message,name_message)
    answer      = save_message (message_info,setting_bot,user_id,message)
    message_out = gets_message (message_info,setting_bot,user_id,message)
    markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
    answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
    return answer
    
def send_user_message_v2    (message_info,status_input,setting_bot,user_id,message_text,picture,markup):
    answer      = send_message (message_info,setting_bot,user_id,message_text,markup)
    return answer
           
def statistic_complite      (namebot,sql,name):
    from iz_bot import connect_postgres as connect_postgres
    db,cursor    = connect_postgres ()
    cursor.execute(sql)
    data = cursor.fetchall()
    sum  = 0
    for rec in data:
        #id,name = rec 
        sum  = sum  + 1
    import datetime
    import time
    now                 = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y')
    unixtime            = int(time.time())
    import iz_bot
    db,cursor           = iz_bot.connect (namebot)
    sql = "INSERT INTO statistica (`name`,`unixtime`,`date`,`status`,`info`) VALUES ('{}',{},'{}','','{}')".format (name,unixtime,current_date_string,sum)
    cursor.execute(sql)
    db.commit()
    return sum    

def get_ask_nober           (message_info,status_input,setting_bot,ask): 
    namebot   = message_info.setdefault ('namebot','') 
    from iz_bot import connect as connect 
    db,cursor = connect (namebot)                                                                                                                               ### Задаем вопрос из списка вопросов. 
    sql       = "select id,name from ask where id = {} ".format(ask)                                                                                            ### Получаем данные для вопроса
    answer    = {}
    cursor.execute(sql)
    data      = cursor.fetchall()
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name = rec
        else:
            id,name = rec.values()
        answer['id']    = id        
        answer['name']  = name        
    return answer    
                                       
def send_message_ask        (message_info,status_input,setting_bot,ask):                                                                                        ### Процедура которая задает вопрос по номеру
    ask_name        = get_ask_nober (message_info,status_input,setting_bot,ask) 
    user_id         = message_info.setdefault('user_id','') 
    message         = setting_bot .setdefault (ask_name['name'],ask_name['name'])
    answer          = save_message   (message_info,setting_bot,user_id,message)
    message_out     = gets_message   (message_info,setting_bot,user_id,message)
    markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
    answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
    print ('[+] Меняе статус сообшения на ввод данный.',ask_name['name'])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",ask_name['name']]])
    return answer,status_input 

def get_list_product        (message_info,status_input,setting_bot,message):                                                                                    ###  Формируем список продуктов, длинный список
    user_id        = message_info['user_id']
    message        = setting_bot .setdefault ("Шапка отчета","Шапка отчета")
    answer         = save_message (message_info,setting_bot,user_id,message)
    message_hat    = gets_message (message_info,setting_bot,user_id,message)
    message        = setting_bot .setdefault ("Строка отчета","Строка отчета")
    answer         = save_message (message_info,setting_bot,user_id,message)
    message_line   = gets_message (message_info,setting_bot,user_id,message)
    message        = setting_bot .setdefault ("Подвал отчета","Подвал отчета")
    answer         = save_message (message_info,setting_bot,user_id,message)
    message_result = gets_message (message_info,setting_bot,user_id,message)
    list_operation = get_list_operation (message_info,status_input,setting_bot,[])
    list_operation = get_user_operation (message_info,status_input,setting_bot,list_operation)
    list_line      = get_user_operation (message_info,status_input,setting_bot,list_operation)
    list_message  = get_user_operation (message_info,status_input,setting_bot,list_line)
    answer = send_message   (message_info,setting_bot,user_id,message_hat,markup)
    for message_out in list_message:
        answer = send_message   (message_info,setting_bot,user_id,message_out,markup)
    answer = send_message   (message_info,setting_bot,user_id,message_result,markup)    

def send_message_user       (message_info,status_input,setting_bot,user_id_list,message_id,wait,change):                                                        ###  Отправка сообщения пользователям (Уникальное)
    message_send         = get_message_send (message_info,status_input,setting_bot,user_id_list,message_id)
    message_01           = message_send['message_01']
    markup01             = message_send['markup01']
    picture01            = message_send['picture01']
    message_02           = message_send['message_02']
    markup02             = message_send['markup02']
    picture02            = message_send['picture02']
    for line in user_id_list:    
        if test_send_message(message_info,status_input,setting_bot,user_id,message_id,'Номер 1') == True:
            if picture01 != '':
                answer = send_sendPhoto (message_info,setting_bot,user_id,message_01,picture01,markup01)
                save_log_messaage       (message_info,status_input,setting_bot,user_id,message_id,'Номер 1',answer) 
            else:
                if message_01 != '':
                    answer = send_message   (message_info,setting_bot,user_id,message_01,markup01)
                    save_log_messaage       (message_info,status_input,setting_bot,user_id,message_id,'Номер 1',answer)
        if test_send_message(message_info,status_input,setting_bot,user_id,message_id,'Номер 2') == True:        
            if picture02 != '':
                answer = send_sendPhoto (message_info,setting_bot,user_id,message_02,picture02,markup02)
                save_log_messaage       (message_info,status_input,setting_bot,user_id,message_id,'Номер 2',answer) 
            else:
                if message_02 != '':
                    answer = send_message   (message_info,setting_bot,user_id,message_02,markup02)
                    save_log_messaage       (message_info,status_input,setting_bot,user_id,message_id,'Номер 2',answer)
                   
def delete_send_message_user(message_info,status_input,setting_bot,user_id,answer,wait):                                                                        ###  Удаление сообшения через определенное время
    pass

##################################################################################################################################################################################################

def save_order_info         (message_info,setting_bot,user_id,nomer_order,colomn,info):
    if nomer_order == 0:
        import time
        unixtime    = int(time.time ())
        namebot     = message_info.setdefault ('namebot','') 
        from iz_bot import connect as connect 
        db,cursor = connect (namebot)
        sql = "INSERT INTO `order` (date,user_id,unixtime,menu01,menu02,menu03,status,regim) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format ()
        sql_save = ('',user_id,unixtime,'','','','','')
        cursor.execute(sql,sql_save)
        db.commit()
        lastid = cursor.lastrowid
        nomer_order = lastid
    if  colomn != '':  
        sql = "UPDATE `order` SET {} = %s WHERE id = {} ".format (colomn,info)
        sql_save = (picture_download,ID)
        cursor.execute(sql,sql_save)    
        db.commit()     
    return nomer_order    

def update_info_main_menu   (message_info,status_input,setting_bot,nomer,info_service):
    sql     = "select id,name,info from `order` where id = {} limit 1".format(nomer)                                                                            ###  Обновляем информацию по ордеру
    cursor.execute(sql)
    data    = cursor.fetchall()
    for rec in data: 
        id,menu01,menu02,menu03 = rec.values() 
        info_service['id_order']  = id
        info_service['id_menu01'] = menu01
        info_service['id_menu02'] = menu02
        info_service['id_menu03'] = menu03
    return info_service

def get_setting             (message_info,setting_bot):
    namebot = message_info['namebot']
    from iz_bot import connect as connect
    db,cursor = connect (namebot)
    answer = setting_bot
    sql = "select id,name,info from setting where 1=1".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        if str(type(row)) == "<class 'tuple'>":
            id,name,info = row
        else:    
            id,name,info = row.values() 
        answer[name] = info
    return answer

def user_get_data           (message_info,setting_bot,user_id):
    namebot = message_info['namebot']
    from iz_bot import connect as connect
    db,cursor = connect (namebot)
    answer = {}
    sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' ;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        if str(type(row)) == "<class 'tuple'>":
            id,name,info,data_id = row
        else:    
            id,name,info,data_id = row.values() 
        sql = "select id,name,info from users where data_id = '{}' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for rew in results:
            if str(type(row)) == "<class 'tuple'>":
                id,name,info = rew
            else:    
                id,name,info = rew.values() 
            answer[name] = info
    return answer

def complite_message_add_list (message_info,status_input,setting_bot,message_text,informanion,list):                                                            ### Заменяем в тексте ##
    for line in list:
        message_text    = message_text.replace('##'+line+'##',str(informanion.setdefault (line,''))) 
    return message_text

def get_list_change         (message_info,status_input,setting_bot,message):                                                                                    ###  Получение всех меток замены             
    list = []
    body  = message
    nm = 0
    while body.find ('##') != -1:
        nm = nm + 1
        nomer_begin     = body.find ("##")
        name_body       = body[nomer_begin+2:]               
        nomer_finishe   = name_body.find ("##")
        name            = name_body[:nomer_finishe]
        list.append (name)        
        body            = name_body[nomer_finishe+2:]
        if nm > 5:
            break
    return list

def change_message          (message_info,status_input,setting_bot,message,list_change,element):                                                                ###  Меняем в сообшение значение на параметры             
    for line in list_change:
        message = message.replace ("##"+str(line)+"##",element.setdefault(line,''))    
    return message
       
def get_service             (message_info,status_input,setting_bot,data_id):                                                                                    ###  Получение информации о услугах  
    from iz_bot import connect as connect
    namebot    = message_info.setdefault('namebot','')
    db,cursor = connect (namebot)
    sql             = "select id,name,`info` from `service` where data_id = {} ".format (data_id)
    print ('[SQL]',sql)
    answer         = {}
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,info = rec.values() 
        print ('[name]',name)
        answer[name] = str(info)
    return answer  
        
def get_time_set            (message_info,status_input,setting_bot,name):                                                                                       ###  Процедура для замера времени
    import time
    unixtime = int(time.time ())
    status_input    = user_save_data (message_info,status_input,setting_bot,[[name,unixtime]])
    ##status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",ask_name['name']]])
    return status_input
        
def get_time_up             (message_info,status_input,setting_bot,name):                                                                                       ###  Проверка что время прошло достаточно  
    import time
    import iz_bot
    unixtime        = int(time.time ())
    status_input    = iz_bot.user_get_data    (message_info,{}) 
    limit           = int(status_input.setdefault (name),0)
    answer = unixtime - limit;
    return answer 
      
def get_message_send        (message_info,status_input,setting_bot,user_id_list,message_id):                                                                    ###  Получаем сообщения для рассылки  
    from iz_bot import connect as connect
    namebot    = message_info.setdefault('namebot','')
    db,cursor = connect (namebot)
    sql = "select id,message_01,message_02,markup01,markup02,picture01,picture02 from send_message where id = {}".format(message_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,message_01,message_02,markup01,markup02,picture01,picture02 = rec.values() 
    answer = {}    
    answer['message_01']    = message_01
    answer['message_02']    = message_02
    answer['markup01']      = markup01
    answer['markup02']      = markup02
    answer['picture01']     = picture01
    answer['picture02']     = picture02
    return answer

def save_log_messaage       (message_info,status_input,setting_bot,user_id,message_id,status,answer):
    import time
    unixtime = int(time.time())
    sql = "INSERT INTO `log_message` (`unixtime`,`user_id`,message_id,label,answer) VALUES (%s,%s,%s,%s,%s)".format ()
    sql_save = (unixtime,user_id,message_id,status,answer)
    cursor.execute(sql,sql_save)
    lastid = cursor.lastrowid 
    db.commit() 

def test_send_message       (message_info,status_input,setting_bot,user_id,message_id,label):
    from iz_bot import connect as connect
    namebot    = message_info.setdefault('namebot','')
    db,cursor = connect (namebot)
    sql = "select id from `log_message` where name = '{}' and label = '{}' ".format(message_id,label)
    cursor.execute(sql)
    results = cursor.fetchall()   
    answer = True
    change = name
    for rec in results:
        id = rec['id']
        answer = False
    return answer    

def change_back             (message_info,status_input,setting_bot,name):                                                                                       ###  Замена символа в предложении
    from iz_bot import connect as connect
    namebot     = message_info.setdefault('namebot','')
    db,cursor   = connect (namebot)
    sql         = "select id,`change` from `key` where name = '{}' ".format(name)
    cursor.execute(sql)
    results     = cursor.fetchall()   
    id = 0
    change = name
    for rec in results:
        id,change = rec.values() 
    if id == 0:
        sql = "INSERT INTO `key` (`name`,`change`,`status`) VALUES ('{}','{}','{}')".format (name,name,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit()  
    return change 

def get_ask_nomer           (message_info,status_input,setting_bot):
    from iz_bot import connect as connect
    user_id   = message_info.setdefault ('user_id','')
    namebot   = message_info.setdefault ('namebot','')
    db,cursor = connect (namebot)                                                                                                            ### Задаем вопрос из списка вопросов. 
    sql         = "select id,name from ask where 1=1 order by id ".format()
    ask         = 0                                                                                                                                 
    cursor.execute(sql)
    data        = cursor.fetchall()
    name        = ''
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name = rec
        else:
            id,name = rec.values()
        if status_input.setdefault (name,'') == '': 
            ask = id
    return ask 

def get_ask_nomer_status    (message_info,status_input,setting_bot,status):
    namebot     = message_info.setdefault ('namebot','') 
    from iz_bot import connect as connect  
    db,cursor   = connect (namebot)
    sql  = "select id,name,answer from ask where name = '{}' ".format(status)                       
    cursor.execute(sql)
    data = cursor.fetchall()
    answer = {}
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":    
            id,name,message_answer = rec
        else:    
            id,name,message_answer = rec.values()
        answer['id']             = id
        answer['name']           = name
        answer['message_answer'] = message_answer    
    return answer        
            
##################################################################################################################################################################################################    

def data_sql                            (message_info,status_input,setting_bot,id_sql,info_data):
    namebot    = message_info.setdefault('namebot','')
    import iz_bot
    db,cursor = iz_bot.connect (namebot)
    list = info_data.keys()
    for line in list:
        element = info_data[line]
        name    = line
        sql = "select id,name,info,data_id from data_info where data_id = {} and name = '{}' ".format(id_sql,name)
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data:
            id,sql,ask,limit,offset,back = rec.values() 
        if id == 0:
            sql = "INSERT INTO data_info (name,info,data_id,status) VALUES (%s,%s,%s,%s)".format ()
            sql_save = (name,element,id_sql,'')
            result = cursor.execute(sql,sql_save)
            db.commit()
        else:
            sql = "UPDATE data_info SET info = '{}' WHERE data_id = {} and name = '{}'".format(id_sql,name)
            cursor.execute(sql)
            db.commit()
    return info_data        
                    
def get_sql_data                        (message_info,status_input,setting_bot,id_sql,info_data):  
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,info,data_id from data_info where data_id = {} ".format(id_sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,info,data_id = rec.values() 
        info_data [name] = info
    return info_data
    
def get_active_ask                      (message_info,status_input,setting_bot,name):
    namebot     = message_info.setdefault ('namebot','') 
    from iz_bot import connect as connect 
    db,cursor   = connect (namebot) 
    sql         = "select id,name,`order`,active1,type1,message11,message12,active2,type2,message21,message22,active3,type3,message31,message32,message,info1,info2,info3,active4,active5,info4,info5,message41,message42,message51,message52,type4,type5  from active where name = '{}' ".format(name)                                                                                            ### Получаем данные для вопроса
    answer      = {}
    id          = 0
    name        = ''
    order       = ''    
    active1     = ''
    type1       = ''    
    message11   = ''
    message12   = ''
    active2     = ''
    type2       = ''    
    message21   = ''
    message22   = ''
    active3     = ''
    type3       = ''    
    message31   = ''
    message32   = ''
    message41   = ''
    message42   = ''
    message51   = ''
    message52   = ''
    message     = ''  
    info1       = ''     
    info2       = ''     
    info3       = '' 
    info4       = '' 
    info5       = '' 
    active4     = ''
    active5     = ''
    type4       = ''
    type5       = ''
    cursor.execute(sql)
    data                    = cursor.fetchall()
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name,order,active1,type1,message11,message12,active2,type2,message21,message22,active3,type3,message31,message32,message,info1,info2,info3,active4,active5,info4,info5,message41,message42,message51,message52,type4,type5 = rec
        else:
            id,name,order,active1,type1,message11,message12,active2,type2,message21,message22,active3,type3,message31,message32,message,info1,info2,info3,active4,active5,info4,info5,message41,message42,message51,message52,type4,type5 = rec.values()
    answer['id']            = id        
    answer['name']          = name 
    answer['order']         = order 
    answer['active1']       = active1  
    answer['type1']         = type1     
    answer['message11']     = message11  
    answer['message12']     = message12       
    answer['active2']       = active2  
    answer['type2']         = type2     
    answer['message21']     = message21  
    answer['message22']     = message22       
    answer['active3']       = active3  
    answer['type3']         = type3     
    answer['message31']     = message31  
    answer['message32']     = message32  
    answer['message41']     = message41 
    answer['message42']     = message42     
    answer['message51']     = message51 
    answer['message52']     = message52     
    
    answer['message']       = message
    answer['info1']         = info1
    answer['info2']         = info2
    answer['info3']         = info3
    answer['info4']         = info4
    answer['info5']         = info5
    answer['active4']       = active4 
    answer['active5']       = active5 
    answer['type4']         = type4
    answer['type5']         = type5 
    return answer 
    
def clear_peremen_for_start_action      (message_info,status_input,setting_bot,ask_info,type_ask,name_active):                           ###  Обнуляем все переменные перед вводом данных
    status_input    = user_save_data (message_info,status_input,setting_bot,[["Сбор данных",name_active]])                          ###  Метка называется как название строки    
    status_input    = user_save_data (message_info,status_input,setting_bot,[["active1",""]])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["active2",""]])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["active3",""]])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["active4",""]])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["active5",""]])
    status_input    = user_save_data (message_info,status_input,setting_bot,[["Номер ордера",""]])
        
def send_message_action                 (message_info,status_input,setting_bot,ask_info,type_ask,name_active,shablon,message_name,key):
    user_id         = message_info['user_id']
    message         = setting_bot.setdefault (shablon,ask_info.setdefault(message_name,message_name))                                                       ###  Выводим текст информированный что это первый запрос    
    answer_null     = save_message (message_info,setting_bot,user_id,message)
    message_out     = gets_message (message_info,setting_bot,user_id,message)
    answer_null     = send_message (message_info,setting_bot,user_id,message_out['Текст'],key)
    
def active_sql_get                      (message_info,status_input,setting_bot,sql,limit,offset,back,ask,name_sql,mark_key):
    id_sql          = save_sql          (message_info,status_input,setting_bot,name_sql,sql,limit,offset,back)                                           
    markup_list     = complite_key      (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,mark_key)          
    return markup_list
    
def action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,message_name): 
    user_id         = message_info['user_id']    
    message         = ask_info[message_name]
    answer_null     = save_message (message_info,setting_bot,user_id,message)
    message_out     = gets_message (message_info,setting_bot,user_id,message)
    markup          = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
    answer_null     = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup) 

def action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,message_name): 
    user_id         = message_info['user_id']    
    message_id      = message_info['message_id']
    print ('message_name',message_name)     
    print ('[5] ask_info',ask_info)     
    message         = ask_info[message_name]
    answer_null     = save_message (message_info,setting_bot,user_id,message)
    message_out     = gets_message (message_info,setting_bot,user_id,message)
    markup          = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
    answer_null     = edit_message (message_info,setting_bot,user_id,message_out['Текст'],markup,message_id)

def active_save_data_base               (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,active,info):
    namebot     = message_info.setdefault ('namebot','')
    import iz_bot
    db,cursor   = iz_bot.connect (namebot)
    namer_order = status_input.setdefault ('Номер ордера','')
    sql = "UPDATE `order` SET {} = '{}' WHERE id = {} ".format (active,info,namer_order)
    cursor.execute(sql)        
    db.commit()
    
def active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save):                      #### Процедура для запроса данных вопросом
    user_id                 = message_info.setdefault ('user_id','')
    if nomer_save == 1:                                                                                                                           ### Ввод первого значения
        message_in      = message_info['message_in']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active1",message_in]])
        label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active1',message_in)
                    
    if nomer_save == 2:
        #action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
        message_in      = message_info['message_in']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active2",message_in]])
        label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active2',message_in)
  
    if nomer_save == 3:
        #action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
        message_in      = message_info['message_in']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active3",message_in]])
        label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active3',message_in)
             
def active_end_data_ask_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active):    
    ### Проверяем что нужно выйти из режима ввода данных
    result                  = {}
    if (ask_info['active1'] != '' and status_input.setdefault ('active1','') != '') or (ask_info['active1'] == ''):
        if (ask_info['active2'] != '' and status_input.setdefault ('active2','') != '') or (ask_info['active2'] == ''):
            if (ask_info['active3'] != '' and status_input.setdefault ('active3','') != '') or (ask_info['active3'] == ''):
                if (ask_info['active4'] != '' and status_input.setdefault ('active4','') != '') or (ask_info['active4'] == ''):
                    if (ask_info['active5'] != '' and status_input.setdefault ('active5','') != '') or (ask_info['active5'] == ''):
                        result['operation'] = "Выполнено" 
                        result['active1']   = status_input['active1']
                        result['active2']   = status_input['active2']
                        result['active3']   = status_input['active3']
                        result['active4']   = status_input['active4']
                        result['active5']   = status_input['active5']
                        result['name'   ]   = name_active
                        clear_peremen_for_start_action (message_info,status_input,setting_bot,ask_info,type_ask,'')
    return result         
   
def active_save_data_calendar_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save):                      #### Процедура для запроса данных вопросом
    user_id                 = message_info.setdefault ('user_id','')
    if nomer_save == 1:                                                                                                                           ### Ввод первого значения
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message12')
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active1",message_in]])
        #label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active1',message_in)
                    
    if nomer_save == 2:
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active2",message_in]])
        #label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active2',message_in)
  
    if nomer_save == 3:
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active3",message_in]])
        #label_in        = False
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active3',message_in)   
     
def active_send_data_calendar_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save): 
    if nomer_save == 1:
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message11')
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP   
        from datetime import datetime, date, timedelta
        callback = "cbcal_0_s_m_2025_1_26"
        result, key, step = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
        user_id                 = message_info.setdefault ('user_id','')
        message_text    = 'Всем привет'
        markup          = key
        print ('[result :]',result)
        print ('[key :]',key)
        print ('[step] :',step)
        answer      = send_message (message_info,setting_bot,user_id,message_text,markup)


        
    if nomer_save == 2:
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message12') 
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP   
        from datetime import datetime, date, timedelta
        callback = "cbcal_0_s_m_2025_1_26"
        result, key, step = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
        user_id                 = message_info.setdefault ('user_id','')
        message_text    = 'Всем привет'
        markup          = key
        print ('[result :]',result)
        print ('[key :]',key)
        print ('[step] :',step)
        answer      = send_message (message_info,setting_bot,user_id,message_text,markup)



        
    if nomer_save == 3:
        action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message13')   
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP   
        from datetime import datetime, date, timedelta
        callback = "cbcal_0_s_m_2025_1_26"
        result, key, step = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
        user_id                 = message_info.setdefault ('user_id','')
        message_text    = 'Всем привет'
        markup          = key
        print ('[result :]',result)
        print ('[key :]',key)
        print ('[step] :',step)
        answer      = send_message (message_info,setting_bot,user_id,message_text,markup)

def active_save_data_list_continued          (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save):                      #### Процедура для запроса данных вопросом
    user_id                 = message_info.setdefault ('user_id','')
    if nomer_save == 1:                                                                                                                           ### Ввод первого значения
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active1",message_in]])
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active1',message_in)
                    
    if nomer_save == 2:
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active2",message_in]])
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active2',message_in)
  
    if nomer_save == 3:
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active3",message_in]])
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active3',message_in)
        
    if nomer_save == 4:
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active4",message_in]])
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active4',message_in)

    if nomer_save == 5:
        message_in      = message_info['Выбор']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active4",message_in]])
        active_save_data_base (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save,'active4',message_in)
               
def get_list_sql_task (message_info,status_input,setting_bot,ask_info,jsonparam,data_id):
    import json
    sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
    ask1            = ask_info[jsonparam]
    parser_sl       = json.loads(ask1)
    limit           = parser_sl.setdefault ('limit',10)
    offset          = parser_sl.setdefault ('offset',0)
    back            = parser_sl.setdefault ('back','')
    ask             = "name = '{}' and data_id = {}".format (parser_sl.setdefault ('ask',''),data_id)
    name_sql        = parser_sl.setdefault ('name_sql','Список услуг')
    mark_key        = parser_sl.setdefault ('mark_key','service')
    markup_list     = active_sql_get (message_info,status_input,setting_bot,sql,limit,offset,back,ask,name_sql,mark_key) 
    return markup_list
        
def active_send_data_list_continued          (message_info,status_input,setting_bot,ask_info,type_ask,name_active,nomer_save):                      ### Процедура для запроса данных списком 
    #label_in                = True
    #user_id                 = message_info.setdefault ('user_id','')
         
    if nomer_save == 1:
        markup_list = get_list_sql_task   (message_info,status_input,setting_bot,ask_info,'info1',0)
        answer      = send_message_action (message_info,status_input,setting_bot,ask_info,type_ask,name_active,ask_info['message11'],ask_info['message11'],markup_list)        
               
    if nomer_save == 2:    
        markup_list = get_list_sql_task   (message_info,status_input,setting_bot,ask_info,'info2',0) 
        send_message_action (message_info,status_input,setting_bot,ask_info,type_ask,name_active,ask_info['message21'],ask_info['message21'],markup_list)        
        
    if nomer_save == 3:    
        markup_list = get_list_sql_task   (message_info,status_input,setting_bot,ask_info,'info3',0)
        send_message_action (message_info,status_input,setting_bot,ask_info,type_ask,name_active,ask_info['message31'],ask_info['message31'],markup_list)   
        
def active_save_data_calendar_contineum     (message_info,status_input,setting_bot,ask_info,type_ask,name_active):
    if ask_info.setdefault('Сохранить','') == '':
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP   
        from datetime import datetime, date, timedelta
        callback            = "cbcal_0_s_m_2025_1_26"
        result, key, step   = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
        user_id             = '7474072878'
        message_text        = 'Всем привет'
        markup              = key
        answer              = send_message (message_info,setting_bot,user_id,message_text,markup)   
    else:
        print ('[+] Сообщаем программе что нужно отправить запрос')        
        action_send_message_contitinum (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
        message_in      = message_info['message_in']
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active3","Запись3"]])
        label_in        = False
        import iz_bot
        nomer_order   = ask_info['Номер']
        nomenclatur   = ask_info['Выбор']  
        namebot       = message_info.setdefault('namebot','')
        db,cursor = iz_bot.connect (namebot)
        sql = "UPDATE `order` SET active3 = '{}' WHERE id = {} ".format (nomenclatur,nomer_order)
        cursor.execute(sql)        
        db.commit()
        status_input    = user_save_data (message_info,status_input,setting_bot,[["active3",str(nomenclatur)]])

def active_nomer_info_param                 (message_info,status_input,setting_bot,name_active,type_ask):
    answer_info = {}
    #ask_info                = get_active_ask (message_info,status_input,setting_bot,name_active)
    #if status_input.setdefault("Сбор данных","") == name_active:
    #    answer_info['Активность'] = "Работает"
    #    label_in                = True
    #    if ask_info['active1'] != '' and status_input.setdefault ('active1','') == '' and label_in == True:
    #        answer_info['Активная'] = 1
    #        label_in        = False 
    #    if ask_info['active2'] != '' and status_input.setdefault ('active2','') == '' and label_in == True:    
    #        answer_info['Активная'] = 2
    #        label_in        = False 
    #    if ask_info['active3'] != '' and status_input.setdefault ('active3','') == '' and label_in == True:
    #        answer_info['Активная'] = 3
    #        label_in        = False 
    #    if ask_info['active4'] != '' and status_input.setdefault ('active4','') == '' and label_in == True:    
    #        answer_info['Активная'] = 4
    #        label_in        = False 
    #    if ask_info['active5'] != '' and status_input.setdefault ('active5','') == '' and label_in == True:        
    #        answer_info['Активная'] = 5
    #        label_in        = False 
    return answer_info
                      
def create_order_new                        (message_info,status_input,setting_bot,name_active):
    namebot         = message_info.setdefault ('namebot','') 
    user_id         = message_info.setdefault ('user_id','') 
    import iz_bot    
    db,cursor   = iz_bot.connect (namebot)
    import time
    unixtime    = int(time.time())
    sql         = "INSERT INTO `order` (`unixtime`,name,`user_id`,`active1`,`active2`,`active3`,`active4`,`active5`,status) VALUES ({},'{}','{}','{}','{}','{}','{}','{}','{}')".format (unixtime,name_active,user_id,'','','','','','')
    cursor.execute(sql)
    lastid = cursor.lastrowid 
    db.commit()     
    return lastid 
          
def active_send_calendar                    (message_info,status_input,setting_bot,name_active):
    from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP   
    from datetime import datetime, date, timedelta
    callback = "cbcal_0_s_m_2025_1_26"
    result, key, step = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
    user_id                 = message_info.setdefault ('user_id','')
    message_text    = 'Всем привет'
    markup          = key
    answer      = send_message (message_info,setting_bot,user_id,message_text,markup)     
            
def active_save_data_main                   (message_info,status_input,setting_bot,name_active,type_ask):  
    answer = True  
    if type_ask == "Сбор данных":    
        answer_info             = active_nomer_info_param (message_info,status_input,setting_bot,name_active,type_ask)
        #ask_info                = get_active_ask          (message_info,status_input,setting_bot,name_active)                                           ### Проверяем запушена информация сбора информации. Если В перемменой есть имя значит работает ввод слова                                                                                            
        #ask_info['Номер']       = message_info.setdefault ('Номер'      ,'')                                                                            ### Номер операции который был запущен. 
        #ask_info['Выбор']       = message_info.setdefault ('Выбор'      ,'')                                                                            ### Сделанный выбор 
        #ask_info['Сохранить']   = message_info.setdefault ('Сохранить'  ,'')                                                                            ### Сохраняем выбранную дату в календаре
        
        if answer_info.setdefault ('Активность','') == "Работает":                                                                                      ### Собираем информацию об задаче сбора информации    
            answer = False
            #print ('[+1] answer_info :',answer_info.setdefault ('Активная',0))
            if answer_info.setdefault ('Активная',0) == 1:
                if ask_info['type1'] == 'ask':
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message12')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)
                if ask_info['type1'] == 'list':    
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message12')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)
                if ask_info['type1'] == 'calendar':  
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message12')
                    active_save_data_calendar_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)                    
            
            if answer_info.setdefault ('Активная',0) == 2:
                if ask_info['type2'] == 'ask':
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,2)
                if ask_info['type2'] == 'list':    
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,2)
                if ask_info['type2'] == 'calendar':  
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
                    #action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message22')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,2)         
            
            if answer_info.setdefault ('Активная',0) == 3:
                if ask_info['type3'] == 'ask':
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,3)
                if ask_info['type3'] == 'list':    
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,3)
                if ask_info['type3'] == 'calendar':  
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message32')
                    active_save_data_list_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,3)         

            if answer_info.setdefault ('Активная',0) == 4:
                if ask_info['type4'] == 'ask':
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message42')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,4)
                if ask_info['type4'] == 'list':    
                    
                    print ('[+] ask_info 4',ask_info)
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message42')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,4)
                    
                    #action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message42')
                    #action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,4)
                if ask_info['type4'] == 'calendar':  
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message42')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,4)         

            if answer_info.setdefault ('Активная',0) == 5:
                if ask_info['type5'] == 'ask':
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message52')
                    active_save_data_ask_continued      (message_info,status_input,setting_bot,ask_info,type_ask,name_active,5)
                if ask_info['type5'] == 'list':    
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message52')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,5)
                if ask_info['type5'] == 'calendar':  
                    action_edit_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message52')
                    active_save_data_list_continued     (message_info,status_input,setting_bot,ask_info,type_ask,name_active,5)         

        ### Проверяем доступность следующего условия    
        answer_info = active_nomer_info_param           (message_info,status_input,setting_bot,name_active,type_ask) 
        if answer_info.setdefault ('Активность','') == "Работает":  
            
            if answer_info.setdefault ('Активная',0) == 1:
                if ask_info['type1'] == 'ask':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message11')
                if ask_info['type1'] == 'list':
                    markup_list = get_list_sql_task     (message_info,status_input,setting_bot,ask_info,'info1',0)
                    action_send_message_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message11')
                if ask_info['type1'] == 'calendar':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message11')
                    
            if answer_info.setdefault ('Активная',0) == 2:
                if ask_info['type2'] == 'ask':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message21')
                if ask_info['type2'] == 'list':
                    markup_list = get_list_sql_task   (message_info,status_input,setting_bot,ask_info,'info2',0)
                    send_message_action (message_info,status_input,setting_bot,ask_info,type_ask,name_active,ask_info['message21'],ask_info['message21'],markup_list)  
                    
                if ask_info['type2'] == 'calendar':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message21')

            if answer_info.setdefault ('Активная',0) == 3:
                if ask_info['type3'] == 'ask':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message31')
                if ask_info['type3'] == 'list':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message31')
                if ask_info['type3'] == 'calendar':
                    active_send_calendar (message_info,status_input,setting_bot,name_active)

            if answer_info.setdefault ('Активная',0) == 4:
                if ask_info['type4'] == 'ask':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message21')

                if ask_info['type4'] == 'list':
                    markup_list = get_list_sql_task   (message_info,status_input,setting_bot,ask_info,'info4',0)
                    send_message_action (message_info,status_input,setting_bot,ask_info,type_ask,name_active,ask_info['message41'],ask_info['message41'],markup_list)
                    
                if ask_info['type4'] == 'calendar':
                    action_send_message_continued (message_info,status_input,setting_bot,ask_info,type_ask,name_active,'message21')



        result = active_end_data_ask_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active)
                

    if type_ask == "Старт":                                                                                                         ###  Запускаем метку сбора данных  
        import iz_bot
        ask_info        = get_active_ask                        (message_info,status_input,setting_bot,name_active)                                        ###  Информация хранится в таблице данный
        lastid          = create_order_new                      (message_info,status_input,setting_bot,name_active)
        clear_peremen_for_start_action                          (message_info,status_input,setting_bot,ask_info,type_ask,name_active)
        answer_info     = active_nomer_info_param               (message_info,status_input,setting_bot,name_active,type_ask)
        
        if answer_info.setdefault ('Активность','') == "Работает":
            if ask_info['type1'] == 'ask':
                status_input    = user_save_data (message_info,status_input,setting_bot,[["Номер ордера",str(lastid)]])
                result          = active_send_data_ask_continued            (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)
            if ask_info['type1'] == 'list': 
                status_input    = user_save_data (message_info,status_input,setting_bot,[["Номер ордера",str(lastid)]])
                result          = active_send_data_list_continued           (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)
            if ask_info['type1'] == 'calendar': 
                status_input    = user_save_data (message_info,status_input,setting_bot,[["Номер ордера",str(lastid)]])
                result          = active_send_data_calendar_continued       (message_info,status_input,setting_bot,ask_info,type_ask,name_active,1)
            if ask_info['type1'] == 'telefon':    
                pass
            if ask_info['type1'] == 'geo':        
                pass

    return answer     
     
def save_sql                                (message_info,status_input,setting_bot,name,sql,limit,offset,back):
    if setting_bot['connect'] == 'sql lite':
        pass
        lastid = 0
    if setting_bot['connect'] == 'MySQL':    
        import iz_bot
        namebot    = message_info.setdefault('namebot','')
        db,cursor = iz_bot.connect (namebot)
        sql = "INSERT INTO data_sql (name,data,limit1,offset1,back1,status) VALUES (%s,%s,%s,%s,%s,'')".format ()
        sql_save = (name,sql,limit,offset,back)
        result = cursor.execute(sql,sql_save)
        db.commit()    
        lastid = cursor.lastrowid
    return lastid

def get_sql                                 (message_info,setting_bot,id_sql):
    from iz_bot import connect as connect
    namebot    = message_info.setdefault('namebot','')
    db,cursor = connect (namebot)
    sql = "select id,sql,ask,limit,offset,back from data_sql where id = {}".format(id_sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,sql,ask,limit,offset,back = rec.values() 
    return sql,ask,limit,offset,back  

def save_message                            (message_info,setting_bot,user_id,message_out):
    from iz_bot import connect as connect
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = connect (namebot)
    answer  = message_out
    id = 0
    sql = "select id,name from message where name = 'Имя' and info = '{}' ;".format(message_out)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name = rec
        else:
            id,name = rec.values() 
        
    if id == 0:
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
    return answer    
        
def gets_message                            (message_info,setting_bot,user_id,message_out): 
    from iz_bot import connect as connect   
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = connect (namebot)
    message      = {}
    sql = "select id,name,info,data_id from message where name = 'Имя' and info = '{}' ;".format(message_out)
    cursor.execute(sql)
    data = cursor.fetchall()
    data_id = 0
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name,info,data_id = rec
        else:
            id,name,info,data_id = rec.values() 
    if data_id == 0:
        message = {}
    else:        
        sql  = "select id,name,info,data_id from message where data_id = {};".format(data_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            if str(type(rec)) == "<class 'tuple'>":
                id,name,info,data_id = rec
            else:    
                id,name,info,data_id = rec.values()
            message[name] = info
        if message.setdefault('Текст','') == '': 
            message['Текст'] = message_out 
        if message.setdefault('Меню','') == '': 
            message['Меню'] = ''        
    return message
       
def user_save_data                          (message_info,status_input,setting_bot,save_data): ### Бот хранит переменные каждого пользователя в базе и в переменной. Эта процедура меняет переменную и в базе и в переменной
    from iz_bot import connect as connect
    namebot     = message_info['namebot']
    user_id     = message_info['user_id']
    db,cursor   = connect (namebot)
    sql         = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' limit 1;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()   
    for row in results:
        if str(type(row)) == "<class 'tuple'>":
            id,name,info,data_id = row
        else:    
            id,name,info,data_id = row.values() 
        for line in save_data:
            name_status    = line[0]
            info_status    = line[1]
            sql     = "select id,name,info from users where data_id = {} and name = '{}';".format (data_id,name_status)
            cursor.execute(sql)
            results = cursor.fetchall()  
            id = 0
            for rec in results:
                if str(type(rec)) == "<class 'tuple'>":
                    id,name,info = rec
                else:    
                    id,name,info = rec.values() 
            if id != 0:
                if setting_bot['connect'] == 'sql lite':
                    sql         = "UPDATE users SET info = '{}' WHERE `name` = '{}' and data_id = {} ".format (info_status,name_status,data_id)
                    cursor.execute(sql)
                    db.commit()                    
                    status_input[name_status] = info_status
                else:
                    sql         = "UPDATE users SET info = %s WHERE `name` = %s and data_id = %s "
                    sql_save    = (info_status,name_status,data_id)
                    cursor.execute(sql,sql_save)
                    db.commit()    
                    status_input[name_status] = info_status
            else:   
                if setting_bot['connect'] == 'sql lite':
                    sql         = "INSERT INTO users (data_id,info,name,status) VALUES ('{}','{}','{}','')".format (data_id,info_status,name_status)
                    cursor.execute(sql)
                    db.commit()                 
                    status_input[name_status] = info_status
                else:
                    sql         = "INSERT INTO users (data_id,info,name,status) VALUES (%s,%s,%s,'')".format ()
                    sql_save    = (data_id,info_status,name_status)
                    cursor.execute(sql,sql_save)
                    db.commit() 
                    status_input[name_status] = info_status
        cursor.close()
        db.close()  
    return status_input 
        
def key_type_message                        (key):                                                          #                                                                   ## Процедура формирует кнопку из Соответствия
    import json
    line = []
    for number in range(20):
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
        key15  = {}
        key15['text']          = key.setdefault('Кнопка ' +str(number+1)+'5','')
        key15['callback_data'] = key.setdefault('Команда '+str(number+1)+'5','')
        key16  = {}
        key16['text']          = key.setdefault('Кнопка ' +str(number+1)+'6','')
        key16['callback_data'] = key.setdefault('Команда '+str(number+1)+'6','')
        key17  = {}
        key17['text']          = key.setdefault('Кнопка ' +str(number+1)+'7','')
        key17['callback_data'] = key.setdefault('Команда '+str(number+1)+'7','')
       
        if key.setdefault('Кнопка ' +str(number+1)+'1','') != '':        
            line1.append(key11)
        if key.setdefault('Кнопка ' +str(number+1)+'2','') != '':
             line1.append(key12)
        if key.setdefault('Кнопка ' +str(number+1)+'3','') != '':        
            line1.append(key13)
        if key.setdefault('Кнопка ' +str(number+1)+'4','') != '':        
            line1.append(key14)
        if key.setdefault('Кнопка ' +str(number+1)+'5','') != '':        
            line1.append(key15)
        if key.setdefault('Кнопка ' +str(number+1)+'6','') != '':        
            line1.append(key16)
        if key.setdefault('Кнопка ' +str(number+1)+'7','') != '':        
            line1.append(key17)
            
        line.append(line1)   
        if key.setdefault('Кнопка ' +str(number+1)+'1','') == '':
            break
    array = {"inline_keyboard":line}  
    markup = json.dumps(array) 
    return markup     
       
def key_type_keybord                        (key):                                                                                                                              ## Процедура формирует кнопку из Соответствия
    import json
    array  = {}        
    line   = []
    for number in range(10):
        line1   = []
        key11   = {}
        key11['text']       = key.setdefault('Кнопка '+str(number)+'1','')  
        if key.setdefault('Замена '+str(number)+'1','') != '':
            key11['text']   = key.setdefault('Замена '+str(number)+'1','')
        line1.append(key11)
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
 
def gets_key                                (message_info,setting_bot,user_id,menu):
    namebot = message_info.setdefault('namebot','')
    from iz_bot import connect as connect
    db,cursor = connect (namebot)
    sql     = "select id,name,info,data_id from menu where name = 'Имя' and info = '{}'".format (menu)
    cursor.execute(sql)
    results = cursor.fetchall()    
    markup     = {}
    key        = {}   
    for rec in results:
        if str(type(rec)) == "<class 'tuple'>":
            id,name,info,data_id = rec
        else:    
            id,name,info,data_id = rec.values() 
        sql = "select id,name,info from menu where data_id = '{}' and status <> 'delete' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for rec in results:
            if str(type(rec)) == "<class 'tuple'>":
                id,name,info = rec
            else:
                id,name,info = rec.values() 
            key[name] = info
    type_key = key.setdefault('Тип кнопки','')
    if type_key == 'Сообщение':
        markup = key_type_message (key)
    if type_key == 'Клавиатура' or type_key == '':    
        markup = key_type_keybord (key)
    return markup
       
##################################################################################################################################################################################################        
    
def send_message            (message_info,setting_bot,user_id,message_out,markup):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup                
    if message_out != '':    
        url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage')
        resp                    = requests.post(url, params) 
        answer                  = resp.json()
    else:
        answer = {'error':'Нет текста сообщения'}
    #print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    #print ( answer)
    #print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    #print ('') 
    #print ('[markup]',markup)
    return answer 
    
def edit_message            (message_info,setting_bot,user_id,message_out,markup,message_id):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    params['message_id']    = message_id
    if markup != {}:
        params['reply_markup'] = markup                
    if message_out != '':    
        url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'editMessageText')
        resp                    = requests.post(url, params) 
        answer                  = resp.json()
    else:
        answer = {'error':'Нет текста сообщения'}
    print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    print ('') 
    return answer     
    
def send_picture            (message_info,setting_bot,user_id,message_out,markup,picture):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params = {}
    params['chat_id']       = user_id
    params['caption']       = str(message_out)
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup
    file_path               = picture
    file_opened = open(file_path, 'rb')
    files = {'photo': file_opened}
    url='https://api.telegram.org/bot{0}/{1}'.format(token, "sendPhoto") 
    resp = requests.post(url, params, files=files)
    answer = resp.json()   
    #print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    #print ( answer)
    #print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    #print ('') 
    return answer 
    
def edit_caption            (message_info,setting_bot,user_id,message_out,markup):    
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params = {}
    params['chat_id'] = user_id
    params['caption'] = str(message_out)
    params['message_id'] = message_id
    params['parse_mode'] = 'HTML'
    if markup != '' or key_array != '':
        params['reply_markup'] = markup
    url='https://api.telegram.org/bot{0}/{1}'.format(token, "editMessageCaption")            
    resp = requests.post(url, params)
    answer = resp.json()   
    #print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    #print ( answer)
    #print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    #print ('') 
    return answer 

def edit_picture            (message_info,setting_bot,user_id,message_out,markup,picture):
    import requests
    import json
    token       = setting_bot.setdefault ('Токен','')
    file_path   = picture 
    file_opened = open(file_path, 'rb')
    files       = {'media':file_opened}
    media       = json.dumps({'type': 'photo','media': 'attach://media'})
    method      = 'editMessageMedia'
    url         = 'https://api.telegram.org/bot{0}/{1}'.format(token, "editMessageMedia")   
    params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':str(message_out)}
    if markup != {}:
        params['reply_markup'] = markup    
    answer = requests.post(url, params,files = files)                
    #print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    #print ( answer)
    #print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    #print ('') 
    return answer             
    
##################################################################################################################################################################################################    
         
def complite_list_key       (message_info,status_input,setting_bot,name):                                                                                       ###  Формируем Много задачную кнопку
    from iz_bot import connect as connect
    from iz_bot import build_jsom as build_jsom
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = connect (namebot) 
    sql                 = "select id,name,key11,key12,key13,key14,key_name from `key` where name = '{}'".format(name)
    cursor.execute(sql)
    data = cursor.fetchall()
    nomer = 0 
    key_array = {}
    for rec in data:
        nomer = nomer + 1
        id,name,key11,key12,key13,key14,key_name = rec.values()
        if status_input.setdefault (key_name,'') == '' or status_input.setdefault (key_name,'') ==  "key11":
            command =  build_jsom ({'o':'key','i':id,'s':1})
            key_array['Кнопка ' +str(nomer)  + "1"] = key11
            key_array['Команда '+str(nomer)  + "1"] = command
            
        if status_input.setdefault (key_name,'') ==  "key12":
            command =  build_jsom ({'o':'key','i':id,'s':2})
            key_array['Кнопка ' +str(nomer)  + "1"] = key12
            key_array['Команда '+str(nomer)  + "1"] = command
            
        if status_input.setdefault (key_name,'') ==  "key13":
            command =  build_jsom ({'o':'key','i':id,'s':3})
            key_array['Кнопка ' +str(nomer)  + "1"] = key13
            key_array['Команда '+str(nomer)  + "1"] = command
            
        if status_input.setdefault (key_name,'') ==  "key14":
            command =  build_jsom ({'o':'key','i':id,'s':4})
            key_array['Кнопка ' +str(nomer)  + "1"] = key14
            key_array['Команда '+str(nomer)  + "1"] = command
    markup   = key_type_message (key_array)
    return markup      
      
def complite_key            (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,metka):                                                                  ###  Формируем кнопокe из списока  по переданным нам параметрам
    from iz_bot import connect as connect
    from iz_bot import build_jsom as build_jsom
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = connect (namebot) 
    sql = sql.replace("##s1##",str(ask))
    sql = sql.replace("##s2##",str(limit))
    sql = sql.replace("##s3##",str(offset))
    print ('[sql]:',sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    key_array = {}
    nomer = 0 
    for rec in data: 
        if setting_bot['connect'] == 'sql lite':
            id,info = rec
        else:    
            id,info = rec.values()  
        command =  build_jsom ({'o':metka,'i':id,'s':id_sql})
        nomer = nomer + 1
        key_array['Кнопка '+str(nomer)  + "1"] = info
        key_array['Команда '+str(nomer) + "1"] = command
    if back != '':                                                                                                                                              ### Если нам передали информацию как вернутся назад заносим ее
        name_key = set_name_key (message_info,'Кнопка назад') 
        command  = iz_bot.build_jsom ({'o':'back','s':id_sql,'b':back})
        key_array.append ([[name_key,command],['',''],['','']]) 
    markup   = key_type_message (key_array)
    return markup                                                          
  
def get_message             (message_info,name):
    namebot     = message_info.setdefault ('namebot')
    from iz_bot import connect as connect
    db,cursor   = connect (namebot) 
    data_message = {'Текст':'Текст'}
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
  
def get_message_tovar       (message_info,status_input,setting_bot,id_list,info_tovar):                                                                         ###  Формируем карточку товара    
    message         = get_message (message_info,"Шаблон товара") 
    message_text    = message
    list            = get_list_change  (message_info,status_input,setting_bot,message.setdefault('Текст',''))                                                                      ###  Список значений исходящего сообщения
    for line in list:
        message_text    = message_text.replace(line,str(info_tovar.setdefault (name,''))) 
    key             = {}
    return message_text,key
   
##################################################################################################################################################################################################    
   
def print_operator            (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                                                           ###  Печать команды оператор в json
    pass
    
def get_name_picture          (message_info,status_input,setting_bot,nomer,move):
    namebot      = message_info.setdefault ("namebot","")
    name_picture = ''
    
    if 1==1:
        id_begin = 0
        id_end   = 0
        db,cursor    = connect_postgres (namebot)
        sql = "select id,name from picture where 1=1 order by id".format(nomer)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec
            print ('[+] id,name',id,name)
            if id_begin == 0:
                id_begin    = id
                name_bigin  = name 
            id_end    =  id
            name_end  =  name
    
    
    print ('[nomer,move] :',nomer,move)
    print ('[id_begin,id_end] :',id_begin,id_end)
    
    #if move == 'right' and nomer == id_end:
    #    nomer = id_begin - 1
    
    if move == 'right':
        db,cursor    = connect_postgres (namebot)
        sql = "select id,name from picture where id > {} order by id limit 1".format(nomer)
        print ('[sql] :',sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec
            name_picture    =  name
        if name_picture == '':
            name_picture = name_bigin
            id           = id_begin
            

    if move == 'left':
        db,cursor    = connect_postgres (namebot)
        sql = "select id,name from picture where id < {} order by id desc limit 1".format(nomer)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec
            name_picture    =  name
            
        if name_picture == '':
            name_picture = name_end
            id           = id_end 
            print ('[+] [+]')            




            
    print ('[name_picture] :',name_picture)        
    return name_picture,id
    
def complite_key_psg_calendar (message_info,setting_bot,month,years,id_order,lab):  
    import json
    key_array = {}
    key_array['Кнопка 11' ] = "ПН"
    key_array['Команда 11'] = "ПН"
    key_array['Кнопка 12' ] = "ВТ"
    key_array['Команда 12'] = "ВТ"
    key_array['Кнопка 13' ] = "СР"
    key_array['Команда 13'] = "СР"
    key_array['Кнопка 14' ] = "ЧТ"
    key_array['Команда 14'] = "ЧТ"
    key_array['Кнопка 15' ] = "ПТ"
    key_array['Команда 15'] = "ПТ"
    key_array['Кнопка 16' ] = "СБ"
    key_array['Команда 16'] = "СБ"
    key_array['Кнопка 17' ] = "ВС"
    key_array['Команда 17'] = "ВС"
    for line in range(6):
        for row in range(7):
            key_tab = line + 2
            key_row = row  + 1
            key_mat = str(line+1)+str(row+1)+"_data"
            info_date  = lab[str(key_mat)]["D"]
            info_see   = lab[str(key_mat)]["S"]
            
            info  = "-"
            label = "N" 
            if info_see == 'A':
                info  = str(info_date)
                label = "A" 
            if info_see == 'T':
                info = str(info_date)
                label = "T" 
            if info_see == 'X':
                info = str('X')
                label = "X" 
            command    =  build_jsom ({'o':'calc','d':str(info_date),'m':'m'+str(month),'y':'y'+str(years),'l':str(label),'lb':id_order})     #### ,'g':str(years),'l':str(label)
            key_array['Кнопка '  + str(key_tab) + str(key_row)] = info
            key_array['Команда ' + str(key_tab) + str(key_row)] = command
    key_array['Кнопка 81' ] = key_change ("ЛЕВО")
    command    =  build_jsom ({'o':'calc','d':str(0),'m':'m'+str(month),'y':'y'+str(years),'l':str('left')})     #### ,'g':str(years),'l':str(label)
    key_array['Команда 81'] = command   
    key_array['Кнопка 82' ] = key_change(lab['name'])
    key_array['Команда 82'] = key_change(lab['name'])        
    key_array['Кнопка 83' ] = key_change ("ПРАВО")
    command    =  build_jsom ({'o':'calc','d':str(0),'m':'m'+str(month),'y':'y'+str(years),'l':str('right')})     #### ,'g':str(years),'l':str(label)
    key_array['Команда 83'] = command
    markup   = key_type_message (key_array)
    return markup    
    
def key_change (key):
    if key == "ЛЕВО": key = "←"
    if key == "ПРАВО": key = "→"
    key = key.replace('January' ,'Январь')
    key = key.replace('February','Февраль')
    key = key.replace('March'   ,'Март')
    key = key.replace('April'   ,'Апрель')
    key = key.replace('May'   ,'Май')
    key = key.replace('June'   ,'Июнь')
    key = key.replace('July'   ,'Июль')
    key = key.replace('August'   ,'Август')
    key = key.replace('September'   ,'Сентябрь')
    key = key.replace('October'   ,'Октябрь')
    key = key.replace('November'   ,'Ноябрь')
    key = key.replace('December'   ,'Декабрь')
    return key    
        
def get_datetime_range        (year, month):
    from calendar import monthrange
    import datetime
    nb_days = monthrange(year, month)[1]
    return [datetime.date(year, month, day) for day in range(1, nb_days+1)]
    
def complite_calendar         (data_g,data_m,day_x):
    import datetime
    days     = get_datetime_range(data_g, data_m)
    str_d    = str(data_g)+"-"+str(data_m)
    object_d = datetime.datetime.strptime(str_d, '%Y-%m')
    month    = object_d.strftime("%B")
    year     = object_d.strftime("%Y")
    ndate    = len(days)
    lab      = {}
    lab['name']    = str(month)+" "+str(year)
    lab['month']   = str(month)
    lab['year']   = str(year)
    for line in range(6):
        for row in range(7):
            dm = str(line+1)+str(row+1)+'_data'
            lab[dm] = {"D":"-","S":"N"}
    weekday = days[0].weekday()
    nomer = 0
    for line in range(6):
        for row in range(7):
            dm = str(line+1)+str(row+1)+'_data'
            if ndate > nomer-weekday and nomer-weekday > -1:
                lab[dm] = {"D":days[nomer-weekday].day,"S":"A"}
                if lab[dm]['D'] < day_x:
                    lab[dm] = {"D":days[nomer-weekday].day ,"S":"X"}
            nomer = nomer + 1    
    return lab   

def get_name_master_in_id     (message_info,status_input,setting_bot,id_list):
    namebot     = message_info.setdefault('namebot','')
    #user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
    sql = "select id,name,info from masters where id = {}".format (id_list)
    cursor.execute(sql)
    records = cursor.fetchall()
    #info_data = {}
    #for row in records:
        #id,name,info = row
    #sql = "UPDATE order_master SET {} = '{}' WHERE id = {}".format(name,info,id)
    #cursor.execute(sql)
    #db.commit()
    #sql         = "INSERT INTO order_master (name,info,user_id,status) VALUES ('','','{}','')  RETURNING id".format (user_id)
    #cursor.execute(sql)
    #result = cursor.fetchone()
    #lastid = result[0]
    #db.commit()
    return records

def get_name_service_in_id    (message_info,status_input,setting_bot,id_list):
    namebot     = message_info.setdefault('namebot','')
    #user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
    sql = "select id,name,info from service where id = {}".format (id_list)
    cursor.execute(sql)
    records = cursor.fetchall()
    #info_data = {}
    #for row in records:
        #id,name,info = row
    #sql = "UPDATE order_master SET {} = '{}' WHERE id = {}".format(name,info,id)
    #cursor.execute(sql)
    #db.commit()
    #sql         = "INSERT INTO order_master (name,info,user_id,status) VALUES ('','','{}','')  RETURNING id".format (user_id)
    #cursor.execute(sql)
    #result = cursor.fetchone()
    #lastid = result[0]
    #db.commit()
    return records

def get_name_adress_in_id     (message_info,status_input,setting_bot,id_list):
    namebot     = message_info.setdefault('namebot','')
    #user_id     = message_info.setdefault('user_id','')
    db,cursor   = connect_postgres (namebot)
    sql = "select id,name,info from address where id = {}".format (id_list)
    cursor.execute(sql)
    records = cursor.fetchall()
    #info_data = {}
    #for row in records:
        #id,name,info = row
    #sql = "UPDATE order_master SET {} = '{}' WHERE id = {}".format(name,info,id)
    #cursor.execute(sql)
    #db.commit()
    #sql         = "INSERT INTO order_master (name,info,user_id,status) VALUES ('','','{}','')  RETURNING id".format (user_id)
    #cursor.execute(sql)
    #result = cursor.fetchone()
    #lastid = result[0]
    #db.commit()
    return records
       
def executing_operator        (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back,id_lab):   ### Для кнопок с командой -i                                                           ###  Выполнение команды оператор в json
    answer = {}
    
    if 1==1:
        import iz_bot
        import json
        callback        = message_info.setdefault   ('callback','')                                                                     ###  Имя нажатой кнопки 
        json_string     = iz_bot.change_back        (callback.replace('i_',''))
        data_json       = json.loads                (json_string)
        label          = data_json.setdefault      ('l','')
        label_y          = data_json.setdefault      ('y','')
        label_m          = data_json.setdefault      ('m','')   
    
    if operation == 'time':
        #name_master = get_name_master_in_id (message_info,status_input,setting_bot,id_list)
        #name_master_text   = '1111'
        #for row in name_master:
        #    id,name_master_text,info = row  
        #id = update_order_psg (message_info,status_input,setting_bot,answer,id_lab,'master',name_master_text)
        
        id = update_order_psg (message_info,status_input,setting_bot,answer,label,'data2','222222')
        
        
        info_order = get_order_psg (message_info,status_input,setting_bot,'',label)
        
        message_id      = message_info.setdefault('message_id','')
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Фильтр'"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'filtr',label) 
        user_id         = message_info.setdefault ('user_id','') 
        message_name        = setting_bot .setdefault ("Показать адрес","Показать адрес")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        for row in info_order:
            id,info,name,master,service = row
        info_service = {}
        info_service ['Адрес']  = name
        info_service ['Услуга'] = service
        info_service ['Мастер'] = master
        list_change         = get_list_change         (message_info,status_input,setting_bot,message_text)
        for change in list_change:
            get_data = info_service.setdefault (change,"4444")
            message_text = message_text.replace ('##'+change+'##',get_data)        
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)      
        
    if operation == 'mastr':
        name_master = get_name_master_in_id (message_info,status_input,setting_bot,id_list)
        name_master_text   = '1111'
        for row in name_master:
            id,name_master_text,info = row  
        id = update_order_psg (message_info,status_input,setting_bot,answer,id_lab,'master',name_master_text)
        info_order = get_order_psg (message_info,status_input,setting_bot,'',label)
        message_id      = message_info.setdefault('message_id','')
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Фильтр'"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'filtr',label) 
        user_id         = message_info.setdefault ('user_id','') 
        message_name        = setting_bot .setdefault ("Показать адрес","Показать адрес")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        for row in info_order:
            id,info,name,master,service = row
        info_service = {}
        info_service ['Адрес']  = name
        info_service ['Услуга'] = service
        info_service ['Мастер'] = master
        list_change         = get_list_change         (message_info,status_input,setting_bot,message_text)
        for change in list_change:
            get_data = info_service.setdefault (change,"4444")
            message_text = message_text.replace ('##'+change+'##',get_data)        
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)      
    
    if operation == 'serv':
        name_servise = get_name_service_in_id (message_info,status_input,setting_bot,id_list)
        name_servise_text   = '1111'
        for row in name_servise:
            id,adress,name_servise_text = row        
        id = update_order_psg (message_info,status_input,setting_bot,answer,id_lab,'service',name_servise_text)
        info_order = get_order_psg (message_info,status_input,setting_bot,'',label)
        message_id      = message_info.setdefault('message_id','')
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Фильтр'"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'filtr',label) 
        user_id         = message_info.setdefault ('user_id','') 
        message_name        = setting_bot .setdefault ("Показать адрес","Показать адрес")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        for row in info_order:
            id,info,name,master,service = row
        info_service = {}
        info_service ['Адрес']  = name
        info_service ['Услуга'] = service
        info_service ['Мастер'] = master
        list_change         = get_list_change         (message_info,status_input,setting_bot,message_text)
        for change in list_change:
            get_data = info_service.setdefault (change,"4444")
            message_text = message_text.replace ('##'+change+'##',get_data)        
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)        
    
    if operation == 'filtr':
        if id_list == 8:
            message_id             = message_info.setdefault('message_id','')
            sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
            limit           = 10
            offset          = 0
            back            = ''
            ask             = "name = 'Услуга'"
            id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
            markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'serv',label) 
            user_id         = message_info.setdefault ('user_id','') 
            message_name    = 'Список услуг'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)
            
        if id_list == 9:
            message_id             = message_info.setdefault('message_id','')
            sql             = "select id,name from masters where ##s1## limit ##s2## offset ##s3##"
            limit           = 10
            offset          = 0
            back            = ''
            ask             = "1=1"
            id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
            markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'mastr',label) 
            user_id         = message_info.setdefault ('user_id','') 
            message_name    = 'Список Мастеров'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)
            
            
        if id_list == 10:
            message_id      = message_info.setdefault('message_id','')
            user_id         = message_info.setdefault ('user_id','') 
            message_name    = 'Список дат'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            from datetime import date
            current_date = date.today()
            year_current  = current_date.year
            month_curren  = current_date.month
            day_curren    = current_date.day
            lab             = complite_calendar (year_current,month_curren,day_curren)
            markup_list     = complite_key_psg_calendar (message_info,setting_bot,month_curren,year_current,label,lab)   
            #answer  = send_message (message_info,setting_bot,user_id,message_out,markup) 
            answer  = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)            
    
    if operation == 'date':
        sql             = "select id,name from time_calendar where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "1=1"
        id_sql          = save_sql_psg              (message_info,status_input,setting_bot,"Список время",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2        (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'time',label) 
        user_id         = message_info.setdefault   ('user_id','') 
        message_name    = 'Список времени'
        message_out     = gets_message_psg (message_info,setting_bot,message_name)
        message_text    = message_out.setdefault ('Текст','')
        answer          = send_message      (message_info,setting_bot,user_id,message_text,markup_list)          
        
    if operation == 'calc':
        
        import iz_bot                                                                                                                   ###  Основные функции программы
        import json
        callback        = message_info.setdefault   ('callback','')                                                                     ###  Имя нажатой кнопки 
        json_string     = iz_bot.change_back        (callback.replace('i_',''))
        data_json       = json.loads                (json_string)
        label          = data_json.setdefault      ('l','')
        label_y          = data_json.setdefault      ('y','')
        label_m          = data_json.setdefault      ('m','')
        label_lb          = data_json.setdefault      ('lb','')
        label_y = int(label_y.replace ('y',''))
        label_m = int(label_m.replace ('m',''))
        label_m_r = label_m + 1
        label_m_l = label_m - 1
        
        if label == "A":
            
            id = update_order_psg (message_info,status_input,setting_bot,answer,label_lb,'data1','1111')
            
            
            message_id      = message_info.setdefault('message_id','')
            sql             = "select id,name from time_calendar where ##s1## limit ##s2## offset ##s3##"
            limit           = 10
            offset          = 0
            back            = ''
            ask             = "1=1"
            id_sql          = save_sql_psg              (message_info,status_input,setting_bot,"Список время",sql,limit,offset,back)                                           
            markup_list     = complite_key_psg_2        (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'time',label_lb) 
            user_id         = message_info.setdefault   ('user_id','') 
            message_name    = 'Список времени'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)          
        
        if label == "right":
            user_id         = message_info.setdefault ('user_id','') 
            message_name    = 'Список дат'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            
            from datetime import date
            current_date = date.today()
            year_current  = current_date.year
            month_curren  = current_date.month
            day_curren    = current_date.day
            label_d     = 0
            if label_m_r == month_curren:
                label_d = day_curren
            lab             = complite_calendar (label_y,label_m_r,label_d)            
            markup_list     = complite_key_psg_calendar (message_info,setting_bot,label_m_r,label_y,"1",lab)   
            answer  = edit_message      (message_info,setting_bot,user_id,message_text,markup_list) 
   
            
        if label == "left":
            user_id         = message_info.setdefault ('user_id','') 
            message_name    = 'Список дат'
            message_out     = gets_message_psg (message_info,setting_bot,message_name)
            message_text    = message_out.setdefault ('Текст','')
            
            from datetime import date
            current_date = date.today()
            year_current  = current_date.year
            month_curren  = current_date.month
            day_curren    = current_date.day
            print ('[month]',month_curren)
            print ('[year]',year_current)
            print ('[day]',day_curren)
            label_d     = 0
            if label_m_l == month_curren:
                label_d = day_curren
            lab             = complite_calendar (label_y,label_m_l,label_d)
            markup_list     = complite_key_psg_calendar (message_info,setting_bot,label_m_l,label_y,"1",lab)   
            answer  = send_message      (message_info,setting_bot,user_id,message_text,markup_list) 

    if operation == 'adress':
        name_adress = get_name_adress_in_id (message_info,status_input,setting_bot,id_list)
        name_adres_text   = ''
        for row in name_adress:
            id,name_adres_text,info = row        
        id = update_order_psg (message_info,status_input,setting_bot,answer,id_lab,'name',name_adres_text)
        message_id      = message_info.setdefault('message_id','')
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Фильтр'"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'filtr',label) 
        user_id         = message_info.setdefault ('user_id','') 
        message_name        = setting_bot .setdefault ("Показать адрес","Показать адрес")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        info_service        = {'Адрес':name_adres_text}
        list_change         = get_list_change         (message_info,status_input,setting_bot,message_text)
        for change in list_change:
            message_text = message_text.replace ('##'+change+'##',info_service.setdefault (change,""))        
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id)
    
    if operation == 'picture':
        if id_list == 7:
            namebot      = message_info.setdefault ("namebot","") 
            user_id      = message_info.setdefault ("user_id","") 
            message_id   = message_info.setdefault ("message_id","")
            name_picture,id_picture = get_name_picture (message_info,status_input,setting_bot,id_lab,'right')
            print ('[name_picture] name_picture :',name_picture)
            sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
            limit           = 10
            offset          = 0
            back            = ''
            ask             = "name = 'Картинка'"
            id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список кнопки",sql,limit,offset,back)                                           
            markup_list     = complite_key_psg   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'picture',id_picture)                                                    
            import json
            import requests
            token = setting_bot['Токен']
            file_path = name_picture 
            files = {'media': open(file_path, 'rb'),}
            media = json.dumps({'type': 'photo','media': 'attach://media'})
            method = 'editMessageMedia'
            url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)               
            params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':'','reply_markup':markup_list}
            resp = requests.post(url, params,files = files)           
    
        if id_list == 6:
            namebot      = message_info.setdefault ("namebot","") 
            user_id      = message_info.setdefault ("user_id","") 
            message_id   = message_info.setdefault ("message_id","")
            name_picture,id_picture = get_name_picture (message_info,status_input,setting_bot,id_lab,'left')
            sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
            limit           = 10
            offset          = 0
            back            = ''
            ask             = "name = 'Картинка'"
            id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список кнопки",sql,limit,offset,back)                                           
            markup_list     = complite_key_psg   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'picture',id_picture)                                                    
            import json
            import requests
            token = setting_bot['Токен']
            file_path = name_picture 
            files = {'media': open(file_path, 'rb'),}
            media = json.dumps({'type': 'photo','media': 'attach://media'})
            method = 'editMessageMedia'
            url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)               
            params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':'','reply_markup':markup_list}
            resp = requests.post(url, params,files = files)           
    
    if operation == 'usr': 
        send_user_message_v1    (message_info,status_input,setting_bot,"Заявка на услугу")
    
    if operation.find ('service') != -1: 
        message_info ['Выбор'] = str(id_list)
        #info_answer = active_save_data_main (message_info,status_input,setting_bot,'Услуга','Сбор данных') 
        return ''
    
    if operation.find ('person') != -1:     
        message_info ['Выбор'] = str(id_list)
        #info_answer = active_save_data_main (message_info,status_input,setting_bot,'Услуга','Сбор данных') 
        return ''

    if operation.find ('time') != -1:     
        message_info ['Выбор'] = str(id_list)
        #info_answer = active_save_data_main (message_info,status_input,setting_bot,'Услуга','Сбор данных') 
        return ''
        
    if operation == 'bots': 
        if id_list == 1:
            user_id         = message_info.setdefault ('user_id','') 
            message         = setting_bot .setdefault ("Главное меню nnm","Главное меню nnm")
            answer          = save_message (message_info,setting_bot,user_id,message)
            message_out     = gets_message (message_info,setting_bot,user_id,message)
            markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
            answer          = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
            #status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",""]]
    
        if id_list == 2:
            user_id         = message_info.setdefault ('user_id','') 
            message         = setting_bot .setdefault ("Главное меню столовая","Главное меню столовая")
            answer          = save_message (message_info,setting_bot,user_id,message)
            message_out     = gets_message (message_info,setting_bot,user_id,message)
            markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
            answer          = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
       
    if operation == 'find':
        send_user_message_v1    (message_info,status_input,setting_bot,"Список последних обновлений по данной категории")
        status_input        = user_save_data (message_info,status_input,setting_bot,[["Сбор данных",""]])
        info_ask_torrent    = get_service       (message_info,status_input,setting_bot,id_list)
        sql = info_ask_torrent['SQL']
        list_answer         = execution_procedure_sql (message_info,status_input,setting_bot,sql)
        send_telegram_message (message_info,status_input,setting_bot,list_answer)
        
    if operation == 'ask': 
        namebot         = message_info.setdefault ('namebot','')
        user_id         = message_info.setdefault ('user_id','') 
        message_id      = message_info.setdefault ('message_id','')
        message_name    = setting_bot .setdefault ("Вопрос анкеты","Вопрос анкеты")
        message_out     = gets_message_psg        (message_info,setting_bot,message_name)
        message_text    = message_out.setdefault  ("Текст","Пустой текст")
        db,cursor       = connect_postgres        (namebot)
        sql = "select id,name,ask,answer1,answer2,answer3,answer4 from  anketa where 1=1;".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name,ask,answer1,answer2,answer3,answer4 = rec
            print ('[+] Анкета: ',id,name,ask,answer1,answer2,answer3,answer4)
        key = {}
        key['Кнопка 11'] = "Ответ 1"
        key['Кнопка 21'] = "Ответ 2"
        key['Кнопка 31'] = "Ответ 3"
        key['Кнопка 41'] = "Ответ 4"
        key['Команда 11'] = "Ответ 1"
        key['Команда 21'] = "Ответ 2"
        key['Команда 31'] = "Ответ 3"
        key['Команда 41'] = "Ответ 4"
        markup_list = key_type_message (key)
        element = {}
        element['ask'] = str(ask)
        element['answer1'] = str(answer1)
        element['answer2'] = str(answer2)
        element['answer3'] = str(answer3)
        element['answer4'] = str(answer4)
        list_change     = get_list_change (message_info,status_input,setting_bot,message_text)    
        message_text    = change_message (message_info,status_input,setting_bot,message_text,list_change,element)    
        answer          = edit_message            (message_info,setting_bot,user_id,message_text,markup_list,message_id) 
        
    if operation == 'anketa': 
        namebot         = message_info.setdefault('namebot','')
        user_id         = message_info.setdefault ('user_id','') 
        message_id      = message_info.setdefault('message_id','')
        sql             = "select id,ask from anketa where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "1=1"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'ask',label) 
        message_name        = setting_bot .setdefault ("Список вопросов","Список вопросов")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id) 
       
    if operation == 'catat':                                                                                                                                    ###  Нажата кнопка в списке
        ### id_list - id товара в списке
        ### id_sql  - id sql запроса
        ### Мы получили код товара и код запроса sql. Теперь нам нужно собрать информацию о товаре. 
        ### Шаг назад это возврашение в список, а именно id_sql.
        
        info_tovar = get_info_tovar (message_info,status_input,setting_bot,id_list)                                                                             ###  Получаем библиотеку информации о товаре. Информация может собиратся из нескольких баз и таблиц.
        
        if info_tovar['catalog'] == 1:                                                                                                                          ###  Это каталог выводим. Выводим список всех товаров в который указан данный каталог 
            sql      = "select id,`info` from `service` where %s limit %s offset %s"
            ask      = "name_catalog = {} ".format (info_tovar['name_catalog'])
            limit    = 10
            offset   = 0            
            back     = id_sql                                                                                                                                   ###  Передаем номер сообщения для возврата из каталога
            id_sql   = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                              ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения            
            key_list = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'catat')
            
        if info_tovar['catalog'] == 0:                                                                                                                          ###  Это товар выводим информацию о товаре
            user_id        = message_info['user_id']
            message_out,markup = get_message_tovar (message_info,status_input,setting_bot,id_list,info_tovar)
            answer         = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
            
    if operation == 'back':                                                                                                                                     ###  Нажата кнопка вернутся назад 
        sql,ask,limit,offset,back = get_sql (message_info,id_sql)
        id_sql                    = id_sql         
        key_list                  = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'catat')
 
    if operation == 'mes': 
        user_id        = message_info['user_id']
        informanion    = get_message_in_id (message_info,status_input,setting_bot,id_list)                                                                      ### Собираем информацию о товаре
        message_out    = get_message_text (message_info,status_input,setting_bot,informanion)                                                                   ### Готовим текст сообщения о товаре
        sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
        limit           = 20
        offset          = 0
        back            = ''
        ask             = "name = 'message'"
        id_sql          = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
        info_data       = {'back':'','message_id':id_list}
        answer          = data_sql     (message_info,status_input,setting_bot,id_sql,info_data)
        markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'com_mes')                                                        ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
        answer          = send_message   (message_info,setting_bot,user_id,message_out,markup_list)  
    
    if operation == 'menu': 
        pass

    if operation == 'key':                                                                                                                                      ### Пришла команда изменения цвета
        from iz_bot import connect as connect  
        namebot             = message_info.setdefault('namebot','')
        db,cursor           = connect (namebot)         
        sql                 = "select id,name,key11,key12,key13,key14,key_name from `key` where id = {}".format(id_list)
        cursor.execute(sql)
        data = cursor.fetchall()
        name                = ''
        for rec in data:
            id,name,key11,key12,key13,key14,key_name = rec.values()
            if id_sql == 1:
                user_save_data (message_info,status_input,setting_bot,[[key_name,"key12"]])
            if id_sql == 2:
                user_save_data (message_info,status_input,setting_bot,[[key_name,"key13"]])
            if id_sql == 3:
                user_save_data (message_info,status_input,setting_bot,[[key_name,"key14"]])
            if id_sql == 4:
                user_save_data (message_info,status_input,setting_bot,[[key_name,"key11"]])
            user_id              = message_info.setdefault ('user_id','') 
            info_service         = {}
            message_id           = message_info.setdefault('message_id',0)
            message_out,markup   = get_message_setting    (message_info,status_input,setting_bot,info_service)                                                  ### Вывод сообщения у которого заполнены все переменные
            answer               = edit_message           (message_info,setting_bot,user_id,message_out,markup,message_id)

    return ''
 
def executing_program_json  (message_info,status_input,setting_bot):                                                                                            ###  Разбор команды оператор в json
    import iz_bot                                                                                                                   ###  Основные функции программы
    import json
    callback        = message_info.setdefault   ('callback','')                                                                     ###  Имя нажатой кнопки 
    json_string     = iz_bot.change_back        (callback.replace('i_',''))
    data_json       = json.loads                (json_string)
    operation       = data_json.setdefault      ('o','')                                                                            ###  Название команды переданной  в json
    id_list         = data_json.setdefault      ('i','')                                                                            ###  Параметр id переданной       в json    
    id_sql          = data_json.setdefault      ('s','')                                                                            ###  Параметр id_sql переданной   в json 
    id_back         = data_json.setdefault      ('b','')                                                                            ###  Параметр id_back переданной  в json
    id_lab          = data_json.setdefault      ('l','')
    print_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back)                                    ###  Печатаем команды полученные  в json
    executing_operator  (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back,id_lab)                                    ###  Выполняем команды полученные в json

def testing_time            (message_info,status_input,setting_bot,hour_start,minute_start,hour_finishe,minute_finishe):                                        ###  Проверка поподания в определенный дэопазон времени    
    import datetime
    import iz_bot
    now         = datetime.datetime.now()
    namebot     = message_info.setdefault('namebot','')
    now_time    = datetime.datetime.now().time()
    now_date    = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y %H:%M:%S')
   
def build_jsom (dict):       #### {"o":"next","sql":id_sql}
    json_message = str(dict)
    json_message = json_message.replace ("'",'"')
    json_message = json_message.replace ('"','#')
    #json_message = change(json_message)
    json_message = "i_"+json_message
    json_message = json_message.replace (", ",',')
    json_message = json_message.replace (": ",':')
    return (json_message) 

def complite_key_psg_2      (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,metka,lab):                                                              ###  Формируем кнопокe из списока  по переданным нам параметрам
    import json
    namebot         = message_info.setdefault('namebot','')
    db,cursor       = connect_postgres (namebot)    
    sql = sql.replace("##s1##",str(ask))
    sql = sql.replace("##s2##",str(limit))
    sql = sql.replace("##s3##",str(offset))
    cursor.execute(sql)
    data = cursor.fetchall()
    key_array = {}
    nomer = 0 
    key_row = 1
    for rec in data: 
        id,info = rec
        command =  build_jsom ({'o':metka,'i':id,'s':id_sql,'l':lab})
        nomer = nomer + 1
        key_tab = nomer
        key_row = 1
        key_array['Кнопка '  + str(key_tab) + str(key_row)] = info
        key_array['Команда ' + str(key_tab) + str(key_row)] = command
    if back != '':                                                                                                                                              ### Если нам передали информацию как вернутся назад заносим ее        
        name_key = set_name_key (message_info,'Кнопка назад') 
        command  = iz_bot.build_jsom ({'o':'back','s':id_sql,'b':back})
        key_array.append ([[name_key,command],['',''],['','']]) 
    markup   = key_type_message (key_array)
    return markup

def complite_key_psg        (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,metka,lab):                                                              ###  Формируем кнопокe из списока  по переданным нам параметрам
    import json
    namebot         = message_info.setdefault('namebot','')
    db,cursor       = connect_postgres (namebot)    
    sql = sql.replace("##s1##",str(ask))
    sql = sql.replace("##s2##",str(limit))
    sql = sql.replace("##s3##",str(offset))
    cursor.execute(sql)
    data = cursor.fetchall()
    key_array = {}
    nomer = 0 
    key_row = 1
    for rec in data: 
        id,info = rec
        command =  build_jsom ({'o':metka,'i':id,'s':id_sql,'l':lab})
        nomer = nomer + 1
        if nomer == 1:
            key_tab = 1
            key_row = 1
        if nomer == 2:
            key_tab = 1
            key_row = 2
        key_array['Кнопка '  + str(key_tab) + str(key_row)] = info
        key_array['Команда ' + str(key_tab) + str(key_row)] = command
    if back != '':                                                                                                                                              ### Если нам передали информацию как вернутся назад заносим ее        
        name_key = set_name_key (message_info,'Кнопка назад') 
        command  = iz_bot.build_jsom ({'o':'back','s':id_sql,'b':back})
        key_array.append ([[name_key,command],['',''],['','']]) 
    markup   = key_type_message (key_array)
    return markup  

def save_sql_psg            (message_info,status_input,setting_bot,name,sql,limit,offset,back):
    namebot    = message_info.setdefault('namebot','')
    #from iz_bot import connect_postgres as connect_postgres
    db,cursor    = connect_postgres (namebot)
    namebot    = message_info.setdefault('namebot','')
    sql = "INSERT INTO data_sql (name,data,limit1,offset1,back1,status) VALUES (%s,%s,%s,%s,%s,'')".format ()
    sql_save = (name,sql,limit,offset,back)
    result = cursor.execute(sql,sql_save)
    db.commit() 
    lastid = 1
    #lastid = cursor.lastrowid
    return lastid 

##################################################################################################################################################################################################   
   
def print_status            (message_info,status_input,setting_bot):
    #print ('[+] Начальные настройки по текущиму пользователю.')
    for line in status_input:
        #print ('        [+]',line,'-',status_input[line])
        pass
    status     = status_input.setdefault('status','')
    
def executing_admin         (message_info,status_input,setting_bot):
    message_in     = message_info.setdefault ('message_in','') 
    if status_input.setdefault('Админ','') == 'Да':
        if message_in   == '/admin':
            user_id     = message_info.setdefault ('user_id','') 
            message     = setting_bot .setdefault ("Сообщение администратору","Вы администратор бота")
            answer      = save_message (message_info,setting_bot,user_id,message)
            message_out = gets_message (message_info,setting_bot,user_id,message)
            markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
            answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
        
        if message_in   == '/send':                                                                                                         ### Рассылка сообщений телеграмм боты
           pass
        
        if  message_in   == '/key':                                                                                                         ### Выводим команды администратора
            user_id     = message_info.setdefault ('user_id','') 
            message     = setting_bot .setdefault ("Сообщение команды администратора","Команды администратора")                             ### Команды администратора
            answer      = save_message (message_info,setting_bot,user_id,message)
            message_out = gets_message (message_info,setting_bot,user_id,message)
            markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
            answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)

        if  message_in   == '/new':                                                                                                             ### Создаем новое питание
            pass
            
        if  message_in   == '/input_01':                                                                                                                ### Исправляем часть питание
            pass
            
        if  message_in   == '/task':                                                                                                                        ### Получаем список заданий
            pass
            
        if  message_in   == '/message':                                                                                                                     ### Исправляем исходящие сообщения    
            user_id         = message_info['user_id']
            sql             = "select id,`info` from `message` where ##s1## limit ##s2## offset ##s3##"
            limit           = 20
            offset          = 0
            back            = ''
            ask             = "name = 'Имя'"
            id_sql          = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
            markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'mes')                                                      ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
            message         = setting_bot .setdefault ("Сообщение заменить сообщение","Заменить сообщение")                                                               ###  Выводим полученный список
            answer          = save_message   (message_info,setting_bot,user_id,message)
            message_out     = gets_message   (message_info,setting_bot,user_id,message)          
            answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list)    
                
        if  message_in   == '/menu':                                                                                                                        ### Исправляем исходящие список меню                
            user_id         = message_info['user_id']
            sql             = "select id,`info` from `menu` where ##s1## limit ##s2## offset ##s3##"
            limit           = 20
            offset          = 0
            back            = ''
            ask             = "name = 'Имя'"
            id_sql          = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
            markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'menu')                                                      ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
            message         = setting_bot .setdefault ("Сообщение заменить меню","Заменить меню")                                                               ###  Выводим полученный список
            answer          = save_message   (message_info,setting_bot,user_id,message)
            message_out     = gets_message   (message_info,setting_bot,user_id,message)          
            answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list) 

        if  message_in   == '/setting':                                                                                                                             ### Исправляем настроки бота
            pass    
                      
def testing_double          (message_info,status_input,setting_bot):
    message_in      =  message_info['message_in']
    if message_in   == status_input.setdefault('message_in','') :
        user_id     = message_info.setdefault('user_id','') 
        message     = setting_bot .setdefault ("Сообщение повторное нажатие клавиши","Повторное нажатие клавиши")
        answer      = save_message (message_info,setting_bot,user_id,message)
        message_out = gets_message (message_info,setting_bot,user_id,message)
        markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
        answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
    save_data   = [['message_in',message_in]] 
    status_input = user_save_data (message_info,status_input,setting_bot,save_data)
    
def testing_blocking        (message_info,status_input,setting_bot):                                                                                            ### Проверяем ввод оснавных параметров пользователя    
    result = {}
    message_in  = message_info.setdefault ('message_in','')                                                                                                     ### Проверяем статус - возможно пользователь ввел значение
    callback    = message_info.setdefault ('callback','')
    ask         = 0
    label_send  = True
    
    if callback == 'Ввести данные' and label_send == True:
        label_send = False
        ask = get_ask_nomer (message_info,status_input,setting_bot) 
        if ask != 0:
            send_message_ask (message_info,status_input,setting_bot,ask)
        result['operation'] = "Ввод данных"
    if message_in.find ('/start') == -1 and label_send == True:                                                                                                 #### Проверяем любое входящие сообщение
        label_send = False
        status     = status_input.setdefault ('Статус','')  
        if status != '':                                                                                                                                        #### Проверяем что это не ответ на поставленный вопрос    
            ask_answer = get_ask_nomer_status (message_info,status_input,setting_bot,status)
            if ask_answer.setdefault('id',0) != 0:
                user_id         = message_info.setdefault('user_id','') 
                message         = ask_answer['message_answer']
                answer          = save_message   (message_info,setting_bot,user_id,message)
                message_out     = gets_message   (message_info,setting_bot,user_id,message)
                markup          = gets_key       (message_info,setting_bot,user_id,message_out['Меню'])
                answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup)
                status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",""],[ask_answer['name'],message_in]])
                #import time
                #time.sleep (20)
        ask = get_ask_nomer (message_info,status_input,setting_bot)                                                                                             #### Проверяем если не заданные вопросы если есть задаем    
        if ask != 0:
            send_message_ask (message_info,status_input,setting_bot,ask)
    return result            
   
def save_info_refer         (message_info,status_input,setting_bot):
    message = message_info.setdefault ('message_in','')
    if message.find ("/start") != -1:
        if status_input.setdefault ('referal','') == '':
            referal = message.replace ("/start","")
            status_input    = user_save_data (message_info,status_input,setting_bot,[["Реферал",referal]])
            user_id         = referal
            message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")
            answer          = save_message   (message_info,setting_bot,user_id,message)
            message_out     = gets_message   (message_info,setting_bot,user_id,message)
            markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
            answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)                                       ### Информируем что пришел Ваш реферал.
            user_id         = referal
            message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")                                                      ### Информируем что клиент стал чем то рефералом 
            answer          = save_message   (message_info,setting_bot,user_id,message)
            message_out     = gets_message   (message_info,setting_bot,user_id,message)
            markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
            answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
            
def save_info_user          (message_info,status_input,setting_bot):                                                                                            ### Информация о пользователе постоянно меняется. Записываем ее в специальный справочник
    pass
    
def save_message_user       (message_info,status_input,setting_bot):
    from iz_bot import connect as connect
    namebot     = message_info.setdefault  ('namebot','') 
    db,cursor = connect (namebot)
    sql = "INSERT INTO log (user_id,user_name,surname,name,message_in,command,full_message,messsage_out_1,messsage_out_2,messsage_out_3,answert) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format ()
    sql_save = ("","","","","","","","","","","")
    result = cursor.execute(sql,sql_save)
    db.commit() 
    lastid = cursor.lastrowid
    return lastid 
    
def executing_status        (message_info,status_input,setting_bot,answer):
    if status_input.setdefault('Статус','') == 'Ввод города':                                                                       ###  Пример работы статусного сообщения
        pass
    message_in      = message_info.setdefault ("message_in","")   
    namebot         = message_info.setdefault ("namebot","")   
    if status_input.setdefault('Статус','') == 'Ввод предложения':     
        save_data   = [['Статус','']]
        user_save_data_psg       (message_info,status_input,setting_bot,save_data)    
        #send_user_message_v1    (message_info,status_input,setting_bot,"Данные записаны")
        user_id      = message_info.setdefault ("user_id","")   
        message_name     = "Данные записаны"
        message_out      = gets_message_psg (message_info,setting_bot,message_name)
        answer_null      = send_message (message_info,setting_bot,user_id,message_out['Текст'],{})
        db,cursor    = connect_postgres (namebot)
        sql         = "INSERT INTO survey (user_id,name,info,answer) VALUES ('{}','Оставить отзыв','{}','')".format (user_id,message_in)
        cursor.execute(sql)
        db.commit()  
        
        list_admin = get_list_admin_psg          (message_info,status_input,setting_bot)
        print ('[list_admin]',list_admin)
        
        for line in list_admin:
            id,send_user_id = line
            print ('[+]',id,send_user_id)
            message_text = 'Рекомендации :' + str(message_in)
            answer_null      = send_message (message_info,setting_bot,send_user_id,message_text,{})
        
        
        
    answer = {}
    return answer 
        
def executing_run           (message_info,status_input,setting_bot,answer):
    answer = {}
    return answer 

def executing_message       (message_info,status_input,setting_bot,answer):
    message_in      = message_info.setdefault ("message_in","")   
    callback        = message_info.setdefault ("callback","")   
    result = {}    
    #print ('[+] message_in:',message_in)    
    if message_in   == '📅 Расписание':
        info_answer = active_save_data_main      (message_info,status_input,setting_bot,'Услуга','Старт')
    else:
        if  message_in != '':
            info_answer = active_save_data_main (message_info,status_input,setting_bot,'Услуга','Сбор данных')         
    user_id         = message_info.setdefault ("user_id","")       
    message_test    = 'Проверка связи' 
    token           = setting_bot['Токен']
    method          = 'sendPhoto'
    
    if callback   == 'Лицензии': 
        namebot      = message_info.setdefault ("namebot","") 
        name_picture,id_picture = get_name_picture (message_info,status_input,setting_bot,0,'right')
        import requests        
        params = {}
        params['chat_id'] = user_id
        params['caption'] = str(message_test)
        params['parse_mode'] = 'HTML'
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Картинка'"
        id_sql          = save_sql_psg       (message_info,status_input,setting_bot,"Список Уроки",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'picture',id_picture)                                                    
        params['reply_markup']  = markup_list
        file_path = name_picture
        file_opened = open(file_path, 'rb')
        files = {'photo': file_opened}
        url='https://api.telegram.org/bot{0}/{1}'.format(token, method) 
        resp = requests.post(url, params, files=files)
        answer = resp.json()   
        
        
        
    if message_in   == 'Вопрос':
        send_user_message_v1    (message_info,status_input,setting_bot,"Помошь по боту")
        result['operation'] = "Вопрос"
    
    if message_in   == 'Анкета':                                                                                                                                ### Формируем список Анкет
        user_id         = message_info['user_id']
        sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Анкета'"
        id_sql          = save_sql     (message_info,status_input,setting_bot,"Список анкет",sql,limit,offset,back)                                           
        markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'service')                                                    
        message         = setting_bot .setdefault ("Сообщение анкета список","Список анкет")                                                                  
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)          
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list)
        result['operation'] = "Анкета"
    
    if message_in   == 'Настройка': 
       user_id              = message_info['user_id']
       info_service         = {}
       message_out,markup   = get_message_setting    (message_info,status_input,setting_bot,info_service)                                                       ### Вывод сообщения у которого заполнены все переменные
       answer               = send_message           (message_info,setting_bot,user_id,message_out,markup)
       result['operation'] = "Настройка"
    
    if message_in   == 'Главное меню':                                                                                                                          ###  Пример работы тестового Входящего сообщения              
        user_id         = message_info['user_id']
        sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
        limit           = 20
        offset          = 0
        back            = ''
        ask             = "name = 'Программа'"
        id_sql          = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
        markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'bots')                                                      ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
        message         = setting_bot .setdefault ("Сообщение тестовый список","Тестовый список")                                                               ###  Выводим полученный список
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)          
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list)
        result['operation'] = "Главное меню"
    
    return result
         
def executing_program       (message_info,status_input,setting_bot,answer):
    callback    =   message_info.setdefault ("callback","")
    user_id     =   message_info.setdefault ("user_id","")
    message_id  =   message_info.setdefault ("message_id","")
    
    if callback   == 'Анкета':
        message_id      = message_info.setdefault('message_id','')
        user_id         = message_info.setdefault ('user_id','') 
        sql             = "select id,info from service where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Анкета'"
        id_sql          = save_sql_psg         (message_info,status_input,setting_bot,"Список фильтр",sql,limit,offset,back)                                           
        markup_list     = complite_key_psg_2   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'anketa',0) 
        message_name        = setting_bot .setdefault ("Показать адрес","Список Анкет")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")      
        answer          = edit_message      (message_info,setting_bot,user_id,message_text,markup_list,message_id) 
    
    if callback   == 'Оставить отзыв':
        save_data  = [['Статус','Ввод предложения']]
        user_save_data_psg       (message_info,status_input,setting_bot,save_data)

    if callback.find ('i_') != -1 and callback.find ('game_farmer') == -1 :                                                                                                  ###  Кнопка которая передала в json информацию
        executing_program_json (message_info,status_input,setting_bot)
    
    if callback == 'О нас':
        import requests
        message_out = "Test video"
        token = setting_bot['Токен']
        method = "sendVideo"
        name_video = 'W:\\Picture_site\\IMG_3950.MOV'
        params = {}
        params['chat_id'] = user_id
        params['caption'] = str(message_out)
        params['parse_mode'] = 'HTML'
        params['show_caption_above_media'] = True
        params['reply_markup'] = {}
        file_path = name_video
        file_opened = open(file_path, 'rb')
        files = {'video': file_opened}
        url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
        resp = requests.post(url, params, files=files)
        answer = resp.json()   
        print (    '[Ответ Отправки] :',answer)          
        
    if callback == 'Записаться':
        last_id = create_order_psg (message_info,status_input,setting_bot,answer)
        user_id             = message_info['user_id']
        message_id          = message_info['message_id']
        message_name        = setting_bot .setdefault ("Показать адрес","Показать адрес")
        message_out         = gets_message_psg (message_info,setting_bot,message_name)
        message_text        = message_out.setdefault ("Текст","Пустой текст")
        info_service        = {'Адрес':'не выбран'}
        list_change         = get_list_change         (message_info,status_input,setting_bot,message_text)
        for change in list_change:
            message_text = message_text.replace ('##'+change+'##',info_service.setdefault (change,""))
        
        sql                 = "select id,name from address where ##s1## limit ##s2## offset ##s3##"
        limit               = 20
        offset              = 0
        back                = ''
        ask                 = "1=1"
        id_sql              = save_sql_psg       (message_info,status_input,setting_bot,"Адрес",sql,limit,offset,back)                                           
        markup_list         = complite_key_psg   (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'adress',last_id) 
        answer              = edit_message       (message_info,setting_bot,user_id,message_text,markup_list,message_id) 
    
    if callback == 'Лево':  
        name_picture = "W:\\Send_Message\\a123bot_00581.jpg"
        import json
        import requests
        token = setting_bot['Токен']
        file_path = name_picture 
        files = {'media': open(file_path, 'rb'),}
        media = json.dumps({'type': 'photo','media': 'attach://media'})
        method = 'editMessageMedia'
        #markup = json.dumps(array)
        markup = '{"inline_keyboard":[[{"text": "Лево","callback_data": "Лево"},{"text": "Право","callback_data": "Право"}]]}'
        url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)   #?chat_id=399838806&message_id=871&media='+str(media)+''            
        params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':'444444444444444444','reply_markup':markup  }
        #if menu_name != '' or key_array != '':
        #token = setting_bot['Токен']
        resp = requests.post(url, params,files = files)                
        print (resp.json())
        
    if callback == 'Право':                                                                                                  ###  Пример работы команды кнопки
        method = "editMessageMedia"
        import requests
        import json
        token = setting_bot['Токен']
        name_picture = "W:\\Send_Message\\a123bot_00581.jpg"
        file_path = name_picture 
        files = {'media': open(file_path, 'rb'),}
        media = json.dumps({'type': 'photo','media': 'attach://media'})
        method = 'editMessageMedia'
        #markup = json.dumps(array)
        url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)   #?chat_id=399838806&message_id=871&media='+str(media)+''
        markup = '{"inline_keyboard":[[{"text": "Лево","callback_data": "Лево"},{"text": "Право","callback_data": "Право"}]]}'        
        params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':'444444444444444444','reply_markup':markup}
        #if menu_name != '' or key_array != '':
        #params['reply_markup'] = '{"inline_keyboard":[[{"text": "Лево","callback_data": "Лево"},{"text": "Право","callback_data": "Право"}]]}'
        
        resp = requests.post(url, params,files = files)                
        print (resp.json())
    
    if callback == 'save_message':                                                                                                  ###  Пример работы команды кнопки
        pass
    
    if callback == 'Вызов меню':                                                                                                    ###  Пример работы команды кнопки
        pass  
        
    if callback.find ("cbcal_") != -1:
        from datetime import datetime, date, timedelta
        from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
        result, key, step = DetailedTelegramCalendar(locale='ru',min_date=date.today(), max_date=date.today() + timedelta(days=3)).process(callback)
    
        if not result and key:
            user_id         = message_info['user_id']
            message_text    = '1111'
            markup          = key
            message_id      = message_info.setdefault ("message_id","")
            answer       = edit_message           (message_info,setting_bot,user_id,message_text,markup,message_id)
        elif result:
            pass
            message_info['Выбор'] = result
            answer           = active_save_data_main (message_info,status_input,setting_bot,'Услуга','Сбор данных')
    
        
    answer = {}
    return answer      
    
def executing_command       (message_info,status_input,setting_bot):                                                                                     ### Выполнение общих команд бота /start
    result      = {}
    message_in  = message_info.setdefault ("message_in","")
    if message_info['callback'] == 'Ввод данных':
        user_id         = message_info.setdefault('user_id','') 
        message         = setting_bot .setdefault ("Сообщение 0001","Ввод данных")
        answer_nul      = save_message (message_info,setting_bot,user_id,message)
        message_out     = gets_message (message_info,setting_bot,user_id,message)
        markup          = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
        answer_nul      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
        result['operation'] = "Ввод данных"
    return result    
       
def gets_message_psg        (message_info,setting_bot,message_name): 
    #from iz_bot import connect as connect   
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = connect_postgres (namebot)
    message_out  = {}
    sql = "select id,name,info,picture,menu from message where name = '{}';".format(message_name)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,info,picture,menu = rec
        message_out['Имя']      = name
        message_out['Текст']    = info 
        message_out['Меню']     = menu 
        message_out['Картинка']  = picture        
    return message_out        
                 
def get_list_admin_psg      (message_info,status_input,setting_bot):
    #from iz_bot import connect as connect
    namebot      = message_info.setdefault  ('namebot','') 
    db,cursor    = connect_postgres (namebot)
    #db,cursor = connect (namebot)
    sql = "select id,name from admin  where 1=1  ;".format ()
    cursor.execute(sql)
    results  = cursor.fetchall()
    #data_id  = 0
    #for row in results:
    #    id,name,info = row.values() 
    #    print ('[+] ',id,name,info)
    return results     
          
def get_list_admin          (message_info,status_input,setting_bot):
    from iz_bot import connect as connect
    namebot     = message_info.setdefault  ('namebot','') 
    db,cursor = connect (namebot)
    sql = "select users.id,users.name,users.info from users as users, users as admin where users.name = 'user_id' and admin.name = 'Админ' and admin.info = 'Да' and users.data_id = admin.data_id  ;".format ()
    cursor.execute(sql)
    results  = cursor.fetchall()
    data_id  = 0
    #for row in results:
    #    id,name,info = row.values() 
    #    print ('[+] ',id,name,info)
    return results
     
def send_message_admin      (message_info,status_input,setting_bot,list_admin,message_text,picture,markup):                                                        ### Рассылка всем администраторам отчета по отправке 
    

    for rec in list_admin:   
        id,name,user_id_admin = rec.values()
        send_user_message_v2    (message_info,status_input,setting_bot,user_id_admin,message_text,picture,markup)

def executing_free_messsage (message_info,status_input,setting_bot,answer):                                                                                     ### Сообщение полученное текстом от пользователя
    #message_in      = message_info.setdefault ("message_in","")
    list_admin      = get_list_admin     (message_info,status_input,setting_bot)
    #answer          = save_message_admin (message_info,status_input,setting_bot)
    #markup          = get_admin_key ()
    message_out     = "Сообщение Администратору"
    picture         = ""
    markup          = {}
    answer          = send_message_admin (message_info,status_input,setting_bot,list_admin,message_out,picture,markup)
    
def executing_start         (message_info,status_input,setting_bot,answer):
    result               = {}
    message_in           = message_info.setdefault ("message_in","")
    if message_in.find ('/start') != -1:                                                                                                                        #### Модуль подготовки сообшения         
        user_id          = message_info.setdefault ('user_id','') 
        message_name     = '/start'
        message_out      = gets_message_psg (message_info,setting_bot,message_name)
        markup           = gets_key_psg (message_info,setting_bot,message_out.setdefault ('Меню',''))
        #answer           = save_message (message_info,setting_bot,user_id,message)
        #message_out      = gets_message (message_info,setting_bot,user_id,message)
        #ask              = get_ask_nomer (message_info,status_input,setting_bot)
        #if ask == 0:
        #    markup              = gets_key                 (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
        #else:
        #    markup              = gets_key                  (message_info,setting_bot,user_id,'Ввод данных')
        #answer                  = send_message              (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        #if ask != 0:
        #    user_id             = message_info.setdefault   ('user_id','') 
        #    message             = setting_bot .setdefault   ("Информирование о вводе данных","Информирование о вводе данных")
        #    answer              = save_message              (message_info,setting_bot,user_id,message)
        #    message_out         = gets_message              (message_info,setting_bot,user_id,message)
        #    key                 = complite_key_for_name     ("Ввести данные")
        #    markup              = key_type_message          (key)
        #    answer              = send_message              (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        #status_input            = user_save_data            (message_info,status_input,setting_bot,[["Статус",""]])                                                                          #### Модуль обнуления данных                                      
        #result['operation'] = "Ответ /start"
        print ('[+] markup : ',markup)
        answer              = send_message      (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        print ('[+] answer :',answer)
        result = ''
    return result    
        
def executing_game_         (message_info,status_input,setting_bot): 
    message_in      = message_info.setdefault ("message_in","")
    callback        = message_info.setdefault ("callback","")
    result          = {}
    if message_in   == 'Coin Farmer' or message_in == '/Farmer':
        label_send  = True
        import iz_game
        iz_game.game_farmer_1 (message_info,status_input,setting_bot)
        result['operation'] = "Coin Farmer"
        #return ''

    if callback.find ('game_farmer_') != -1:
        label_send = True
        import iz_game
        iz_game.game_farmer_2 (message_info,status_input,setting_bot)
        result['operation'] = "Coin Farmer"
    return result
 
def analis                  (message_info,status_input,setting_bot,answer):
    status  = answer.setdefault ('status' ,'')
    message = answer.setdefault ('message','')
    program = answer.setdefault ('program','')
    user_id = answer.setdefault ('user_id','')
    if message == '':
        message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")                                                          
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)
        markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
        answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
   
def save_out_message        (message_info,status_input,setting_bot):
    pass
     
def get_setting_psg         (message_info):
    namebot = message_info['namebot']
    db,cursor = connect_postgres (namebot)
    answer = {}
    sql = "select id,name,info from setting where status <> 'delete' ".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row
        answer[name] = info
    return answer   
     
def gets_key_psg            (message_info,setting_bot,menu_name):   #### Получить меню из базы
    namebot = message_info.setdefault('namebot','')
    db,cursor = connect_postgres (namebot)
    sql     = "select id,name,menu,key11,key12,key13,key21,key22,key23,key31,key32,key33,key41,key42,key43,change11,change12,change13,change21,change22,change23,change31,change32,change33,change41,change42,change43,command11,command12,command13,command21,command22,command23,command31,command32,command33,command41,command42,command43 from menu where id = {}".format (menu_name)
    cursor.execute(sql)
    results     = cursor.fetchall()    
    markup      = {}
    key         = {}
    for rec in results:
        id,name,type_key,key11,key12,key13,key21,key22,key23,key31,key32,key33,key41,key42,key43,change11,change12,change13,change21,change22,change23,change31,change32,change33,change41,change42,change43,command11,command12,command13,command21,command22,command23,command31,command32,command33,command41,command42,command43 = rec
        key['Кнопка 11']    = key11    
        key['Замена 11']    = change11    
        key['Команда 11']   = command11    
        key['Кнопка 12']    = key12
        key['Замена 12']    = change12
        key['Команда 12']   = command12    
        key['Кнопка 13']    = key13
        key['Замена 13']    = change13
        key['Команда 13']   = command13    
        key['Кнопка 21']    = key21    
        key['Замена 21']    = change21    
        key['Команда 21']   = command21    
        key['Кнопка 22']    = key22
        key['Замена 22']    = change22
        key['Команда 22']   = command22    
        key['Кнопка 23']    = key23
        key['Замена 23']    = change23
        key['Команда 23']   = command23    
        key['Команда 23']   = change23    
        key['Кнопка 31']    = key31    
        key['Замена 31']     = change31    
        key['Команда 31']   = command31    
        key['Кнопка 32']    = key32
        key['Замена 32']    = change32
        key['Команда 32']   = command32    
        key['Кнопка 33']    = key33
        key['Замена 33']    = change33
        key['Команда 33']   = command33    
        key['Кнопка 41']    = key41    
        key['Замена 41']    = change41    
        key['Команда 41']   = command41    
        key['Кнопка 42']    = key42
        key['Замена 42']    = change42
        key['Команда 42']   = command42    
        key['Кнопка 43']    = key43
        key['Замена 43']    = change43
        key['Команда 43']   = command43    
        
    sql     = "select id,name from key_type where id = {}".format (type_key)
    cursor.execute(sql)
    results     = cursor.fetchall()    
    name_key = ''
    for rec in results:
        id_key,name_key = rec 
    
    
    if name_key == 'Сообщение':
        print ('------------- key ------------------->')
        print (key)
        markup = key_type_message (key)
    if name_key == 'Клавиатура' or name_key == '': 
        markup = key_type_keybord (key)
        
        
    print ('[markup] :',markup)    
        
    return markup   
    
def user_get_data_psg       (message_info,setting_bot,user_id):
    namebot     = message_info['namebot']
    db,cursor   = connect_postgres (namebot)
    answer = {}
    sql = "select id,name,info from user_setting where user_id = '{}'".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row
        answer[name] = info
    return answer   
    
   #message_info,status_input,setting_bot,save_data
def user_save_data_psg       (message_info,status_input,setting_bot,save_data):
    namebot     = message_info['namebot']
    user_id     = message_info['user_id']
    db,cursor   = connect_postgres (namebot)
    print ('[+] save_data :',save_data)
    for line in save_data:
        id      = 0
        name    = ''
        info    = ''
        sql = "select id,name,info from user_setting where user_id = '{}' and name = '{}'".format (user_id,line[0])
        cursor.execute(sql)
        results = cursor.fetchall()   
        for row in results:
            id,name,info = row
            
        #print ('[+]',sql,id)    
            
        if id == 0:
            sql         = "INSERT INTO user_setting (user_id,info,name,status) VALUES (%s,%s,%s,'')".format ()
            sql_save    = (user_id,line[1],line[0])
            cursor.execute(sql,sql_save)
            db.commit() 
        else:    
            sql         = "UPDATE user_setting SET info = '{}' WHERE user_id = '{}' and name = '{}' ".format (line[1],user_id,line[0])
            cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()  
    return status_input     
       
def executing_autostart     (message_info,status_input,setting_bot,answer):
    namebot     = message_info['namebot']
    message_in  = message_info['message_in']
    user_id     = message_info['user_id']
    db,cursor = connect_postgres (namebot)
    answer = {}
    sql = "select id,name,info from message where name = '{}' and status = 'Автоматически'".format (message_in)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row
        message_name     = name
        message_out      = gets_message_psg (message_info,setting_bot,message_name)
        answer_null      = send_message (message_info,setting_bot,user_id,message_out['Текст'],{})        
    callback =   message_info.setdefault ("callback","")
    sql = "select id,name,info,menu from command where name = '{}' and status = 'Автоматически'".format (callback)
    #print ('[sql] :',sql)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info,menu = row
        message_name     = name
        message_text     = info 
        #message_out      = gets_message_psg (message_info,setting_bot,message_name)
        markup           = gets_key_psg (message_info,setting_bot,menu)
        answer_null      = send_message (message_info,setting_bot,user_id,message_text,markup)    
    return answer 
      
##################################################################################################################################################################################################
   
def start_prog (message_info,parsed_string):                                                                                                                                  ###  Получение сигнала от бота. Расшифровка команды и сообщения
    setting_bot                     = get_setting_psg           (message_info)                                                                          ###  Получение из базы информации по боту. Параметры и данные.        
    status_input                    = user_get_data_psg         (message_info,setting_bot,message_info['user_id'])                                                  ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    #message_in                      = message_info.setdefault   ("message_in","")
    #save_in_log (message_info,parsed_string)
    answer = {}
    #setting_bot                     = get_setting           (message_info,setting_bot)                                                                          ###  Получение из базы информации по боту. Параметры и данные.        
    #status_input                    = user_get_data         (message_info,setting_bot,message_info['user_id'])                                                  ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    #message_in                      = message_info.setdefault ("message_in","")
    #answer = {}
    #if message_in == '⛔ Отмена':
    #    send_user_message_v1      (message_info,status_input,setting_bot,'Отмена ввода слова')
    #    status_input              = user_save_data (message_info,status_input,setting_bot,[["Сбор данных",""]]) 
    #    return ''
    #callback        = message_info.setdefault ("callback","")
    #answer                         = testing_time          (message_info,status_input,setting_bot,14,15,9,15)                                                  ###  Проверка выполнения программы в указаннно деапазоне времени                                                           
    #print_status                                            (message_info,status_input,setting_bot)                                                             ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    #executing_admin                                         (message_info,status_input,setting_bot)                                                             ###  Выполнение команды администраторов бота 
    #testing_double                                         (message_info,status_input,setting_bot)                                                             ###  Проверка на повторно нажатые клавиши
    #answer                         = executing_run         (message_info,status_input,setting_bot,{})                                                          ###  Выполнение команды из базы данных
    result                          = executing_start       (message_info,status_input,setting_bot,{})                                                          ###  Выполнение команды /start
    
    #result                          = automat_message       (message_info,status_input,setting_bot,{})
    #result                           = automat_command       (message_info,status_input,setting_bot,{})
    
    
    #result                          = testing_blocking      (message_info,status_input,setting_bot)  
    ###  Проверка заполнения данных
    #if answer.setdefault ('Ответ','') == '':
        
        
    answer      =  executing_autostart     (message_info,status_input,setting_bot,{})    
        
    if 1==1:
        #save_info_refer                         (message_info,status_input,setting_bot)                                                                        ###  Записываем информацию по полученной реферальной ссылке 
        #save_info_user                          (message_info,status_input,setting_bot)                                                                        ###  Обновляем информацию по текущему пользователю 
        #lastid_log  = save_message_user         (message_info,status_input,setting_bot)                                                                        ###  Записываем входяшие сообшение для протоколирования
        #result       = executing_command          (message_info,status_input,setting_bot)                                                                 ###  Выполняем команды присланные боту
        answer      = executing_status          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем на действие статуса бота. Например ввод данных
        print ('message_info :',message_info)
        #result      = executing_message          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем код прописанный в базе данных
        result      = executing_program          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем код прописанный в этом файле
        #executing_free_messsage                  (message_info,status_input,setting_bot,answer)                                                                ###  Слова введенные вне команд   
        #analis                                   (message_info,status_input,setting_bot,answer)                                                                ###  Выполнение кода если нет действия на сообщения
        #save_out_message                         (message_info,status_input,setting_bot)                                                                        ###  Протоколирование исходящего сообщения
        #statictic                                (message_info,status_input,setting_bot)
        #backUp                                   (message_info,status_input,setting_bot)   

##################################################################################################################################################################################################

def backUp ():
    pass
    
def statictic (message_info):
    sql     = "select id,name from torrent where 1=1 ".format()
    name    = 'Всего записей торрент'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    
    sql     = "select id,name from torrent where (magnet = 'нет' or magnet = '')".format()
    name    = 'Нет магнитной ссылки'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)

    sql     = "select id,name from torrent where pic_type = 'Файл не найден'  ".format()
    name    = 'Нет картинки у торента'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)

    sql     = "select id,name from torrent where url_picture = ''  ".format()
    name    = 'Не проставлены ссылки на картинку'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)

    sql     = "select id,name from torrent where parset = ''  ".format()
    name    = 'Нет скаченного тела сайта'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    
def reglament_operation ():
    import datetime
    now     = datetime.datetime.now().time()
    hour    = now.hour
    minute  = now.minute
    second  = now.second
    now     = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y')
    
    if hour > 2 and hour < 4:
        pass
    
    
#                                                                  <Главное меню>                                       /start
#                                                                 [Заказать меню]
#                                                                         |
#                                                                         |    
#                                                               <Основное текст меню>                                   / Удаление сообщение в 10-00 /Ввод только после 14-00
#                                                              [Основное]  [Правильное]
#                                                                [Назад]      [Далее]
#                                                                    |          |
#                                                                    |          |
#                                                                <Основное текст меню>
#                                                                 [Гарнир]  [Гарнир]
#                                                                 [Назад]      [Далее]
#                                                                    |          |
#                                                                    |          |
#                                                                <Основное текст меню>
#                                                                 [Блюдо]    [Блюдо]
#                                                                 [Назад]      [Далее]
#                                                                    |          |
#                                                                    |          |
#                                                                <Основное текст меню>
#                                                              [Подтвердить] / [Отменить]










