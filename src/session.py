import pandas as pd


class Session:
    """
    Class initialized at the beginning of a session. Is an attribute of st.session_state
    """

    def __init__(self):
        self._users = {}
        self._users_df = {}

    def insert_user(self, user_name: str, user_id: int):
        self._users[user_id] = user_name

    def reset_user_df(self, user_id: str):
        self._users_df[user_id] = None

    def insert_user_df(self, user_df: pd.DataFrame, user_id: str):
        self._users_df[user_id] = user_df

    @property
    def users(self):
        return self._users

    @property
    def users_df(self):
        return self._users_df
