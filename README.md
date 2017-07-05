## Description
Simple gas station search made using Flask and yandex.maps API.

## Dependencies
* Python 3.5
* Flask
* requests

## Using

```
$ git clone https://github.com/max-lv/yamap-search.git
$ cd yamap-search
[!] Put yandex.maps API KEY into APIKEY constant inside app.py
$ ./app.py
```

App should be available at `127.0.0.1:5000`

## API

`GET api`
Preforms search and returns results

GET parameters

`city` : (string) city name

Returns:

```
{
  "success": (bool)
  "data": { first five gas stations
    "id": yandex.maps company id
    "address": address in Russian
    "coordinates": array with two float numbers
  },
  "total": (int) total number of gas stations found
  "file_id": id of csv file. To download go to: 127.0.0.1:5000/csv/<file_id>
}
```
