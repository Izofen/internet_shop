


if 1==2:
    import sqlite3
    connection = sqlite3.connect('orenklip_bot.db')
    cursor = connection.cursor()
    
    if 1==2:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        info TEXT NOT NULL,
        status TEXT NOT NULL,
        data_id INTEGER
        )
        ''')
    
    connection.commit()
    connection.close()


if 1==1:
    ### Программа для тестирования телеграмм ботов
    import start_sell_a123bot

    #message_info = {}
    #message_info['namebot']     = 'orenklip_bot'
    #message_info['user_id']     = '7474072878'
    #message_info['message_in']  = '/start'
    #start_sell_a123bot.start_prog (message_info)

    #message_info = {}
    #message_info['namebot']     = 'orenklip_bot'
    #message_info['user_id']     = '7474072878'
    #message_info['callback']    = 'Ввести данные'
    #start_sell_a123bot.start_prog (message_info)
    
    message_info = {}
    message_info['namebot']     = 'orenklip_bot'
    message_info['user_id']     = '7474072878'
    message_info['message_in']    = 'Каталог'
    start_sell_a123bot.start_prog (message_info)
    
    message_info = {}
    message_info['namebot']     = 'orenklip_bot'
    message_info['user_id']     = '7474072878'
    message_info['callback']    = 'i_{#o#:#catat#,#i#:1,#s#:0}'
    start_sell_a123bot.start_prog (message_info)
    
    
    
    
    