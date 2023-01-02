import sqlite3


class DatabaseManager:
    '''
    データベース（sqlite3）との接続を行うクラス
    '''

    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statemanet, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statemanet, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict):
        columns_with_types = [
            f'{columns_name} {data_type}' for columns_name, data_type in columns.items()
        ]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({','.join(columns_with_types)});
            '''
        )

    def add(self, table_name: str, data: dict):
        '''
        データベースにレコードを追加
        INSERT INTO {tablename}
        {data,keys}
        VALUES data.values
        '''
        placeholders = ','.join('?'*len(data))
        columns_names = ','.join(data.keys())
        columns_values = tuple(data.values)

        self._execute(statemanet=f'''
            INSERT INTO {table_name}
            ({columns_names})
            VALUES ({placeholders});
            ''', values=columns_values
                      )

    def delete(self, table_name: str, criteria: dict):
        placeholders = [f'{column}=?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(statemanet=f'''
        DELETE FROM {table_name}
        WHERE {delete_criteria}
        ''', values=tuple(criteria.values())
                      )

    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}

        query = f'SELECT * FORM {table_name}'

        if criteria:
            placeholders = [f'{column}=?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += select_criteria
        if order_by:
            query += f'ORDER BY {order_by}'
        return self._execute(statemanet=query, values=tuple(criteria.values()))
