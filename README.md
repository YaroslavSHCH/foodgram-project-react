# Foodgram - продуктовый помощник
**_Дипломный проект Yandex.Praktikum_**
![FOODGRAM-WORKFLOW](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)
### Краткое описание:
Продуктовый помощник. Веб приложение с возможностью создавать рецепты.
Реализованный функционал: система аутентификации по токену, создание новых рецептов, просмотр рецептов и их изменение. Созданные рецепты могут быть добавлены в избранное и в корзину. Добавленные в корзину рецепты, могут быть выгружены в pdf-файл, который формируется из суммы ингредиентов всех добавленых рецептов. Так же реализован функционал подписок на авторов (пользователей) рецептов.

В backend-части проекта использованы следующие инструменты:
_Python3, Django3, Django REST Framework, PostgreSQL_

Frontend-часть была подготовлена командой Yandex.praktikum. Использован:
_React_

CI/CD:
_GitHub Actions, Docker, Nginx, YandexCloud_

## Подготовка проекта
### 1. Установить Docker и Docker-compose.
### 2. Клонировать репозиторий.
### 3. Наполнить необходимым .env (secret key django, secrets для PostgreSQL и пр.)
(Необходимо заполнить POSTGRES_USER и POSTGRES_PASSWORD)
При запуске на сервере:

В файле /<project_dir>/backend/config/settings.py добавить IP-адрес сервера в список ALLOWED_HOSTS

### 4. При первом запуске из директории /<project_dir>/infra/ выполнить:
```sh
docker-compose up -d --build
```
При последующих:
```sh
docker-compose up -d
```
### 5. Собрать статические файлы:
```sh
docker-compose exec web python manage.py collectstatic
```
### 6. Создать структуру базы данныз и применить миграции:
```sh
docker-compose exec web python manage.py migrate
```
** 7. Загрузка списка ингредиентов в базу:**
```sh
docker-compose exec web bash loaddata.sh
```
### 8. Создать запись администратора:
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
**Документация будет доступна по адресу: http://localhost/api/docs/**
**Админ-панель: http://localhost/admin/**

## Проект в сети:
В настоящий момент проект доступен [ТУТ](http://projectus.tk/)
Учетные данные для админки:
adminus@projectus.tk 
62486248

_Автор Щавровский Ярослав_
