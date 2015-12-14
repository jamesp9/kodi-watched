#!/usr/bin/env python

import sqlite3
import unittest


class TestKWatched(unittest.TestCase):

    def setUp(self):
        self.conn_a = sqlite3.connect(':memory:')
        self.cur_a = self.conn_a.cursor()

        # Create table
        self.sql = (
            'CREATE TABLE files '
            '( idFile integer primary key, idPath integer, strFilename text, '
            'playCount integer, lastPlayed text, dateAdded text) '
            )
        self.cur_a.execute(self.sql)

        # Insert test rows
        self.sql = (
            "INSERT INTO files "
            "(idFile, idPath, strFilename, playCount, lastPlayed, dateAdded) VALUES "
            "(1, 3, 'I.like.programming', 1, '2015-03-01 09:00:00', '2015-01-01 09:00:00'), "
            "(5, 7, 'Make.reusable.code.', 3, '2015-03-01 09:00:00', '2015-01-01 09:00:00'), "
            "(10, 8, 'Testing.is.great', NULL, NULL, '2015-04-01 13:30:00')"
            )
        self.cur_a.execute(self.sql)

        self.conn_a.commit()

    def tearDown(self):
        self.conn_a.close()
        pass

    def test_table_files_exists(self):
        self.cur_a.execute('SELECT * FROM files')
        rows = self.cur_a.fetchall()
        self.assertGreaterEqual(len(rows), 1)

    def test_select_watched(self):
        self.cur_a.execute('SELECT * FROM files WHERE playCount IS NOT NULL')
        rows = self.cur_a.fetchall()
        self.assertEqual(len(rows), 2)


if __name__ == '__main__':
    unittest.main()
