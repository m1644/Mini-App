from typing import Dict, List

ITEMS_PER_PAGE = 4

WELCOME_IMAGES = [
    "https://i.postimg.cc/1zmBDfvD/IMG-0494.png",
    "https://i.postimg.cc/W4zr2r9Y/IMG-0495.png",
    "https://i.postimg.cc/5NJCXD7C/IMG-0496.png",
    "https://i.postimg.cc/tg81pcn7/IMG-0497.png",
    "https://i.postimg.cc/RZFqfmcN/IMG-0498.png",
    "https://i.postimg.cc/xTjZSjrx/IMG-0510.png",
    "https://i.postimg.cc/TYTzYqbc/IMG-0511.png",
    "https://i.postimg.cc/0yTZrP3q/IMG-0508.png",
]

CATEGORY_IMAGES = {
    "pizza": "https://i.postimg.cc/9QKgTGDK/IMG-0507.png",
    "drinks": "https://i.postimg.cc/W4zr2r9Y/IMG-0495.png",
}

MENU: Dict[str, List[dict]] = {
    "pizza": [
        {"id": 1, "name": "Маргарита", "price": 450, "description": "Классическая пицца с томатами и моцареллой",
         "image": "https://i.postimg.cc/G2Y9gpfp/IMG-0478.png"},
        {"id": 2, "name": "Пепперони", "price": 500, "description": "Острая пицца с колбасками пепперони",
         "image": "https://i.postimg.cc/503WtdY3/IMG-0480.png"},
        {"id": 3, "name": "Гавайская", "price": 480, "description": "С ветчиной и ананасами",
         "image": "https://i.postimg.cc/NGJZCx15/IMG-0482.png"},
        {"id": 4, "name": "Четыре сыра", "price": 520, "description": "Сырный микс: моцарелла, пармезан, дор-блю, чеддер",
         "image": "https://i.postimg.cc/9z3fdHb7/IMG-0493.png"},
        {"id": 5, "name": "Мясная", "price": 550, "description": "Ассорти из мяса: ветчина, бекон, пепперони",
         "image": "https://i.postimg.cc/R0xcMjzq/IMG-0472.jpg"},
        {"id": 6, "name": "Вегетарианская", "price": 460, "description": "Свежие овощи и грибы",
         "image": "https://i.postimg.cc/HkR6bZ1C/IMG-0473.jpg"},
        {"id": 7, "name": "Карбонара", "price": 490, "description": "С беконом, сливочным соусом и яйцом",
         "image": "https://i.postimg.cc/90gMrqRJ/IMG-0490.png"},
        {"id": 8, "name": "Маргарита XL", "price": 600, "description": "Большая классическая пицца",
         "image": "https://i.postimg.cc/j2pc0Cxk/IMG-0488.png"},
        {"id": 9, "name": "Диабло", "price": 530, "description": "Очень острая с перцем чили",
         "image": "https://i.postimg.cc/6QtHp7dk/IMG-0487.png"},
        {"id": 10, "name": "Грибная", "price": 470, "description": "С шампиньонами и трюфельным маслом",
         "image": "https://i.postimg.cc/kMphvgmS/IMG-0485.png"},
    ],
    "drinks": [
        {"id": 11, "name": "Кола", "price": 120, "description": "Газированный напиток 0.5л",
         "image": "https://i.postimg.cc/V62SRVWX/IMG-0499.png"},
        {"id": 12, "name": "Фанта", "price": 120, "description": "Газированный напиток 0.5л",
         "image": "https://i.postimg.cc/hjQvf0Rv/IMG-0500.png"},
        {"id": 13, "name": "Спрайт", "price": 120, "description": "Газированный напиток 0.5л",
         "image": "https://i.postimg.cc/5t6NRm0g/IMG-0501.png"},
        {"id": 14, "name": "Вода", "price": 80, "description": "Минеральная вода 0.5л",
         "image": "https://i.postimg.cc/4ybJ9LLf/IMG-0502.png"},
        {"id": 15, "name": "Сок", "price": 150, "description": "Апельсиновый сок 0.3л",
         "image": "https://i.postimg.cc/7YwPk4hf/IMG-0503.png"},
    ],
}

PROMO_CODES = {"PIZZA2023": 10, "WELCOME5": 5, "1644": 44}

ITEM_ID_TO_ITEM = {item["id"]: item for category in MENU.values() for item in category}