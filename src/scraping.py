import requests
from bs4 import BeautifulSoup

import pandas as pd


def create_user_base_url(user_name: str) -> str:
    return f'https://letterboxd.com/{user_name}/'


def check_user_existance(user_name: str) -> bool:
    url = create_user_base_url(user_name)
    page = requests.get(url=url)
    if str(page.status_code)[0] == '2':
        return True
    else:
        return False


def compute_film_rating(stars_string: str):
    if not len(stars_string):
        return None
    rating = 0
    for char in stars_string:
        if ord(char) == 9733:
            rating += 1
        else:
            rating += 0.5
    return rating


def build_films_df(movies: list, fav_films):
    df = pd.DataFrame({
        'film': [x[0] for x in movies],
        'rating': [x[1] for x in movies],
        'film_id': [x[2] for x in movies]
    })
    df_fav = pd.DataFrame({
        'film': [x[0] for x in fav_films],
        'film_id': [x[1] for x in fav_films],
        'favorite': [1] * len(fav_films)
    })

    df = df.merge(df_fav, how='left', on=['film', 'film_id'])
    df['favorite'].fillna(0, inplace=True)

    return df

def scrap_favorite_films(user_name):
    url = create_user_base_url(user_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    poster_containers = soup.find_all(class_='poster-container')

    return [(poster.contents[1].contents[1].attrs['alt'], poster.contents[1].attrs['data-film-id']) for poster in
            list(poster_containers)[:4]]


def scrap_user_films(user_name: str, place):
    url = create_user_base_url(user_name) + 'films/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    no_pages = int(soup.find_all(class_='paginate-page')[-1].get_text())

    movies = []
    print(f'Processing movies of page {1}')
    movies = get_films_from_page(movies, soup)
    for_bar = place.empty()
    for page_num in range(2, no_pages + 1):
        print(f'Processing movies of page {page_num}')
        page_url = f'{url}/page/{page_num}/'
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for_bar.progress((page_num - 1) / (no_pages - 1))

        movies = get_films_from_page(movies, soup)

    fav_films = scrap_favorite_films(user_name)
    df = build_films_df(movies, fav_films)

    return df


def get_films_from_page(movies, soup):
    poster_containers = soup.find_all(class_='poster-container')
    for poster_container in poster_containers:
        film_info = list(poster_container.children)[1]
        film_name = film_info.contents[1].attrs['alt']
        film_id = film_info.attrs['data-film-id']

        user_rating = list(poster_container.children)[3]
        film_rating = compute_film_rating(user_rating.get_text().strip())

        movies.append((film_name, film_rating, film_id))
        # print(f'film: {film_name} -> {film_rating}')
    return movies


class STReplica:
    def empty(self):
        return STReplica()

    def progress(self, x=None):
        return None


if __name__ == '__main__':
    st_replica = STReplica()
    # df = scrap_user_films('mateusoler', st_replica)
    # print(df)

    fav_films = scrap_user_films('jsalvasoler', st_replica)
    print(fav_films)
