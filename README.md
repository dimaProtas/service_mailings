Тестовый проект "Рассылка сообщений"
- Создан API и UI для управления рассылкой
- Возможность создавать удалять и редактировать сущности "Код оператора",
"Таим-зону", "Теги", "Клиента", "Рассылку". 
- Отправка сообщений на удалённый API.
- Сор статистики по отправке.
- Отправка сообщений в соответсвии с задонным временем
- Фильтрация рассылки по времени и коду оператора.
- Настроен сигнал который отправляет задачи
в celry когда создана рассылка(или в будущем). 
- Настроено логирование в соответсвии с ТЗ.
- Документация swegger
- Тестирование проекта(написал 22 теста pytest)
- Авторизация через сторонний сервис(GitHub для примера)


Сборка проекта:
docker-compose build

Запуск проекта:
docker-compose up

admin:
'''http://127.0.0.1:8000/admin/'''
username: admin
password: admin

API:
'''http://127.0.0.1:8000/api/'''

django:
'''http://127.0.0.1:8000/'''

flower:
'''http://127.0.0.1:5555/'''

docs:
'''http://127.0.0.1:8000/api/docs/'''

rebbitMQ-admin:
'''http://127.0.0.1:15672/'''
