#!/usr/bin/python
# -*- coding: utf-8
############################################### ИГРА ПОКЕР ############################################################


def poker_send_message (user_id,namebot,hand2,message_id):
    import iz_telegram
    import time
    if 1==1:
        markup = ''
        message_out,menu = iz_telegram.get_message (user_id,'Сообщение 1 Ваши карты',namebot)
        message_out = message_out.replace('%%Ваши карты%%',str(hand2))  
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        time.sleep (2)
        answer = iz_telegram.bot_send (user_id,namebot,str(hand2.game_cards),markup,0)
        time.sleep (2)
        answer = iz_telegram.bot_send (user_id,namebot,str(hand2.game_name),markup,0)
        #message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Ваша ставка','S',0) 

def poker_save_game (summ):
    from hand import hand
    from player import player
    from deck import deck
    from utils import compare_games
    from card import card   
    import iz_func 
    db,cursor = iz_func.connect ()
    if 1==1:
        my_deck = deck()
        my_deck.shuffle()
        card1 = my_deck.draw(5) 
        card2 = my_deck.draw(5)
        markup = ''
        #card3 = my_deck.draw(2)
        hand1 = hand(card1)
        hand2 = hand(card2)
        me1 = player(hand1)
        me2 = player(hand2)
        table = [me1,me2]
        table = compare_games(table)
        winner = table[0]
        result = 'нет данных' 
        if winner.hand.cards == hand1.cards:
            result = 'Проиграли'
        if winner.hand.cards == hand2.cards:    
            result = 'Победа'            
        hand_save_1 = '' 
        for line in hand1.cards:
            hand_save_1 = hand_save_1 + str(line.label)+';'+str(line.suit)+';'+str(line.value)+':'
        hand_save_2 = '' 
        for line in hand2.cards:
            hand_save_2 = hand_save_2 + str(line.label)+';'+str(line.suit)+';'+str(line.value)+':'
        sql = "INSERT INTO game_poker (`hand1`,`hand2`,`winner`,summ) VALUES ('{}','{}','{}',{})".format (iz_func.change(str(hand_save_1)),iz_func.change(str(hand_save_2)),result,summ)
        cursor.execute(sql)
        db.commit()
    return hand1,hand2,winner

############################################### ИГРА ФЕРМЕР ############################################################


def get_koll_priz (message_info,game_id):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor  = iz_bot.connect (namebot)
    sql = "select id,profile,param from game_farmer where id = {} limit 1;".format (game_id)
    cursor.execute(sql)
    data  = cursor.fetchall()
    id = 0
    profile = ''
    param   = ''
    for row in data:  
        id,profile,param = row.values() 

    kl1 = 0
    kl2 = 0
    kl3 = 0
    kl4 = 0
    kl5 = 0

    nm = 0 
    for line in param:
        if line == 'Y':
            sm = profile[nm]
            if sm == '1': 
                kl1 = kl1 + 1
            if sm == '2': 
                kl2 = kl2 + 1
            if sm == '3': 
                kl3 = kl3 + 1
            if sm == '4': 
                kl4 = kl4 + 1
            if sm == '5': 
                kl5 = kl5 + 1
        nm = nm + 1
    return kl1,kl2,kl3,kl4,kl5

def set_name_key (message_info,namekey):
    import iz_bot
    info_data   = {'Имя':namekey}
    info        = iz_bot.get_message(message_info,info_data)
    return_key  = info.setdefault('Текст',info_data.setdefault('Имя',''))
    return return_key

def game_farmer (message_info,message_in,refer):                                                                                        ### НАЧАЛЬНОЕ ПРОВЕРКА ДАННЫХ
    import iz_bot
    import requests
    namebot                 = message_info.setdefault   ('namebot','')
    user_id                 = message_info.setdefault   ('user_id','') 
    message_id              = message_info.setdefault   ('message_id','') 
    db,cursor               = iz_bot.connect            (namebot)
    setting                 = iz_bot.get_setting        (message_info)
    stavka                  = int(setting.setdefault    ('Начальная ставка',100))
    token                   = setting.setdefault        ('Токен','')
    currency                = 'RUB'
    balans_user             = get_balans_user  (message_info,currency)

    if message_in == 'start':                                                                                                           ####   САМЫЙ ПЕРВЫЙ ВХОД ПО КНОПКУ ФЕРМЕР   ####        
        from telebot import TeleBot
        game_id                     = create_new_game_farmer    (message_info)
        
        game_amount,game_currency   = get_balans_farmer         (message_info,game_id)

        koll01                      = int(setting.setdefault    ('Количество первого'  ,5))
        koll02                      = int(setting.setdefault    ('Количество второго'  ,5))
        koll03                      = int(setting.setdefault    ('Количество третьего' ,5))
        koll04                      = int(setting.setdefault    ('Количество проигрышь',5))
        koll05                      = 36 - koll01 - koll02 - koll03 - koll04
        
        info_data                   =                           {'Имя':'Текст игры','Сохранить':'Да'}
        data_message                = iz_bot.get_message        (message_info,info_data)
        message_out                 = data_message.setdefault   ('Текст','Текст игры')
        message_out                 = message_out.replace       ('%%Баланс игры%%'  ,str(game_amount))        
        message_out                 = message_out.replace       ('%%Ставка  игры%%' ,str(stavka))
        message_out                 = message_out.replace       ('%%Общий баланс%%' ,str(balans_user))
        message_out                 = message_out.replace       ('##Ставка1##'      ,str(stavka))
        message_out                 = message_out.replace       ('##Ставка2##'      ,str(stavka*2))
        message_out                 = message_out.replace       ('##Ставка3##'      ,str(stavka*3))
        message_out                 = message_out.replace       ('##Колличество1##' ,str(koll01))
        message_out                 = message_out.replace       ('##Колличество2##' ,str(koll02))
        message_out                 = message_out.replace       ('##Колличество3##' ,str(koll03))
        message_out                 = message_out.replace       ('##Колличество4##' ,str(koll04))
        message_out                 = message_out.replace       ('##Колличество5##' ,str(koll05))
        
        markup                      = get_menu_game_farmer      (message_info,game_id)
        namekey                     = set_name_key              (message_info,'Начать игру кнопка')
        namekey                     = namekey.replace           ('##Ставка##',str(stavka))
        data_info                   =                           {'markup':markup,'game_id':game_id,'Имя':namekey,'name_m':'game_farmer_new_games_'}
        markup                      = menu_down                 (data_info)                
        
        bot                         = TeleBot(token)        
        bot.send_message(user_id,message_out,reply_markup = markup,parse_mode='HTML') 

    if message_in.find ("game_farmer_key_") != -1:                                                                                      ####   НАЖАТИЕ КНОПКИ УГАДАЙКИ ####
        import json
        word                        = message_in.replace('game_farmer_key_','')
        status                      = ''        
        json_string                 = iz_bot.change_back(word.replace('i_',''))
        data_json                   = json.loads(json_string)
        game_id                     = data_json.setdefault('g','')
        number_row                  = data_json.setdefault('r','')        
        number_line                 = data_json.setdefault('l','')        
        sql                         = "select id,status from game_farmer where id = {} limit 1;".format (str(game_id))
        cursor.execute(sql)
        data                        = cursor.fetchall()
        id                          = 0
        for row in data:  
            id,status = row.values() 
        if id != 0:    
            if status == 'Начало игры':
                from telebot import types
                from telebot import TeleBot
                info_data           = {'Имя':'Начало игры','Сохранить':'Да'}
                data_message        = iz_bot.get_message (message_info,info_data)
                message_out         = data_message.setdefault ('Текст','Начало игры')
                markup              = types.InlineKeyboardMarkup(row_width=1)
                name_key            = set_name_key (message_info,'Начать игру')
                name_key            = name_key.replace ('##Сумма##',str(stavka))
                data_info           = {'markup':markup,'game_id':game_id,'Имя':name_key,'name_m':'game_farmer_new_games_'}
                markup              = menu_down (data_info)                
                bot                 = TeleBot(token)
                bot.edit_message_text(chat_id=user_id,text=message_out,message_id = message_id,reply_markup = markup,parse_mode='HTML') 

            if status == 'Игра':
                answer = rename_game_farmer (message_info,int(game_id),int(number_line),int(number_row))
                markup = get_menu_game_farmer (message_info,game_id)
                if answer == 0:                    
                    game_amount,game_currency   = get_balans_farmer (message_info,game_id)
                    balans_user                 = get_balans_user  (message_info,"RUB")
                    info_data                   = {'Имя':'Забрать выигрыш сумма','Сохранить':'Да'}
                    data_message                = iz_bot.get_message (message_info,info_data)
                    message_out                 = data_message.setdefault ('Текст','Забрать выигрыш сумма')
                    message_out                 = message_out.replace ('%%Баланс игры%%',str(game_amount))
                    message_out                 = message_out.replace ('%%Ставка  игры%%',str(stavka))
                    message_out                 = message_out.replace ('%%Общий баланс%%',str(balans_user))
                    koll01 = int(setting.setdefault('Количество первого',5))
                    koll02 = int(setting.setdefault('Количество второго',5))
                    koll03 = int(setting.setdefault('Количество третьего',5))
                    koll01 = int(setting.setdefault('Количество первого',5))
                    koll02 = int(setting.setdefault('Количество второго',5))
                    koll03 = int(setting.setdefault('Количество третьего',5))
                    koll_v_1,koll_v_2,koll_v_3,koll_v_4,koll_v_5 = get_koll_priz (message_info,game_id)
                    summ_koll = ((koll01-koll_v_1) + (koll02-koll_v_2*2) + (koll03-koll_v_3)*3)*stavka                    
                    koll = koll01-koll_v_1 + koll02-koll_v_2 + koll03-koll_v_3
                    message_out = message_out.replace ('##Колличество##',str(koll))
                    message_out = message_out.replace ('##Сумма_приза##',str(summ_koll))                    
                    name_key = set_name_key (message_info,'Забрать выигрыш')
                    name_key = name_key.replace ('##Сумма##',str(game_amount))
                    data_info = {'markup':markup,'game_id':game_id,'Имя':name_key,'name_m':'game_farmer_get_price_'}
                    markup = menu_down (data_info)                

                if answer == 1:
                    info_data = {'Имя':'Начать новую игру','Сохранить':'Да'}
                    data_message = iz_bot.get_message (message_info,info_data)
                    game_amount,game_currency  = get_balans_farmer (message_info,game_id)
                    balans_user = get_balans_user  (message_info,"RUB")
                    message_out  = data_message.setdefault ('Текст','Начать новую игру')
                    message_out = message_out.replace ('%%Баланс игры%%',str(game_amount))
                    message_out = message_out.replace ('%%Ставка  игры%%',str(stavka))
                    message_out = message_out.replace ('%%Общий баланс%%',str(balans_user))



                    setting = iz_bot.get_setting (message_info)
                    stavka  = int(setting.setdefault ('Начальная ставка',100))

                    #name_key = 'Новая игра. Ставка: '+str(stavka)+ 'рублей'
                    name_key = set_name_key (message_info,'Новая игра')
                    name_key = name_key.replace ('##Сумма##',str(stavka))


                    data_info = {'markup':markup,'game_id':game_id,'Имя':name_key,'name_m':'game_farmer_get_price_'}



                    markup = menu_down (data_info)                
                setting = iz_bot.get_setting (message_info)
                token    = setting.setdefault ('Токен','')
                from telebot import TeleBot
                from telebot import types
                bot = TeleBot(token)
                bot.edit_message_text(chat_id=user_id,text=message_out, reply_markup = markup,message_id = message_id,parse_mode='HTML') 

        if message_in.find ("game_farmer_start_game_") != -1:                                                                               ####   КЛИЕН ВЫБРАЛ ИГРАТЬ  #### :  
            import json
            word  = message_in.replace('game_farmer_start_game_','')
            status = ''        
            json_string  = iz_bot.change_back(word.replace('i_',''))
            data_json = json.loads(json_string)
            game_id   = data_json.setdefault('g','')
            number_row       = data_json.setdefault('r','')        
            number_line      = data_json.setdefault('l','')   
            save_status (game_id,'Игра')

            info_data = {'Имя':'Забрать выигрыш сумма','Сохранить':'Да'}
            data_message = iz_bot.get_message (message_info,info_data)

            game_amount,game_currency  = get_balans_farmer (message_info,game_id)
            balans_user = get_balans_user  (message_info,"RUB")

            message_out  = data_message.setdefault ('Текст','Начало игры')
            message_out = message_out.replace ('%%Баланс игры%%',str(game_amount))        
            message_out = message_out.replace ('%%Ставка  игры%%',str(stavka))
            message_out = message_out.replace ('%%Общий баланс%%',str(balans_user))


            koll01 = int(setting.setdefault('Количество первого',5))
            koll02 = int(setting.setdefault('Количество второго',5))
            koll03 = int(setting.setdefault('Количество третьего',5))

            summ_koll = koll01 + koll02*2 + koll03*3
            koll      = koll01 + koll02 + koll03

            message_out = message_out.replace ('##Колличество##',str(balans_user))
            message_out = message_out.replace ('##Сумма_приза##',str(koll))



            markup = get_menu_game_farmer (message_info,game_id)

            name_key = set_name_key (message_info,'Забрать выигрыш')
            name_key = name_key.replace ('##Сумма##',str(game_amount))

            data_info = {'markup':markup,'game_id':game_id,'Имя':name_key,'name_m':'game_farmer_get_price_'}
            markup = menu_down (data_info)                

            from telebot import TeleBot
            bot = TeleBot(token)
            bot.edit_message_text(chat_id=user_id,text=message_out, reply_markup = markup,message_id = message_id,parse_mode='HTML') 

    if message_in.find ("game_farmer_return_game_") != -1:                                                                              ####   ИГРАЕНТ ПЕРВЫЙ РАЗ ####
        game_id      = create_new_game_farmer (user_id,namebot)
        balans_user  = get_balans_user  (user_id,namebot,"RUB")
        if balans_user > 0:            
            iz_telegram.add_money (namebot,user_id,-1*stavka,'Ставка игры: '+str(game_id),'Руб')
            balans_game  = get_balans_farmer (user_id,namebot,game_id)        
            balans_user  = get_balans_user  (user_id,namebot,"RUB")
            message_out,menu = get_message_global (namebot,user_id,"Текст игры")
            list_in  = ['Баланс','Баланс игры','Сумма игры','Описание игры']
            list_out = [balans_user,balans_game,stavka,'']
            message_out = iz_telegram.replace(message_out,list_in,list_out)
            markup = get_menu_game_farmer (user_id,namebot,game_id)
            menu00,delete = get_message_global (namebot,user_id,"Забрать выигрыш") 
            menu00 = menu00.replace ("%%"+str("Сумма выигрыша")+"%%",str(balans_game))
            comd00 = "game_farmer_get_price_"+str(game_id)
            markup = menu_down (menu00,comd00,markup)
            save_status (game_id,'игра')
            answer  = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
        else:    
            message_out,menu = get_message_global (namebot,user_id,"Пополнить баланс")
            markup = ''
            message_out = message_out.replace ("%%Ваш баланс%%",str(balans_user))
            message_out = message_out.replace ("%%Сумма игры%%",str(stavka))
            message_out = message_out.replace ("%%РефСсылка%%" ,str(refer))
            answer  = iz_telegram.bot_send (user_id,namebot,message_out,markup,message_id)
         
    if message_in.find ("game_farmer_new_games")   != -1:                                                                               ####   КЛИЕНТ ВЫБРАЛ ИГРАТЬ ПО КНОПКЕ ПОВТОР #### :
        from telebot import TeleBot
        from telebot import types
        import json
        word                            = message_in.replace('game_farmer_new_games_','')                             ## Получаем параметры кнопки
        json_string                     = iz_bot.change_back(word.replace('i_',''))
        data_json                       = json.loads(json_string)
        game_id                         = data_json.setdefault('g','')
        number_row                      = data_json.setdefault('r','')        
        number_line                     = data_json.setdefault('l','')        
        
        ### Баланс
        add_money                       (message_info,game_id,-1*stavka,"Ставка за игру",'RUB')
        game_amount,game_currency       = get_balans_farmer (message_info,game_id)
        balans_user = get_balans_user   (message_info,"RUB")
        
        save_status                     (message_info,game_id,'Игра')    
        
        info_data       = {'Имя':'Забрать выигрыш сумма','Сохранить':'Да'}
        data_message    = iz_bot.get_message (message_info,info_data)
        message_out     = data_message.setdefault ('Текст','Забрать выигрыш сумма')         
        
        koll01          = int(setting.setdefault     ('Количество первого'   ,5))                                       ### Определяем колличество призов
        koll02          = int(setting.setdefault     ('Количество второго'   ,5))
        koll03          = int(setting.setdefault     ('Количество третьего'  ,5))
        
        summ_koll       = (koll01 + koll02*2 + koll03*3)*stavka
        koll            = koll01 + koll02 + koll03
        
        ### Сообщение
        message_out = message_out.replace   ('%%Баланс игры%%'      ,str(game_amount))                                  ### Создаем исходящие сообщение
        message_out = message_out.replace   ('%%Ставка  игры%%'     ,str(stavka))
        message_out = message_out.replace   ('%%Общий баланс%%'     ,str(balans_user))
        message_out = message_out.replace   ('##Колличество##'      ,str(koll))
        message_out = message_out.replace   ('##Сумма_приза##'      ,str(summ_koll))
        
        markup                      = get_menu_game_farmer (message_info,game_id)
        name_key                    = set_name_key (message_info,'Забрать выигрыш')
        name_key                    = name_key.replace ('##Сумма##',str(game_amount))
        data_info                   = {'markup':markup,'game_id':game_id,'Имя':name_key,'name_m':'game_farmer_get_price_'}
        markup                      = menu_down (data_info)
        
        setting                     = iz_bot.get_setting (message_info)
        token                       = setting.setdefault ('Токен','')
        bot = TeleBot(token)
        bot.edit_message_text(chat_id=user_id,text=message_out, reply_markup = markup,message_id = message_id,parse_mode='HTML') 

    if message_in.find ("game_farmer_game_end_") != -1:
        import json
        word  = message_in.replace('game_farmer_game_end_','')
        json_string  = iz_bot.change_back(word.replace('i_',''))
        data_json = json.loads(json_string)
        game_id   = data_json.setdefault('g','')
        number_row       = data_json.setdefault('r','')        
        number_line      = data_json.setdefault('l','')  

        info_data = {'Имя':'Завершить игру текст','Сохранить':'Да'}      
        data_message   = iz_bot.get_message (message_info,info_data)
        message_out    = data_message.setdefault ('Текст','Завершить игру текст')

        from telebot import TeleBot
        bot = TeleBot(token)
        #reply_markup = markup
        bot.edit_message_text(chat_id=user_id,text=message_out,message_id = message_id,parse_mode='HTML') 
        
    if message_in.find ("game_farmer_get_price_") != -1:                                                                                ####   КЛИЕН ЗАБРАЛ ПРИЗ  ###### 
        print ('    [+] Клиент забирает приз ....')
        import json
        word  = message_in.replace('game_farmer_get_price_','')
        json_string  = iz_bot.change_back(word.replace('i_',''))
        data_json = json.loads(json_string)
        game_id   = data_json.setdefault('g','')
        number_row       = data_json.setdefault('r','')        
        number_line      = data_json.setdefault('l','')        
        amount_game,currency_game  = get_balans_farmer (message_info,game_id)
        save_status (message_info,game_id,"Конец игры")
        add_money (message_info,game_id,amount_game,"Выигрыш в игре",'RUB')
        balans_user = get_balans_user  (message_info,"RUB")
        game_id = create_new_game_farmer (message_info) 
        save_status (message_info,game_id,'Игра')   
        add_money (message_info,game_id,-1*stavka,"Ставка за игру",'RUB')
        game_amount,game_currency  = get_balans_farmer (message_info,game_id)
        info_data = {'Имя':'Текст игры','Сохранить':'Да'}

        data_message   = iz_bot.get_message (message_info,info_data)
        message_out    = data_message.setdefault ('Текст','Текст игры')

        message_out = message_out.replace ('%%Баланс игры%%',str(game_amount))        
        message_out = message_out.replace ('%%Ставка  игры%%',str(stavka))
        message_out = message_out.replace ('%%Общий баланс%%',str(balans_user))

        message_out = message_out.replace ('##Ставка1##',str(stavka))
        message_out = message_out.replace ('##Ставка2##',str(stavka*2))
        message_out = message_out.replace ('##Ставка3##',str(stavka*3))

        koll01 = int(setting.setdefault('Количество первого',5))
        koll02 = int(setting.setdefault('Количество второго',5))
        koll03 = int(setting.setdefault('Количество третьего',5))
        koll04 = int(setting.setdefault('Количество проигрышь',5))

        message_out = message_out.replace ('##Колличество1##',str(koll01))
        message_out = message_out.replace ('##Колличество2##',str(koll02))
        message_out = message_out.replace ('##Колличество3##',str(koll03))
        message_out = message_out.replace ('##Колличество4##',str(koll04))

        koll05 = 36 - koll01 - koll02 - koll03 - koll04
        message_out = message_out.replace ('##Колличество5##',str(koll05))

        markup        = get_menu_game_farmer (message_info,game_id)

        namekey       = set_name_key (message_info,'Завершить игру')
        data_info = {'markup':markup,'game_id':game_id,'Имя':namekey,'name_m':'game_farmer_game_end_'}
        markup = menu_down (data_info) 

        from telebot import TeleBot
        bot = TeleBot(token)
        bot.edit_message_text(chat_id=user_id,text=message_out, reply_markup = markup,message_id = message_id,parse_mode='HTML') 

    if message_in.find ("game_farmer_QIWI") != -1:
        message_out,menu = get_message_global (namebot,user_id,'Счет QIWI') 
        message_out = message_out.replace('%%user_id%%',str(user_id))   
        markup = ''
        answer = iz_telegram.bot_send (user_id,namebot,message_out,markup,0) 

def add_money               (message_info,game_id,summ,comment,currency):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,amount,currency from balans where user_id = {} and currency = '{}' ORDER BY id DESC limit 1".format (user_id,currency)
    cursor.execute(sql)
    results = cursor.fetchall() 
    amount    = 0
    currency  = ''
    for rec in results:
        id,amount,currency = rec.values() 
    sql = "INSERT INTO balans (`amount`,`currency`,`data_id`,`info`,`name`,`summ`,`user_id`) VALUES ( {},'{}',{},'{}','{}',{},'{}')".format(int(amount)+int(summ),currency,0,comment,'Полнение',summ,user_id)
    cursor.execute(sql)
    db.commit()  

def create_new_game_farmer  (message_info):                                                                                             ###    Создаем структуру новый игры и записываем в базу
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','')
    import iz_bot    
    db,cursor = iz_bot.connect (namebot)
    list_game,param  = create_list_game_farmer (message_info)
    sql = "INSERT INTO game_farmer (comment,game_id,profile,user_id,amount,status,summ_game,param,currency) VALUES ('{}',0,'{}','{}','{}','{}',0,'{}','RUB')".format ('',list_game,user_id,0,'Начало игры',param)
    cursor.execute(sql)
    db.commit() 
    game_id   = cursor.lastrowid ## Номер созданной игры
    db.close
    return game_id

def create_list_game_farmer (message_info):                                                                                             ###    Получаем случайную последовательность
    import random
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','')
    setting = iz_bot.get_setting (message_info)
    koll01 = int(setting.setdefault('Количество первого',5))
    koll02 = int(setting.setdefault('Количество второго',5))
    koll03 = int(setting.setdefault('Количество третьего',5))
    koll04 = int(setting.setdefault('Количество проигрышь',5))
    list_st = []
    for number in range(koll01):
        list_st.append('1')
    for number in range(koll02):
        list_st.append('2')
    for number in range(koll03):
        list_st.append('3')
    for number in range(koll04):
        list_st.append('4')
    max = 36 - koll01 - koll02 - koll03 - koll04
    for number in range(max):
        list_st.append('5')    
    #list = ['1','1','1','1','1','1','2','2','2','2','2','2','3','3','3','3','3','3','4','4','4','4','4','4','4','4','4','4','4','4','4','4','4','4','4','4']
    random.shuffle(list_st)
    new_list = ''
    for m in list_st:
        new_list = new_list + m
    param = 'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN'
    return new_list,param

def get_balans_user         (message_info,currency):                                                                                    ###    Получение баланса пользователя
    import iz_bot
    namebot     = message_info.setdefault('namebot','')
    user_id     = message_info.setdefault('user_id','')
    db,cursor   = iz_bot.connect (namebot)
    sql         = "select id,amount from balans where user_id = '{}' and currency = '{}'  ORDER BY id DESC limit 1".format (user_id,currency)
    cursor.execute(sql)
    results = cursor.fetchall() 
    amount = 0   
    for rec in results:
        id,amount = rec.values() 
    db.close 
    return amount

def get_balans_farmer       (message_info,game_id):                                                                                     ###    ТЕКУЩИЙ БАЛАНС ИГРЫ
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','')
    db,cursor = iz_bot.connect (namebot)
    sql = "select id,amount,currency from game_farmer where id = {} limit 1".format (game_id)
    cursor.execute(sql)
    results = cursor.fetchall() 
    amount    = 0
    currency  = ''
    for rec in results:
        id,amount,currency = rec.values() 
    return amount,currency

def get_menu_game_farmer    (message_info,game_id):                                                                                     ###    МЕНЮ НЕОБХОДИМОЕ ДЛЯ ИГРЫ
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    db,cursor = iz_bot.connect (namebot)
    from telebot import types
    markup = types.InlineKeyboardMarkup(row_width=6)
    setting_bot  = iz_bot.get_setting (message_info)
    clear_key   = setting_bot.setdefault('Начальная кнопка','0')
    interes_key = setting_bot.setdefault('Кнопка под вопросом','?')
    param = ''
    value = ''
    sql = "select id,param,profile,status from game_farmer where id = "+str(game_id)+" limit 1;"
    cursor.execute(sql)
    data  = cursor.fetchall()
    for row in data:  
        id,param,profile,status = row.values() 
    print ('[+] Параметры игры',game_id)   
    print ('[+] Показы:  ',param)
    print ('[+] Значение:',profile)
    fruit01 = setting_bot.setdefault('Фрукт 1','1') 
    fruit02 = setting_bot.setdefault('Фрукт 2','2') 
    fruit03 = setting_bot.setdefault('Фрукт 3','3') 
    Loss    = setting_bot.setdefault('Проигрыш','4')
    fruit05 = setting_bot.setdefault('Отображение кнопки отсутвия данных','7')
    fruit = 'Нет'
    print ('[status]',status)
    if status == 'Конец игры':
         param = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    if status == 'Выигрыш':
         param = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    for number_line in range(6):
        for number_row in range(6):
            namekey = int(number_line)*6+int(number_row)
            value = param   [namekey:namekey+1]
            fr = profile [namekey:namekey+1]
            if fr == '1':
                fruit = fruit01
            if fr == '2':
                fruit = fruit02
            if fr == '3':
                fruit = fruit03
            if fr == '4':
                fruit = Loss
            if fr == '5':
                fruit = fruit05                
            if value == 'N':
                if number_row == 0:
                    if status == 'Начало игры':
                        menu10 = clear_key
                    if status == 'Игра':
                        menu10 = interes_key    
                    comd10 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn10 = types.InlineKeyboardButton(text=menu10,callback_data=comd10)
                if number_row == 1:
                    if status == 'Начало игры':
                        menu11 = clear_key
                    if status == 'Игра':
                        menu11 = interes_key                        
                    comd11 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn11 = types.InlineKeyboardButton(text=menu11,callback_data=comd11)                    
                if number_row == 2:
                    if status == 'Начало игры':
                        menu12 = clear_key
                    if status == 'Игра':
                        menu12 = interes_key                        
                    comd12 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn12 = types.InlineKeyboardButton(text=menu12,callback_data=comd12)                    
                if number_row == 3:
                    if status == 'Начало игры':
                        menu13 = clear_key
                    if status == 'Игра':
                        menu13 = interes_key                        
                    comd13 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn13 = types.InlineKeyboardButton(text=menu13,callback_data=comd13) 
                if number_row == 4:
                    if status == 'Начало игры':
                        menu14 = clear_key
                    if status == 'Игра':
                        menu14 = interes_key                        
                    comd14 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn14 = types.InlineKeyboardButton(text=menu14,callback_data=comd14) 
                if number_row == 5:
                    if status == 'Начало игры':
                        menu15 = clear_key
                    if status == 'Игра':
                        menu15 = interes_key                        
                    comd15 = "game_farmer_key_"+str(iz_bot.build_jsom({'g':game_id,'l':number_line,'r':number_row}))
                    mn15 = types.InlineKeyboardButton(text=menu15,callback_data=comd15)
                    markup.add(mn10,mn11,mn12,mn13,mn14,mn15)
            if value == 'Y':
                if number_row == 0:
                    namekey = str(number_line)+'_'+str(number_row)
                    menu10 = fruit
                    comd10 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn10 = types.InlineKeyboardButton(text=menu10,callback_data=comd10)
                if number_row == 1:
                    menu11 = fruit
                    comd11 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn11 = types.InlineKeyboardButton(text=menu11,callback_data=comd11)
                if number_row == 2:
                    menu12 = fruit
                    comd12 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn12 = types.InlineKeyboardButton(text=menu12,callback_data=comd12)
                if number_row == 3:
                    menu13 = fruit
                    comd13 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn13 = types.InlineKeyboardButton(text=menu13,callback_data=comd13)
                if number_row == 4:
                    menu14 = fruit
                    comd14 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn14 = types.InlineKeyboardButton(text=menu14,callback_data=comd14)
                if number_row == 5:
                    menu15 = fruit
                    comd15 = "game_farmer_not_key_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
                    mn15 = types.InlineKeyboardButton(text=menu15,callback_data=comd15)
                    markup.add(mn10,mn11,mn12,mn13,mn14,mn15)                
    db.close              
    return markup

def rename_game_farmer      (message_info,game_id,number_line,number_row):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    user_id    = message_info.setdefault('user_id','') 
    db,cursor = iz_bot.connect (namebot)
    setting = iz_bot.get_setting (message_info)
    stavka  = int(setting.setdefault ('Начальная ставка',100))
    namekey = int(number_line)*6+int(number_row)
    param = ''
    value = ''
    sql = "select id,param,profile from game_farmer where id = "+str(game_id)+" limit 1;"
    id = 0
    cursor.execute(sql)
    data  = cursor.fetchall()
    for row in data:  
        id,param,profile = row.values() 
    if id != 0:    
        namekey = int(number_line)*6+int(number_row)    
        param = param[0:namekey]+'Y'+param[namekey+1:]
    else:
        print ('[+] игра не найдена')
    sql = "UPDATE game_farmer SET param = '"+param+"' WHERE id = '"+str(game_id)+"'"
    cursor.execute(sql)
    db.commit()    
    print ('    [+] param',param[namekey])
    print ('    [+] profile',profile[namekey])
    print ('    [+] namekey',namekey)
    if profile[namekey] == "1":
        add_money_game_farmer (message_info,stavka,game_id)
        return 0
    if profile[namekey] == "2":
        add_money_game_farmer (message_info,stavka*2,game_id)
        return 0
    if profile[namekey] == "3":
        add_money_game_farmer (message_info,stavka*3,game_id)
        return 0
    if profile[namekey] == "4":
        sql = "UPDATE game_farmer SET amount = 0 WHERE id = "+str(game_id)+""
        cursor.execute(sql)
        db.commit()    
        save_status (message_info,game_id,'Конец игры')
        return 1
    if profile[namekey] == "5":
        add_money_game_farmer (message_info,0,game_id)
        return 0
    db.close    
    
def save_status             (message_info,game_id,status):
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "UPDATE game_farmer SET status = '"+str(status)+"' WHERE id = "+str(game_id)+""
    cursor.execute(sql)
    db.commit()

def see_menu                (game_id,number,namebot,user_id):
    from telebot import types
    clear_key = load_setting_global (namebot,user_id,"Отображение кнопки отсутвия данных")
    ask_key   = load_setting_global (namebot,user_id,"Начальная кнопка")
    markup = types.InlineKeyboardMarkup(row_width=6)
    for number_line in range(6):
        if number_line > number:
            press_key = clear_key
        else:    
            press_key = ask_key
        number_row = 0
        namekey = str(number_line)+'_'+str(number_row)
        menu10 = press_key
        comd10 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn10 = types.InlineKeyboardButton(text=menu10,callback_data=comd10)
        number_row = 1
        namekey = str(number_line)+'_'+str(number_row)
        menu11 = press_key
        comd11 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn11 = types.InlineKeyboardButton(text=menu11,callback_data=comd11)
        number_row = 2
        namekey = str(number_line)+'_'+str(number_row)
        menu12 = press_key
        comd12 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn12 = types.InlineKeyboardButton(text=menu12,callback_data=comd12)
        number_row = 3
        namekey = str(number_line)+'_'+str(number_row)
        menu13 = press_key
        comd13 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn13 = types.InlineKeyboardButton(text=menu13,callback_data=comd13)
        number_row = 4
        namekey = str(number_line)+'_'+str(number_row)
        menu14 = press_key
        comd14 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn14 = types.InlineKeyboardButton(text=menu14,callback_data=comd14)
        number_row = 5
        namekey = str(number_line)+'_'+str(number_row)
        menu15 = press_key
        comd15 = "game_farmer_pause_"+str(game_id)+"__"+str(number_line)+"**"+str(number_row)
        mn15 = types.InlineKeyboardButton(text=menu15,callback_data=comd15)
        markup.add(mn10,mn11,mn12,mn13,mn14,mn15)                
    return markup

def create_game_farmer      (user_id,namebot,game_id,numer,list):                                                                       ### ЗАПОЛНЕНИЕ ИГРЫ НОВЫМИ ДАННЫМИ
    import iz_func
    db,cursor = iz_func.connect ()
    nm = 0
    for number_line in range(6):
        for number_row in range(6):
            namekey = str(number_line)+'_'+str(number_row)
            liter   = list [nm]
            nm      = nm + 1
            #print ('[+] nm',number_line,numer)
            if numer == number_line:
                sql = "INSERT INTO bot_game (comment,game_id,namebot,profile,user_id,value) VALUES ('{}',{},'{}','{}','{}','{}')".format (liter,game_id,namebot,namekey,user_id,"0")
                cursor.execute(sql)
                db.commit()  

def add_money_game_farmer   (message_info,summ,game_id):                                                                                ### РАСЧЕТЫ ВНУТРИ ИГРЫ
    import iz_bot
    namebot    = message_info.setdefault('namebot','')
    db,cursor = iz_bot.connect (namebot)
    sql = "UPDATE game_farmer SET amount = amount + {} WHERE id = {} ".format(summ,game_id)
    cursor.execute(sql)
    db.commit()

def load_setting_global     (namebot,user_id,namekey):                                                                                  ### Настройки для программ в других ботах 
    import iz_telegram
    key = ''
    key = iz_telegram.load_variable (user_id,namebot,namekey)
    if key == '':
        key = iz_telegram.load_setting (namebot,namekey)
    if key == '':
        key = iz_telegram.load_setting ('@Help_client_bot',namekey)
    return key    

def get_message_global      (namebot,user_id,message):                                                                                  ### Сообщения в других бота 
    import iz_telegram
    message_out,menu = iz_telegram.get_message (user_id,message,namebot) 
    if message_out == '' or message_out == message:
        message_out,menu = iz_telegram.get_message (user_id,message,'@Help_client_bot')     
    return message_out,menu    

def menu_down               (data_info):
    import iz_bot
    #data_info = {'markup':markup,'game_id':game_id,'Имя':'Название кнопки','name_m':name_m}
    markup    = data_info.setdefault ('markup')
    name_m    = data_info.setdefault ('name_m')
    game_id   = data_info.setdefault ('game_id') 
    nomer_row   = data_info.setdefault ('nomer_row',0) 
    nomer_line  = data_info.setdefault ('nomer_line',0) 
    menu_name   = data_info.setdefault ('Имя','Нет названия') 
    
    
    ## game_farmer_get_price_
    from telebot import types
    comd  = name_m+str(iz_bot.build_jsom({'g':game_id,'l':nomer_line,'r':nomer_row}))
    mn   = types.InlineKeyboardButton(text=menu_name,callback_data=comd)
    markup.add(mn)     
    return markup 

def start_full_menu (user_id,namebot,game_id,answer_move,menu00,comd00,message_out):
    import iz_telegram
    if 1==1:
        pass

###############################  МАФИЯ   ####################################

def create_mafiya (namebot,user_id):
    import iz_func
    import json
    name = iz_func.load_variable (user_id,"Имя игрока",namebot)
    db,cursor = iz_func.connect ()
    sql = "INSERT INTO game_mafiya (name,status,gamer06,gamer07,gamer08,gamer09,gamer10,gamer11) VALUES ('Мафия','Добавление игроков','','','','','','')".format ()
    cursor.execute(sql)
    db.commit()
    id_game = cursor.lastrowid
    return id_game                                                                    ### Создаем игру

def koll_user_in_game (namebot,id_game):
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id,life,loser,`kill`,add_golos,list_golos FROM `game_mafiya_user` where id_game = "+str(id_game)+" ORDER BY list"
    cursor.execute(sql)
    data = cursor.fetchall()
    NM   = 0
    name_user = []
    for rec in data: 
        NM = NM + 1 
        id,id_game,name,roles,status,user_id,life,loser,kill,add_golos,list_golos = rec   
        name_user.append([name,user_id,roles,status,life,loser,kill,add_golos,list_golos])
    return NM,name_user  

def save_new_user_id (user_id,namebot,id_game):                       #### Записываем user_id
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+" and user_id = '"+str(user_id)+"' "
    cursor.execute(sql)
    data = cursor.fetchall()
    lim = 0
    for rec in data: 
        lim = lim + 1
    if lim == 0:
        sql = "INSERT INTO game_mafiya_user (`id_game`,`name`,`roles`,`status`,`user_id`) VALUES ({},'','','','{}')".format (id_game,user_id)
        cursor.execute(sql)
        db.commit()
    else:
        pass
    return lim

def save_name_game_in_user_id (user_id,namebot,id_game,message_in):   #### !!!!! 
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,name,roles,status,user_id_m = rec
        if str(user_id_m) == str(user_id):
            sql = "UPDATE `game_mafiya_user` SET name = '"+str(message_in)+"' WHERE `id` = "+str(id)+""
            cursor.execute(sql)
            db.commit()     	
            iz_func.save_variable (user_id_m,"status","",namebot) 

def test_start_game (namebot,id_game):
    import iz_func
    db,cursor   = iz_func.connect ()
    stop_game = 'No'
    sql = "SELECT id,stop_game FROM `game_mafiya` where id = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
    	id,stop_game = rec
    return stop_game

def send_message_mafiya (message_out,namebot,id_game):
    print ('    [+] Груповая рассылка [+]')
    print ('        [+] Текст сообщения:',message_out)
    import iz_func
    db,cursor   = iz_func.connect ()
    #stop_game = 'No'
    #sql = "SELECT id,stop_game FROM `game_mafiya` where id = "+str(id_game)+""
    #cursor.execute(sql)
    #data = cursor.fetchall()
    #for rec in data: 
    	#id,stop_game = rec
    stop_game = test_start_game (namebot,id_game)

    if stop_game == '':
        sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,id_game,name,roles,status,user_id = rec
            id_game_k = iz_func.load_variable (user_id,"Номер игры",namebot)
            if user_id != '' and str(id_game_k) == str(id_game):
                message_send = iz_func.send_message (user_id,message_out,'S',namebot)   
                if name == '':
                    message_send = iz_func.send_message (user_id,"Введите имя для возможности вести переписку",'S',namebot)   

def send_picture_mafiya (namefile,namebot,id_game):
    print ('    [+] Груповая рассылка [+]')
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,id_game,name,roles,status,user_id = rec
        id_game_k = iz_func.load_variable (user_id,"Номер игры",namebot)
        if user_id != '' and str(id_game_k) == str(id_game):
            import telebot
            token    = iz_func.get_token (namebot)
            bot      = telebot.TeleBot(token)    
            photo = open(namefile, 'rb')
            try:           
               bot.send_sticker(user_id, photo) 
               #bot.send_photo(user_id, photo) 
            except:  
                pass   

def save_variable_mafiya (id_game,name_val,znak,namebot):
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,id_game,name,roles,status,user_id = rec
        if user_id != '':
        	iz_func.save_variable (user_id,name_val,znak,namebot)

def send_role (role_list,id_game):                                                  # Пресваеваем роли игрокам
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    NM = 0
    for rec in data: 
        id,id_game,name,roles,status,user_id = rec
        if user_id != '':
            sql = "UPDATE game_mafiya_user SET roles = '"+role_list[NM]+"' WHERE `id` = '"+str(id)+"'"
            cursor.execute(sql)
            db.commit()  
            NM = NM + 1

def status_game (status,id_game):
    import iz_func
    db,cursor = iz_func.connect ()
    sql = "UPDATE game_mafiya SET status = '"+str(status)+"' WHERE `id` = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()

def send_message_mafiya_only_blok (message_out,id_game,user_id,namebot):
    print ('    [+] Груповая рассылка [+]')
    print ('        [+] Текст сообщения:',message_out)
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,id_game,name,roles,status,user_id FROM `game_mafiya_user` where id_game = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,id_game,name,roles,status,user_id = rec
        if user_id != '' and (roles == 'Мафия' or roles == 'Дон'):
            message_send = iz_func.send_message (user_id,message_out,'S',namebot)    	

def kill_mafiya (user_id,namebot,id_game):
    import iz_game
    import iz_func
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game)
    import telebot
    import time        
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    nomer = 0
    for line in name_user:
    	print ('[+] список на убийство гражданскими мафию: ',line,' 5:',line[5])
    	if line[5] == "Да" and line[4] == '':
            nomer = nomer + 1
            tx1    = str(nomer)+" "+str(line[0])
            cl1    = "pushe_"+str(line[1])
            mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 

    if line[3] != 'Убил мафию':
        NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)        
        for line in name_user_list:
            if line[4] == '':
                user_id_send = str(line[1]) 
                db,cursor = iz_func.connect ()
                sql = "UPDATE game_mafiya_user SET status = 'Убил мафию' WHERE `user_id` = "+str(user_id_send)+" and id_game = '"+str(id_game)+"' "
                cursor.execute(sql)
                db.commit()
                message_out = 'Голосование на решение голоса'
                token    = iz_func.get_token (namebot)
                bot      = telebot.TeleBot(token)    
                answer = bot.send_message(user_id_send,message_out,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup

def find_mafiya (user_id,namebot,id_game):
    import iz_game
    import iz_func
    import time    
    import telebot
    ### Формируем список для убийства ###

    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    for line in name_user_list:
    	if line[3] != 'Выбрал мафию' and line[4] == '':
            user_id_send = str(line[1])
            db,cursor = iz_func.connect ()
            sql = "UPDATE game_mafiya_user SET status = 'Выбрал мафию' WHERE `user_id` = "+str(user_id_send)+" and id_game = '"+str(id_game)+"' "
            cursor.execute(sql)
            db.commit()
            set_message_all (user_id,namebot,id_game,str(user_id_send)) 
            tm = iz_func.chislo(iz_func.load_setting ('Время ожидания',namebot),60)                
            iz_game.save_variable_mafiya (id_game,'Имя игрока',str(line[0]),namebot)
            answer   = iz_game.send_message_mafiya ('Сейчас говорит 1 игрок',namebot,id_game)
            message_out1 = "Ждем Ваше сообшение"
            token    = iz_func.get_token (namebot)
            bot      = telebot.TeleBot(token)    
            markup   = telebot.types.InlineKeyboardMarkup(row_width=4)
            tx1      = str("Прервать ожидание")
            name_key = "stop_"+str('g2_')+str(id_game)
            cl1      = name_key
            mn1      = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1)          
            answer = bot.send_message(user_id_send,message_out1,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
            message_id  = answer.message_id 
            time_start   = time.time ()
            time_finishe = time.time ()
            iz_func.save_variable (user_id_send,name_key,'Ждем',namebot)  
            exit_label = 'Работаем'
            while exit_label == 'Работаем':                
                time_finishe = time.time () 
                pt = tm - int(time_finishe - time_start)
                message_out2  = message_out1 + '\n'+'Осталось '+str(pt)+ ' сек.'
                bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML',reply_markup=markup)
                time.sleep (1) 
                if time_finishe - time_start > tm:
                    exit_label = 'Выходим'
                exit_key   = iz_func.load_variable (user_id_send,name_key,namebot)
                if exit_key != 'Ждем':
                    exit_label = 'Выходим'
                message_out2 = 'Закрыта задача'
                if exit_label == 'Выходим':
                    bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML')






            NM1,name_user1 = iz_game.koll_user_in_game (namebot,id_game)
            markup_list    = telebot.types.InlineKeyboardMarkup(row_width=4)
            nomer1 = 0
            for line1 in name_user1:    	
    	        if line1[4] == '' and str(line1[1]) != str(line[1]) and line1[5] != 'Да':
                    nomer1 = nomer1 + 1
                    tx1    = str(nomer1)+" "+str(line1[0])
                    cl1    = "kill_"+str(line1[1])
                    mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
                    markup_list.add(mn1)  






            nomer1 = nomer1 + 1
            tx1    = str(nomer1)+" "+str('Пропустить')
            cl1    = "kill_"+str('000000000')
            mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup_list.add(mn1)  




            message_out = 'Кто у нас мафия?'
            token    = iz_func.get_token (namebot)
            bot      = telebot.TeleBot(token)    
            answer = bot.send_message(user_id_send,message_out,reply_markup=markup_list,parse_mode='HTML')
            exit (0)
      
def start_game (user_id,namebot,id_game):
    import iz_game
    import iz_func
    import random
    db,cursor = iz_func.connect ()        
    sql = "UPDATE game_mafiya_user SET `loser` = '' WHERE id_game = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()        
    sql = "UPDATE game_mafiya_user SET `kill` = '' WHERE id_game = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()        
    sql = "UPDATE game_mafiya SET `kill_mafiya` = '' WHERE id = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()        
    sql = "UPDATE game_mafiya SET `message` = '' WHERE id = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()        
    sql = "UPDATE game_mafiya SET `select_mafiya` = '' WHERE id = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit() 
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    list = []
    l_nomer = 0
    for line in name_user_list:
        l_nomer = l_nomer + 1
        list.append(l_nomer)
    random.shuffle(list) 
    k_nomer = 0
    db,cursor = iz_func.connect ()        
    sql = "SELECT id,list FROM game_mafiya_user where id_game = "+str(id_game)+""    
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id_l,list_l = rec
        sql = "UPDATE game_mafiya_user SET list = '"+str(list[k_nomer])+"' WHERE id = "+str(id_l)+""
        cursor.execute(sql)
        db.commit()
        k_nomer = k_nomer + 1
    game02 (user_id,namebot,id_game)                ### Список ролей
    game03 (user_id,namebot,id_game)

def get_roly (user_id,namebot,id_game):             ### Распределяем роли ы случайном порядке 
    import random
    import iz_func
    import iz_game
    rl01 = 'Мирный житель'
    rl02 = 'Мафия'
    rl03 = 'Дон'
    rl04 = 'Комисар'
    rl05 = 'Доктор'
    id_game = iz_func.load_variable (user_id,"Номер игры",namebot) 
    db,cursor   = iz_func.connect () 
    gamer06 = ''
    gamer07 = ''
    gamer08 = ''
    gamer09 = ''
    gamer10 = ''
    gamer11 = ''
    sql = "SELECT id,gamer06,gamer07,gamer08,gamer09,gamer10,gamer11 FROM game_mafiya where id = "+str(id_game)+""  
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,gamer06,gamer07,gamer08,gamer09,gamer10,gamer11 = rec
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game) 
    NM   = 0
    list = []
    for line in name_user:
        NM = NM + 1            
        if NM == 1:
            list.append(rl01)
        if NM == 2:
            list.append(rl02)
        if NM == 3:
            list.append(rl03)
        if NM == 4:
            list.append(rl04)
        if NM == 5:
            list.append(rl05)
        if NM == 6:
            if gamer06 != '':
               list.append(gamer06)
            else:
               list.append(rl01)   
        if NM == 7:
            if gamer07 != '':
               list.append(gamer07)
            else:
               list.append(rl01)   
        if NM == 8:
            if gamer08 != '':
               list.append(gamer08)
            else:
               list.append(rl01)   
        if NM == 9:
            if gamer09 != '':
               list.append(gamer09)
            else:
               list.append(rl01)   
        if NM == 10:
            if gamer10 != '':
               list.append(gamer10)
            else:
               list.append(rl01)   
        if NM == 11:
            if gamer11 != '':
               list.append(gamer11)
            else:
               list.append(rl01)   
        if NM > 11:       
        	list.append(rl01)


    random.shuffle(list) 

    
    return list   

def get_user_in_user_id (user_id,namebot,id_game):
    import iz_func
    import iz_game
    answer = ['','']
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    for line in name_user_list:
    	if line[1] == str(user_id):
    		answer = line
    return answer

def timer_key_tip_1 (line,namebot,id_game):
    import telebot    
    import time        
    import iz_func

    token        = iz_func.get_token (namebot)
    bot          = telebot.TeleBot(token)
    user_id_send = str(line[1])
    name_send    = str(line[0])
    tm           = iz_func.chislo(iz_func.load_setting ('Время ожидания',namebot),60)    
    message_out1 = "Ждем Ваше сообшение"
    
    markup   = telebot.types.InlineKeyboardMarkup(row_width=4)
    tx1      = str("Прервать ожидание")
    name_key = "stop_"+str('g1_')+str(id_game)
    cl1      = name_key
    mn1      = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
    markup.add(mn1)          

    answer = bot.send_message(user_id_send,message_out1,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
    message_id  = answer.message_id 
    time_start   = time.time ()
    time_finishe = time.time ()
    iz_func.save_variable (user_id_send,name_key,'Ждем',namebot)  
    exit_label = 'Работаем'

    while exit_label == 'Работаем':                
        time_finishe = time.time () 
        pt = tm - int(time_finishe - time_start)
        message_out2  = message_out1 + '\n'+'Осталось '+str(pt)+ ' сек.'
        bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML',reply_markup=markup)
        time.sleep (1) 
        if time_finishe - time_start > tm:
            exit_label = 'Выходим'
        exit_key   = iz_func.load_variable (user_id_send,name_key,namebot)
        if exit_key != 'Ждем':
            exit_label = 'Выходим'
        message_out2 = 'Закрыта задача'
        if exit_label == 'Выходим':
            bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML')

def set_message_all (user_id,namebot,id_game,message_set):
    import iz_func
    import iz_game
    db,cursor = iz_func.connect ()        
    #sql = "SELECT id,message FROM game_mafiya where id = "+str(id_game)+""
    sql = "UPDATE game_mafiya SET message = '"+str(message_set)+"' WHERE `id` = '"+str(id_game)+"'"
    cursor.execute(sql)
    db.commit()

def game01 (user_id,namebot,id_game): 
    import iz_func
    import iz_game
    id_game = iz_func.load_variable (user_id,"Номер игры",namebot) 
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game)    
    role_list    = iz_game.get_roly (user_id,namebot,id_game)
    list_roly = ''
    for line in role_list:
        list_roly = list_roly + line + '\n'
    iz_game.save_variable_mafiya (id_game,"Список ролей",list_roly,namebot)      
    iz_game.send_message_mafiya ('Роли:',namebot,id_game)

def game02 (user_id,namebot,id_game):               ### Рассылка №01 рассылка ролей.
    import iz_func
    import iz_game	
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    list_gamer = ""
    nomer      = 0
    for line in name_user_list:
        nomer = nomer + 1
        life_user = line[4]
        if life_user == '':
        	life_user = 'Живой'
        list_gamer  = list_gamer + str(nomer) + '. '+line[0] + ' - ' + life_user + '\n'
    iz_game.save_variable_mafiya (id_game,"Список участников",list_gamer,namebot)      
    set_message_all (user_id,namebot,id_game,"Запретить")  
    answer = iz_game.send_message_mafiya ('Список участников с их номерами',namebot,id_game)

def game03 (user_id,namebot,id_game):
    import iz_func
    import iz_game		
    ####           РАЗДАЧА РОЛЕЙ            ####
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    for line in name_user_list:
        namefile = ''
        if str(line[2]) == 'Мирный житель':
            namefile = 'm11.webp'
        if str(line[2]) == 'Мафия':
            namefile = 'm12.webp'
        if str(line[2]) == 'Дон':
            namefile = 'm15.webp'
        if str(line[2]) == 'Доктор':
            namefile = 'm14.webp'
        if str(line[2]) == 'Комисар':
            namefile = 'm13.webp'
        if namefile != '':
            #answer = iz_game.send_picture_mafiya (namefile,namebot,id_game)
            import telebot
            token    = iz_func.get_token (namebot)
            bot      = telebot.TeleBot(token)    
            photo = open(namefile, 'rb')                    
            bot.send_sticker(line[1], photo) 
            iz_func.save_variable (line[1],'Ваша роль',str(line[2]),namebot)  
            message_send = iz_func.send_message (line[1],'В этой игре вы - ','S',namebot)    
    answer = iz_game.send_message_mafiya ('Чтобы посмотреть описание своей роли введите команду:',namebot,id_game)
    game70 (user_id,namebot,id_game)

def game70 (user_id,namebot,id_game):
    import iz_func
    import iz_game		
    answer = iz_game.send_picture_mafiya ('m03.webp',namebot,id_game)
    answer = iz_game.send_message_mafiya ('Наступает первая ночь',namebot,id_game)
    ####        СООБЩЕНИЕ ДЛЯ МАФИИ       ####
    ####       Формируем спиок мафии      ####
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    list_mafiya = ""
    nomer = 0
    for line in name_user_list:
        print ('[+] line[2]',line[2])
        if line[2] == 'Мафия':
            nomer = nomer + 1
            list_mafiya = list_mafiya + str(nomer) + '. '+line[0]+'\n'                  
    iz_game.save_variable_mafiya (id_game,'Послание для мафии',list_mafiya,namebot)
    answer = iz_game.send_message_mafiya_only_blok ("Послание для мафии",id_game,user_id,namebot)
    import time
    time.sleep (4)
    # Рассылка №02 Кто у нас мафия
    answer = iz_game.send_message_mafiya ('Мафия познакомилась и засыпает',namebot,id_game)
    answer = iz_game.send_picture_mafiya ('m02.webp',namebot,id_game)
    answer = iz_game.send_message_mafiya ('Город просыпается',namebot,id_game)
    answer = iz_game.send_message_mafiya ('Этой ночью в нашем городе появилась мафия.',namebot,id_game)        
    game55 (user_id,namebot,id_game)

def game55 (user_id,namebot,id_game):
    import iz_func
    import iz_game		
    answer = iz_game.send_message_mafiya ('Каждый может высказаться перед началом игры',namebot,id_game)
    #### ПЕРВОЕ МИНУТНОЕ ОБСУЖДЕНИЕ  ####
    # Рассылка №03 Разговор по душам
    ### ВЕРНУТЬ КАК БЫЛО
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    for line in name_user_list:
        stop_game = test_start_game (namebot,id_game)
        if stop_game == '': 
            iz_game.save_variable_mafiya (id_game,'Имя игрока',str(line[0]),namebot)
            answer   = iz_game.send_message_mafiya ('Сейчас говорит 1 игрок',namebot,id_game)
            set_message_all (user_id,namebot,id_game,str(line[1]))  
            timer_key_tip_1 (line,namebot,id_game)
    set_message_all (user_id,namebot,id_game,str("Нет данных"))  
    answer = iz_game.send_message_mafiya ('Время дневного обсуждения окончено',namebot,id_game)
    game71 (user_id,namebot,id_game)

def game71 (user_id,namebot,id_game):
    import iz_func
    import iz_game			
    answer = iz_game.send_picture_mafiya ('m03.webp',namebot,id_game) 	
    answer = iz_game.send_message_mafiya ('Город засыпает! Просыпается мафия',namebot,id_game)
    #### ВТОРОЕ СООБЩЕНИЕ ДЛЯ МАФИИ ####
    import telebot
    import time        
    token    = iz_func.get_token (namebot)
    bot      = telebot.TeleBot(token)    
    ####  Сбор данных для голосования мафии  ####  
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game) 
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    nomer = 0
    for line in name_user:
        print ('[+] Список для мафии:',line,' 4:',line[4])
        if line[4] == '':
            nomer = nomer + 1
            tx1    = str(nomer)+" "+str(line[0])
            cl1    = "mafiya_"+str(line[1])
            mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1)
    #### Рассылка мафии ####  
    set_message_all (user_id,namebot,id_game,"Мафия")
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)        
    for line in name_user_list:
        stop_game = test_start_game (namebot,id_game)
        if line[2] == 'Мафия' and stop_game == '':
            user_id_send = str(line[1]) 
            message_out = 'Мафия ищет жертву'
            answer = bot.send_message(user_id_send,message_out,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
    
def game10 (user_id,namebot,id_game):               #### Оправдательные речи закончены
    import iz_func
    import iz_game		

    if 1==1:
        #### Третие 1 минутное обсуждение
        NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
        import telebot
        import time        
        for line in name_user_list:
            if line[5] == 'Да':
                user_id_send = str(line[1])
                set_message_all (user_id,namebot,id_game,str(user_id_send)) 
                tm = iz_func.chislo(iz_func.load_setting ('Время ожидания',namebot),60)    
                iz_game.save_variable_mafiya (id_game,'Имя игрока',str(line[0]),namebot)
                answer   = iz_game.send_message_mafiya ('Сейчас говорит 1 игрок',namebot,id_game)
                message_out1 = "Ждем Ваше сообшение"
                token    = iz_func.get_token (namebot)
                bot      = telebot.TeleBot(token)    
                markup   = telebot.types.InlineKeyboardMarkup(row_width=4)
                tx1      = str("Прервать ожидание")
                name_key = "stop_"+str('g1_')+str(id_game)
                cl1      = name_key
                mn1      = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
                markup.add(mn1)          
                answer = bot.send_message(user_id_send,message_out1,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
                message_id  = answer.message_id 
                time_start   = time.time ()
                time_finishe = time.time ()
                iz_func.save_variable (user_id_send,name_key,'Ждем',namebot)  
                exit_label = 'Работаем'
                while exit_label == 'Работаем':                
                    time_finishe = time.time () 
                    pt = tm - int(time_finishe - time_start)
                    message_out2  = message_out1 + '\n'+'Осталось '+str(pt)+ ' сек.'
                    bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML',reply_markup=markup)
                    time.sleep (1) 
                    if time_finishe - time_start > tm:
                        exit_label = 'Выходим'
                    exit_key   = iz_func.load_variable (user_id_send,name_key,namebot)
                    if exit_key != 'Ждем':
                        exit_label = 'Выходим'
                    message_out2 = 'Закрыта задача'
                    if exit_label == 'Выходим':
                        bot.edit_message_text(chat_id=user_id_send, message_id=message_id, text=message_out2,parse_mode='HTML')

        set_message_all (user_id,namebot,id_game,"") 

def game05 (user_id,namebot,id_game):
    import iz_func
    import iz_game			
    if 1==1:
        #iz_game.send_message_mafiya ('Дон сделал свой выбор',namebot,id_game)

        ### Список для выбора комисара
        import telebot
        NM,name_user = iz_game.koll_user_in_game (namebot,id_game) 
        markup = telebot.types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            if line[4] == '':
                nomer = nomer + 1
                tx1    = str(nomer)+" "+str(line[0])
                cl1    = "komisar_"+str(line[1])
                mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
                markup.add(mn1)

        NM,name_user = iz_game.koll_user_in_game (namebot,id_game)                
        lab_komisar = 'No'
        for line in name_user:
            if str(line[2]) == 'Комиссар':
                lab_komisar = 'Yes'
                token    = iz_func.get_token (namebot)
                bot      = telebot.TeleBot(token)    
                answer   = iz_game.send_message_mafiya ('Сейчас выбирает Комисар',namebot,id_game)
                message_out = 'Комисар Вы должены сделать выбор'
                answer = bot.send_message(line[1],message_out,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
        if lab_komisar == 'Yes':
            exit (0)
        else:    
            iz_game.game06 (user_id,namebot,id_game)

def game06 (user_id,namebot,id_game):
    import iz_func
    import iz_game		
    if 1==1:
        #iz_game.send_message_mafiya ('Комиссар сделал свой выбор',namebot,id_game)

        import telebot
        NM,name_user = iz_game.koll_user_in_game (namebot,id_game) 
        markup = telebot.types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            if line[4] == '':
                nomer = nomer + 1
                tx1    = str(nomer)+" "+str(line[0])
                cl1    = "doctor_"+str(line[1])
                mn1    = telebot.types.InlineKeyboardButton(text=tx1,callback_data = cl1)
                markup.add(mn1)

        lab_doctor = 'No'
        NM,name_user = iz_game.koll_user_in_game (namebot,id_game) 
        for line in name_user:
            if str(line[2]) == 'Доктор'  and line[4] == '':
                lab_doctor = 'Yes'
                token    = iz_func.get_token (namebot)
                bot      = telebot.TeleBot(token)    
                answer   = iz_game.send_message_mafiya ('Сейчас выбирает Доктор',namebot,id_game)
                message_out = 'Доктор Вы должены сделать выбор'
                answer = bot.send_message(line[1],message_out,reply_markup=markup,parse_mode='HTML')  ### ,reply_markup=markup
        if lab_doctor == 'Yes':
            exit (0)
        else:    
            iz_game.game07 (user_id,namebot,id_game)

def game07 (user_id,namebot,id_game):
    import iz_func
    import iz_game		
    id_game = iz_func.load_variable (user_id,"Номер игры",namebot) 
    if 1==1:
        #z_game.send_message_mafiya ('Доктор сделал свой выбор',namebot,id_game)
        answer = iz_game.send_picture_mafiya ('m02.webp',namebot,id_game) 
        iz_game.send_message_mafiya ('Просыпается город!',namebot,id_game)
        db,cursor = iz_func.connect ()        
        sql = "SELECT id,kill_mafiya,select_mafiya FROM game_mafiya where id = "+str(id_game)+""
        cursor.execute(sql)
        data = cursor.fetchall()
        message = 'No'
        for rec in data: 
            id,kill_mafiya,select_mafiya = rec        
        kill_user = get_user_in_user_id (select_mafiya,namebot,id_game) 
        iz_game.save_variable_mafiya (id_game,'Пользователь',kill_user[0],namebot) 
        iz_game.send_message_mafiya ('Сегодня в нашем городе никто не умер',namebot,id_game)
        iz_game.send_message_mafiya ('Попытаемся вычислить мафию на общем дневном обсуждении',namebot,id_game)
        db,cursor = iz_func.connect ()   
        sql = "UPDATE game_mafiya_user SET status = '' WHERE id_game = '"+str(id_game)+"' "
        cursor.execute(sql)
        db.commit()
        sql = "UPDATE game_mafiya_user SET life = 'Убит мафией' WHERE id_game = '"+str(id_game)+"' and user_id = '"+str(select_mafiya)+"' "
        cursor.execute(sql)
        db.commit()
        iz_game.find_mafiya (user_id,namebot,id_game)

def game40 (user_id,namebot,id_game):
    import iz_func
    import iz_game	
    NM,name_user_list  = iz_game.koll_user_in_game (namebot,id_game)
    nomer = 0
    for line in name_user_list:
        nomer = nomer + 1
        list_gamer = list_gamer + str(nomer) + '. '+line[0]+'\n'
    iz_game.save_variable_mafiya (id_game,"Ваше имя",list_gamer,namebot)      
    answer = iz_game.send_message_mafiya ('Информация о игроке',namebot,id_game)

def get_message_1 (user_id_base,id_game,namebot):
    import iz_func
    message_send = iz_func.send_message (user_id_base,'Игрок номер 1','S',namebot)
    message_send = iz_func.send_message (user_id_base,'Выберете журтву и укажите почему именно она','S',namebot)
    #id_game = iz_func.load_variable (user_id_base,"Номер игры",namebot)
    NM,name_user = koll_game (user_id_base,namebot,id_game)
    message_out = 'Список людей для голосования'
    from telebot import types 
    markup = types.InlineKeyboardMarkup(row_width=4)
    nomer = 0
    for line in name_user:
        nomer = nomer + 1
        tx1    = str(line[0])
        cl1    = "line_"+str(nomer)
        mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
        markup.add(mn1)  
    iz_func.bot_send (user_id_base,message_out,markup,namebot)

def golos_start_1 (id_game,namebot,message_in):
    import iz_func
    name01,user_id_base01,name_gertva01,role01 = get_gamer_in_nomer (namebot,id_game,1)
    if name01 != '' and name_gertva01 == '':	
    	get_message_1 (user_id_base01,id_game,namebot)

    name02,user_id_base02,name_gertva02,role02 = get_gamer_in_nomer (namebot,id_game,2)    
    if name02 != '' and name_gertva02 == '':	    	
    	message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)
    	get_message_1 (user_id_base02,id_game,namebot)

    name03,user_id_base03,name_gertva03,role03 = get_gamer_in_nomer (namebot,id_game,3)
    if name03 != '' and name_gertva03 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base03,id_game,namebot)

    name04,user_id_base04,name_gertva04,role04 = get_gamer_in_nomer (namebot,id_game,3)
    if name04 != '' and name_gertva04 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base04,id_game,namebot)

    name05,user_id_base05,name_gertva05,role05 = get_gamer_in_nomer (namebot,id_game,3)
    if name05 != '' and name_gertva05 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base05,id_game,namebot)

    name06,user_id_base06,name_gertva06,role06 = get_gamer_in_nomer (namebot,id_game,3)
    if name06 != '' and name_gertva06 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base06,id_game,namebot)

    name07,user_id_base07,name_gertva07,role07 = get_gamer_in_nomer (namebot,id_game,3)
    if name07 != '' and name_gertva07 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base07,id_game,namebot)

    name08,user_id_base08,name_gertva08,role08 = get_gamer_in_nomer (namebot,id_game,3)
    if name08 != '' and name_gertva08 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base08,id_game,namebot)

    name09,user_id_base09,name_gertva09,role09 = get_gamer_in_nomer (namebot,id_game,3)
    if name09 != '' and name_gertva09 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base09,id_game,namebot)

    name10,user_id_base10,name_gertva10,role10 = get_gamer_in_nomer (namebot,id_game,3)
    if name10 != '' and name_gertva10 == '':
        message_send = iz_func.send_message (user_id_base01,'Отправлено сообщение игроку на голосование','S',namebot)	
        get_message_1 (user_id_base10,id_game,namebot)

def get_message_2 (user_id_base,id_game,namebot,nomer_gamer):
    import iz_func
    iz_func.save_variable (user_id_base,"Номер игрока",str(nomer_gamer),namebot)
    message_send = iz_func.send_message (user_id_base,'Мне не нравиться игрок','S',namebot)

def golos_start_2 (id_game,namebot,message_in,user_id):
    import iz_func
    nomer_gamer = message_in.replace('line_','')
    name01,user_id_base01,name_gertva01,role01 = get_gamer_in_nomer (namebot,id_game,1)
    name02,user_id_base02,name_gertva02,role02 = get_gamer_in_nomer (namebot,id_game,2)
    name03,user_id_base03,name_gertva03,role03 = get_gamer_in_nomer (namebot,id_game,3)
    name04,user_id_base04,name_gertva04,role04 = get_gamer_in_nomer (namebot,id_game,4)
    name05,user_id_base05,name_gertva05,role05 = get_gamer_in_nomer (namebot,id_game,5)
    name06,user_id_base06,name_gertva06,role06 = get_gamer_in_nomer (namebot,id_game,6)
    name07,user_id_base07,name_gertva07,role07 = get_gamer_in_nomer (namebot,id_game,7)
    name08,user_id_base08,name_gertva08,role08 = get_gamer_in_nomer (namebot,id_game,8)
    name09,user_id_base09,name_gertva09,role09 = get_gamer_in_nomer (namebot,id_game,9)
    name10,user_id_base10,name_gertva10,role10 = get_gamer_in_nomer (namebot,id_game,10)

    print ('[+]1:',name01,'[+]2:',name_gertva01,'[+]3:',user_id,'[+]4:',user_id_base01)

    if name01 != '' and name_gertva01 == '' and str(user_id) == str(user_id_base01):	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva01 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base01,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base01,"status","Почему мне не нравиться",namebot)

    if name02 != '' and name_gertva02 == '' and user_id == user_id_base02:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva02 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base02,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base02,"status","Почему мне не нравиться",namebot)

    if name03 != '' and name_gertva03 == '' and user_id == user_id_base03:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva03 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base03,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base03,"status","Почему мне не нравиться",namebot)

    if name04 != '' and name_gertva04 == '' and user_id == user_id_base04:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva04 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base04,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base04,"status","Почему мне не нравиться",namebot)

    if name05 != '' and name_gertva05 == '' and user_id == user_id_base05:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva05 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base05,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base05,"status","Почему мне не нравиться",namebot)

    if name06 != '' and name_gertva06 == '' and user_id == user_id_base06:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva06 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base06,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base06,"status","Почему мне не нравиться",namebot)

    if name07 != '' and name_gertva07 == '' and user_id == user_id_base07:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva07 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base07,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base07,"status","Почему мне не нравиться",namebot)

    if name08 != '' and name_gertva08 == '' and user_id == user_id_base08:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva08 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base08,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base08,"status","Почему мне не нравиться",namebot)

    if name09 != '' and name_gertva09 == '' and user_id == user_id_base09:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva09 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base09,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base09,"status","Почему мне не нравиться",namebot)

    if name10 != '' and name_gertva10 == '' and user_id == user_id_base10:	
        db,cursor = iz_func.connect ()
        sql = "UPDATE game_mafiya SET name_gertva10 = '"+str(nomer_gamer)+"' WHERE `id` = '"+str(id_game)+"'"
        cursor.execute(sql)
        db.commit()
        get_message_2 (user_id_base10,id_game,namebot,nomer_gamer)
        message_send = iz_func.send_message (user_id_base01,'Игрок ответил на голосование','S',namebot)
        iz_func.save_variable (user_id_base10,"status","Почему мне не нравиться",namebot)

def golos_start_3 (id_game,namebot,message_in,user_id):

    import iz_func
    #word = message_in.replace('line_','')    
    name01,user_id_base01,name_gertva01,role01 = get_gamer_in_nomer (namebot,id_game,1)
    name02,user_id_base02,name_gertva02,role02 = get_gamer_in_nomer (namebot,id_game,2)
    name03,user_id_base03,name_gertva03,role03 = get_gamer_in_nomer (namebot,id_game,3)
    name04,user_id_base04,name_gertva04,role04 = get_gamer_in_nomer (namebot,id_game,4)
    name05,user_id_base05,name_gertva05,role05 = get_gamer_in_nomer (namebot,id_game,5)
    name06,user_id_base06,name_gertva06,role06 = get_gamer_in_nomer (namebot,id_game,6)
    name07,user_id_base07,name_gertva07,role07 = get_gamer_in_nomer (namebot,id_game,7)
    name08,user_id_base08,name_gertva08,role08 = get_gamer_in_nomer (namebot,id_game,8)
    name09,user_id_base09,name_gertva09,role09 = get_gamer_in_nomer (namebot,id_game,9)
    name10,user_id_base10,name_gertva10,role10 = get_gamer_in_nomer (namebot,id_game,10)

    if name01 != '' and name_gertva01 != ''  and str(user_id) == str(user_id_base01):	
        message_send = iz_func.send_message (user_id,'Рассылаем текст основание не нравиться','S',namebot)
        iz_func.save_variable (user_id_base01,"status","",namebot)
        message_out = 'Рассылка сообщения кто не нравиться' 
        message_send = iz_func.send_message (user_id,message_out,'S',namebot)
        save_variable_mafiya (id_game,"Имя писателя","112233",namebot)
        message_send = send_message_mafiya (message_out,namebot,id_game)

def golos_start_4 (id_game,namebot,message_in):    

    import iz_func
    name01,user_id_base01,name_gertva01,role01 = get_gamer_in_nomer (namebot,id_game,1)
    name02,user_id_base02,name_gertva02,role02 = get_gamer_in_nomer (namebot,id_game,2)
    name03,user_id_base03,name_gertva03,role03 = get_gamer_in_nomer (namebot,id_game,3)
    name04,user_id_base04,name_gertva04,role04 = get_gamer_in_nomer (namebot,id_game,4)
    name05,user_id_base05,name_gertva05,role05 = get_gamer_in_nomer (namebot,id_game,5)
    name06,user_id_base06,name_gertva06,role06 = get_gamer_in_nomer (namebot,id_game,6)
    name07,user_id_base07,name_gertva07,role07 = get_gamer_in_nomer (namebot,id_game,7)
    name08,user_id_base08,name_gertva08,role08 = get_gamer_in_nomer (namebot,id_game,8)
    name09,user_id_base09,name_gertva09,role09 = get_gamer_in_nomer (namebot,id_game,9)
    name10,user_id_base10,name_gertva10,role10 = get_gamer_in_nomer (namebot,id_game,10)


    if name01 != '': 
        sp01 = ''
        if name_gertva01 == '1':
            sp01 = sp01 + '1 '
        if name_gertva02 == 1:
            sp01 = sp01 + '2 '
        if name_gertva03 == 1:
            sp01 = sp01 + '3 '
        if name_gertva04 == 1:
            sp01 = sp01 + '4 '
        if name_gertva05 == 1:
            sp01 = sp01 + '5 '
        if name_gertva06 == 1:
            sp01 = sp01 + '6 '
        if name_gertva07 == 1:
            sp01 = sp01 + '7 '
        if name_gertva08 == 1:
            sp01 = sp01 + '8 '
        if name_gertva09 == 1:
            sp01 = sp01 + '9 '
        if name_gertva10 == 1:
            sp01 = sp01 + '10 '

        if sp01 != '':
            message_send = iz_func.send_message (user_id_base01,'Вас обвини. Что скажете в свое оправдание?','S',namebot)
            iz_func.save_variable (user_id_base01,"status","Слово в свое оправдание",namebot)
             
def golos_start_5 (id_game,namebot,message_in):    
    import iz_func
    db,cursor   = iz_func.connect ()
    sql = "SELECT id,user_id,user_id02,user_id03,user_id04,user_id05,user_id06,user_id07,user_id08,user_id09,user_id10,name01,name02,name03,name04,name05,name06,name07,name08,name09,name10,name_gertva01,name_gertva02,name_gertva03,name_gertva04,name_gertva05,name_gertva06,name_gertva07,name_gertva08,name_gertva09,name_gertva10 FROM `game_mafiya` where id = "+str(id_game)+""
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,user_id,user_id02,user_id03,user_id04,user_id05,user_id06,user_id07,user_id08,user_id09,user_id10,name01,name02,name03,name04,name05,name06,name07,name08,name09,name10,name_gertva01,name_gertva02,name_gertva03,name_gertva04,name_gertva05,name_gertva06,name_gertva07,name_gertva08,name_gertva09,name_gertva10 = rec
    if name01 != '' and name_gertva01 == '':	
        message_send = iz_func.send_message (user_id,'Вы проголосовали что бы убить','S',namebot)
        message_send = iz_func.send_message (user_id,'Вопрос второму кондидату','S',namebot)

def golos_start_6 (id_game,namebot,message_in): 
    import iz_func
    name01,user_id_base01,name_gertva01,role01 = get_gamer_in_nomer (namebot,id_game,1)
    name02,user_id_base02,name_gertva02,role02 = get_gamer_in_nomer (namebot,id_game,2)
    name03,user_id_base03,name_gertva03,role03 = get_gamer_in_nomer (namebot,id_game,3)
    name04,user_id_base04,name_gertva04,role04 = get_gamer_in_nomer (namebot,id_game,4)
    name05,user_id_base05,name_gertva05,role05 = get_gamer_in_nomer (namebot,id_game,5)
    name06,user_id_base06,name_gertva06,role06 = get_gamer_in_nomer (namebot,id_game,6)
    name07,user_id_base07,name_gertva07,role07 = get_gamer_in_nomer (namebot,id_game,7)
    name08,user_id_base08,name_gertva08,role08 = get_gamer_in_nomer (namebot,id_game,8)
    name09,user_id_base09,name_gertva09,role09 = get_gamer_in_nomer (namebot,id_game,9)
    name10,user_id_base10,name_gertva10,role10 = get_gamer_in_nomer (namebot,id_game,10)

    if name01 != '' and role01 == 'Мафия':
        NM,name_user = koll_game (user_id_base01,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base01,message_out,markup,namebot)   

    if name02 != '' and role02 == 'Мафия':
        NM,name_user = koll_game (user_id_base02,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base02,message_out,markup,namebot)   

    if name03 != '' and role03 == 'Мафия':
        NM,name_user = koll_game (user_id_base03,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base03,message_out,markup,namebot)   

    if name04 != '' and role04 == 'Мафия':
        NM,name_user = koll_game (user_id_base04,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base04,message_out,markup,namebot)   

    if name05 != '' and role05 == 'Мафия':
        NM,name_user = koll_game (user_id_base05,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base05,message_out,markup,namebot)   

    if name06 != '' and role06 == 'Мафия':
        NM,name_user = koll_game (user_id_base06,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base06,message_out,markup,namebot)   

    if name07 != '' and role07 == 'Мафия':
        NM,name_user = koll_game (user_id_base07,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base07,message_out,markup,namebot)   

    if name08 != '' and role08 == 'Мафия':
        NM,name_user = koll_game (user_id_base08,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base08,message_out,markup,namebot)   

    if name09 != '' and role09 == 'Мафия':
        NM,name_user = koll_game (user_id_base09,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base09,message_out,markup,namebot)   

    if name10 != '' and role10 == 'Мафия':
        NM,name_user = koll_game (user_id_base10,namebot,id_game)
        message_out = "Список для убийства"
        from telebot import types
        markup = types.InlineKeyboardMarkup(row_width=4)
        nomer = 0
        for line in name_user:
            nomer = nomer = 1
            tx1    = iz_func.get_namekey (line[0],namebot)
            cl1    = 'Убийство_'+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1) 
        answer = iz_func.bot_send (user_id_base10,message_out,markup,namebot)   

def mafiya_start_4 (user_id,namebot,id_game):
    import iz_func
    import time
    nomer = 0
    gololos_list = ''
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game)                
    for line in name_user: 
        nomer = nomer + 1        
        name_list,user_id_base_list,name_gertva_list,role_list = get_gamer_in_nomer (namebot,id_game,nomer)
        if name_gertva_list != '' and line[4] == '':
            gololos_list = gololos_list + name_gertva_list + '\n'
    iz_func.save_variable (user_id,"Выставлены игроки",str(gololos_list),namebot) 
    message_send = iz_func.send_message (user_id,'Выставлены игроки:','S',namebot)              
    message_send = iz_func.send_message (user_id,'Этап выставления на голосование завершен!','S',namebot)  
    message_send = iz_func.send_message (user_id,'Начинаем оправдательные речи','S',namebot) 

    nomer = 0
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game)                
    for line in name_user:    
        nomer = nomer + 1        
        name_list,user_id_base_list,name_gertva_list,role_list = get_gamer_in_nomer (namebot,id_game,nomer)
        if name_gertva_list != '' and line[4] == '':
            message_send = iz_func.send_message (user_id,'Выновный. Что скажите в оправдание?','S',namebot)                    
            message_list = ['Сейчас очередь оправдаваться','Время голосования завершено'] 

    message_send = iz_func.send_message (user_id,'Оправдательные речи окончены.','S',namebot)  
    NM,name_user = koll_game (user_id,namebot,id_game)
    message_out = 'Список людей для голосования'
    from telebot import types 
    markup = types.InlineKeyboardMarkup(row_width=4)
    nomer = 0
    for line in name_user:
        if name_gertva_list != '':
            nomer = nomer + 1
            tx1    = str(line[0])
            cl1    = "line_"+str(nomer)
            mn1    = types.InlineKeyboardButton(text=tx1,callback_data = cl1)
            markup.add(mn1)
        iz_func.bot_send (user_id,message_out,markup,namebot)
        message_list = ['Сейчас очередь','Время голосования завершено'] 
        iz_func.send_message_time (user_id,message_list,namebot,10)

    message_send = iz_func.send_message (user_id,'По итогам  голосования из города был изгнан','S',namebot)  
    message_send = iz_func.send_message (user_id,'Город засыпает! Просыпается мафия😈Мафия выбирает жертву...','S',namebot)  


    nm_mafiya = 0
    NM,name_user = iz_game.koll_user_in_game (namebot,id_game)                
    for line in name_user:    
    	if line[2] == 'Мафия':
            nm_mafiya = nm_mafiya + 1

    if nm_mafiya == 0:
        iz_game.send_message_mafiya ('Мафии нет. Город победил',namebot,id_game)       
    else:    
        start55 (user_id,namebot,id_game)

