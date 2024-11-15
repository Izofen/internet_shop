   
def send_message (user_id,message_out):
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
   
   
def start_prog (message_info):                                       ###  Получение сигнала от бота. Расшифровка команды и сообщения
    status_input = iz_bot.user_get_data    (message_info,get_data)   ###  Получение из базы информацию по пользователю. Настройки и статусы. 
    setting_bot  = iz_bot.get_setting      (message_info)            ###  Получение из базы информации по боту. Параметры и данные.
    status       = status_input.setdefault ('status','')             ###  Получаем основной статус пользователя например о том что он вводит данные и какие
    print_status        (message_info,status_input,setting_bot)      ###  Отображаем инфрмацию о настройках и статусах пользователя на экран 
    executing_admin     (message_info,status_input,setting_bot)      ###  Выполнение команды администраторов бота 
    testing_double      (message_info,status_input,setting_bot)      ###  Проверка на повторно нажатые клавиши
    testing_blocking    (message_info,status_input,setting_bot)      ###  Проверка на повторно нажатые клавиши
    save_info_refer     (message_info,status_input,setting_bot)      ###  Записываем информацию по полученной реферальной ссылке 
    save_info_user      (message_info,status_input,setting_bot)      ###  Обновляем информацию по текущему пользователю 
    save_message_user   (message_info,status_input,setting_bot)      ###  Записываем входяшие сообшение для протоколирования
    executing_message   (message_info,status_input,setting_bot)      ###  Выполняем код прописанный в базе данных
    executing_program   (message_info,status_input,setting_bot)      ###  Выполняем код прописанный в этом файле
    analis              (message_info,status_input,setting_bot)      ###  Выполнение кода если нет действия на сообщения
    save_out_message    (message_info,status_input,setting_bot)      ###  Протоколирование исходящего сообщения



