# Тестовое задание от компании Numbers
[ТЗ](https://soldigital.notion.site/soldigital/developer-5b79683045a64129a2625a19bfb0c944) </br>
[Ссылка на Google Sheets документ](https://docs.google.com/spreadsheets/d/1WVv67Ma43A0lWml8r1wH1Wq14jD4-lLfoxnpkTBUjlw/edit#gid=0)
## Настройка проекта
1. Перейдите по [ссылке](https://console.developers.google.com/)
2. Библиотека – Создать проект
3. Поиск в библиотеке API:
4. Google Drive – Включить
4. Google Sheets API – Включить
5. Учетные данные - Управление сервисными аккаунтами - Создать аккаунт
   6. Ключи - Создать ключ - JSON
    
7. Загрузить json-файл с ключем в папку secret под названием secret_key.json
8. Выдать разрешение на редактирование и просмотр на email из файла secret_key.json (поле client_email)

## Создание телеграмм-бота
1. Введите в поле поиска @BotFather и выберите бота.
2. Нажмите «Запустить» для активации бота BotFather.
3. Выберите или напечатайте и отправьте команду `/newbot`
4. Дайте имя боту и никнейм
5. Скопируйте токен и вставьте в .env файл

## Конфигурация проекта

Создайте и заполните .env файл

| .env              | description                                                |
|------------------|-------------------------------------------------------------|
| POSTGRES_USER    | Имя пользователя БД                                         |
| POSTGRES_PASSWORD| Пароль от пользователя БД                                   |
| POSTGRES_DB      | Название БД                                                 |
| TG_TOKEN         | Токен от телеграмм-бота                                     |
| DB_HOST          | Название host'a (не изменять) default = pg                  |
| SHEET_FILE_NAME  | Название файла в Google Drive                               |


## Запуск с [docker-compose](https://docs.docker.com/compose/)

Чтобы запустить приложение пропишите в консоли:

```shell
docker-compose up -d
```
Чтобы оповещения работали нужно отправить созданному боту команду `/start` после запуска приложения