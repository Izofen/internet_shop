
#!/usr/bin/python
# -*- coding: utf-8
def connect_postgres ():  
    import psycopg2
    db = psycopg2.connect(dbname='main', user='postgres', password='podkjf4', host='localhost')
    cursor = db.cursor()       
    return db,cursor 

def connect (namebot):
    #import pymysql 
    #base = namebot.replace("@","")
    #db = pymysql.connect(host='localhost',user='root',password='podkjf4',database=base,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)  
    #cursor = db.cursor()
    
    import sqlite3
    db      = sqlite3.connect('orenklip_bot.db')
    cursor  = db.cursor()
    
    return db,cursor
        
def change (word):
    word = word.replace("'","<1>")
    word = word.replace('"',"<2>")
    word = word.replace('/',"<3>")
    word = word.replace(')',"<4>")
    word = word.replace('(',"<5>")
    return (word)

def change_back (word):
    word = word.replace("#1#","'")
    word = word.replace("#2#",'"')
    word = word.replace("#3#",'/')
    word = word.replace("#4#",')')
    word = word.replace("#5#",'(')
    word = word.replace("#",'"')
    return (word)

def build_jsom (dict):    #### {"o":"next","sql":id_sql}
    json_message = str(dict)
    json_message = json_message.replace ("'",'"')
    json_message = json_message.replace ('"','#')
    #json_message = change(json_message)
    json_message = "i_"+json_message
    json_message = json_message.replace (", ",',')
    json_message = json_message.replace (": ",':')
    return (json_message)

def user_get_data (message_info,get_data):
    namebot = message_info['namebot']
    if get_data.setdefault('user_id','') == '':
        user_id = message_info['user_id']
    else:
        user_id = get_data['user_id']
    
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' ;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info,data_id = row.values() 
        #data_answer[name] = info
        sql = "select id,name,info from users where data_id = '{}' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            #print (id,name,info)
            data_answer[name] = info
    return data_answer 

def save_FIO (message_info):
    import time
    namebot       = message_info ['namebot']
    first_name    = message_info ['first_name']
    last_name     = message_info ['last_name']
    username      = message_info ['username']
    message_in    = message_info ['message_in']
    db,cursor = connect (namebot)
    user_id = message_info ['user_id'] 
    sql = "select id,name from users where name = 'user_id' and info = '"+str(user_id)+"' limit 1" 
    cursor.execute(sql)
    results = cursor.fetchall()        
    id = 0
    for row in results:    
        id,name = row.values()
    if id == 0:
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('user_id',str(user_id),0)
        cursor.execute(sql)
        db.commit()  
        lastid = cursor.lastrowid
        sql = "UPDATE users SET data_id = {} WHERE id = {}".format(lastid,lastid)
        cursor.execute(sql)
        db.commit()       
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('first_name',str(first_name),lastid)
        cursor.execute(sql)
        db.commit()          
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('last_name',str(last_name),lastid)
        cursor.execute(sql)
        db.commit()          
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('username',str(username),lastid)
        cursor.execute(sql)
        db.commit()  
        sql = "INSERT INTO users (`name`,`info`,`data_id`,`status`) VALUES ('{}','{}',{},'')".format ('time_start',str(int(time.time())),lastid)
        cursor.execute(sql)
        db.commit()
    else:
        sql = "UPDATE users SET info = '{}' WHERE data_id = {} and name = 'username' ".format(username,id)
        cursor.execute(sql)
        db.commit()  
        
    id = 0
    sql = "select a2.id,a2.info from users as a1,users as a2 where a1.name = 'Игнор' and a1.info = 'Да' and a1.data_id = a2.id and a2.name = 'user_id' and a2.info = '{}';".format(user_id)
    #print ('[+] sql:',sql)
    cursor.execute(sql)
    results = cursor.fetchall()        
    for row in results:
        id,info = row.values()
        print ('[+] Игнор по пользователю:',id,info)
    
    if id == 0 and message_in != '/start':
        sql = "select a2.id,a2.info from users as a1,users as a2 where a1.name = 'Новый клиент' and a1.info = 'Да' and a1.data_id = a2.id and a2.name = 'user_id';"
        #print ('[+] sql:',sql)
        cursor.execute(sql)
        results = cursor.fetchall()        
        for row in results: 
            id,user_id_name = row.values()
            print ('    [+] Пользователь для администрирования:')            
            key_array = []
            key11     = ["Игнор","ig_"+str(user_id)]
            key12     = ["Заказ","za_"+str(user_id)]
            key21     = ["Удалить","del_"+str(user_id)]
            key1      = [key11,key12,['','']]
            key2      = [key21,['',''],['','']]
            key_array.append(key1)
            key_array.append(key2)
            send_data = {'Text':'Новый клиент','Замена':[['#user_id#',user_id],['#first_name#',first_name],['#last_name#',last_name],['#username#',username],['#message_in#',message_info['message_in']]],'Кнопки':key_array,'Тип кнопки':'Сообщение'}
            message_info['user_id'] = user_id_name
            answer = send_message (message_info,send_data)
            #print ('[answer]:',answer)
            try:
                answer_message_id = answer['result']['message_id']
                import datetime
                dt_now = datetime.datetime.now()
                data = str(dt_now)
                sql = "INSERT INTO message_id (`name`,`data_id`,`message_id`,`data`,`user_id`,`status`) VALUES ( '{}','{}',{},'{}','{}','')".format ('Информирование',user_id,answer_message_id,data,user_id_name)
                cursor.execute(sql)
                db.commit()
            except:
                pass
            message_info['user_id'] = user_id
    db.close
        
def dict (menu,name,empty):
    try:
        text = menu[name]
    except:    
        text = empty
    return text


def get_setting_prog (namebot):         ### Получение всех настроек программы
    db,cursor = connect_postgres ()
    info = {}
    sql = "SELECT * FROM SETTING WHERE namebot = '{}' and status <> 'delete' ".format(namebot)
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:    
        l1 = row[1].strip()
        info[l1] = row[2].strip()
    return info 

def get_menu  (message_info,menu_data): 
    import json
    markup = ''
    namebot    = message_info ['namebot']
    name       = menu_data.setdefault ('Имя меню','')
    key_array  = menu_data.setdefault ('Кнопки','')
    db,cursor = connect (namebot)
    data_menu = {}
    data_menu ['Тип кнопки'] = menu_data.setdefault('Тип кнопки','Клавиатура')
    
    if key_array != '' and data_menu['Тип кнопки'] == 'Интернет':
        number = 0
        for line in key_array: 
            number = number + 1
            try:
                data_menu ['Кнопка ' +str(number)+'1'] = line[0][0]
            except:
                pass                                
            try:    
                data_menu ['Кнопка ' +str(number)+'2'] = line[1][0]
            except:
                pass                
            try:    
                data_menu ['Кнопка ' +str(number)+'3'] = line[2][0]
            except:
                pass                                
            try:    
                data_menu ['Кнопка ' +str(number)+'4'] = line[3][0]
            except:
                pass                                
            try:    
                data_menu ['Интернет '+str(number)+'1'] = line[0][1]
            except:
                pass                                
            try:    
                data_menu ['Интернет '+str(number)+'2'] = line[1][1]
            except:
                pass                                
            try:    
                data_menu ['Интернет '+str(number)+'3'] = line[2][1]
            except:
                pass                                
            try:    
                data_menu ['Интернет '+str(number)+'4'] = line[3][1]
            except:
                pass                       
                

    if key_array != '' and data_menu['Тип кнопки'] != 'Интернет':
        number = 0
        for line in key_array: 
            number = number + 1
            try:
                data_menu ['Кнопка ' +str(number)+'1'] = line[0][0]
            except:
                pass                                
            try:    
                data_menu ['Кнопка ' +str(number)+'2'] = line[1][0]
            except:
                pass                
            try:    
                data_menu ['Кнопка ' +str(number)+'3'] = line[2][0]
            except:
                pass                                
            try:    
                data_menu ['Кнопка ' +str(number)+'4'] = line[3][0]
            except:
                pass                                
            try:    
                data_menu ['Команда '+str(number)+'1'] = line[0][1]
            except:
                pass                                
            try:    
                data_menu ['Команда '+str(number)+'2'] = line[1][1]
            except:
                pass                                
            try:    
                data_menu ['Команда '+str(number)+'3'] = line[2][1]
            except:
                pass                                
            try:    
                data_menu ['Команда '+str(number)+'4'] = line[3][1]
            except:
                pass                
                

    if name != '':    
        sql = "select id,name,info from menu where name = 'Имя' and info = '{}' ;".format (name)
        cursor.execute(sql)
        results = cursor.fetchall()    
        id = 0
        for row in results:
            id,name,info = row.values() 
            data_menu[name] = info
        sql = "select id,name,info from menu where  data_id = '{}' and status <> 'delete' ;".format (id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            data_menu[name] = info
            
    if data_menu['Тип кнопки'] == 'Интернет':
        line = []
        
        print ('------------------------------------------------------------------------[+]')
        
        for number in range(30):
            line1  = []
            key11  = {}
            
            print ('[data_menu]',data_menu)
            
            
            key11['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'1','')
            key11['url'] = data_menu.setdefault('Интернет '+str(number+1)+'1','')
            key12  = {}
            key12['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'2','')
            key12['url'] = data_menu.setdefault('Интернет '+str(number+1)+'2','')
            
            key13  = {}
            key13['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'3','')
            key13['url'] = data_menu.setdefault('Интернет '+str(number+1)+'3','')
            
            key14  = {}
            key14['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'4','')
            key14['url'] = data_menu.setdefault('Интернет '+str(number+1)+'4','')
            
            if data_menu.setdefault('Кнопка ' +str(number+1)+'1','') != '':        
                line1.append(key11)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'2','') != '':
                line1.append(key12)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'3','') != '':        
                line1.append(key13)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'4','') != '':        
                line1.append(key14)
            line.append(line1)    
        array = {"inline_keyboard":line} 

        print ('[+] array',array)

        
        markup = json.dumps(array)
     
    if data_menu['Тип кнопки'] == 'Сообщение':
        line = []
        for number in range(30):
            line1  = []
            key11  = {}
            key11['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'1','')
            key11['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'1','')
            key12  = {}
            key12['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'2','')
            key12['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'2','')
            key13  = {}
            key13['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'3','')
            key13['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'3','')
            key14  = {}
            key14['text']          = data_menu.setdefault('Кнопка ' +str(number+1)+'4','')
            key14['callback_data'] = data_menu.setdefault('Команда '+str(number+1)+'4','')
            if data_menu.setdefault('Кнопка ' +str(number+1)+'1','') != '':        
                line1.append(key11)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'2','') != '':
                line1.append(key12)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'3','') != '':        
                line1.append(key13)
            if data_menu.setdefault('Кнопка ' +str(number+1)+'4','') != '':        
                line1.append(key14)
            line.append(line1)    
        array = {"inline_keyboard":line}  
        markup = json.dumps(array)
    
    if data_menu['Тип кнопки'] == 'Клавиатура':    
        array  = {}        
        line   = []
        for number in range(10):
            line1  = []
            key11  = {}
            key11['text'] = data_menu.setdefault('Кнопка '+str(number)+'1','')   

            if data_menu.setdefault('Тип {}1'.format (number),'') == 'Условия': 
                get_data = {}
                status_input = user_get_data (message_info,get_data)
                
                print ('    [+] 2',status_input.setdefault ('Вид кнопки {}1'.format(number),''))
                if status_input.setdefault ('Кнопка {}1'.format(number),'') == '':
                    if data_menu.setdefault('Замена {}1'.format(number),'') != '':
                        key11['text'] = data_menu.setdefault('Замена {}1'.format(number),'')
                        
                if status_input.setdefault ('Кнопка {}1'.format(number),'') == 'A':
                    if data_menu.setdefault('Кнопка {}1-A'.format(number),'') != '':    
                        if data_menu.setdefault('Замена {}1-A'.format(number),'') != '':
                            key11['text'] = data_menu.setdefault('Замена {}1-A'.format(number),'') 
                        else:
                            key11['text'] = data_menu.setdefault('Кнопка {}1-A'.format(number),'') 
                        
                if status_input.setdefault ('Кнопка {}1'.format(number),'') == 'B':
                    if data_menu.setdefault('Кнопка {}1-B'.format(number),'') != '':    
                        if data_menu.setdefault('Замена {}1-B'.format(number),'') != '':
                            key11['text'] = data_menu.setdefault('Замена {}1-B'.format(number),'')
                        else:
                            key11['text'] = data_menu.setdefault('Кнопка {}1-B'.format(number),'')
                        
                        
            
            if data_menu.setdefault('Тип {}1'.format (number),'') == '': 
                if data_menu.setdefault('Замена {}1'.format(number),'') != '':
                    key11['text'] = data_menu.setdefault('Замена {}1'.format(number),'')                                        
                    
            
            
            if data_menu.setdefault('Тип {}1'.format(number),'') == 'Телефон':
                key11['request_contact'] =True
                    
                    
                    
            line1.append(key11)
            key12 = {}
            key12['text'] = data_menu.setdefault('Кнопка '+str(number)+'2','')
            if data_menu.setdefault('Замена '+str(number)+'2','') != '':
                key12['text'] = data_menu.setdefault('Замена '+str(number)+'2','')
            line1.append(key12)    
            key13 = {}
            key13['text'] = data_menu.setdefault('Кнопка '+str(number)+'3','')
            if data_menu.setdefault('Замена '+str(number)+'3','') != '':
                key13['text'] = data_menu.setdefault('Замена '+str(number)+'3','')
            line1.append(key13)        
            line.append(line1)
        print ('[+] line',line)            
        array = {"keyboard":line,"resize_keyboard":True}  
        markup = json.dumps(array)      
        
    if data_menu['Тип кнопки'] == 'Удалить':        
        array = {"remove_keyboard":True,"resize_keyboard":True}  
        markup = json.dumps(array)      
        
        
    return markup

def get_setting (message_info):
    namebot = message_info['namebot']
    db,cursor = connect (namebot)
    data_answer = {}
    sql = "select id,name,info from setting where 1=1".format ()
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        if str(type(row)) == "<class 'tuple'>":
            id,name,info = row
        else:    
            id,name,info = row.values() 
        data_answer[name] = info
    return data_answer 
      
def get_message (message_info,info_data):
    namebot = message_info.setdefault ('namebot')
    name    = info_data.setdefault ('Имя','')
    save    = info_data.setdefault ('Сохранить','')
    db,cursor = connect (namebot) 
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
    if save == 'Да' and data_message == {}:
        sql = "INSERT INTO message (name,info,data_id,status) VALUES (%s,%s,%s,%s)".format ()
        sql_save = ('Имя',name,0,'')
        cursor.execute(sql,sql_save)
        db.commit()
        lastid = cursor.lastrowid        
        sql = "UPDATE message SET data_id = {} WHERE id = {}".format(lastid,lastid)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO message (name,info,data_id,status) VALUES (%s,%s,%s,%s)".format ()
        sql_save = ('Текст',name,lastid,'')
        cursor.execute(sql,sql_save)
        db.commit()
        lastid = cursor.lastrowid
        data_message['Имя'] = name
        data_message['Текст'] = name
    return data_message    

def send_message (message_info,send_data):
    import requests
    answer  = 'Ответ'
    setting = get_setting (message_info)
    token    = setting.setdefault ('Токен','')
    if token == '':
        print ('[!!!] Нужно указать токен')
    menu_name    = ''
    message_out  = ''
    picture      = ''
    menu_list    = ''
    message_type = ''
    data_message = {}
    namebot    = message_info.setdefault ('namebot')
    message_in = message_info.setdefault ('message_in','')
    avtomat    = message_info.setdefault ('Автомат','')
    language   = message_info.setdefault ('Язык','')   
    menu_send  = message_info.setdefault ('Меню','') 
    menu_main  = message_info.setdefault ('Добавить меню','') 
    db,cursor = connect (namebot)    
    message_id   = send_data.setdefault ('message_id',0)  
    key_array    = send_data.setdefault ('Кнопки','')
    only_text    = send_data.setdefault ('Text','')
    type_text    = send_data.setdefault ('Тип','Из базы')
    method       = send_data.setdefault ('Метод','sendMessage')
    save_base    = send_data.setdefault ('Запись в базу','Записать')
    type_key     = send_data.setdefault ('Тип кнопки','Клавиатура')
    name_picture = send_data.setdefault ('Картинка','')    
    base_picture = send_data.setdefault ('Картинка база','')
    base_video   = send_data.setdefault ('Видео база','')
    name_video   = send_data.setdefault ('Видео','')
    name_docum   = send_data.setdefault ('Документ','')
    user_id      = send_data.setdefault ('user_id','')
    if user_id == '':
        user_id = message_info.setdefault('user_id','') 
    message = message_in

    ###################################################################################################### ПОЛУЧЕНИЕ ПЕРВОГО ТЕСТА #####################################################################
    if only_text != '':
        data_message['Текст'] = only_text
        id = 0
        sql = "select id,name from message where name = 'Имя' and info = '{}' ;".format(only_text)
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data:
            id,name = rec.values()     
        if id == 0:    
            if save_base != 'Не записывать':
                sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (0,only_text,'Имя')
                cursor.execute(sql)
                db.commit()
                lastid = cursor.lastrowid
                sql = "UPDATE message SET data_id = '{}' WHERE id = {}".format(lastid,lastid)
                cursor.execute(sql)
                db.commit()
                sql = "INSERT INTO message (data_id,info,name,status) VALUES ({},'{}','{}','')".format (lastid,only_text,'Текст')
                cursor.execute(sql)
                db.commit()
        message  = only_text     
        message_out = only_text
        
    ############################################################################################ Поиск сообщения в базе ########################################################################################################################
    message_in  = message_in.replace('\\','')    
    sql = 'select id,name,info from message where name = %s and info = %s ;'.format (message)
    sql_save = ('Имя',message)
    cursor.execute(sql,sql_save)
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
    ############################################################################################# [Делаем замену сообщений] ##################################################################################################
                
    message_out = data_message.setdefault('Текст'  ,'') 
    
    if language == 'en':
        message_out = data_message.setdefault('en'  ,'')
    log         = data_message.setdefault('Лог'  ,'')
    avtomat_base         = data_message.setdefault('Автомат','')     
    
    if send_data.setdefault('Замена','')  != '':
        
        #print ('[send_data]',send_data)
        
        
        for line in send_data.setdefault('Замена',''):
            print ('[line]',line)
            message_out = message_out.replace(str(line[0]),str(line[1]))                                
    if send_data.setdefault('Автомат','') == 'Да' and  data_message.setdefault('Автомат','') == 'Нет':
        message_out = ''
        
    menu_name = data_message.setdefault('Меню'  ,'')    
    
    print ('[+] menu_name:',menu_name)
    
    if menu_name != '' or key_array != '':
        menu_data = {'Имя меню':menu_name,'Кнопки':key_array,'Тип кнопки':type_key}
        markup = get_menu  (message_info,menu_data) 
        
    if menu_send != '':    
        menu_data = {'Имя меню':menu_send}
        markup = get_menu  (message_info,menu_data)
        #print ('[+] markup',markup)  
        menu_name = menu_send        
        
    if data_message.setdefault('Видео' ,'') != '':
        method = "sendVideo"
        name_video = data_message.setdefault('Видео' ,'')
        
    type_message = data_message.setdefault('Тип картинки' ,'')    
    if data_message.setdefault('Картинка' ,'') != '':
        if type_message == 'Отдельно':
            method = "sendMessage"
            name_picture = ''
        else:
            method = "sendPhoto"
            name_picture = data_message.setdefault('Картинка' ,'')

    if type_message == 'Отдельно':
        params = {}
        params['chat_id'] = user_id
        name_picture = data_message.setdefault('Картинка' ,'')
        params['parse_mode'] = 'HTML'
        try:   
            file_path = name_picture
            file_opened = open(file_path, 'rb')
        except:    
            file_path = "/home/izofen/Main/Server/picture/file_2.jpg"
            file_opened = open(file_path, 'rb')
        files = {'photo': file_opened}
        url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendPhoto') 
        resp = requests.post(url, params, files=files)
        answer = resp.json()   
        print (    '[Ответ Отправки] :',answer)    

    if method == 'sendDocument':
        message_out = '-1'
    print ('[+] message_out',message_out,avtomat,avtomat_base)

    if message_out != '' or (avtomat == 'Да' and avtomat_base == ''):
        if message_id != 0 and method == "sendMessage": 
            method = "editMessageText"       
        if method == "sendMessage":
            params = {}
            params['chat_id'] = user_id                  
            params['text'] = message_out
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup                
                print ('[markup]:',markup)                
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            print ('[]',url)
            resp = requests.post(url, params) 
            answer = resp.json()
            print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
            #print ('    [+] message_out',message_out)            
            print ( answer)
            print ('[+]👧------------------------------------------------------------ [Ответ Отправки] -------------------------------------------------------👧[+]') 
            print ('')
       
        if method == "editMessageText":        
            #print ('[+] message_out:',message_out)        
            params = {}
            params['chat_id']    = user_id
            params['text']       = str(message_out)
            params['message_id'] = message_id
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            #print ('[params]',params)               
            url  = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)
            resp = requests.post(url, params) 
            answer = resp.json()
            print ('[+]👧👧----------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧👧[+]') 
            print (    '[Ответ Отправки] :',answer)
            print ('[+]👧👧----------------------------------------------------------- [Ответ Отправки] ------------------------------------------------------👧👧[+]') 
            
            
            
        if method == 'sendDocument':
            print ('[+][+][+][+][+][+][+]')
            setting  = get_setting (message_info)
            token    = setting.setdefault ('Токен','')
            params = {}
            params['chat_id'] = user_id
            message_out = ''
            params['caption'] = str(message_out)
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            file_path = name_docum
            file_opened = open(file_path, 'rb')
            files = {'document': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)                
                        
        if method == "sendPhoto":
            if message_out == 'Пусто':
                message_out = ''
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            if base_picture != '':
                sql = "select id,name,file from files where name = '{}'".format (base_picture)
                cursor.execute(sql)
                results = cursor.fetchall()    
                id = 0
                for row in results:
                    id,name,file = row.values() 
                    file_opened = file
            else: 
                try:   
                    file_path = name_picture
                    file_opened = open(file_path, 'rb')
                except:   
                    try:
                        file_path = "/var/www/html/html/upload/TemplateIzBot/"+name_picture
                        file_opened = open(file_path, 'rb')
                    except:       
                        file_path = "/home/izofen/Main/Server/picture/file_2.jpg"
                        file_path = "c:/Main/Server/picture/file_2.jpg"
                        file_opened = open(file_path, 'rb')
                    
            print ('[+]-----------------------------------------------------[+]')        
                    
            files = {'photo': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method) 
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)    

        if method == "sendVideo":
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            file_path = name_video
            file_path = '/home/main314_bot/Main/video_2023-02-02_18-22-23.mp4'
            file_opened = open(file_path, 'rb')
            files = {'video': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)    

        if method == "editMessageCaption":
            params = {}
            params['chat_id'] = user_id
            params['caption'] = str(message_out)
            params['message_id'] = message_id
            params['parse_mode'] = 'HTML'
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup
            file_path = name_picture
            file_opened = open(file_path, 'rb')
            files = {'photo': file_opened}
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method)            
            resp = requests.post(url, params, files=files)
            answer = resp.json()   
            print (    '[Ответ Отправки] :',answer)      

        if method == "editMessageMedia":
            import json
            file_path = name_picture 
            files = {'media': open(file_path, 'rb'),}
            media = json.dumps({'type': 'photo','media': 'attach://media'})
            method = 'editMessageMedia'
            #markup = json.dumps(array)
            url    = 'https://api.telegram.org/bot{0}/{1}'.format(token, method)   #?chat_id=399838806&message_id=871&media='+str(media)+''            
            params = {'chat_id': user_id,'message_id':message_id,'media':media,'caption':'444444444444444444'}
            if menu_name != '' or key_array != '':
                params['reply_markup'] = markup    
            resp = requests.post(url, params,files = files)                
            print (resp.json())
            
    if log != '':   
        sql = "INSERT INTO message_log (answer,message_id,name,text,user_id,status) VALUES (%s,%s,%s,%s,%s,%s)".format ()
        sql_save = (str(answer),answer['result']['message_id'],log,message_out,user_id,'')
        cursor.execute(sql,sql_save)
        db.commit()    
            
    return answer

def sendDice (user_id,namebot):
    import requests
    import iz_telegram
    import json
    setting = get_setting (message_info)
    token    = setting.setdefault ('Токен','')
    method = "sendDice"
    params = {'chat_id': user_id} 
    url='https://api.telegram.org/bot{0}/{1}'.format(token, method)
    resp = requests.post(url, params)
    answer = resp.json()
    print ('[sendDice]',answer)
    return resp.json()

def user_save_data (message_info,save_data): 
    #### ИСПРАВИТЬ ID И DATA_ID   
    namebot = message_info['namebot']
    user_id = message_info['user_id']
    #print ('    [+] Запись информации в базу данных:',user_id)
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    data_id     = 0
    sql = "select id,name,info,data_id from users where name = 'user_id' and info = '{}' ;".format (user_id)
    cursor.execute(sql)
    results = cursor.fetchall()   
    for row in results:
        id_save,name,info,data_id = row.values() 
        #print ('[+] ---->',id_save,name,info,data_id)
        sql = "select id,name,info from users where data_id = {} ;".format (id_save)
        cursor.execute(sql)
        results = cursor.fetchall()  
        for row in results:
            id,name,info = row.values() 
            data_answer[name] = info
        for line in save_data:
            if data_answer.setdefault(line[0],'not in base') == 'not in base':
                #print ('    [+] Параметр:',line,' у пользователя:',user_id,' - записан новый')
                sql = "INSERT INTO users (data_id,info,name,status) VALUES ({},'{}','{}','')".format (id_save,str(line[1]),str(line[0]))
                print ('[sql]',sql)
                cursor.execute(sql)
                db.commit() 
            else: 
                #print ('    [+] Параметр:',line,' у пользователя:',user_id,' - Обновлен')      
                sql = "UPDATE users SET info = %s WHERE `name` = %s and data_id = %s "
                #print ('[sql]',sql)
                sql_save = (str(line[1]),str(line[0]),str(id_save))
                #print ('[sql_save]',sql_save)
                cursor.execute(sql,sql_save)
                db.commit()
                
def deleteMessage (message_info,message_id):
    import requests
    namebot = message_info['namebot']
    setting = get_setting (message_info)
    #token    = setting.setdefault ('Токен','')
    #user_id = message_info['user_id']
    #method = "deleteMessage"
    #params = {'chat_id': user_id,'message_id':message_id} 
    #url='https://api.telegram.org/bot{0}/{1}'.format(token, method)
    #try:
    #    resp = requests.post(url, params)
    #    answer = resp.json()
    #except:   
    #    answer = 'error' 
    #    return  answer        
    #print ('[deleteMessage]',answer)
    #return resp.json()    
    print ('[deleteMessage]')
    return 'ok'

def task_save_data (message_info,save_data):
    namebot     = message_info['namebot']
    id_task     = save_data['id_task']
    name_task   = save_data['Параметр'] 
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    data_id     = 0
    sql = "select id,name,info,data_id from task where id = {};".format (id_task)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info,data_id = row.values() 
        sql = "select id,name,info from task where data_id = '{}' ;".format (data_id)
        cursor.execute(sql)
        results = cursor.fetchall()    
        for row in results:
            id,name,info = row.values() 
            data_answer[name] = info

        for line in name_task:
            print (line)
            if data_answer.setdefault(line[0],'not in base') == 'not in base':
                sql = "INSERT INTO task (data_id,info,name,status) VALUES ({},'{}','{}','')".format (data_id,str(line[1]),str(line[0]))
                cursor.execute(sql)
                db.commit() 
            else:       
                sql = "UPDATE task SET info = '"+str(line[1])+"' WHERE `name` = '"+str(line[0])+"' "
                cursor.execute(sql)
                db.commit()    

def task_get_data (message_info,get_data):
    
    namebot = message_info['namebot']
    id_task     = get_data['id_task']
    db,cursor = connect (namebot)
    connect (namebot)
    data_answer = {}
    sql = "select id,name,info from task where data_id = '{}' ;".format (id_task)
    cursor.execute(sql)
    results = cursor.fetchall()    
    for row in results:
        id,name,info = row.values() 
        data_answer[name] = info
    return data_answer                 

