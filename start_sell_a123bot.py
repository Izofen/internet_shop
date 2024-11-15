
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

def get_sql                 (message_info,id_sql):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,sql,ask,limit,offset,back from data_sql where id = {}".format(id_sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data:
        id,sql,ask,limit,offset,back = rec.values() 
    return sql,ask,limit,offset,back  

def send_message            (user_id,message_out):
    import requests
    params = {}
    params['chat_id']    = user_id                  
    params['text']       = message_out
    params['parse_mode'] = 'HTML'
    token = '6442674165:AAFdJo3xAcxSvCknaeqmixgSsWUbO6Szk7s'
    url   = 'https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage')
    print ('[+] url',url)
    resp = requests.post(url, params) 
    answer = resp.json()
    print ('[+]👧------------------------------------------------------------ [Ответ sendMessage] -------------------------------------------------------👧[+]')
    print ( answer)
    print ('[+]👧-------------------------------------------------------------- [Ответ Отправки] --------------------------------------------------------👧[+]') 
    print ('') 
      
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
    message = get_message (message_info,"Шаблон товара")
    key     = {}
    return message,key
   
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
    pass
    
def executing_admin         (message_info,status_input,setting_bot):
    pass
    
def testing_double          (message_info,status_input,setting_bot):
    pass
    
def testing_blocking        (message_info,status_input,setting_bot):
    pass
    
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
    testing_blocking        (message_info,status_input,setting_bot)                                                                 ###  Проверка на повторно нажатые клавиши
    save_info_refer         (message_info,status_input,setting_bot)                                                                 ###  Записываем информацию по полученной реферальной ссылке 
    save_info_user          (message_info,status_input,setting_bot)                                                                 ###  Обновляем информацию по текущему пользователю 
    save_message_user       (message_info,status_input,setting_bot)                                                                 ###  Записываем входяшие сообшение для протоколирования
    executing_status        (message_info,status_input,setting_bot)                                                                 ###  Выполняем на действие статуса бота. Например ввод данных
    executing_message       (message_info,status_input,setting_bot)                                                                 ###  Выполняем код прописанный в базе данных
    executing_program       (message_info,status_input,setting_bot)                                                                 ###  Выполняем код прописанный в этом файле
    analis                  (message_info,status_input,setting_bot)                                                                 ###  Выполнение кода если нет действия на сообщения
    save_out_message        (message_info,status_input,setting_bot)                                                                 ###  Протоколирование исходящего сообщения



