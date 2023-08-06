# Leaders of Digital Sber Case #5

Команда: Дедовщина

## Установка

1. Установите модуль `pip install lod-dedovschina-sber`
2. В необходимом файле укажите `from models.Address import Address`

## Использование

### Получение строки адреса

В конструктор класса необходимо указать строку. Метод `address_string()` возвращает строку адреса. Пример:
```
addr = Address("117042, г.Москва, ул. Южнобутовская, дом 139, эт. 1, пом. II, ком. 6 РМ 5")

addr.address_string()
```