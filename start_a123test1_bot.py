
### message         - Список данных сообщение полученный из базы данных
### message_out     - Текст отправленного сообшения 
### message_name    - Название текстового сообшения
### message_text    - Текст сообщения для обработки


### informanion     - Список информации о товаре


### Узко специализированные программы ###


def create_order (message_info,status_input,setting_bot,answer):
    if answer.setdefault('order','') == 'message':
        namebot     = message_info.setdefault('namebot','')
        message_in  = answer['message_in']
        from iz_bot import connect as connect
        db,cursor = connect (namebot)
        sql = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES (0,'','{}','Имя')".format (message_in)
        cursor.execute(sql)
        db.commit()
        lastid = cursor.lastrowid 
        sql = "UPDATE message SET data_id = {} WHERE id = {}".format (lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES ({},'','','Текст')".format (lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO message (`data_id`,`status`,`info`,`name`) VALUES ({},'','','Меню')".format (lastid)
        cursor.execute(sql)
        db.commit()
        


##################################################################################################################################################################################################
def complite_key_for_name (name):
    if name == 'Ввести данные':
        key                 = {}
        key['Кнопка 11']    = 'Ввести данные' 
        key['Команда 11']   = 'Ввести данные' 
    return key    

def get_message_in_id (message_info,status_input,setting_bot,id_list):
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

def get_message_text (message_info,status_input,setting_bot,informanion):  
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

##################################################################################################################################################################################################

def get_info_main_menu      (message_info,status_input,setting_bot):
    answer = {}
    namebot     = message_info.setdefault('namebot','')
    from iz_bot import connect as connect
    db,cursor = connect (namebot)
    sql = "select id,menu01,menu02,menu11,menu12,menu21,menu22 from food where status = 'main' ORDER BY id desc limit 1 ;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()  
    for row in results:
        id,menu01,menu02,menu11,menu12,menu21,menu22 = row.values() 
        answer['m_d1']        = id
        answer['m_menu01']    = menu01
        answer['m_menu02']    = menu02
        answer['m_menu11']    = menu11
        answer['m_menu12']    = menu12
        answer['m_menu21']    = menu21
        answer['m_menu22']    = menu22
    sql = "select id,menu01,menu02,menu11,menu12,menu21,menu22 from food where status = 'good' ORDER BY id desc limit 1 ;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()  
    for row in results:
        id,menu01,menu02,menu11,menu12,menu21,menu22 = row.values() 
        answer['g_id']       = id
        answer['g_menu01']    = menu01
        answer['g_menu02']    = menu02
        answer['g_menu11']    = menu11
        answer['g_menu12']    = menu12
        answer['g_menu21']    = menu21
        answer['g_menu22']    = menu22
    return answer

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

def get_active_ask (message_info,status_input,setting_bot,name):
    namebot   = message_info.setdefault ('namebot','') 
    from iz_bot import connect as connect 
    db,cursor = connect (namebot)                                                                                                                               ### Задаем вопрос из списка вопросов. 
    sql       = "select id,name,active1,type1,`order`,message11,message12 from active where name = '{}' ".format(name)                                                                                            ### Получаем данные для вопроса
    print ('[sql]',sql)
    answer    = {}
    id          = 0
    name        = ''
    active1     = ''
    type1       = ''    
    order       = ''    
    message11   = ''
    message12   = ''
    cursor.execute(sql)
    data      = cursor.fetchall()
    for rec in data:
        if str(type(rec)) == "<class 'tuple'>":
            id,name,active1,type1,order,message11,message12 = rec
        else:
            id,name,active1,type1,order,message11,message12 = rec.values()
    answer['id']        = id        
    answer['name']      = name 
    answer['active1']   = active1  
    answer['type1']     = type1     
    answer['order']     = order 
    answer['message11'] = message11  
    answer['message12'] = message12       
    return answer 




def statistic_complite (namebot,sql,name):
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
    #namebot             = message_info.setdefault('namebot','')
    import iz_bot
    db,cursor           = iz_bot.connect (namebot)
    sql = "INSERT INTO statistica (`name`,`unixtime`,`date`,`status`,`info`) VALUES ('{}',{},'{}','','{}')".format (name,unixtime,current_date_string,sum)
    #print ('[+] sql',sql)
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
    ### Рассылка всем администраторам отчета по отправке                

def send_message_admin      (message_info,status_input,setting_bot,user_id_list,message_id,wait,change): 
    pass

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
    print ('[+] body')
    print (body)
    print ('----------------------')
    while body.find ('##') != -1:
        print ('[+][+][+][+][+][+][+][+]',nm)
        nm = nm + 1
        nomer_begin     = body.find ("##")
        name_body       = body[nomer_begin+2:]       
        
        print ('+[name_body]')
        print (name_body)
        print ('-[name_body]')
        
        nomer_finishe   = name_body.find ("##")
        name            = name_body[:nomer_finishe]
        
        print ('+[name]')
        print (name)
        print ('-[name]')
        list.append (name)
        
        body            = name_body[nomer_finishe+2:]
        print ('+[body]')
        print (body)
        print ('-[body]')
        if nm > 5:
            break
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

def data_sql                (message_info,status_input,setting_bot,id_sql,info_data):
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
                    
def get_sql_data            (message_info,status_input,setting_bot,id_sql,info_data):  
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
    
def active_save_data        (message_info,status_input,setting_bot,name,type_ask):
    user_id         = message_info['user_id']
    answer          = {}
    if status_input.setdefault("Сбор данных","") == name:                                                       ### .setdefault ("Сообщение ввод значения 12","Ввод значения 12")
        if status_input.setdefault ('active1','') == '': 
            ask_info        = get_active_ask (message_info,status_input,setting_bot,name)
            status_input    = user_save_data (message_info,status_input,setting_bot,[["Сбор данных",""]])
            message         = setting_bot.setdefault ("Сообщение ввод значения 12",ask_info['message12'])
            answer_null     = save_message (message_info,setting_bot,user_id,message)
            message_out     = gets_message (message_info,setting_bot,user_id,message)
            answer_null     = send_message (message_info,setting_bot,user_id,message_out['Текст'],{}) 
            message_in              = message_info['message_in']
            status_input            = user_save_data (message_info,status_input,setting_bot,[["active1",message_in]])
        if status_input.setdefault ('active1','') != '': 
            answer['operation']     = 'message'
            answer['order']         = 'message'
            message_in              = message_info['message_in']
            answer['message_in']    = message_in
            status_input            = user_save_data (message_info,status_input,setting_bot,[["active1",""]])
            
            
            
            
            
            
            
            
            
    if type_ask == "Старт":
        ask_info        = get_active_ask (message_info,status_input,setting_bot,name)
        if status_input.setdefault ('active1','') == '': 
            status_input    = user_save_data (message_info,status_input,setting_bot,[["Сбор данных",name]])
            message         = setting_bot.setdefault ("Сообщение ввод значения 11",ask_info['message11'])
            answer_null     = save_message (message_info,setting_bot,user_id,message)
            message_out     = gets_message (message_info,setting_bot,user_id,message)
            answer_null     = send_message (message_info,setting_bot,user_id,message_out['Текст'],{})
    return answer     
    
def save_sql                (message_info,status_input,setting_bot,name,sql,limit,offset,back):
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

def get_sql                 (message_info,setting_bot,id_sql):
    from iz_bot import connect as connect
    namebot    = message_info.setdefault('namebot','')
    db,cursor = connect (namebot)
    sql = "select id,sql,ask,limit,offset,back from data_sql where id = {}".format(id_sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,sql,ask,limit,offset,back = rec.values() 
    return sql,ask,limit,offset,back  

def save_message            (message_info,setting_bot,user_id,message_out):
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
        
def gets_message            (message_info,setting_bot,user_id,message_out): 
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
       
def user_save_data          (message_info,status_input,setting_bot,save_data): 
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
            print ('[sql user]',sql)
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
                else:
                    sql         = "UPDATE users SET info = %s WHERE `name` = %s and data_id = %s "
                    sql_save    = (info_status,name_status,data_id)
                    cursor.execute(sql,sql_save)
                    db.commit()    
            else:   
                if setting_bot['connect'] == 'sql lite':
                    sql         = "INSERT INTO users (data_id,info,name,status) VALUES ('{}','{}','{}','')".format (data_id,info_status,name_status)
                    cursor.execute(sql)
                    db.commit()                 
                else:
                    sql         = "INSERT INTO users (data_id,info,name,status) VALUES (%s,%s,%s,'')".format ()
                    sql_save    = (data_id,info_status,name_status)
                    cursor.execute(sql,sql_save)
                    db.commit() 
            status_input[name_status] = info
        cursor.close()
        db.close()    
    return status_input 
        
def key_type_message        (key):                                                          #                                                                   ## Процедура формирует кнопку из Соответствия
    import json
    line = []
    for number in range(5):
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
 
def gets_key                (message_info,setting_bot,user_id,menu):
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
    key             = {}
    return message_text,key
   
##################################################################################################################################################################################################    
   
def print_operator          (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                                                           ###  Печать команды оператор в json
    pass
   
def executing_operator      (message_info,status_input,setting_bot,operation,id_list,id_sql,id_back):                                                           ###  Выполнение команды оператор в json
    answer = {}
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
            #status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",""]]
       
    if operation == 'anketa': 
        namebot      = message_info.setdefault('namebot','')
        db,cursor    = iz_bot.connect (namebot)
        sql = "select id,name,data_id from service where id = {} and name = 'Вопрос' ".format(nomer_ask)            
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name,data_id = rec.values() 
            nomer_anketa = data_id
        sql = "select id,name,info from service where data_id = {} ".format(id)
        cursor.execute(sql)
        data = cursor.fetchall()
        key       = {}
        for rec in data:
            id,name,info = rec.values() 
            key[name] = info
        sql = "INSERT INTO answer (`anketa`,`answer`,`ask`,`name`,`status`,`unixtime`,`user_id`) VALUES ({},'{}',{},'{}','{}',{},'{}')".format (nomer_anketa,nomer_key,nomer_ask,'Ответ на анкету','',0,user_id)
        cursor.execute(sql)
        db.commit()   
        if str(nomer_key) == key.setdefault('Правильные ответы','Нет'):
            send_data = {'Text':'Вы ответили правильно'}
            iz_bot.send_message (message_info,send_data)    
            time.sleep (10)
        else:    
            send_data = {'Text':'Правильный ответ','Замена':[['%%Ваш ответ%%',str(nomer_key)],['%%Правельный ответ%%',key.setdefault('Правильные ответы','Нет')]]}    ##  key.setdefault('Правильные ответы','Нет'),'Запись в базу':'Не записывать'
            iz_bot.send_message (message_info,send_data) 
            time.sleep (5)
            send_data = {'Text':'Коментарий к ответу','Замена':[['%%Коментарий%%',key.setdefault('Комментарий','Нет')]]}  ## key.setdefault('Комментарий','Нет'),'Запись в базу':'Не записывать'
            iz_bot.send_message (message_info,send_data)               
            time.sleep (10)
        select_ask (message_info,nomer_anketa,nomer_ask)
       
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


    if operation == 'com_mes':
        #user_id         = message_info['user_id']
        #message         = setting_bot .setdefault ("Сообщение команды сообщения","Команды сообщения")
        #answer          = save_message (message_info,setting_bot,user_id,message)
        #message_out     = gets_message (message_info,setting_bot,user_id,message)
        #answer          = send_message (message_info,setting_bot,user_id,message_out['Текст'],{})
        #info_data       = get_sql_data (message_info,status_input,setting_bot,id_sql,{})
        if id_list == 3:
            answer = active_save_data (message_info,status_input,setting_bot,'Новое сообщение в боте','Старт')
    if operation == 'menu': 
        pass

    return answer
 
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
    message_in  = message_info.setdefault ('message_in','')                                                                                                     ### Проверяем статус - возможно пользователь ввел значение
    callback    = message_info.setdefault ('callback','')
    ask         = 0
    label_send  = True
    
    if callback == 'Ввести данные' and label_send == True:
        label_send = False
        ask = get_ask_nomer (message_info,status_input,setting_bot) 
        if ask != 0:
            send_message_ask (message_info,status_input,setting_bot,ask)

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
                import time
                print ('[pause]')
                time.sleep (20)
        ask = get_ask_nomer (message_info,status_input,setting_bot)                                                                                             #### Проверяем если не заданные вопросы если есть задаем    
        if ask != 0:
            send_message_ask (message_info,status_input,setting_bot,ask)
    return ask            
   
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
    answer = {}
    return answer 
        
def executing_run           (message_info,status_input,setting_bot,answer):
    answer = {}
    return answer 

def executing_message       (message_info,status_input,setting_bot,answer):
    message_in      = message_info.setdefault ("message_in","")   
    if message_in   == 'Анкета':                                                                                                                              ### Формируем список Анкет
        user_id         = message_info['user_id']
        sql             = "select id,`info` from `service` where ##s1## limit ##s2## offset ##s3##"
        limit           = 10
        offset          = 0
        back            = ''
        ask             = "name = 'Анкета'"
        id_sql          = save_sql     (message_info,status_input,setting_bot,"Список анкет",sql,limit,offset,back)                                           
        markup_list     = complite_key (message_info,setting_bot,id_sql,sql,ask,limit,offset,back,'anket')                                                    
        message         = setting_bot .setdefault ("Сообщение анкета список","Список анкет")                                                                  
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)          
        answer          = send_message   (message_info,setting_bot,user_id,message_out['Текст'],markup_list)
    
    if message_in   == 'Обед': 
       info_service         = get_info_main_menu     (message_info,status_input,setting_bot)
       nomer                = save_order_info        (message_info,setting_bot,user_id,nomer_order,'date',info_service['date'])
       info_service         = update_info_main_menu  (message_info,status_input,setting_bot,nomer,info_service)
       message_out,markup   = get_message_main_menu  (message_info,status_input,setting_bot,info_service) 
       answer               = send_message           (message_info,setting_bot,user_id,message_out,markup)
    
    if message_in   == 'Главное меню':                                                                                                                              ###  Пример работы тестового Входящего сообщения              
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
    #if callback == "Ввести данные":
    #    user_id         = message_info.setdefault ('user_id','') 
    #    message         = setting_bot .setdefault ("Сообщение ввести данные","Ввести данные")
    #    answer          = save_message (message_info,setting_bot,user_id,message)
    #    message_out     = gets_message (message_info,setting_bot,user_id,message)
    #    markup          = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
    #    answer          = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
    #    #status_input    = user_save_data (message_info,status_input,setting_bot,[["Статус",""]]) 
    return answer      
    
def executing_command       (message_info,status_input,setting_bot,answer):                                                                                     ### Выполнение общих команд бота /start
    message_in  = message_info.setdefault ("message_in","")
    if message_info['callback'] == 'Ввод данных':
        user_id     = message_info.setdefault('user_id','') 
        message     = setting_bot .setdefault ("Сообщение 0001","Ввод данных")
        answer      = save_message (message_info,setting_bot,user_id,message)
        message_out = gets_message (message_info,setting_bot,user_id,message)
        markup      = gets_key     (message_info,setting_bot,user_id,message_out['Меню'])
        answer      = send_message (message_info,setting_bot,user_id,message_out['Текст'],markup)
              
def executing_start         (message_info,status_input,setting_bot,answer):
    message_in      = message_info.setdefault ("message_in","")
    if message_in.find ('/start') != -1:                                                                                                                        #### Модуль подготовки сообшения         
        user_id          = message_info.setdefault ('user_id','') 
        message          = setting_bot .setdefault ("Сообщение при старте программы","Старт программы")
        answer           = save_message (message_info,setting_bot,user_id,message)
        message_out      = gets_message (message_info,setting_bot,user_id,message)
        ask              = get_ask_nomer (message_info,status_input,setting_bot)
        if ask == 0:
            markup               = gets_key     (message_info,setting_bot,user_id,message_out.setdefault ('Меню',''))
        else:
            markup              = gets_key     (message_info,setting_bot,user_id,'Ввод данных')
        answer                  = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        if ask != 0:
            user_id             = message_info.setdefault ('user_id','') 
            message             = setting_bot .setdefault ("Информирование о вводе данных","Информирование о вводе данных")
            answer              = save_message          (message_info,setting_bot,user_id,message)
            message_out         = gets_message          (message_info,setting_bot,user_id,message)
            key                 = complite_key_for_name ("Ввести данные")
            markup              = key_type_message  (key)
            answer              = send_message (message_info,setting_bot,user_id,message_out.setdefault ('Текст',''),markup)
        status_input            = user_save_data (message_info,status_input,setting_bot,[["Статус",""]])                                                                          #### Модуль обнуления данных                                      
 
def analis                  (message_info,status_input,setting_bot,answer):
    status  = answer.setdefault('status','')
    message = answer.setdefault('message','')
    program = answer.setdefault('program','')
    user_id = answer.setdefault('user_id','')
    if message == '':
        message         = setting_bot .setdefault ("Сообщение о новом реферале","У Вас новый реферал")                                                          ### Информируем что клиент стал чем то рефералом 
        answer          = save_message   (message_info,setting_bot,user_id,message)
        message_out     = gets_message   (message_info,setting_bot,user_id,message)
        markup          = gets_key       (message_info,setting_bot,user_id,message_out.setdefault('Меню',''))
        answer          = send_message   (message_info,setting_bot,user_id,message_out.setdefault('Текст',''),markup)
   
def save_out_message        (message_info,status_input,setting_bot):
    pass
   
##################################################################################################################################################################################################
   
def start_prog (message_info):                                                                                                                                  ###  Получение сигнала от бота. Расшифровка команды и сообщения
    setting_bot                     = {'connect':'MySQL'}
    setting_bot                     = get_setting           (message_info,setting_bot)                                                              ###  Получение из базы информации по боту. Параметры и данные.        
    status_input                    = user_get_data         (message_info,setting_bot,message_info['user_id'])                                      ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    answer                          = active_save_data      (message_info,status_input,setting_bot,'Новое сообщение в боте','')                     ###  Проверка что идет ввод данных от клиента
    if answer.setdefault ('operation') == "message":
        create_order (message_info,status_input,setting_bot,answer)    
    #answer                         = testing_time          (message_info,status_input,setting_bot,14,15,9,15)                                      ###  Проверка выполнения программы в указаннно деапазоне времени                                                           
    print_status                                            (message_info,status_input,setting_bot)                                                 ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    executing_admin                                         (message_info,status_input,setting_bot)                                                 ###  Выполнение команды администраторов бота 
    #testing_double                                         (message_info,status_input,setting_bot)                                                 ###  Проверка на повторно нажатые клавиши
    #answer                         = executing_run         (message_info,status_input,setting_bot,{})                                              ###  Выполнение команды из базы данных
    answer                          = executing_start       (message_info,status_input,setting_bot,{})                                              ###  Выполнение команды /start
    answer                          = testing_blocking      (message_info,status_input,setting_bot)                                                 ###  Проверка заполнения данных
    if answer == 0:
        #save_info_refer                         (message_info,status_input,setting_bot)                                                                        ###  Записываем информацию по полученной реферальной ссылке 
        #save_info_user                          (message_info,status_input,setting_bot)                                                                        ###  Обновляем информацию по текущему пользователю 
        #lastid_log  = save_message_user         (message_info,status_input,setting_bot)                                                                        ###  Записываем входяшие сообшение для протоколирования
        answer      = executing_command          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем команды присланные боту
        #answer      = executing_status          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем на действие статуса бота. Например ввод данных
        answer      = executing_message          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем код прописанный в базе данных
        answer      = executing_program          (message_info,status_input,setting_bot,answer)                                                                 ###  Выполняем код прописанный в этом файле
        #executing_free_messsage                  (message_info,status_input,setting_bot,answer)                                                                ###  Слова введенные вне команд   
        #analis                                  (message_info,status_input,setting_bot,answer)                                                                 ###  Выполнение кода если нет действия на сообщения
        #save_out_message                        (message_info,status_input,setting_bot)                                                                        ###  Протоколирование исходящего сообщения
        #statictic                               (message_info,status_input,setting_bot)
        #backUp                                  (message_info,status_input,setting_bot)   

##################################################################################################################################################################################################

def backUp ():
    pass
    
def statictic (message_info):
    sql     = "select id,name from torrent where 1=1 ".format()
    name    = 'Всего записей торрент'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    print ('[sql]',sql)
    print ('[sum]',sum)
    
    
    sql     = "select id,name from torrent where (magnet = 'нет' or magnet = '')".format()
    name    = 'Нет магнитной ссылки'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    print ('[sql]',sql)
    print ('[sum]',sum)    

    sql     = "select id,name from torrent where pic_type = 'Файл не найден'  ".format()
    name    = 'Нет картинки у торента'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    print ('[sql]',sql)
    print ('[sum]',sum)    

    sql     = "select id,name from torrent where url_picture = ''  ".format()
    name    = 'Не проставлены ссылки на картинку'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    print ('[sql]',sql)
    print ('[sum]',sum)   


    sql     = "select id,name from torrent where parset = ''  ".format()
    name    = 'Нет скаченного тела сайта'
    namebot = message_info.setdefault('namebot','')
    sum = statistic_complite (namebot,sql,name)
    print ('[sql]',sql)
    print ('[sum]',sum) 
    

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










