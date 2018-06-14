# Functions responsible for generating geolocalization data.

import numpy as np


# Geographic data (only cities with >50000 inhabitants)
# Format: (location name, inhabitants, criteria ID)
geo_data = [
    # dolnośląskie
    ('Wrocław', 640000, 1011243),
    ('Wałbrzych', 115000, 1011239),
    ('Legnica', 100000, 1011214),
    ('Jelenia Góra', 80000, 1011206),
    ('Lubin', 70000, 1011217),
    ('Głogów', 60000, 1011203),
    ('Świdnica', 60000, 1011233),
    # kujawsko-pomorskie
    ('Bydgoszcz', 350000, 1011251),
    ('Toruń', 200000, 1011272),
    ('Włocławek', 110000, 1011276),
    ('Grudziądz', 95000, 1011256),
    ('Inowrocław', 75000, 1011257),
    # lubelskie
    ('Lublin', 340000, 1011347),
    ('Zamość', 65000, 1011354),
    ('Chełm', 65000, 1031027),
    ('Biała Podlaska', 60000, 1011337),
    ('Puławy', 50000, 1011296),
    # lubuskie
    ('Zielona Góra', 140000, 1011308),
    ('Gorzów Wielkopolski', 125000, 1011282),
    # łódzkie
    ('Łódź', 710000, 1011320),
    ('Piotrków Trybunalski', 75000, 1011324),
    ('Pabianice', 70000, 1011323),
    ('Tomaszów Mazowiecki', 65000, 1011331),
    ('Bełchatów', 60000, 1011310),
    ('Zgierz', 60000, 1011335),
    ('Skierniewice', 50000, 1011328),
    # małopolskie
    ('Kraków', 760000, 1011367),
    ('Tarnów', 110000, 1011388),
    ('Nowy Sącz', 85000, 1011373),
    # mazowieckie
    ('Warszawa', 1730000, 1011419),
    ('Radom', 220000, 1011414),
    ('Płock', 120000, 1011412),
    ('Siedlce', 75000, 1031114),
    ('Pruszków', 60000, 1031100),
    ('Legionowo', 55000, 1031063),
    ('Ostrołęka', 55000, 1011409),
    # opolskie
    ('Opole', 130000, 1011430),
    ('Kędzierzyn-Koźle', 60000, 1011426),
    # podkarpackie
    ('Rzeszów', 185000, 1011463),
    ('Przemyśl', 65000, 1011461),
    ('Stalowa Wola', 65000, 1011466),
    ('Mielec', 60000, 1011457),
    # podlaskie
    ('Białystok', 295000, 1011435),
    ('Suwałki', 70000, 1011445),
    ('Łomża', 63000, 1011443),
    # pomorskie
    ('Gdańsk', 465000, 1011475),
    ('Gdynia', 245000, 1011476),
    ('Słupsk', 90000, 1011486),
    ('Tczew', 60000, 1011489),
    ('Wejherowo', 50000, 1011491),
    # śląskie
    ('Katowice', 305000, 1011521),
    ('Częstochowa', 230000, 1011515),
    ('Sosnowiec', 210000, 1011539),
    ('Gliwice', 185000, 1011517),
    ('Zabrze', 175000, 1011545),
    ('Bielsko-Biała', 175000, 1011545),
    ('Bytom', 170000, 1011510),
    ('Ruda Śląska', 140000, 1011536),
    ('Rybnik', 140000, 1011537),
    ('Tychy', 130000, 1011541),
    ('Dąbrowa Górnicza', 125000, 1011516),
    ('Chorzów', 110000, 1011511),
    ('Jaworzno', 95000, 1011519),
    ('Jastrzębie-Zdrój', 90000, 1011518),
    ('Mysłowice', 75000, 1011528),
    ('Siemianowice Śląskie', 70000, 1011538),
    ('Żory', 60000, 1011547),
    ('Tarnowskie Góry', 60000, 1011540),
    ('Będzin', 60000, 1031025),
    ('Piekary Śląskie', 55000, 1011532),
    ('Racibórz', 55000, 1011534),
    ('Świętochłowice', 50000, 1031145),
    ('Zawiercie', 50000, 1011546),
    # świętokrzyskie
    ('Kielce', 200000, 1011498),
    ('Ostrowiec Świętokrzyski', 70000, 1011500),
    ('Starachowice', 50000, 1011504),
    # warmińsko-mazurskie
    ('Olsztyn', 170000, 1011564),
    ('Elbląg', 120000, 1011552),
    ('Ełk', 60000, 1011553),
    # wielkopolskie
    ('Poznań', 540000, 1011615),
    ('Kalisz', 100000, 1011583),
    ('Konin', 75000, 1011590),
    ('Piła', 75000, 1011610),
    ('Ostrów Wielkopolski', 70000, 1011607),
    ('Gniezno', 70000, 1011577),
    ('Leszno', 65000, 1011598),
    # zachodniopomorskie
    ('Szczecin', 405000, 1011672),
    ('Koszalin', 110000, 1011658),
    ('Stargard', 110000, 1011669),
]


def init_distribution():
    inhabitants = np.array(list(zip(*geo_data))[1])
    return inhabitants / np.sum(inhabitants)


def generate_geoids(visits_no):
    dist = init_distribution()
    ids = np.random.choice(len(geo_data), visits_no, p=dist)
    return list(np.array(list(zip(*geo_data))[2])[ids])
