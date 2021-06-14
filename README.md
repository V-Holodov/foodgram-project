# Продуктовый помощник "Foodgram"

![example workflow](https://github.com/v-holodov/foodgram-project/actions/workflows/fg_workflow.yml/badge.svg)

## Описание
**Foodgram** -  онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
В проекте используются следующие основные пакеты:
- Python 3.7
- Django 2.2
- Django REST framework 3.11.0  
- Djangorestframework-simplejwt 4.6.0
- Gunicorn 20.0.4
- Psycopg2-binary 2.8.5
- Docker  20.10.5
- Nginx 1.19.9
- PostgreSQL 12.6
## Пример развернутого проекта
Проект запущен и доступен по адресу:
[http://130.193.41.192/](http://130.193.41.192/)
## Установка

Для начала склонируйте репозиторий 
```bash
git clone https://github.com/V-Holodov/foodgram-project.git
```
Создайте файл .env с переменными окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
Для запуска приложения выполните развертывание контейнеров в фоновом режиме командой:
```bash
docker-compose up -d --build 
```
Для запуска миграций выполните команды:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
```
Создать суперпользователя необходимо командой:
```bash
docker-compose exec web python manage.py createsuperuser
```
После этого необходимо собрать статику командой:
```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Для заполнения базы начальными данными нужно выполнить команду:
```bash
docker-compose exec web python manage.py load_ingredient
```
## Коротко о структуре проекта

1. `config` - корневая директория, здесь settings.py джанги
2. `recipes` - основное приложение проекта:
    * содержит описание всех моделей кроме модели пользователя
    * отвечает за отображение и доступ ко всем страницам
    * вспомогательные инструменты - кастомный фильтр для смены класса html-элемента, а также шаблонный тег для генерации урлов при переходе по тегам
    * директория `api` - с помощью DRF реализует функционал передачи данных из базы JS-скриптам: при нажатии на кнопку "подписаться/отписаться", при добавлении / исключении из избранного, при добавлении рецептов в список покупок, а также удалению из него
3. `users` - приложение для работы с пользователями.
4. `.github/workflows` - настройка workflows для gihub actions
5. `templates` - все шаблоны проекта.
6. файлы статики и медиафайлы собраны в одноименных директориях.
7. в директории `nginx` - настройки сервера.
8. `Dockerfile`, `docker-compose.yaml` - развертывания проекта в докер-контенейрах.
9. `ingredients.csv` - ингредиенты для заполнения базы данных.

## Об авторе
Проект подготовлен выпускником бэкенд-факультета Яндекс-Практикума Виталием Холодовым.

## Лицензия
MIT
