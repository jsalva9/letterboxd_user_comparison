import math

import pandas as pd


def custom_write(place, text: str, align: str = 'left', color: str = 'black', bold: bool = False, italic: bool = False,
                 size: str = 'medium'):
    """
    Args:
        place: streamlit container or column
        text: the text to be displayed
        align: can be ['center', 'left', 'right']
        color: supported by CSS color keywords
        bold: whether to write in bold style
        italic: whether to write in italic style
        size: font size. Default is 'medium'
    """
    if bold:
        text = "<strong>" + text + "</strong>"
    if italic:
        text = "<em>" + text + "</em>"

    place.markdown(f'<div style="text-align: {align}; color: {color}; font-size: {size}"> {text} </div>',
                   unsafe_allow_html=True)


def endline(place, times=1):
    for _ in range(times):
        place.markdown(f'##')


def compute_cosine_similarity(df_1, df_2, watched: bool, rated: bool):
    aux_1 = df_1 if watched else df_1.dropna(subset=['rating'])
    aux_2 = df_2 if watched else df_2.dropna(subset=['rating'])

    c_1 = {x.film: 1 if not rated or pd.isna(x.rating) else x.rating for x in aux_1.itertuples()}
    c_2 = {x.film: 1 if not rated or pd.isna(x.rating) else x.rating for x in aux_2.itertuples()}

    terms = set(c_1).union(set(c_2))
    dot_product = sum(c_1.get(k, 0) * c_2.get(k, 0) for k in terms)
    norm_1 = math.sqrt(sum(c_1.get(k, 0) ** 2 for k in terms))
    norm_2 = math.sqrt(sum(c_2.get(k, 0) ** 2 for k in terms))

    return dot_product / (norm_1 * norm_2)
