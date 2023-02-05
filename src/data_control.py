import pandas as pd
import yaml
from datetime import datetime
from pathlib import Path


class DataControl:
    def __init__(self):
        self._project_root = self.get_project_root()
        self._data_dir = f'{self._project_root}/data'

        self._users_filepath = f'{self._data_dir}/users.yaml'
        self._users_in_db = self.read_yaml(self._users_filepath)['users_in_db']
        self._films_by_user_filepath = f'{self._data_dir}/films_by_user.csv'
        self._films_by_user = pd.read_csv(f'{self._films_by_user_filepath}')

    @staticmethod
    def read_yaml(filepath):
        with open(filepath) as file:
            structure = yaml.load(file, Loader=yaml.FullLoader)
        return structure

    def check_user_is_in_db(self, user_name):
        return user_name in self._users_in_db

    def get_user_films(self, user_name):
        return self._films_by_user[self._films_by_user.user == user_name]

    def add_user_to_db(self, user_name):
        self._users_in_db.append(user_name)
        self.write_users_to_db()

    def insert_table_in_db(self, user_name, table):
        table['user'] = user_name
        assert len(table.user.unique()) == 1, 'Table to insert has more than one user'
        assert table.user.values[0] not in set(self._films_by_user.user.tolist()), \
            'User to insert already in films by user table'
        self._films_by_user = pd.concat([self._films_by_user, table])

        self.write_films_by_user_to_db()

    def write_users_to_db(self):
        with open(self._users_filepath, 'w') as file:
            documents = yaml.dump({'users_in_db': self._users_in_db}, file)

    def write_films_by_user_to_db(self):
        self._films_by_user.to_csv(self._films_by_user_filepath, index=False)

    def write_back_copy(self):
        timestamp = datetime.now().strftime(format='%Y-%m-%d_%H.%M')
        self._films_by_user.to_csv(f'{self._data_dir}/films_by_user_backcopy_{timestamp}.csv', index=False)
        with open(f'{self._data_dir}/users_backcopy_{timestamp}.yaml', 'w') as file:
            documents = yaml.dump({'users_in_db': self._users_in_db}, file)

    def erase_data_base(self, password):
        assert password == 'jsalva_admin_1234', 'Incorrect password'
        self.write_back_copy()

        self._users_in_db = ['sentinel']
        self._films_by_user.drop(self._films_by_user.index, inplace=True)

        self.write_users_to_db()
        self.write_films_by_user_to_db()

    @staticmethod
    def get_project_root() -> Path:
        """Get the project root filepath"""
        return Path(__file__).parent.parent


if __name__ == '__main__':
    data_control = DataControl()
    data_control.erase_data_base('jsalva_admin_1234')
