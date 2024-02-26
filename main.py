from json import loads
from requests import get
from bs4 import BeautifulSoup


url1 = 'https://vkusnoitochka.ru/api/restaurants/near' # Получить список ресторанов (нужны координаты lat и long) 
url2 = 'https://vkusnoitochka.ru/api/menu/restaurant/' # Получить меню ресторана (нужен xmlId ресторана)


# Функция получения списка ресторанов (и их координат)
def get_restaraunts():
    # Получаем список ресторанов
    restaurants = loads(get(url1, params={'lat': 55.755864, 'long': 37.617698}).text)
    # Записываем id, и координаты в отдельный словарь
    A = {}
    for restaurant in restaurants:
        A[restaurant['xmlId']] = {'id': restaurant['xmlId'], 'lat': restaurant['latitude'], 'lon': restaurant['longitude']}
    return A


# Поиск Гранд Фри или Картофеля Фри в меню
def get_fries(restaurant_id):
    products = loads(get(url2+str(restaurant_id)).text)
    # (КОСТЫЛЬ) Сначала ищем раздел "Картофель, стартеры и салаты"
    try:
        try:
            products = products['categories'][6]['subcategories'][1]['products']
        except:
            products = products['categories'][3]['subcategories'][1]['products']
    except:
        return restaurant_id, '000000'
    # Если нашлось:
    if 10056 in products:
        return 'Гранд Фри', 'aa3c3c'
    elif 10012 in products:
        return 'Картофель фри', '3caa3c'
    # Если не нашлось:
    else:
        return restaurant_id, '000000'


# Итерация по всем ресторанам
for restaurant in get_restaraunts().values():
    fries, color = get_fries(restaurant['id'])
    # Полученные данные можно добавить на Яндекс Карту для визуализации
    print(f'myMap.geoObjects.add(new ymaps.Placemark([{restaurant["lat"]}, {restaurant["lon"]}], {{balloonContent: "{fries}"}}, {{preset: "islands#circleIcon", iconColor: "#{color}"}}));')