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
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


def get_watched_rows(db):
    '''
    Fetch rows of watched videos
    '''
    cursor = db.cursor()
    cursor.execute('SELECT strFilename, playCount, lastPlayed FROM files '
                   'WHERE playCount IS NOT NULL')
    return cursor.fetchall()


def get_table_info(db, table_name):
    cursor = db.cursor()
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    return cursor.fetchall()


def update_files_table(db, update_list):
    '''
    Update DB row for watched videos
    '''
    cursor = db.cursor()

    for str_filename, play_count, last_played in update_list:
        sql = ('UPDATE files '
               'SET playCount = ?, lastPlayed = ? '
               'WHERE strFilename = ?')
        cursor.execute(sql, (play_count, last_played, str_filename))
    db.commit()


def find_rewatched_video(previous_list, current_list):
    '''
    Find videos that have been rewatched.
    Return the tuple list of rows to update.
    '''
    update_rows = []
    for previous in previous_list:
        update = ()
        for current in current_list:
            if previous[0] == current[0]:
                update = (previous[0], previous[1] + current[1], current[2])
                break

        if len(update) >= 1:
            update_rows.append(update)
            update = ()
        else:
            update_rows.append(previous)

    return update_rows


if __name__ == '__main__':
    db = SqliteDB()
