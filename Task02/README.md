# Требования к окружению

Для корректной работы скрипта `db_init.bat` необходимо:

## Установленное программное обеспечение:

- **Python 3.x** - интерпретатор Python версии 3.6 или выше
- **SQLite 3** - система управления базами данных

## Структура базы данных:

После выполнения скрипта создается база данных `movies_rating.db` со следующими таблицами:

### movies
- id (primary key)
- title
- year 
- genres

### ratings
- id (primary key)
- user_id
- movie_id
- rating
- timestamp

### tags
- id (primary key)
- user_id
- movie_id
- tag
- timestamp

### users
- id (primary key)
- name
- email
- gender
- register_date
- occupation

## Результат выполнения:

После запуска скрипта `db_init.bat` будет создана заполненная база данных `movies_rating.db` с данными из каталога `dataset`.