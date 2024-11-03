# BankAPI

## Настройка запуска

Установка всех зависимостей:
```
pip install -r requirements.txt
```

Сам запуск:
``` 
python init.py
```

## Запросы

1. Запрос для регистрации пользователя:
```
curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d "{\"username\": \"test\", \"password\": \"12345\"}"
```
2. Запрос для входа:
```
curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -c cookies.txt -d "{\"username\": \"test\", \"password\": \"12345\"}"
```
- Для сохранения сессии используем `-c cookies.txt`

3. Запрос для добавления банковского реквизита:
```
curl -X POST http://127.0.0.1:5000/bank_details -H "Content-Type: application/json" -b cookies.txt -d "{\"bank_name\": \"Sber\", \"bic\": \"23415223\", \"account_number\": \"12321462\"}"
```
- Добавляем ключ сессии `-b cookies.txt`

4. Просмотр банковских реквизитов авторизованного пользователя:
```
curl -X GET http://127.0.0.1:5000/bank_details -b cookies.txt
```

5. Установка активного банковского реквизита по его ID:
```
curl -X PUT http://127.0.0.1:5000/bank_details/1/activate -b cookies.txt
```
- ID в данном запросе это 1

6. Обновление банковского реквизита по его ID:
```
curl -X PUT http://127.0.0.1:5000/bank_details/1 -H "Content-Type: application/json" -b cookies.txt -d "{\"bank_name\": \"T-Bank\", \"bic\": \"654321\", \"account_number\": \"0987654321\"}"
```
7. Удаление банковских реквизитов по его ID:
```
curl -X DELETE http://127.0.0.1:5000/bank_details/1 -b cookies.txt
```
