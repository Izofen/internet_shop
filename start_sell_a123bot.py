

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
   
###############################################################################################################################################################    
   
def print_operator          (message_info,status_input,setting_bot,operation,nomer,date):                               ###  Печать команды оператор в json
    pass
   
def executing_operator      (message_info,status_input,setting_bot,operation,nomer,date):                               ###  Выполнение команды оператор в json
    if operation == 'message2':                                                         ###  Пример работы json команды
        pass
   
def executing_program_json  (message_info,status_input,setting_bot):                                                    ###  Разбор команды оператор в json
    import iz_bot                                                                       ###  Основные функции программы
    import json
    callback        = message_info.setdefault   ('callback','')                         ###  Имя нажатой кнопки 
    json_string     = iz_bot.change_back        (callback.replace('i_',''))
    data_json       = json.loads                (json_string)
    operation       = data_json.setdefault      ('o','')                                ###  Название команды переданной  в json
    nomer           = data_json.setdefault      ('n','')                                ###  Параметр N переданной в json    
    date            = data_json.setdefault      ('d','')                                ###  Параметр D переданной в json        
    print_operator      (message_info,status_input,setting_bot,operation,nomer,date)    ###  Печатаем команды полученные  в json
    executing_operator  (message_info,status_input,setting_bot,operation,nomer,date)    ###  Выполняем команды полученные в json
    
###############################################################################################################################################################   
   
def print_status        (message_info,status_input,setting_bot):
    pass
    
def executing_admin     (message_info,status_input,setting_bot):
    pass
    
def testing_double      (message_info,status_input,setting_bot):
    pass
    
def testing_blocking    (message_info,status_input,setting_bot):
    pass
    
def save_info_refer     (message_info,status_input,setting_bot):
    pass
    
def save_info_user      (message_info,status_input,setting_bot):
    pass
    
def save_message_user   (message_info,status_input,setting_bot):
    pass
    
def executing_status    (message_info,status_input,setting_bot):
    if status_input.setdefault('Статус','') == 'Ввод города':                           ###  Пример работы статусного сообщения
        pass
        
def executing_message   (message_info,status_input,setting_bot):
    if message_in   == 'Каталог':                                                                                        ###  Пример работы тестового сообщения 
        sql     = "select id,`info` from `order` where {} limit {} offset {}"
        limit   = 10
        offset  = 10
        back    = ''
        
def executing_program   (message_info,status_input,setting_bot):
    if callback.find ('i_') != -1:                                                      ###  Кнопка которая передала в json информацию
        executing_program_json (message_info,status_input,setting_bot)
    if callback == 'save_message':                                                      ###  Пример работы команды кнопки
        pass

def analis              (message_info,status_input,setting_bot):
    pass

def save_out_message    (message_info,status_input,setting_bot):
    pass
   
###############################################################################################################################################################
   
def start_prog (message_info):                                                                                          ###  Получение сигнала от бота. Расшифровка команды и сообщения
    status_input = iz_bot.user_get_data    (message_info,get_data)                      ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    setting_bot  = iz_bot.get_setting      (message_info)                               ###  Получение из базы информации по боту. Параметры и данные.
    status       = status_input.setdefault ('status','')                                ###  Получаем основной статус пользователя например о том что он вводит данные и какие
    print_status        (message_info,status_input,setting_bot)                         ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    executing_admin     (message_info,status_input,setting_bot)                         ###  Выполнение команды администраторов бота 
    testing_double      (message_info,status_input,setting_bot)                         ###  Проверка на повторно нажатые клавиши
    testing_blocking    (message_info,status_input,setting_bot)                         ###  Проверка на повторно нажатые клавиши
    save_info_refer     (message_info,status_input,setting_bot)                         ###  Записываем информацию по полученной реферальной ссылке 
    save_info_user      (message_info,status_input,setting_bot)                         ###  Обновляем информацию по текущему пользователю 
    save_message_user   (message_info,status_input,setting_bot)                         ###  Записываем входяшие сообшение для протоколирования
    executing_status    (message_info,status_input,setting_bot)                         ###  Выполняем на действие статуса бота. Например ввод данных
    executing_message   (message_info,status_input,setting_bot)                         ###  Выполняем код прописанный в базе данных
    executing_program   (message_info,status_input,setting_bot)                         ###  Выполняем код прописанный в этом файле
    analis              (message_info,status_input,setting_bot)                         ###  Выполнение кода если нет действия на сообщения
    save_out_message    (message_info,status_input,setting_bot)                         ###  Протоколирование исходящего сообщения



