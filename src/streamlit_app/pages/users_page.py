import streamlit as st
from scraping import check_user_existance, scrap_user_films
from streamlit_app.utils import custom_write, endline


def handle_input_user(user_id):
    user_name = st.session_state[f'input_user_{user_id}']
    st.session_state.session.insert_user(user_name, user_id)
    st.session_state.session.reset_user_df(user_id)


def users_page():
    base = st.container()

    col_1, col_2 = base.columns(2)

    col_1.text_input('User 1', value=st.session_state.user_1, key='input_user_1', on_change=handle_input_user,
                     kwargs={'user_id': 1})
    col_2.text_input('User 2', value=st.session_state.user_2, key='input_user_2', on_change=handle_input_user,
                     kwargs={'user_id': 2})

    for user_id, col in zip((1, 2), (col_1, col_2)):
        user_name = st.session_state.session.users.get(user_id, '')
        if user_name != '':
            in_db = st.session_state.data_control.check_user_is_in_db(user_name)
            if in_db:
                col.success(f'The user {user_name} is already in our database :)')
                if st.session_state.session.users_df[user_id] is None:
                    user_df = st.session_state.data_control.get_user_films(user_name)
                    st.session_state.session.insert_user_df(user_df, user_id)

                col.table(st.session_state.session.users_df[user_id])

            else:
                exists = check_user_existance(user_name)
                if not exists:
                    col.error(f'The user {user_name} does not exist')
                    continue

                col.success(f'The user {user_name} exists')
                if st.session_state.session.users_df[user_id] is None:
                    custom_write(col, 'Getting all-time watched movies list...', align='center',
                                 color=st.session_state.text_color)

                    df = scrap_user_films(user_name, col)
                    st.session_state.session.users_df[user_id] = df

                    st.session_state.data_control.add_user_to_db(user_name)
                    st.session_state.data_control.insert_table_in_db(user_name, table=df)
                endline(col)
                col.table(st.session_state.session.users_df[user_id])


if __name__ == '__main__':
    users_page()
