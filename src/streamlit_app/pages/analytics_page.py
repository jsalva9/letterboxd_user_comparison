import streamlit as st
from streamlit_app.utils import compute_cosine_similarity, custom_write, endline

import plotly.graph_objects as go


def users_basic_info(place):
    col_1, col_2 = place.columns(2)
    for col, user_id in zip((col_1, col_2), (1, 2)):
        user_name = st.session_state.session.users[user_id]

        custom_write(col, user_name, align='center', bold=True, size='x-large', color=st.session_state.text_color)
        endline(col)

    df_1, df_2 = st.session_state.session.users_df[1], st.session_state.session.users_df[2]
    columns = place.columns(9)
    user_1_cols = columns[:4]
    user_2_cols = columns[5:]

    films_1 = len(df_1.index)
    films_2 = len(df_2.index)
    avg_1 = df_1[~df_1.rating.isna()].rating.mean()
    avg_2 = df_2[~df_2.rating.isna()].rating.mean()

    user_1_cols[0].metric('Watched movies', value=films_1)
    user_2_cols[0].metric('Watched movies', value=films_2)
    user_1_cols[1].metric('Rated movies', value=len(df_1[~df_1.rating.isna()].index))
    user_2_cols[1].metric('Rated movies', value=len(df_2[~df_2.rating.isna()].index))
    user_1_cols[2].metric('Average rating', value="{:.2f}".format(avg_1))
    user_2_cols[2].metric('Average rating', value="{:.2f}".format(avg_2))
    # TODO: fav movies list
    user_1_cols[3].write('Favorite films')
    user_2_cols[3].write('Favorite films')
    user_1_fav_films = df_1.loc[df_1.favorite == 1, 'film'].values.tolist()
    user_2_fav_films = df_2.loc[df_2.favorite == 1, 'film'].values.tolist()
    for id in range(1, 3):
        fav_films = eval(f'user_{id}_fav_films')
        col = eval(f'user_{id}_cols[3]')
        for film in fav_films:
            custom_write(col, f'- {film}', size='small', color=st.session_state.text_color)
        endline(col, 2)

    columns = place.columns(7)
    user_1_cols = columns[:3]
    user_2_cols = columns[4:]

    user_name_1 = st.session_state.session.users[1]
    user_name_2 = st.session_state.session.users[2]

    merged_table = df_1.rename(columns={'user': 'user_name_1'}).merge(
        df_2.rename(columns={'user': 'user_name_2'}), how='outer', on=['film', 'film_id'])

    films_2_not_1 = len(merged_table[(merged_table.user_name_2 == user_name_2) &
                                     (merged_table.user_name_1.isna())].index)
    films_1_not_2 = len(merged_table[(merged_table.user_name_1 == user_name_1) &
                                     (merged_table.user_name_2.isna())].index)

    fig_1, fig_2 = get_plots(films_1, films_1_not_2, films_2, films_2_not_1)

    custom_write(user_1_cols[0], f'{user_name_2} movies watched by {user_name_1}', align='center', size='small',
                 color=st.session_state.text_color)
    custom_write(user_2_cols[0], f'{user_name_1} movies watched by {user_name_2}', align='center', size='small',
                 color=st.session_state.text_color)
    user_1_cols[0].plotly_chart(fig_1, use_container_width=True)
    user_2_cols[0].plotly_chart(fig_2, use_container_width=True)

    value_1 = merged_table[(merged_table.user_name_1 == user_name_1) &
                           (merged_table.user_name_2 == user_name_2) &
                           (~merged_table.rating_x.isna())].rating_x.mean()
    value_2 = merged_table[(merged_table.user_name_1 == user_name_1) &
                           (merged_table.user_name_2 == user_name_2) &
                           (~merged_table.rating_y.isna())].rating_y.mean()
    custom_write(user_1_cols[1], f'{user_name_1} rating of {user_name_2} films', size='small', align='center',
                 color=st.session_state.text_color)
    custom_write(user_2_cols[1], f'{user_name_2} rating of {user_name_1} films', size='small', align='center',
                 color=st.session_state.text_color)
    user_1_cols[1].metric("", value="{:.2f}".format(value_1), delta="{:.2f}".format(- avg_2 + value_1))
    user_2_cols[1].metric("", value="{:.2f}".format(value_2), delta="{:.2f}".format(- avg_1 + value_2))

    custom_write(user_1_cols[1], f'Watched {films_2 - films_2_not_1} films of {user_name_2}', size='small',
                 align='center', color=st.session_state.text_color)
    custom_write(user_2_cols[1], f'Watched {films_1 - films_1_not_2} films of {user_name_1}', size='small',
                 align='center', color=st.session_state.text_color)

    custom_write(user_1_cols[2], f'{user_name_1} rating of {user_name_2} favorite films', size='small', align='center',
                 color=st.session_state.text_color)
    custom_write(user_2_cols[2], f'{user_name_2} rating of {user_name_1} favorite films', size='small', align='center',
                 color=st.session_state.text_color)

    value_1 = merged_table[(merged_table.favorite_y == 1) & (~merged_table.rating_x.isna())].rating_x.mean()
    fav_2_own_rating = merged_table[(merged_table.favorite_y == 1) & (~merged_table.rating_y.isna())].rating_y.mean()
    value_2 = merged_table[(merged_table.favorite_x == 1) & (~merged_table.rating_y.isna())].rating_y.mean()
    fav_1_own_rating = merged_table[(merged_table.favorite_x == 1) & (~merged_table.rating_x.isna())].rating_x.mean()

    user_1_cols[2].metric('', value="{:.2f}".format(value_1), delta="{:.2f}".format(value_1 - fav_2_own_rating))
    seen = len(merged_table[(merged_table.favorite_y == 1) & (merged_table.user_name_1 == user_name_1)].index)
    rating = len(merged_table[(merged_table.favorite_y == 1) & (~merged_table.rating_x.isna())].index)
    custom_write(user_1_cols[2], f'Watched {seen} / 4 films', size='small', align='center',
                 color=st.session_state.text_color)
    custom_write(user_1_cols[2], f'Rated {rating} / 4 films', size='small', align='center',
                 color=st.session_state.text_color)

    user_2_cols[2].metric('', value="{:.2f}".format(value_2), delta="{:.2f}".format(value_2 - fav_1_own_rating))
    seen = len(merged_table[(merged_table.favorite_x == 1) & (merged_table.user_name_2 == user_name_2)].index)
    rating = len(merged_table[(merged_table.favorite_x == 1) & (~merged_table.rating_y.isna())].index)
    custom_write(user_2_cols[2], f'Watched {seen} / 4 films', size='small', align='center',
                 color=st.session_state.text_color)
    custom_write(user_2_cols[2], f'Rated {rating} / 4 films', size='small', align='center',
                 color=st.session_state.text_color)


def get_plots(films_1, films_1_not_2, films_2, films_2_not_1):
    arg_dict = {'textinfo': "value+percent+label", 'labels': ['Watched', 'Unwatched'], 'showlegend': False,
                'automargin': False, 'marker': {'colors': [st.get_option('theme.secondaryBackgroundColor'), 'white']}}
    size = 150
    plot_layout_dict = {'autosize': False, 'width': size, 'height': size, 'margin': dict(l=0, r=0, b=0, t=0)}
    fig_1 = go.Figure(go.Pie(values=[films_2 - films_2_not_1, films_2_not_1], **arg_dict))
    fig_2 = go.Figure(go.Pie(values=[films_1 - films_1_not_2, films_1_not_2], **arg_dict))
    fig_1.update_layout(**plot_layout_dict)
    fig_2.update_layout(**plot_layout_dict)
    return fig_1, fig_2


def user_comparison(place):
    df_1, df_2 = st.session_state.session.users_df[1], st.session_state.session.users_df[2]

    common_movies = set(df_1.film.unique()).intersection(set(df_2.film.unique()))

    custom_write(place, 'Users similarity', align='center', color=st.session_state.text_color, size='x-large')
    endline(place)
    cols = place.columns(6)
    cols[1].metric('Movies in common', value=len(common_movies))

    sim_1 = compute_cosine_similarity(df_1, df_2, watched=True, rated=False)
    sim_2 = compute_cosine_similarity(df_1, df_2, watched=True, rated=True)
    sim_3 = compute_cosine_similarity(df_1, df_2, watched=False, rated=True)

    cols[2].metric('Watched films similarity', value=f'{"{:.2f}".format(sim_1 * 100)}%')
    cols[3].metric('Watched films and ratings similarity', value=f'{"{:.2f}".format(sim_2 * 100)}%')
    cols[4].metric('Ratings similarity', value=f'{"{:.2f}".format(sim_3 * 100)}%')


def analytics_page():
    base = st.container()

    df_1 = st.session_state.session.users_df.get(1, None)
    df_2 = st.session_state.session.users_df.get(1, None)
    if df_1 is None or df_2 is None:
        base.error('Missing inputs. Make sure you introduce two existing Letteboxd users')
        return

    users_info = base.container()
    base.markdown("***")
    analytics = base.container()

    users_basic_info(users_info)
    user_comparison(analytics)


if __name__ == '__main__':
    analytics_page()
