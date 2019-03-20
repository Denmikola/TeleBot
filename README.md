# TeleBot
Описание:
Приложение разработано на языке Python с использованием фрейморка Flask, базы данных SQLite и фреймворка Bootstrap
Реализован механизм ведения пользователей, разделение их запросов. 
Осуществляется запрос к БД судебных приставов по API сайта fssprus.ru и разбор полученного в формате JSON ответа.
Реализован запрос истории общения с ботом в Телеграмме, дальше процесс разработки был остановлен.
Это приложение является пилотной версией проекта. По идее заказчика это должен был быть сервис сбора и консолидации информации о физическом или юридическом лице из открытых баз данных. В качестве мобильного интерфейса используется бот в Телеграмме. Но деньги у заказчика неожиданно быстро закончились и проект был остановлен.

Установка:
1.1. Скопируйте все содержимое репозитория в каталог /home/telebot вашего вебсервера. 
1.2. Установите на сервере интерпретатор языка Python версии от 3.4 и выше
1.3. Установите виртуальное окружение и дополнительные модули, перечисленные в файле requiriments.txt командами
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
1.4 Настройте ваш веб-сервер на выполнение приложения TeleBot.py и установите необходимый IP-адрес для обращения к этому приложению по протоколу HTTP

Использование:
2.1. При первом входе в программу необходимо зарегистрировать пользователя.
2.2. На страничке "Запросы" заполнить поля формы "Регион", "Фамилия", "Имя" и нажать кнопку "Создать запрос".
2.3. Появится обьект содержащий исходные данные запроса, управляющий функционал, статистику результата и функционал просмотрарезультата
2.4. Нажать ссылку "Отправить запрос", через несколько секунд появится либо ссылка содержащая результат запроса, либо сообщение об ошибке.
2.5. Для просмотра результата нажмите на ссылку "Найдено ИП: %NNN"
2.6. Результаты запроса хранятся в базе данных до следующего нажатия на ссылку "Отправить запрос"
