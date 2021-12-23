# Продуктовый помощник FOODGRAM
---
### Описание
Учебный проект студента Яндекс.Практикум. Веб сервис дает возможность делиться своими рецептами, искать рецепты других. При необходимости пользователь может подписаться на интересующего его автора, добавлять рецепты в избранное, а также скачивать список ингредиентов перед походом в магазин.
### Сервис доступен по следующему адресу
[Foodgram.Продуктовый помощник](http://51.250.30.189// "Главная страница")
### Доступ в админ панель:
  - логин: admin@mail.ru
  - пароль: admin
### Команда для клонирования репозитория 
    git clone https://github.com/timelord78/foodgram-project-react.git foodgram
### Заполните файл переменных окружения в директории /backend проекта(.env)
- DB_NAME=<имя базы данных>
- POSTGRES_USER=<имя пользователя БД>
- POSTGRES_PASSWORD=<пароль>
- DB_HOST=<хост БД>
- DB_PORT=<порт БД>
- SECRET_KEY='ключ джанго проекта'
### Инструкция по запуску
 - docker-compose up (построение контейнеров и запуск)
 - docker-compose exec web python manage.py migrate --noinput (выполнить миграции)
 - docker-compose exec web python manage.py createsuperuser (создать суперпользователя)
 - docker-compose exec web python manage.py collectstatic --no-input (собрать статические файлы)
### Используемые технологии
 - Python
 - Django
 - Django Rest Framework
 - Docker
 - Gunicorn
 - Nginx
 - PostgreSQL
 - дополнительно - см.(requirements.txt)
### Об авторе
Яков Зубец, github.com/timelord78, yakovzubets@gmail.com

