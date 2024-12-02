### Узко специализированные программы ###
##################################################################################################################################################################################################
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
    import iz_bot
    namebot     = message_info.setdefault('namebot','')
    answer  = {}    
    db,cursor = iz_bot.connect (namebot)
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

def get_info_tovar (message_info,status_input,setting_bot,id_list):
    info_tovar = {'Имя':'Пробный товар'}
    info_tovar['catalog'] = 0
    return info_tovar


##################################################################################################################################################################################################

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
    #    import iz_bot
    #    namebot     = message_info.setdefault('namebot','')
    #    db,cursor   = iz_bot.connect (namebot)
    #    sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete' ".format(setting_bot.setdefault('Последний ID',0))
    #    cursor.execute(sql)
    #    data = cursor.fetchall()
    #    st_line1 = ""
    #    st_line2 = ""
    #    str_koll = 0
    #    for rec in data: 
    #        id,user_id_p,menu01,menu02,menu03 = rec.values()
    #        str_koll = str_koll + 1
    #        get_data    = {'user_id':user_id_p}
    
    list_operation = get_user_operation (message_info,status_input,setting_bot,list_operation)
    #        status_user = iz_bot.user_get_data (message_info,get_data)
    #        st_one = str(str_koll) + ") " + str(status_user.setdefault('Имя cотрудника',str(user_id))) +'('+ str(user_id_p) + "), <code>" + str(menu01) + ", " +str(menu02) + ", " + str(menu03) + " </code>\n"
    #        if str_koll < 30:
    #            st_line1 = st_line1 + st_one   
    #        else:
    #            st_line2 = st_line2 + st_one               

    #    if st_line1 != '':
    #        send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line1]]} 
    #        iz_bot.send_message (message_info,send_data)
    #    if st_line2 != '':
    #        send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line2]]} 
    #        iz_bot.send_message (message_info,send_data)
    list_line      = get_user_operation (message_info,status_input,setting_bot,list_operation)
  
    #    import iz_bot
    #    db,cursor = iz_bot.connect (namebot)
    #    sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete'".format(setting_bot.setdefault('Последний ID',0))
    #    cursor.execute(sql)
    #    data = cursor.fetchall()
    #    st_line = ""
    #        
    #    menu01_a = 0
    #    menu01_b = 0
    #    menu02_a = 0
    #    menu02_b = 0
    #    menu03_a = 0
    #    menu03_b = 0
    #    element = get_list_product (message_info,"main")   
    #    
    #    for rec in data: 
    #        id,user_id_p,menu01,menu02,menu03 = rec.values()
    #        if element['Mmenu01'] == menu01:
    #            menu01_a = menu01_a + 1
    #        if element['Mmenu02'] == menu01:
    #            menu01_b = menu01_b + 1
    #            
    #        if element['Mmenu11'] == menu02:
    #            menu02_a = menu02_a + 1    
    #        if element['Mmenu12'] == menu02:
    #            menu02_b = menu02_b + 1  
    #
    #        if element['Mmenu21'] == menu03:
    #            menu03_a = menu03_a + 1    
    #        if element['Mmenu22'] == menu03:
    #            menu03_b = menu03_b + 1   
    #            
    #            
    #    
    #    s01_a = ['#Menu01#',str(menu01_a)]    
    #    n01_a = ['#name01#',str(element['Mmenu01'])]
    #    s02_a = ['#Menu02#',str(menu01_b)]    
    #    n02_a = ['#name02#',str(element['Mmenu02'])]
    #
    #
    #    s03_a = ['#Menu03#',str(menu02_a)]    
    #    n03_a = ['#name03#',str(element['Mmenu11'])]
    #    s04_a = ['#Menu04#',str(menu02_b)]    
    #    n04_a = ['#name04#',str(element['Mmenu12'])]
    # 
    #
    #    s05_a = ['#Menu05#',str(menu03_a)]    
    #    n05_a = ['#name05#',str(element['Mmenu21'])]
    #    s06_a = ['#Menu06#',str(menu03_b)]    
    #    n06_a = ['#name06#',str(element['Mmenu22'])]
    #
    # 
    #    st_long = ''
    #    if element['Mmenu01'] != '': 
    #        st_long = st_long + ' ' + element['Mmenu01'] + ' ' + str(menu01_a)+'\n'
    #    if element['Mmenu02'] != '':         
    #        st_long = st_long + ' ' + element['Mmenu02'] + ' ' + str(menu01_b)+'\n' 
    #    if element['Mmenu11'] != '':     
    #        st_long = st_long + ' ' + element['Mmenu11'] + ' ' + str(menu02_a)+'\n' 
    #    if element['Mmenu12'] != '':     
    #        st_long = st_long + ' ' + element['Mmenu12'] + ' ' + str(menu02_b)+'\n' 
    #    if element['Mmenu21'] != '':     
    #        st_long = st_long + ' ' + element['Mmenu21'] + ' ' + str(menu03_a)+'\n' 
    #    if element['Mmenu22'] != '':     
    #        st_long = st_long + ' ' + element['Mmenu22'] + ' ' + str(menu03_b)+'\n' 
    #    send_data = {'Text':'Статистика заказов','Замена':[['#Статистика#',st_long]]} 
    #    iz_bot.send_message (message_info,send_data)
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
    ### Рассылка всем администраторам отчета по отправке                

def send_message_admin      (message_info,status_input,setting_bot,user_id_list,message_id,wait,change): 
    pass

def delete_send_message_user(message_info,status_input,setting_bot,user_id,answer,wait):                                                                        ###  Удаление сообшения через определенное время
    pass

##################################################################################################################################################################################################

def get_list_change         (message_info,status_input,setting_bot,message):                                                                                    ###  Получение всех меток замены             
    list = []
    body  = message
    while body.find ('##') != -1:
        nomer_begin     = message.find ("##")
        name_body       = message[nomer_begin:]       
        nomer_finishe   = message.find ("##")
        name            = name_body[:nomer_finishe]
        body            = name_body[nomer_finishe+2:]
    return list

def change_message          (message_info,status_input,setting_bot,message,list_change,element):                                                                ###  Меняем в сообшение значение на параметры             
    for line in list_change:
        message = message.replace (line,element.setdefault(line,''))    
    return message
       
def get_service             (message_info,status_input,setting_bot,data_id):                                                                                    ###  Получение информации о услугах  
        sql             = "select id,name,`info` from `service` where data_id = {} ".format (data_id)
        answer         = []
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name,info = rec.values() 
            answer[name] = info
        return answer  
        
def get_time_set            (message_info,status_input,setting_bot,name):                                                                                       ###  Процедура для замера времени
    import time
    unixtime = int(time.time ())
    status_input    = user_save_data (message_info,status_input,[[name,unixtime]])
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
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
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
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
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
    import iz_bot
    namebot     = message_info.setdefault('namebot','')
    db,cursor   = iz_bot.connect (namebot)
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
    import iz_bot
    user_id  = message_info.setdefault ('user_id','')
    namebot  = message_info.setdefault ('namebot','')
    db,cursor = iz_bot.connect (namebot)                                                                                                            ### Задаем вопрос из списка вопросов. 
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

##################################################################################################################################################################################################    

def save_sql                (message_info,status_input,setting_bot,name,sql,limit,offset,back):
    if setting_bot['connect'] == 'sql lite':
        pass
        lastid = 0
    if setting_bot['connect'] == 'MySQL':    
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
    import iz_bot
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = iz_bot.connect (namebot)
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
        
def gets_message            (message_info,setting_bot,user_id,message_out): 
    import iz_bot    
    namebot      = message_info.setdefault('namebot','')
    db,cursor    = iz_bot.connect (namebot)
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
                sql_save    = (data_id,info,name)
                cursor.execute(sql,sql_save)
                db.commit() 
            status_input[name] = info
    return status_input 
        
def key_type_message        (key):                                                          #                                                                   ## Процедура формирует кнопку из Соответствия
    #print (key) 
    import json
    line = []
    for number in range(5):
        #print ('[111]','Кнопка ' +str(number+1)+'1') 
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
       
def key_type_keybord        (key):                                                                                                                              ## Процедура формирует кнопку из Соответствия
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
 
def gets_key                (message_info,setting_bot,user_id,menu):
    namebot = message_info.setdefault('namebot','')
    import iz_bot  
    db,cursor = iz_bot.connect (namebot)
    sql     = "select id,name,info,data_id from menu where name = 'Имя' and info = '{}' ;".format (menu)
    cursor.execute(sql)
    results = cursor.fetchall()    
    markup     = {}
    #key        = {}   
    for row in results:
        id,name,info,data_id = row.values() 
        sql = "select id,name,info from menu where data_id = '{}' and status <> 'delete' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            key[name] = info
    if menu.setdefault('Тип кнопки','') == 'Сообщение':
        markup = key_type_message (key)
    if menu.setdefault('Тип кнопки','') == 'Клавиатура':    
        markup = key_type_keybord (key)
    return markup
    
def send_message            (message_info,setting_bot,user_id,message_out,markup):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    if markup != {}:
        params['reply_markup'] = markup                
    print ('[+] Данные для отправки')
    print ('[+]',params['chat_id'])
    print ('[+]',params['text'])
    if message_out != '':    
        url                     = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage')
        resp                    = requests.post(url, params) 
        answer                  = resp.json()
    else:
        answer = {'error':'Нет текста сообщения'}
    print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    print ('') 
    #print ('[markup]',markup)
    return answer 
       
def send_sendPhoto          (message_info,setting_bot,user_id,message_out,picture,markup):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
    params                  = {}
    params['chat_id']       = user_id
    params['text']          = message_out
    params['parse_mode']    = 'HTML'
    try:   
        file_path   = picture
        file_opened = open(file_path, 'rb')
    except:    
        file_path   = setting_bot.setdefault ('Картинка как нет основной','')
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
    token                   = setting_bot.setdefault ('Токен','')
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
    token                   = setting_bot.setdefault ('Токен','')
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
    print ('[+]👧------------------------------------------------------------ [Ответ editMessageCaption] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧[+]') 
    print ('') 
    return answer     
    
def editMessageMedia        (message_info,setting_bot,user_id,message_out,message_id,picture,markup):
    import requests
    token                   = setting_bot.setdefault ('Токен','')
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
      
def complite_key            (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,metka):                                                                  ###  Формируем кнопокe из списока  по переданным нам параметрам
    from iz_bot import connect as connect
    from iz_bot import build_jsom as build_jsom
    import json
    namebot             = message_info.setdefault('namebot','')
    db,cursor           = connect (namebot) 
    sql = sql.replace("##s1##",str(ask))
    sql = sql.replace("##s2##",str(limit))
    sql = sql.replace("##s3##",str(offset))
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
    #print ('[key_array]',key_array)
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
    #message_text    = message['Текст']
    #
    #message_text    = message_text.replace('##about##'   ,str(about)) 
    #message_text    = message_text.replace('##catalog##' ,str(catalog)) 
    #message_text    = message_text.replace('##comment##' ,str(comment)) 
    #message_text    = message_text.replace('##currency##',str(currency)) 
    #message_text    = message_text.replace('##picture##' ,str(picture)) 
    #message_text    = message_text.replace('##pocket##'  ,str(pocket)) 
    #message_text    = message_text.replace('##price##'   ,str(price))
    #message_text    = message_text.replace('##quantity##',str(quantity)) 
    key             = {}
    return message_text,key
   
##################################################################################################################################################################################################    
   
def print_operator          (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                                                           ###  Печать команды оператор в json
    pass
   
def executing_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                                                           ###  Выполнение команды оператор в json
    
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
    print_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back)                                    ###  Печатаем команды полученные  в json
    executing_operator  (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back)                                    ###  Выполняем команды полученные в json

def testing_time (message_info,status_input,setting_bot,hour_start,minute_start,hour_finishe,minute_finishe):                                                   ###  Проверка поподания в определенный дэопазон времени    
    import datetime
    import iz_bot
    now         = datetime.datetime.now()
    namebot     = message_info.setdefault('namebot','')
    now_time    = datetime.datetime.now().time()
    now_date    = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y %H:%M:%S')
    
##################################################################################################################################################################################################   
   
def print_status            (message_info,status_input,setting_bot):
    print ('[+] Начальные настройки по текущиму пользователю.')
    for line in status_input:
        print ('        [+]',line,'-',status_input[line])
    status     = status_input.setdefault('status','')
    
def executing_admin         (message_info,status_input,setting_bot):
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

        if  message_in   == '/new':             ### Создаем новое питание
            pass
            
        if  message_in   == '/input_01':        ### Исправляем часть питание
            pass
            
        if  message_in   == '/task':            ### Получаем список заданий
            pass
            
        if  message_in   == '/message':         ### Исправляем исходящие сообщения    
            pass

        if  message_in   == '/menu':            ### Исправляем исходящие список меню
            pass
            
        if  message_in   == '/setting':         ### Исправляем настроки бота
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
    status_input = user_save_data (message_info,status_input,save_data)
    
def testing_blocking        (message_info,status_input,setting_bot):                                                                                            ### Проверяем ввод оснавных параметров пользователя
    message_in  = message_info.setdefault ('message_in','')                                                                                                                                                  ### Проверяем статус - возможно пользователь ввел значение
    if message_in.find ('/start') == -1:
        status      = status_input.setdefault ('Статус','')  
        if status != '':    
            namebot     = message_info.setdefault ('namebot','') 
            from iz_bot import connect as connect  
            db,cursor   = connect (namebot)
            sql  = "select id,name,answer from ask where name = '{}' ".format(status)
            cursor.execute(sql)
            data = cursor.fetchall()
            id   = 0
            for rec in data:
                id,name,message_answer = rec.values()
            if id != 0:
                print ('[+] Найден необходимый статус ...')
                user_id         = message_info.setdefault('user_id','') 
                message         = setting_bot .setdefault (message_answer,message_answer)
                answer          = save_message   (message_info,setting_bot,user_id,message)
                message_out     = gets_message   (message_info,setting_bot,user_id,message)
                markup          = gets_key       (message_info,setting_bot,user_id,message_out['Меню'])
                answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup)
                status_input    = user_save_data (message_info,status_input,[["Статус",""]])
        ask = get_ask_nomer (message_info,status_input,setting_bot)        
        if ask != 0:
            namebot   = message_info.setdefault ('namebot','') 
            from iz_bot import connect as connect 
            db,cursor = connect (namebot)                                                                                                              ### Задаем вопрос из списка вопросов. 
            sql       = "select id,name from ask where id = {} ".format(ask)                                                                                     ### Получаем данные для вопроса
            data        = cursor.fetchall()
            for rec in data:
                if str(type(rec)) == "<class 'tuple'>":
                    id,name = rec
                else:
                    id,name = rec.values()
                user_id         = message_info.setdefault('user_id','') 
                message         = setting_bot .setdefault (name,name)
                answer          = save_message   (message_info,setting_bot,user_id,message)
                message_out     = gets_message   (message_info,setting_bot,user_id,message)
                markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
                answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
                status_input    = user_save_data (message_info,status_input,[["Статус",name]])
   
def save_info_refer         (message_info,status_input,setting_bot):
    message = message_info.setdefault ('message_in','')
    if message.find ("/start") != -1:
        if status_input.setdefault ('referal','') == '':
            referal = message.replace ("/start","")
            status_input    = user_save_data (message_info,status_input,[["Реферал",referal]])
            user_id         = referal
            message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")
            answer          = save_message   (message_info,setting_bot,user_id,message)
            message_out     = gets_message   (message_info,setting_bot,user_id,message)
            markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
            answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)                                 ### Информируем что пришел Ваш реферал.
            user_id         = referal
            message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")                                  ### Информируем что клиент стал чем то рефералом 
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
    answer = {}
    return answer 
        
def executing_run           (message_info,status_input,setting_bot,answer):
    answer = {}
    return answer 

def executing_message       (message_info,status_input,setting_bot,answer):
    message_in      = message_info.setdefault ("message_in","")
    if message_in   == 'Каталог':                                                                                                                               ###  Пример работы тестового Входящего сообщения 
        user_id         = message_info['user_id']
        sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = '1=1'
        id_sql          = save_sql     (message_info,status_input,setting_bot,"Список товаров",sql,limit,offset,back)                                           ###  Мы делаем запись в базе, теперь получив номер выбора, можем расчитать изменения
        markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'catat')                                                      ###  id_sql - Код SQL запроса, по этому коду будем получать данные, метка - оператор в json параметре, ask - отбор выборки 1=1
        message         = setting_bot .setdefault ("Сообщение тестовый список","Тестовый список")                                                               ###  Выводим полученный список
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)          
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list)
    answer = {}
    return answer
         
def executing_program       (message_info,status_input,setting_bot,answer):
    callback =   message_info.setdefault ("callback","")
    if callback.find ('i_') != -1:                                                                                                  ###  Кнопка которая передала в json информацию
        executing_program_json (message_info,status_input,setting_bot)
    if callback == 'save_message':                                                                                                  ###  Пример работы команды кнопки
        pass
    if callback == 'Вызов меню':                                                                                                    ###  Пример работы команды кнопки
        pass  
    answer = {}
    if callback == "Ввести данные":
        user_id         = message_info.setdefault ('user_id','') 
        message         = setting_bot .setdefault ("Сообщение ввести данные","Ввести данные")
        answer          = save_message (message_info,setting_bot,user_id,message)
        message_out     = gets_message (message_info,setting_bot,user_id,message)
        markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
        answer          = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        #status_input    = user_save_data (message_info,status_input,[["Статус",""]]) 
    return answer      
    
def executing_command       (message_info,status_input,setting_bot,answer):                                                                                     ### Выполнение общих команд бота /start
    message_in  = message_info.setdefault ("message_in","")
    
def executing_start         (message_info,status_input,setting_bot,answer):
    message_in      = message_info.setdefault ("message_in","")
    if message_in.find ('/start') != -1:
        #### Модуль подготовки сообшения
        user_id          = message_info.setdefault ('user_id','') 
        message          = setting_bot .setdefault ("Сообщение при старте программы","Старт программы")
        answer           = save_message (message_info,setting_bot,user_id,message)
        message_out      = gets_message (message_info,setting_bot,user_id,message)
        #markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
        answer           = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),{})
        ask = get_ask_nomer (message_info,status_input,setting_bot)
        if ask != 0:
            user_id           = message_info.setdefault ('user_id','') 
            message           = setting_bot .setdefault ("Информирование о вводе данных","Информирование о вводе данных")
            answer            = save_message (message_info,setting_bot,user_id,message)
            message_out       = gets_message (message_info,setting_bot,user_id,message)
            key               = {}
            key['Кнопка 11']  = 'Ввести данные' 
            key['Команда 11'] = 'Ввести данные' 
            markup            = key_type_message (key)
            answer            = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        
        #### Модуль обнуления данных
        status_input     = user_save_data (message_info,status_input,[["Статус",""]]) 
 
def analis                  (message_info,status_input,setting_bot,answer):
    status  = answer.setdefault('status','')
    message = answer.setdefault('message','')
    program = answer.setdefault('program','')
    user_id = answer.setdefault('user_id','')
    if message == '':
        message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")                              ### Информируем что клиент стал чем то рефералом 
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)
        markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
        answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
   
def save_out_message        (message_info,status_input,setting_bot):
    pass
   
##################################################################################################################################################################################################
   
def start_prog (message_info):                                                                                                                                  ###  Получение сигнала от бота. Расшифровка команды и сообщения
    import iz_bot
    status_input = iz_bot.user_get_data      (message_info,{})                                                                                       ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    setting_bot  = iz_bot.get_setting        (message_info)                                                                                          ###  Получение из базы информации по боту. Параметры и данные.    
    setting_bot['connect']                   = 'sql lite'
    #answer       = testing_time             (message_info,status_input,setting_bot,14,15,9,15)                                                      ###  Проверка выполнения программы в указаннно деапазоне времени                                                           
    #print_status                            (message_info,status_input,setting_bot)                                                                 ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    #executing_admin                         (message_info,status_input,setting_bot)                                                                 ###  Выполнение команды администраторов бота 
    #testing_double                          (message_info,status_input,setting_bot)                                                                 ###  Проверка на повторно нажатые клавиши
    #answer      = executing_run             (message_info,status_input,setting_bot,{})                                                              ###  Выполнение команды из базы данных
    answer      = executing_start            (message_info,status_input,setting_bot,{})                                                              ###  Выполнение команды /start
    testing_blocking                         (message_info,status_input,setting_bot)                                                                 ###  Проверка заполнения данных
    #save_info_refer                         (message_info,status_input,setting_bot)                                                                 ###  Записываем информацию по полученной реферальной ссылке 
    #save_info_user                          (message_info,status_input,setting_bot)                                                                 ###  Обновляем информацию по текущему пользователю 
    #lastid_log  = save_message_user         (message_info,status_input,setting_bot)                                                                 ###  Записываем входяшие сообшение для протоколирования
    answer      = executing_command          (message_info,status_input,setting_bot,answer)                                                          ###  Выполняем команды присланные боту
    #answer      = executing_status          (message_info,status_input,setting_bot,answer)                                                          ###  Выполняем на действие статуса бота. Например ввод данных
    answer      = executing_message          (message_info,status_input,setting_bot,answer)                                                          ###  Выполняем код прописанный в базе данных
    answer      = executing_program          (message_info,status_input,setting_bot,answer)                                                          ###  Выполняем код прописанный в этом файле
    #analis                                  (message_info,status_input,setting_bot,answer)                                                                     ###  Выполнение кода если нет действия на сообщения
    #save_out_message                        (message_info,status_input,setting_bot)                                                                            ###  Протоколирование исходящего сообщения
    #statictic                               (message_info,status_input,setting_bot)
    #backUp                                  (message_info,status_input,setting_bot)   

##################################################################################################################################################################################################


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










