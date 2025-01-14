

def get_user_id (message_info,data_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    id_name = data_info.setdefault('id_name','')    
    data_answer = {}    
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,info,data_id from users where id = {} limit 1".format (id_name)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,info,data_id = rec.values()        
        data_answer = {'user_id':info}    
    return data_answer

def message_send_list (message_info,data_info):  #### Печатаем список
    import iz_bot
    text       = data_info.setdefault('Текст','')
    key_array  = data_info.setdefault('Кнопки','')
    message_id = data_info.setdefault('Номер Сообшения',0)    
    if message_id == 0:
        send_data = {"Text":text,'Кнопки':key_array,'Тип кнопки':'Сообщение'} 
        iz_bot.send_message (message_info,send_data) 
    else:   
        send_data = {"Text":text,'Кнопки':key_array,'Тип кнопки':'Сообщение','Метод':'editMessageText'}     
        iz_bot.send_message (message_info,send_data) 

def messaage_in_list (message_info,data_info):   #### Выводит сообщение с кнопками
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    kolon      = data_info.setdefault('Колличество колонок',3) 
    
    ### Номер заказа который выбираем  
    zakaz      = data_info.setdefault('Заказ','')   
        
    ### Команда выполнения
    prit       = data_info.setdefault('Прификс','')
    param      = data_info.setdefault('Значение',0)    
        
    ### Запрос у базе
    sql        = data_info.setdefault('sql_main','')

    step_left = data_info.setdefault('Шаг влево',0) 
    step_prav = data_info.setdefault('Шаг вправо',0) 

    key_array = []
 
    
    db,cursor = iz_bot.connect (namebot)   
    cursor.execute(sql)
    results = cursor.fetchall()    
    polka = 0    
    list = [] 
     
    for row in results:
        id,info,reting,change = row.values()         
        list.append ([id,info,reting,change])
        
        if change != None:
            name = change
        else:
            name = info        
        
        
        if kolon == 1:
            key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            key1      = [key11,['',''],['','']]
            key_array.append(key1)
        if kolon == 2:    
            polka = polka + 1
            if polka == 1:
                key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            if polka == 2:    
                key12     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
                key1      = [key11,key12,['','']]
                key_array.append(key1)
                polka = 0                
        if kolon == 3:    
            polka = polka + 1
            if polka == 1:
                key11     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
            if polka == 2:
                key12     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]                
            if polka == 3:    
                key13     = [name,iz_bot.build_jsom({"o":prit,"p":id,"z":zakaz})]
                key1      = [key11,key12,key13]
                key_array.append(key1)
                polka = 0  

    if kolon == 3: 

        if polka == 1:  
            key1 = [key11,['',''],['','']]
            key_array.append(key1)            
        if polka == 2:  
            key1 = [key11,key12,['','']]        
            key_array.append(key1)
            
    key11     = ['Назад',iz_bot.build_jsom({"o":prit+'_left',"p":param,"z":zakaz,"s":step_left})]
    key12     = ['Цент',iz_bot.build_jsom( {"o":'ex_cent',"p":param,"z":zakaz, "s":0  })]
    key13     = ['Право',iz_bot.build_jsom({"o":prit+'_prav',"p":param,"z":zakaz, "s":step_prav})]
    
    key1      = [key11,key12,key13]
    key_array.append(key1)
            
                
            
            
    data_info['Кнопки'] = key_array       
    message_send_list (message_info,data_info)     
   
def input_message (message_info,data_info): 
    import iz_bot
    namebot    = message_info.setdefault('namebot','')      
    text       = data_info.setdefault('Текст','')
    message_id = data_info.setdefault('Номер Сообшения',0)  
    prit       = data_info.setdefault('Прификс','')    
    ask        = data_info.setdefault('Вопрос','') 
    zakaz      = data_info.setdefault('Заказ','')
    zamena    = data_info ['Замена']
    if ask == 'Да':
        send_data = {"Text":text} 
        iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',prit],['Номер заказа',zakaz]]
        iz_bot.user_save_data (message_info,save_data)
    else:
        send_data = {"Text":text,'Замена':zamena} 
        iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',''],['Номер заказа','']]
        iz_bot.user_save_data (message_info,save_data)    

def save_info_zakaz (message_info,data_info):
    import iz_bot
    namebot     = message_info.setdefault('namebot','') 
    name_z      = data_info.setdefault('Имя','')
    user_id     = message_info.setdefault('user_id','')
    id_z        = data_info.setdefault('Статус','')
    param_z     = data_info.setdefault('Значение','')
    
    lastid = 0
    if data_info.setdefault('Статус','')  == 'Новый':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,info from users where name = 'user_id' and info = '"+str(user_id)+"' limit 1"
        cursor.execute(sql)
        data = cursor.fetchall()
        id = 0
        for rec in data: 
            id,name,info = rec.values()
            sql = "INSERT INTO users (`name`,`info`,`data_id`) VALUES ('Заказ','"+str(name_z)+"','"+str(id)+"')"
            cursor.execute(sql)
            db.commit()            
        db.close
        lastid = cursor.lastrowid
    else:
        db,cursor = iz_bot.connect (namebot)
        sql = "INSERT INTO users (`name`,`info`,`data_id`) VALUES ('"+str(name_z)+"','"+str(param_z)+"','"+str(id_z)+"')"
        cursor.execute(sql)
        db.commit()            
        db.close
    return lastid   
              
def get_data_zakaz (message_info,data_info):        
    import iz_bot
    namebot = message_info['namebot']
    user_id = message_info['user_id']
    data_id   = data_info ['Заказ']
    data_list = data_info ['Список замены']
    data_parm = data_info ['Список значения']
    db,cursor = iz_bot.connect (namebot)
    data_answer = {}   
    sql = "select id,name,info from users where data_id = '{}' ;".format (data_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row1 in results:
        id1,name1,info1 = row1.values()         
        data_answer[name1] = info1
    data_answer2 = {}
    
    print ('data_answer',data_answer)
    
    for line in data_list:
        data =  data_answer.setdefault(line,'')         
        sql = "select id,name,info from service where id = '{}' ;".format (data)
        cursor.execute(sql)
        results = cursor.fetchall()    
        id2 = 0
        for row2 in results:
            id2,name2,info2 = row2.values()
            data_answer2[line] = [info2,data]
        #if id2 == 0   
        #   data_answer[name1] = ['Сумма',info1]
    for line in data_parm:    
        data =  data_answer.setdefault(line,'')  
        data_answer2[line] = [data]                
    return data_answer2    

def set_name_key (message_info,namekey):
    import iz_bot
    info_data = {'Имя':namekey}
    info    = iz_bot.get_message(message_info,info_data)
    return_key = info.setdefault('Текст',info_data.setdefault('Имя',''))
    return return_key

def get_data_in_base (message_info,data_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    sql        = data_info.setdefault('sql','')
    nomer      = data_info.setdefault('nomer','')
    go         = data_info.setdefault('go','id')
    info = ''
    data = ''
    name = ''
    if go == 'prev':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,data,`text` from name_file where id < {} and status <> 'delete'  ORDER BY id DESC limit 1".format(nomer)
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,data,text = row.values() 
            if text == '':
                text = name
        info = data+name
    if go == 'next' or go == 'new':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,data,`text` from name_file where id > {}  and status <> 'delete'  ORDER BY id limit 1".format(nomer)   
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,data,text = row.values() 
            if text == '':
                text = name
        info = data+name           
        get_data_in_info = {'picture':info,'id':id,'text':text}    
    return get_data_in_info
            
def get_name_message (message_info,name_message): ##'Запрос геолокации
    import iz_bot
    info_data = {'Имя':name_message,'Сохранить':'Да'}
    data_message = iz_bot.get_message (message_info,info_data)
    print ('[data_message]',data_message)
    message_out    = data_message.setdefault ('Текст',name_message)
    return message_out
     
def foto_presentation (message_info,data_info):
    import iz_bot
    message_id = message_info.setdefault('message_id','')
    key_array = []
    picture_send_info = get_data_in_base (message_info,data_info)
    nomer     = picture_send_info['id']
    name1     = set_name_key (message_info,'Кнопка лево')
    name2     = set_name_key (message_info,'Кнопка право')    
    key11     = [name1,iz_bot.build_jsom({"o":'pict_l',"p":nomer})]
    key12     = [name2,iz_bot.build_jsom({"o":'pict_p',"p":nomer})]
    key1 = [key11,['',''],key12]
    key_array.append(key1)    
    if data_info.setdefault('go','new') == 'new':
        send_data = {"Text":picture_send_info['text'],'Метод':'sendPhoto','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение'}
        answer = iz_bot.send_message (message_info,send_data)
    else:    
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageCaption','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageMedia','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
        send_data = {"Text":picture_send_info['text'],'Метод':'editMessageCaption','Картинка':picture_send_info['picture'],'Кнопки':key_array,'Тип кнопки':'Сообщение','message_id':message_id}
        answer = iz_bot.send_message (message_info,send_data)
               
def delete_message (message_info,data_info): 
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    name = data_info['name']
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,message_id from message_log where name = '{}' and user_id = '{}' and status <> 'delete'".format (name,user_id,)
    cursor.execute(sql)
    data = cursor.fetchall()    
    for rec in data:
        id,message_id_del = rec.values()
        iz_bot.deleteMessage (message_info,message_id_del) 

    sql = "UPDATE message_log SET status = 'delete' WHERE name = '{}' and user_id = '{}' and status <> 'delete'".format (name,user_id,)
    cursor.execute(sql)
    db.commit()
        
def save_sql (message_info,sql_param,param):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "INSERT INTO data_sql (name,data) VALUES (%s,%s)".format ()
    sql_save = (sql_param,str(param))
    result = cursor.execute(sql,sql_save)
    db.commit()    
    lastid = cursor.lastrowid
    return lastid
    
def get_sql (message_info,param):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,name,data from data_sql where id = {}".format(param)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,name,param = rec.values() 
    return name,param  
       
def list_music (message_info,id_code,command):
    namebot    = message_info.setdefault('namebot','')
    import iz_bot
    import json
    db,cursor = iz_bot.connect (namebot)
    sql,param_string = get_sql (message_info,id_code)            
    param_string = param_string.replace("'",'"')
    print ('[+] param_string',param_string)
    param = json.loads(param_string)
    limit = str(param.setdefault('limit',20))
    offet = str(param.setdefault('offset',20))
    if command == 'next':
        offet = str(int(offet) + int(limit))
        param = {'limit':int(limit),'offset':int(offet)}
        id_code = save_sql (message_info,sql,param)
    sql = sql.replace("#limit#",limit)
    sql = sql.replace("#offset#",offet)
    cursor.execute(sql)
    data = cursor.fetchall()
    key_array = []
    for rec in data: 
        id,info = rec.values()  
        #sql = "select id,name,info from exchange where name = '{}' limit 1".format (info)
        #cursor.execute(sql)
        #results = cursor.fetchall()  
        info_exchange = info
        #for row in results:
        #    id_exchange,name_exchange,info_exchange  = row.values() 
        #    print ('        [+] id,name',id_exchange,name_exchange,info_exchange)
        print ('[Композиция]',info)
        command =  iz_bot.build_jsom ({'o':'list','s':id})
        key_array.append ([[info_exchange,command],['',''],['','']])  
    command =  iz_bot.build_jsom ({'o':'next','s':id_code})

    name_key     = set_name_key (message_info,'Кнопка далее')        
    key_array.append ([[name_key,command],['',''],['','']])         
    return key_array       
  
def send_answer (send_data,message_id,sostav,message_info,nomer):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    if 1==1:
        if 1==1:
            data_info = {'nomer':nomer,'go':'prev'}
            print ('[+] Модуль обработки ответа')
            #print ('[message_id]:',message_id)
            iz_bot.deleteMessage (message_info,message_id)
            #send_data = {"Text":'Вы сделали заказ. Выбор второе'}
            answer = iz_bot.send_message (message_info,send_data)             
            namebot    = message_info.setdefault('namebot','')
            db,cursor = iz_bot.connect (namebot)            
            sql = "INSERT INTO service (name,data_id,info,status) VALUES ('Заказ',1,'{}','')".format (nomer)
            cursor.execute(sql)
            db.commit() 
            lastid = cursor.lastrowid
            sql = "UPDATE service SET data_id = '{}' WHERE id = {}  ".format(lastid,lastid)
            cursor.execute(sql)
            db.commit()
            sql = "INSERT INTO service (name,data_id,info,status) VALUES ('Клиент','{}','{}','')".format (lastid,user_id)
            cursor.execute(sql)
            db.commit()             
            sql = "select data_id,name from task where name = 'Дата' and info = '{}' limit 1".format(nomer) 
            cursor.execute(sql)
            results = cursor.fetchall()        
            id = 0
            info = "Нет меню на это время"
            for row in results:    
                data_id,name = row.values()
                name = ''
                sql = "select id,name,info from task where name = 'Наименование' and data_id = {} limit 1".format(data_id) 
                print ('[=] sql:',sql)
                cursor.execute(sql)
                results = cursor.fetchall() 
                for row in results:    
                    id,name,info = row.values()                
            
            sql = "INSERT INTO service (name,data_id,info,status) VALUES ('Меню','{}','{}','')".format (lastid,info)
            cursor.execute(sql)
            db.commit() 
            
            sql = "INSERT INTO service (name,data_id,info,status) VALUES ('Состав','{}','{}','')".format (lastid,sostav)
            cursor.execute(sql)
            db.commit() 
 
def message_menu(message_info,status_input,message_id):
    import iz_bot 
    import datetime   
    key_array = []
    now = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y')
    key11 = [change_back("Основное",message_info)  ,iz_bot.build_jsom({"o":"menu01","d":current_date_string})]
    key12 = [change_back("Правильное",message_info),iz_bot.build_jsom({"o":"menu02","d":current_date_string})]
    key1 = [key11,key12]
    key_array.append(key1)
    return key_array

def to_data (time_data):
    t001 = time_data
    t002 = int(float(t001))
    t003 = float (t001)
    t004 = int((t003 - t002) * 100)
    return t002,t004    
    
def clear_status (status_input,message_info):
    import iz_bot
    save_data = [['Vmenu01',''],['Vmenu02',''],['Vmenu03','']]
    status_input['Vmenu01']  = ''
    status_input['Vmenu02']  = ''
    status_input['Vmenu03']  = ''
    status_input['Режим']    = ''
    iz_bot.user_save_data (message_info,save_data)     
    return status_input
    
def send_message_menu (status_input,message_info,message_id,add_message,key_array,setting_bot):
    import datetime
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','')
    a   = datetime.datetime.now().time()
    now = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y %H:%M:%S')       
    Vmenu01 = status_input.setdefault('Vmenu01','')
    Vmenu02 = status_input.setdefault('Vmenu02','')
    Vmenu03 = status_input.setdefault('Vmenu03','')
    regim   = status_input.setdefault('Режим','')   
    dolg    = status_input.setdefault('Баланс','')   
    #fio     = status_input.setdefault('1С','')   
    fio     = status_input.setdefault('Имя cотрудника','')   
    activ   = setting_bot.setdefault('Дата_расчета','')   
    message_out = "Вывести список меню"
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,menu01,menu02,menu11,menu12,menu21,menu22 from food where status = 'main' ORDER BY id desc limit 1 ;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()  
    for row in results:
        id,menu01,menu02,menu11,menu12,menu21,menu22 = row.values()  
    change = []
    change.append(['##Дата##',setting_bot.setdefault('Шапка','')])##str(current_date_string)])
    change.append(['##Mmenu01##',menu01])
    change.append(['##Mmenu02##',menu02])
    change.append(['##Mmenu11##',menu11])
    change.append(['##Mmenu12##',menu12])
    change.append(['##Mmenu21##',menu21])
    change.append(['##Mmenu22##',menu22])
    sql = "select id,menu01,menu02,menu11,menu12,menu21,menu22 from food where status = 'good'  ORDER BY id desc limit 1 ;".format ()
    cursor.execute(sql)
    results = cursor.fetchall()  
    for row in results:
        id,menu01,menu02,menu11,menu12,menu21,menu22 = row.values()  
    change.append(['##Pmenu01##',menu01])
    change.append(['##Pmenu02##',menu02])
    change.append(['##Pmenu11##',menu11])
    change.append(['##Pmenu12##',menu12])
    change.append(['##Pmenu21##',menu21])
    change.append(['##Pmenu22##',menu22])
    change.append(['##Первый##',Vmenu01])
    change.append(['##Второй##',Vmenu02])
    change.append(['##Третий##',Vmenu03])   
    change.append(['##Долг##',str(dolg)]) 
    change.append(['##Расчет##',str(activ)]) 
    try:
        if int(dolg) > 0:
            change.append(['##Коммент##',str("Указанную сумму оплатить в пятницу 17.01.2025 в 14-00")]) 
        if int(dolg) <= 0:
            change.append(['##Коммент##',str("До 17-01-2025 у Вас все оплачено ")]) 
    except:        
        change.append(['##Коммент##',str("")]) 
    change.append(['##ФИО##',str(fio)]) 
    change.append(['##add_message##',add_message])
    regim  = regim.replace("Правельный","Правильный")
    change.append(['##Режим##',regim]) 
    change.append(['##user_id##',str(user_id)])    
    if message_id == 0:
        send_data = {"Text":message_out,'Кнопки':key_array,'Тип кнопки':'Сообщение','Замена':change}
    else:
        send_data = {"Text":message_out,'Кнопки':key_array,'Тип кнопки':'Сообщение','Замена':change,'message_id':message_id}
    answer = iz_bot.send_message (message_info,send_data)  
    
def get_list_product (message_info,status):
    import datetime
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    now = datetime.datetime.now()
    current_date_string = now.strftime('%d.%m.%y')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,menu01,menu02,menu11,menu12,menu21,menu22 from food where status = '{}'  ORDER BY id desc limit 1".format(status)
    cursor.execute(sql)
    data = cursor.fetchall()
    element = {}
    for rec in data: 
        id,menu01,menu02,menu11,menu12,menu21,menu22 = rec.values()
        print ('[--------------]',id,menu01,menu02,menu11,menu12,menu21,menu22)
        element['Mmenu01'] = menu01
        element['Mmenu02'] = menu02
        element['Mmenu11'] = menu11
        element['Mmenu12'] = menu12
        element['Mmenu21'] = menu21
        element['Mmenu22'] = menu22
    return element    

def get_name (message_info,status_input):
    import iz_bot
    #print ('[+] Ваше имя')
    if status_input.setdefault('Имя cотрудника','') == '':
        send_data = {"Text":"Введите ваше имя"}
        answer = iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',"Ввод имени"]]
        iz_bot.user_save_data (message_info,save_data)    
        return (False)
    else:
        return (True)        
 
def change_back (name,message_info):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,`change` from `key` where name = '{}' ".format(name)
    print (sql)
    cursor.execute(sql)
    results = cursor.fetchall()   
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
    
    
    answer = setting_bot.setdefault(name,'')
    if answer == '':
        db,cursor = iz_bot.connect (namebot) 
        sql = "INSERT INTO `menu` (`name`,`data_id`,`info`,`status`) VALUES ('{}',{},'{}','{}')".format (name_key2,data_id,key11,'')
        sql_save = ()
        cursor.execute(sql,sql_save)
        lastid = cursor.lastrowid 
        db.commit() 
    return answer
 
def get_key_menu_list (message_info,element1,element2,current_date_string,menu11,menu12,back,nextkey,backcommand,nextcommand,status):
    import iz_bot
    element = get_list_product (message_info,status)
    #print ('[element]',element)
    key_array = []            
    key11 = [change_back(element.setdefault(element1,'нет'),message_info),iz_bot.build_jsom({"o":menu11,"d":current_date_string})]
    key1 = [key11]
    key12 = [change_back(element.setdefault(element2,'нет'),message_info),iz_bot.build_jsom({"o":menu12,"d":current_date_string})]
    key2 = [key12]
    key31 = [change_back(back,message_info),iz_bot.build_jsom({"o":backcommand,"p":"Суп"})]
    key32 = [change_back(nextkey,message_info),iz_bot.build_jsom({"o":nextcommand,"p":"Мясо"})]
    key3 = [key31,key32]
    key_array.append(key1)  
    key_array.append(key2) 
    key_array.append([key31,key32])             
    return key_array 
  
def status_in (message_info,status_in,date_in):
    import iz_bot
    save_data = [['Статус ввода',status_in]]
    iz_bot.user_save_data (message_info,save_data)
    send_data = {"Text":status_in,'Замена':[['##Дата##',str(date_in)]]}
    answer = iz_bot.send_message (message_info,send_data)  
    
def status_out (message_info,id,status_in,date_in,message_in):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    menu = status_in.replace ('main','menu')
    menu = status_in.replace ('good','menu')
    sql = "UPDATE food SET {} = '{}' WHERE id = {} ".format (menu,message_in,id)
    print ('[sql]',sql)
    cursor.execute(sql)        
    db.commit()   
    send_data = {"Text":str(status_in)+'_Записан','Замена':[['##Дата##',str(date_in)]]}
    answer = iz_bot.send_message (message_info,send_data) 
    save_data = [['Статус ввода','']]
    iz_bot.user_save_data (message_info,save_data)
    
def start_prog (message_info):
    import iz_bot
    message_in = message_info.setdefault('message_in','')
    message_id = message_info.setdefault('message_id','')
    callback   = message_info.setdefault('callback','')
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    get_data = {}
    status_input = iz_bot.user_get_data (message_info,get_data)
    setting_bot  = iz_bot.get_setting (message_info)  
    for line in status_input:
        print ('        [+]',line,'-',status_input[line])
    status     = status_input.setdefault('Статус ввода','') 
    import datetime
    a   = datetime.datetime.now().time()
    now = datetime.datetime.now()
    setting = iz_bot.get_setting (message_info)
    t001 = setting.setdefault('Время начала','')
    t002 = setting.setdefault('Время конец','') 
    t1,t2 = to_data (t001)
    b1 = datetime.time(t1,t2,0,0)        
    t1,t2 = to_data (t002)
    b2  = datetime.time(t1,t2,0,0) 
    a1  = datetime.timedelta(hours=a.hour, minutes=a.minute, seconds=a.second)
    d11 = datetime.timedelta(hours=b1.hour, minutes=b1.minute, seconds=b1.second)
    d12 = datetime.timedelta(hours=b2.hour, minutes=b2.minute, seconds=b2.second)       
    u1  = (a1-d11).total_seconds()
    u2  = (a1-d12).total_seconds()        
    try:
        ls = int(message_in)
    except:
        ls = 0    
    if message_in != '' and ls != 0:
        import iz_game2
        iz_game2.gos_avto (message_info)
        return
        
    if message_in == '/remind':
        save_data = [['Напоминалка',"Да"]]
        iz_bot.user_save_data (message_info,save_data)
        send_data = {"Text":'Напоминание включено'}        
        answer = iz_bot.send_message (message_info,send_data) 
        
    if message_in == '/new':
        db,cursor = iz_bot.connect (namebot)
        sql = "UPDATE setting SET info = 'на 11 сентября 2024' WHERE id = 16 ".format ()
        cursor.execute(sql)        
        db.commit()         
        sql = "UPDATE setting SET info = '1922' WHERE id = 20 ".format ()
        cursor.execute(sql)        
        db.commit()         
        sql = "INSERT INTO food (`date`,`menu01`,`menu02`,`menu11`,`menu12`,`menu21`,`menu22`,`status`) VALUES ('09.09.2024','','','','','','','main')"
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO food (`date`,`menu01`,`menu02`,`menu11`,`menu12`,`menu21`,`menu22`,`status`) VALUES ('09.09.2024','','','','','','','good')"
        cursor.execute(sql)
        db.commit()
        send_data = {"Text":'Создан новый обед','Замена':[['##Обед##',str('09.09.2024')]]}
        answer = iz_bot.send_message (message_info,send_data) 
        
    id_s    = '84' 
    data_s  = '11.09.2024'
    if message_in == '/main01': 
        status_in (message_info,'main01',data_s)
    if status == "main01":
        status_out (message_info,id_s,'main01',data_s,message_in)
    if message_in == '/main02': 
        status_in (message_info,'main02',data_s)
    if status == "main02":
        status_out (message_info,id_s,'main02',data_s,message_in)

    if message_in == '/main11': 
        status_in (message_info,'main11',data_s)
    if status == "main11":
        status_out (message_info,id_s,'main11',data_s,message_in)
    if message_in == '/main12': 
        status_in (message_info,'main12',data_s)
    if status == "main12":
        status_out (message_info,id_s,'main12',data_s,message_in)

    if message_in == '/main21': 
        status_in (message_info,'main21',data_s)
    if status == "main21":
        status_out (message_info,id_s,'main21',data_s,message_in)
    if message_in == '/main22': 
        status_in (message_info,'main22',data_s)
    if status == "main22":
        status_out (message_info,id_s,'main22',data_s,message_in)


    id_s    = '85' 
    data_s  = '11.09.2024'
    if message_in == '/good01': 
        status_in (message_info,'good01',data_s)
    if status == "good01":
        status_out (message_info,id_s,'good01',data_s,message_in)
    if message_in == '/good02': 
        status_in (message_info,'good02',data_s)
    if status == "good02":
        status_out (message_info,id_s,'good02',data_s,message_in)
    if message_in == '/good11': 
        status_in (message_info,'good11',data_s)
    if status == "good11":
        status_out (message_info,id_s,'good11',data_s,message_in)
    if message_in == '/good12': 
        status_in (message_info,'good12',data_s)
    if status == "good12":
        status_out (message_info,id_s,'good12',data_s,message_in)
    if message_in == '/good21': 
        status_in (message_info,'good21',data_s)
    if status == "good21":
        status_out (message_info,id_s,'good21',data_s,message_in)
    if message_in == '/good22': 
        status_in (message_info,'good22',data_s)
    if status == "good22":
        status_out (message_info,id_s,'good22',data_s,message_in)
  
    if message_in == '/balance':
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,amount,nomer from balans where user_id = '{}' ORDER BY nomer DESC limit 20 ".format (user_id)
        cursor.execute(sql)
        results = cursor.fetchall()   
        message_out = ""
        summ        = status_input.setdefault('Баланс','') 
        #try:
            #summ        = int(summ) * -1
        #except:
        #    pass
        for rec in results: 
            id,name,amount,nomer = rec.values() 
            message_out = message_out 
            st = str(nomer) +'] '+name.ljust(45) +"<code>Итог:" +str(amount)+ " руб </code>" 
            message_out = message_out + st + "\n"
        send_data = {"Text":'Ваш баланс','Замена':[['##Ответ##',str(message_out)],['##Сумма##',str(summ)]]}
        answer = iz_bot.send_message (message_info,send_data)  
        
    if message_in == '/nomer':
        #import code_main314_bot
        #code_main314_bot.send_user_id  (message_info)    
        send_data = {"Text":'Ваш номер в списке','Замена':[['##user_id##',str(user_id)]]}
        answer = iz_bot.send_message (message_info,send_data)  
        return ('ok')

    ### str(user_id) != '399838806' or

    if str(user_id) != '7474072878':
        if u2 > 0 and u1 < 0 and message_in != '/list' and  message_in != '/food': 
            send_data = {"Text":'Запись на сегодня остановлена'}
            answer = iz_bot.send_message (message_info,send_data)  
            return ('ok')
   
    if message_in == 'Coin Farmer' or message_in == '/Farmer':
        label_send = True
        import iz_game
        iz_game.game_farmer (message_info,"start",'')
        message_in = ''
        callback   = ''
  
    if status == "Ввод имени":
        send_data = {"Text":"Информация записана"}
        answer = iz_bot.send_message (message_info,send_data)
        save_data = [["Статус ввода",""],["Имя cотрудника",str(message_in)]]
        iz_bot.user_save_data (message_info,save_data)
            
    if callback.find ('game_farmer_') != -1:
        label_send = True
        import iz_game
        iz_game.game_farmer (message_info,callback,'')
        message_in = ''
        callback   = ''

    if message_in.find ('/start') != -1:
        status = ''
        send_data = {"Text":'/start'}
        answer = iz_bot.send_message (message_info,send_data)

##################################  начало 93472672893 Вставка администратора ##################################

    if callback == "Вызов меню":
        import datetime        
        if 1==1:
            #send_message_menu (status_input,message_info,0,"Выбор рациона питания",setting_bot)
            iz_bot.deleteMessage (message_info,message_id)
            status_input = clear_status (status_input,message_info)
            key_array = message_menu(message_info,status_input,0)        
            send_message_menu (status_input,message_info,0,change_back ("Выбор рациона питания",message_info),key_array,setting_bot)
 
    if message_in.find ('Меню на сегодня') != -1: 
        answer = get_name (message_info,status_input)  
        status_input = clear_status (status_input,message_info)
        key_array = message_menu(message_info,status_input,0)        
        send_message_menu (status_input,message_info,0,change_back ("Выбор рациона питания",message_info),key_array,setting_bot)
                
    if callback.find ('i_') != -1:
        import json
        import requests
        import datetime
        json_string  = iz_bot.change_back(callback.replace('i_',''))
        data_json = json.loads(json_string)
        operation = data_json.setdefault('o','')
        nomer     = data_json.setdefault('p','') 
        date      = data_json.setdefault('d','') 
        now = datetime.datetime.now()
        current_date_string = now.strftime('%d.%m.%y') 
        print ('    [+] operation:',operation)    
        print ('    [+] nomer    :',nomer)  
        print ('    [+] current_date :',current_date_string)                
        
        
        if operation == 'Назад рацион':  ## Основное
            status_input = clear_status (status_input,message_info)
            key_array = message_menu(message_info,status_input,0)        
            send_message_menu (status_input,message_info,message_id,change_back ("Выбор рациона питания",message_info),key_array,setting_bot)
            date = current_date_string
            
        if operation == 'Назад в мясо':  ## Основное
            status_input = clear_status (status_input,message_info)
            key_array = message_menu(message_info,status_input,0)        
            send_message_menu (status_input,message_info,message_id,change_back ("Выбор рациона питания",message_info),key_array,setting_bot)
            date = current_date_string

        if operation == 'Мясо':  ## Основное
            status_input = clear_status (status_input,message_info)
            key_array = message_menu(message_info,status_input,0)        
            send_message_menu (status_input,message_info,message_id,change_back ("Выбор рациона питания",message_info),key_array,setting_bot)
            date = current_date_string
                    
        if operation == 'Далее мясо':
            if status_input['Режим'] == 'Основной':
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее гарнир","Назад рацион","Далее гарнир","main")               
                send_message_menu (status_input,message_info,message_id,change_back("Список основного питания",message_info),key_array,setting_bot)
            if status_input['Режим'] == 'Правельный':    
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее гарнир","Назад рацион","Далее гарнир","good")
                send_message_menu (status_input,message_info,message_id,change_back("Список основного питания",message_info),key_array,setting_bot)
            date = current_date_string
            
        if operation == 'Далее гарнир':
            if status_input['Режим'] == 'Основной':
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","main")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot) 
            if status_input['Режим'] == 'Правельный':    
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","good")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot) 
            date = current_date_string            
            
        if operation == 'Далее в итого':
            key_array = []            
            key11 = [change_back('Подтвердить заказ',message_info),iz_bot.build_jsom({"o":'menu41',"d":current_date_string})]
            key1 = [key11]
            key_array.append(key1)  
            send_message_menu (status_input,message_info,message_id,"Подтвердить заказ выбор",key_array,setting_bot)             
            date = current_date_string 
        
        
        print ('[+]............[+]')
        print (a.hour)
        print (b1.hour)
        print ('[+]............[+]')
        
        
        if current_date_string != date and a.hour > 9:
            send_data = {"Text":"Данная информация устарела","message_id":message_id}     
            iz_bot.send_message (message_info,send_data)
            return
        
        if operation == 'menu01':  ## Основное
            save_data = [['Режим','Основной']]
            status_input['Режим']  = 'Основной'
            iz_bot.user_save_data (message_info,save_data) 
            key_array = get_key_menu_list (message_info,'Mmenu01','Mmenu02',current_date_string,"menu11" ,"menu12","Назад в рацион","Далее в мясо","Назад рацион","Далее мясо","main")
            send_message_menu (status_input,message_info,message_id,change_back("Список основного питания",message_info),key_array,setting_bot)
        
        if operation == 'menu02':  # Правельный
            save_data = [['Режим','Правельный']]
            status_input['Режим']  = 'Правельный'
            iz_bot.user_save_data (message_info,save_data) 
            key_array = get_key_menu_list (message_info,'Mmenu01','Mmenu02',current_date_string,"menu11" ,"menu12","Назад в рацион","Далее в мясо","Назад рацион","Далее мясо","good")
            send_message_menu (status_input,message_info,message_id,change_back("Список основного питания",message_info),key_array,setting_bot)        
           
        if operation == 'menu11': ## Мясо 
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')                
                save_data = [['Vmenu01',element['Mmenu01']]]
                status_input['Vmenu01']  = element['Mmenu01']
                iz_bot.user_save_data (message_info,save_data)                 
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее в мясо","Назад рацион","Далее гарнир","main")                            
            if status_input['Режим'] == 'Правельный': 
                element = get_list_product (message_info,'good')                
                save_data = [['Vmenu01',element['Mmenu01']]]
                status_input['Vmenu01']  = element['Mmenu01']
                iz_bot.user_save_data (message_info,save_data)                 
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее в мясо","Назад рацион","Далее гарнир","good")
            send_message_menu (status_input,message_info,message_id,change_back("Список выбора мяса",message_info),key_array,setting_bot)    
        
        if operation == 'menu12': ## Мясо 
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')                
                save_data = [['Vmenu01',element['Mmenu02']]]
                status_input['Vmenu01']  = element['Mmenu02']
                iz_bot.user_save_data (message_info,save_data)                 
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее в мясо","Назад рацион","Далее гарнир","main")                
            if status_input['Режим'] == 'Правельный': 
                element = get_list_product (message_info,'good')                
                save_data = [['Vmenu01',element['Mmenu02']]]
                status_input['Vmenu01']  = element['Mmenu02']
                iz_bot.user_save_data (message_info,save_data)                 
                key_array = get_key_menu_list (message_info,'Mmenu11','Mmenu12',current_date_string,"menu21" ,"menu22","Назад в режим","Далее в мясо","Назад рацион","Далее гарнир","good")
            send_message_menu (status_input,message_info,message_id,change_back("Список выбора мяса",message_info),key_array,setting_bot)              
                  
        if operation == 'menu21':   ## Гарнир 
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')  
                save_data = [['Vmenu02',element['Mmenu11']]]
                status_input['Vmenu02']  = element['Mmenu11']
                iz_bot.user_save_data (message_info,save_data)  
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","main")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot) 
            if status_input['Режим'] == 'Правельный':
                element = get_list_product (message_info,'good')  
                save_data = [['Vmenu02',element['Mmenu11']]]
                status_input['Vmenu02']  = element['Mmenu11']
                iz_bot.user_save_data (message_info,save_data)  
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","good")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot) 

        if operation == 'menu22':   ## Гарнир 
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')  
                save_data = [['Vmenu02',element['Mmenu12']]]
                status_input['Vmenu02']  = element['Mmenu12']
                iz_bot.user_save_data (message_info,save_data)  
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","main")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot) 
            if status_input['Режим'] == 'Правельный':
                element = get_list_product (message_info,'good')  
                save_data = [['Vmenu02',element['Mmenu12']]]
                status_input['Vmenu02']  = element['Mmenu12']
                iz_bot.user_save_data (message_info,save_data)  
                key_array = get_key_menu_list (message_info,'Mmenu21','Mmenu22',current_date_string,"menu31" ,"menu32","Назад в режим","Далее в итого","Назад в мясо","Далее в итого","good")                
                send_message_menu (status_input,message_info,message_id,"Список выбора второго",key_array,setting_bot)                 
                
        if operation == 'menu31':   ##  
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')  
                save_data = [['Vmenu03',element['Mmenu21']]]
                status_input['Vmenu03']  = element['Mmenu21']
                iz_bot.user_save_data (message_info,save_data) 
            if status_input['Режим'] == 'Правельный':
                element = get_list_product (message_info,'good')  
                save_data = [['Vmenu03',element['Mmenu21']]]
                status_input['Vmenu03']  = element['Mmenu21']
                iz_bot.user_save_data (message_info,save_data)  
            key_array = []            
            key11 = [change_back('Подтвердить заказ',message_info),iz_bot.build_jsom({"o":'menu41',"d":current_date_string})]
            key1 = [key11]
            key_array.append(key1)  
            send_message_menu (status_input,message_info,message_id,"Подтвердить заказ выбор",key_array,setting_bot) 
        
        if operation == 'menu32':   ##  
            if status_input['Режим'] == 'Основной':
                element = get_list_product (message_info,'main')  
                save_data = [['Vmenu03',element['Mmenu22']]]
                status_input['Vmenu03']  = element['Mmenu22']
                iz_bot.user_save_data (message_info,save_data) 
            if status_input['Режим'] == 'Правельный':
                element = get_list_product (message_info,'good')  
                save_data = [['Vmenu03',element['Mmenu22']]]
                status_input['Vmenu03']  = element['Mmenu22']
                iz_bot.user_save_data (message_info,save_data)  
            key_array = []            
            key11 = [change_back('Подтвердить заказ',message_info),iz_bot.build_jsom({"o":'menu41',"d":current_date_string})]
            key1 = [key11]
            key_array.append(key1)  
            send_message_menu (status_input,message_info,message_id,"Подтвердить заказ выбор",key_array,setting_bot) 
            
        if operation == 'menu41':   ##  
            Vmenu01 = status_input.setdefault('Vmenu01','')
            Vmenu02 = status_input.setdefault('Vmenu02','')
            Vmenu03 = status_input.setdefault('Vmenu03','')
            regim = status_input['Режим']
            db,cursor = iz_bot.connect (namebot)
            sql = "INSERT INTO `order` (`date`,`user_id`,`menu01`,`menu02`,`menu03`,status,regim,`dateT`) VALUES ('{}','{}','{}','{}','{}','{}','{}','')".format (current_date_string,user_id,Vmenu01,Vmenu02,Vmenu03,'',regim)
            sql_save = ()
            cursor.execute(sql,sql_save)
            lastid = cursor.lastrowid 
            db.commit() 
            key_array = []
            key11 = [change_back("Отменить заказ",message_info),iz_bot.build_jsom({"o":"menu51","d":current_date_string,"p":lastid})]
            key1 = [key11]
            key_array.append(key1)    
            send_message_menu (status_input,message_info,message_id,change_back("Заказ выполнен",message_info),key_array,setting_bot)  
            
        if operation == 'menu51':   ##  
            key_array = []
            key11 = [change_back("Вернуть заказ",message_info),iz_bot.build_jsom({"o":"menu61","d":current_date_string,"p":nomer})]
            key1 = [key11]
            key_array.append(key1)    
            send_message_menu (status_input,message_info,message_id,change_back("Заказ отменен",message_info),key_array,setting_bot)  
            Vmenu01 = status_input.setdefault('Vmenu01','')
            Vmenu02 = status_input.setdefault('Vmenu02','')
            Vmenu03 = status_input.setdefault('Vmenu03','')
            db,cursor = iz_bot.connect (namebot)
            id = nomer
            sql = "UPDATE `order` SET status = %s WHERE id = %s ".format ()
            sql_save = ('Отказ',id)
            cursor.execute(sql,sql_save)
            db.commit()
            
            
        if operation == 'menu61':   ##  
            Vmenu01 = status_input.setdefault('Vmenu01','')
            Vmenu02 = status_input.setdefault('Vmenu02','')
            Vmenu03 = status_input.setdefault('Vmenu03','')
            db,cursor = iz_bot.connect (namebot)
            db.commit() 
            key_array = []
            key11 = [change_back("Отменить заказ",message_info),iz_bot.build_jsom({"o":"menu51","d":current_date_string,"p":nomer})]
            key1 = [key11]
            key_array.append(key1)    
            send_message_menu (status_input,message_info,message_id,change_back("Заказ выполнен",message_info),key_array,setting_bot)              
            id = nomer
            sql = "UPDATE `order` SET status = %s WHERE id = %s ".format ()
            sql_save = ('Работает',id)
            cursor.execute(sql,sql_save)
            db.commit()
                    
    if message_in == '/excel':
        import iz_bot
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete' and status <> 'Отказ'".format(setting_bot.setdefault('Последний ID',0))
        cursor.execute(sql)
        data = cursor.fetchall()
        st_line1 = ""
        st_line2 = ""
        str_koll = 0
        for rec in data: 
            id,user_id_p,menu01,menu02,menu03 = rec.values()
            str_koll = str_koll + 1
            get_data    = {'user_id':user_id_p}
            status_user = iz_bot.user_get_data (message_info,get_data)
            st_one = str(str_koll) + ";" + str(status_user.setdefault('Имя cотрудника',str(user_id))) +';'+ str(user_id_p) + ";" + str(menu01) + ", " +str(menu02) + ", " + str(menu03) + "\n"
            if str_koll < 30:
                st_line1 = st_line1 + st_one   
            else:
                st_line2 = st_line2 + st_one               
        if st_line1 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line1]]} 
            iz_bot.send_message (message_info,send_data)
        if st_line2 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line2]]} 
            iz_bot.send_message (message_info,send_data)
        
    if message_in == '/list':
        import iz_bot
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete' and status <> 'Отказ'".format(setting_bot.setdefault('Последний ID',0))
        cursor.execute(sql)
        data = cursor.fetchall()
        st_line1 = ""
        st_line2 = ""
        st_line3 = ""
        st_line4 = ""
        
        list = []    
        for rec in data: 
            id,user_id_p,menu01,menu02,menu03 = rec.values()
            get_data    = {'user_id':user_id_p}
            status_user = iz_bot.user_get_data (message_info,get_data)
            st_one = str(status_user.setdefault('Имя cотрудника',str(user_id))) +'('+ str(user_id_p) + "), <code>" + str(menu01) + ", " +str(menu02) + ", " + str(menu03) + " </code>"
            list.append (st_one)
            
        list = sorted(list)    
        print ('[+]----------------------------------------------------------------------------------------------------------[+]')    
        str_koll = 0    
        for st_one in list: 
            print ('[+] st_one:',st_one)            
            str_koll = str_koll + 1
            if str_koll < 30:
                st_line1 = st_line1 + str(str_koll) + ") " + st_one + '\n'  
            if str_koll >= 30 and str_koll < 60:
                st_line2 = st_line2 + str(str_koll) + ") " + st_one + '\n'  
            if str_koll >= 60 and str_koll < 90:
                st_line3 = st_line3 + str(str_koll) + ") " + st_one + '\n'  
            if str_koll >= 90 and str_koll < 120:
                st_line4 = st_line4 + str(str_koll) + ") " + st_one + '\n'  
        print ('[+]----------------------------------------------------------------------------------------------------------[+]')    
                
        if st_line1 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line1]]} 
            iz_bot.send_message (message_info,send_data)
        if st_line2 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line2]]} 
            iz_bot.send_message (message_info,send_data)
        if st_line3 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line3]]} 
            iz_bot.send_message (message_info,send_data)
        if st_line4 != '':
            send_data = {'Text':'Список заказав','Замена':[['#Список#',st_line4]]} 
            iz_bot.send_message (message_info,send_data)
            

        import iz_bot
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete' and status <> 'Отказ'  and regim = 'Основной' ".format(setting_bot.setdefault('Последний ID',0))
        cursor.execute(sql)
        data = cursor.fetchall()
        st_line = ""
            
        menu01_a = 0
        menu01_b = 0
        menu02_a = 0
        menu02_b = 0
        menu03_a = 0
        menu03_b = 0
        element = get_list_product (message_info,"main")   
        
        for rec in data: 
            id,user_id_p,menu01,menu02,menu03 = rec.values()
            if element['Mmenu01'] == menu01:
                menu01_a = menu01_a + 1
            if element['Mmenu02'] == menu01:
                menu01_b = menu01_b + 1
                
            if element['Mmenu11'] == menu02:
                menu02_a = menu02_a + 1    
            if element['Mmenu12'] == menu02:
                menu02_b = menu02_b + 1  

            if element['Mmenu21'] == menu03:
                menu03_a = menu03_a + 1    
            if element['Mmenu22'] == menu03:
                menu03_b = menu03_b + 1   
                
                
        
        s01_a = ['#Menu01#',str(menu01_a)]    
        n01_a = ['#name01#',str(element['Mmenu01'])]
        s02_a = ['#Menu02#',str(menu01_b)]    
        n02_a = ['#name02#',str(element['Mmenu02'])]


        s03_a = ['#Menu03#',str(menu02_a)]    
        n03_a = ['#name03#',str(element['Mmenu11'])]
        s04_a = ['#Menu04#',str(menu02_b)]    
        n04_a = ['#name04#',str(element['Mmenu12'])]


        s05_a = ['#Menu05#',str(menu03_a)]    
        n05_a = ['#name05#',str(element['Mmenu21'])]
        s06_a = ['#Menu06#',str(menu03_b)]    
        n06_a = ['#name06#',str(element['Mmenu22'])]


        st_long = ''
        if element['Mmenu01'] != '': 
            st_long = st_long + ' ' + element['Mmenu01'] + ' ' + str(menu01_a)+'\n'
        if element['Mmenu02'] != '':         
            st_long = st_long + ' ' + element['Mmenu02'] + ' ' + str(menu01_b)+'\n' 
        if element['Mmenu11'] != '':     
            st_long = st_long + ' ' + element['Mmenu11'] + ' ' + str(menu02_a)+'\n' 
        if element['Mmenu12'] != '':     
            st_long = st_long + ' ' + element['Mmenu12'] + ' ' + str(menu02_b)+'\n' 
        if element['Mmenu21'] != '':     
            st_long = st_long + ' ' + element['Mmenu21'] + ' ' + str(menu03_a)+'\n' 
        if element['Mmenu22'] != '':     
            st_long = st_long + ' ' + element['Mmenu22'] + ' ' + str(menu03_b)+'\n' 
        send_data = {'Text':'Статистика заказов','Замена':[['#Статистика#',st_long]]} 
        iz_bot.send_message (message_info,send_data)        
                
####### ---------------

        import iz_bot
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,user_id,menu01,menu02,menu03 from `order` where id > {} and status <> 'delete' and status <> 'Отказ' and regim = 'Правельный' ".format(setting_bot.setdefault('Последний ID',0))
        cursor.execute(sql)
        data = cursor.fetchall()
        st_line = ""
            
        menu01_a = 0
        menu01_b = 0
        menu02_a = 0
        menu02_b = 0
        menu03_a = 0
        menu03_b = 0
        element = get_list_product (message_info,"good")   
        
        for rec in data: 
            id,user_id_p,menu01,menu02,menu03 = rec.values()
            if element['Mmenu01'] == menu01:
                menu01_a = menu01_a + 1
            if element['Mmenu02'] == menu01:
                menu01_b = menu01_b + 1
                
            if element['Mmenu11'] == menu02:
                menu02_a = menu02_a + 1    
            if element['Mmenu12'] == menu02:
                menu02_b = menu02_b + 1  

            if element['Mmenu21'] == menu03:
                menu03_a = menu03_a + 1    
            if element['Mmenu22'] == menu03:
                menu03_b = menu03_b + 1   
                
                
        
        s01_a = ['#Menu01#',str(menu01_a)]    
        n01_a = ['#name01#',str(element['Mmenu01'])]
        s02_a = ['#Menu02#',str(menu01_b)]    
        n02_a = ['#name02#',str(element['Mmenu02'])]


        s03_a = ['#Menu03#',str(menu02_a)]    
        n03_a = ['#name03#',str(element['Mmenu11'])]
        s04_a = ['#Menu04#',str(menu02_b)]    
        n04_a = ['#name04#',str(element['Mmenu12'])]


        s05_a = ['#Menu05#',str(menu03_a)]    
        n05_a = ['#name05#',str(element['Mmenu21'])]
        s06_a = ['#Menu06#',str(menu03_b)]    
        n06_a = ['#name06#',str(element['Mmenu22'])]


        st_long = ''
        if element['Mmenu01'] != '': 
            st_long = st_long + ' ' + element['Mmenu01'] + ' ' + str(menu01_a)+'\n'
        if element['Mmenu02'] != '':         
            st_long = st_long + ' ' + element['Mmenu02'] + ' ' + str(menu01_b)+'\n' 
        if element['Mmenu11'] != '':     
            st_long = st_long + ' ' + element['Mmenu11'] + ' ' + str(menu02_a)+'\n' 
        if element['Mmenu12'] != '':     
            st_long = st_long + ' ' + element['Mmenu12'] + ' ' + str(menu02_b)+'\n' 
        if element['Mmenu21'] != '':     
            st_long = st_long + ' ' + element['Mmenu21'] + ' ' + str(menu03_a)+'\n' 
        if element['Mmenu22'] != '':     
            st_long = st_long + ' ' + element['Mmenu22'] + ' ' + str(menu03_b)+'\n' 
        send_data = {'Text':'Статистика заказов','Замена':[['#Статистика#',st_long]]} 
        iz_bot.send_message (message_info,send_data)
                                
    if message_in == '/time_zona':
        user_id    = message_info.setdefault('user_id','') 
        namebot    = message_info.setdefault('namebot','')    
        send_data = {"Text":'Укажите Ваш город'}        
        answer = iz_bot.send_message (message_info,send_data) 
        save_data = [['Статус ввода',"Ввод города"],['Город','']]
        iz_bot.user_save_data (message_info,save_data)  
        status = ''

    global_prif = "ex_"
    if message_in == '/status_2' or callback.find ('ex_') != -1 or status_input.setdefault('Статус ввода','').find (global_prif) != -1:  
        import code_shkepeerbot
        if message_in == '/status_2':
            message_info['message_in'] = '➕ Добавить'
        code_shkepeerbot.code03 (message_info,status_input,global_prif)       
         
    if status_input.setdefault('Статус ввода','')  == 'Ввод нового сообщения':
        db,cursor = iz_bot.connect (namebot)
        save_data = [['Статус ввода',''],['Номер заменяемого сообщения','']]
        iz_bot.user_save_data (message_info,save_data)
        nomer_id = status_input.setdefault('Номер заменяемого сообщения','')
        sql = "UPDATE message SET info = '"+message_in+"' WHERE id = "+str(nomer_id)+""
        cursor.execute(sql)
        db.commit()
        send_data = {"Text":"Редактирование сообщения завершено"}        
        iz_bot.send_message (message_info,send_data) 

    if status_input.setdefault('Статус ввода','')  == 'Ввод куска текста':
        send_data = {"Text":'Поиск текста'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Текст поиска',message_in]]
        iz_bot.user_save_data (message_info,save_data)
        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)        
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,name,info,data_id from message where name = 'Текст' and info like '%"+str(message_in)+"%' limit 5"
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,name,info,data_id = rec.values()
            sql = "select id,name,info from message where name = 'Имя' and id = '"+str(data_id)+"' limit 1"
            cursor.execute(sql)
            data = cursor.fetchall()
            info_v = ''
            for rec_v in data: 
                id_v,name_v,info_v = rec_v.values()
            send_data = {"Text":"Номер сообшения","Замена":[['%id%',id],['%name%',info_v]]}        
            iz_bot.send_message (message_info,send_data)          
            send_data = {"Text":info,'Запись в базу':'Не записывать'}        
            iz_bot.send_message (message_info,send_data)
        
    if status_input.setdefault('Статус ввода','')  == 'Ввод сообщения':
        send_data = {"Text":'Сообщение сохранено'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Сообщение для отправки',message_in]]
        iz_bot.user_save_data (message_info,save_data)
        save_data = [['Статус ввода',""]]
        iz_bot.user_save_data (message_info,save_data)

    if message_in == '/in_message':        
        send_data = {"Text":'Введите сообщение для отправки'}        
        iz_bot.send_message (message_info,send_data)         
        save_data = [['Статус ввода',"Ввод сообщения"]]
        iz_bot.user_save_data (message_info,save_data)

    if message_in == '/status':
        send_data = {"Text":'Статус телеграмм бота'}        
        iz_bot.send_message (message_info,send_data) 

    if message_in == '/send':
        send_data = {"Text":'Отправить сообшение'}        
        iz_bot.send_message (message_info,send_data) 
    
    if message_in == '/stop':
        send_data = {"Text":'Админка отключна'}        
        iz_bot.send_message (message_info,send_data) 
        
    if message_in == '/stat':
        send_data = {"Text":'Статистика бота'}        
        iz_bot.send_message (message_info,send_data)     
        
    if message_in == '/server':
        send_data = {"Text":'Информация о работе сервера'}        
        iz_bot.send_message (message_info,send_data)     
     
    if message_in == '/help':
        send_data = {"Text":'Помощь'}        
        iz_bot.send_message (message_info,send_data)      

    if message_in == '/trafic':  
        import code_main314_bot   
        code_main314_bot.trafic (message_info)

    if message_in == '/memory':     
        import psutil
        hdd = psutil.disk_usage('/')
        total   = hdd.total   #)      #/ (2**30))
        used    = hdd.used    #)      #/ (2**30))
        free    = hdd.free    #)      #/ (2**30))
        percent = hdd.percent #)      #/ (2**30))
        send_data = {"Text":'Информация о системе','Замена':[['%percent%',percent]]}
        iz_bot.send_message (message_info,send_data)      
 
    if message_in == '/food':
        import iz_bot
        db,cursor = iz_bot.connect (namebot)
        sql = "select id,date,menu01,menu02,menu03 from `order` where user_id = '{}' ORDER BY id desc limit 20".format(user_id)
        print ('[sql]',sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        st_long = ''
        for rec in data: 
            id,date,menu01,menu02,menu03 = rec.values()
            st_long = st_long + str(date) + ' : ' +str(menu01) +' ' + str(menu02) +' '+ str(menu03) + '\n'
            
        send_data = {'Text':'Мои заказы','Замена':[['#Заказы#',st_long]]} 
        iz_bot.send_message (message_info,send_data)
        
        
 
 
