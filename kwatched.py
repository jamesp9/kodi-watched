#!/usr/bin/env python

import sqlite3


class SqliteDB(object):
    def connect(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except Exception as e:
            print('Database connection failed: {}'.format(e))

    def cursor(self):
        """Return database cursor"""
        return self.conn.cursor()

    def execute(self, query, parameters=None):
        cursor = self.cursor()
        if parameters:
            cursor.execute(query)
        else:
            cursor.execute(query, parameters)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def table_info(self, table_name):
        cursor = self.cursor()
        cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
        return cursor.fetchall()


def get_watched_rows(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM files WHERE playCount IS NOT NULL')
    return cursor.fetchall()


if __name__ == '__main__':
    db = SqliteDB()
