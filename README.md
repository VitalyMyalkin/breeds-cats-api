Апишка для администратора онлайн выставки котят (тестовое задание для Workmate)

## Описание ##

Апишка выполнена на FastApi+SQLAlchemy. 
Включены файлы докера и докер компоуз, но запустить контейнеры так и не получилось):
В обратной связи буду рад видеть указание на ошибки в файлах и причины, по которым контейнеры не поднялись. А пока придется поднимать приложение локально, извините!
Документация Swagger доступна после запуска сервера по адресу http://localhost:8000/docs

В апишке восемь ручек: 

![image](https://github.com/user-attachments/assets/719b474f-1c5f-4f7b-a2fa-6e64b11c0d76)


1. Добавление породы (просто ручка для удобного создания породы)

![image](https://github.com/user-attachments/assets/3301d4ad-b7b9-4725-88ed-eed2e45fe831)

2. Добавление котенка - с указанием айдишника его породы

![image](https://github.com/user-attachments/assets/6453c4e7-f4fc-42e6-83b8-1fe3fc9d5b48)

3. Получение списка всех пород

![image](https://github.com/user-attachments/assets/1648d091-b20e-4775-99ed-43d8e67af748)

4. Получение списка всех котят

![image](https://github.com/user-attachments/assets/4a4ca8dc-85cb-49dd-8d50-f37b826c7bd4)

5. Получение подробной информации о котенке - по айдишнику

![image](https://github.com/user-attachments/assets/0865144f-3492-4d14-8e9e-5651d6e4c58d)

6. Изменение информации о котенке - надо отправить все данные котенка, даже те, что не изменяются, иначе Pydantic вас не пропустит!

![image](https://github.com/user-attachments/assets/28e4426d-9342-415e-9fc4-e9bede20eb0a)

7. Удаление информации о котенке - по айдишнику

![image](https://github.com/user-attachments/assets/3ae42828-2057-4c07-b747-728191bdc6fd)

8. Получение списка котят определенной породы по фильтру. Фильтр - название породы

![image](https://github.com/user-attachments/assets/8469c1ba-8e5d-46e6-a40a-b613d0088e46)


## Установка ##

git clone https://github.com/VitalyMyalkin/breeds-cats-api.git

cd ./breeds-cats-api

python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt

uvicorn main:app

Перед запуском не забудьте создать в постгрес базу breeds_cats, а также вам нужен .env файл в корневой директории, содержащий данные для подключения к ней:

DB_HOST=<хост>

DB_PORT=<порт>

DB_USER=<юзер>

DB_PASSWORD=<пароль>

DB_NAME=breeds_cats

## Минимум данных для проверки работы приложения: ##

1. Добавьте породу (POST http://127.0.0.1:8000/breed)
2. Добавьте котеночка (POST http://127.0.0.1:8000/cat)
3. Получите список котят, там будет указана порода (GET http://127.0.0.1:8000/cats)

## Схема таблиц в базе данных: ##

![image](https://github.com/user-attachments/assets/f0f53d38-047a-43fa-9845-4bf9560351ae)

Постскриптум. После остановки приложения база очищается!
