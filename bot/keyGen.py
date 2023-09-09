from telethon import Button

def keyGenerator(status):
    if(status == "menu"):
        return [[Button.inline("Вернуться в меню", b"menu")]]
    elif(status == "confirming_message"):
        return [[Button.inline("Да, я уверен (начать рассылку)", b"start_sending")],[Button.inline("Нет, я ошибся (написать заново)", b"creating_message")]]
    elif(status == "start"):
        return [[Button.inline("Меню", b"menu")]]
    elif(status == "creating_database"):
        return [Button.inline("Вписать пользователей для рассылки", b"create_database")]
    elif(status == "confirming_database"):
        return [[Button.inline("Да, я уверен (переход к созданию сообщение)", b"creating_message")],[Button.inline("Нет, я ошибся (написать заново)", b"create_database")]]
    elif(status == "managing_database"):
        return [Button.inline("Управление базой данных", b"managing_database")]
    elif(status == "managing_database_buttons"):
        return [[Button.inline("Добавить канал(ы) для парсинга", b"add_chanel")],[Button.inline("Удалить канал(ы) для парсинга", b"remove_chanel")],[Button.inline("Посмотреть все каналы в базе", b"show_chanel")], [Button.inline("Изменить канал назначения", b"change_origin_chanel")], [Button.inline("В меню", b"menu")]]
    elif(status == "confirming_adding_chanel_to_database"):
        return [[Button.inline("Да, я уверен (Добавление каналов в базу)", b"adding_chanel_handler")],[Button.inline("Нет, я ошибся (написать заново)", b"add_chanel")]] 
    elif(status == "confirming_removing_chanel_to_database"):
        return [[Button.inline("Да, я уверен (Удаление каналов из базы)", b"removing_chanel_handler")],[Button.inline("Нет, я ошибся (написать заново)", b"remove_chanel")]]    