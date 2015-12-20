#!/usr/bin/env python

import unittest

import kwatched


class TestKWatched(unittest.TestCase):

    def setUp(self):
        self.db = kwatched.SqliteDB()
        self.db.connect(':memory:')
        self.cur_a = self.db.cursor()

        # Create table
        self.sql = (
            'CREATE TABLE files '
            '( idFile integer primary key, idPath integer, strFilename text, '
            'playCount integer, lastPlayed text, dateAdded text) '
            )
        self.cur_a.execute(self.sql)

        # Insert test rows
        self.num_watched = 2
        self.sql = (
            "INSERT INTO files "
            "(idFile, idPath, strFilename, playCount, lastPlayed, dateAdded) VALUES "
            "(1, 3, 'I.like.programming', 1, '2015-03-01 09:00:00', '2015-01-01 09:00:00'), "
            "(5, 7, 'Make.reusable.code.', 3, '2015-03-01 09:00:00', '2015-01-01 09:00:00'), "
            "(10, 8, 'Testing.is.great', NULL, NULL, '2015-04-01 13:30:00')"
            )
        self.cur_a.execute(self.sql)

        self.updated_list = [
            ('I.like.programming', 2, '2015-08-13 21:15:00'),
            ('Make.reusable.code.', 3, '2015-03-01 09:00:00'),
            ]

        self.db.commit()

    def tearDown(self):
        self.db.close()
        pass

    def test_table_files_exists(self):
        self.cur_a.execute('SELECT * FROM files')
        rows = self.cur_a.fetchall()
        self.assertGreaterEqual(len(rows), 1)

    def test_select_watched(self):
        rows = kwatched.get_watched_rows(self.db)
        self.assertEqual(len(rows), self.num_watched)

    def test_get_table_info(self):
        rows = kwatched.get_table_info(self.db, 'files')
        expected = [
            (0, 'idFile', 'integer', 0, None, 1),
            (1, 'idPath', 'integer', 0, None, 0),
            (2, 'strFilename', 'text', 0, None, 0),
            (3, 'playCount', 'integer', 0, None, 0),
            (4, 'lastPlayed', 'text', 0, None, 0),
            (5, 'dateAdded', 'text', 0, None, 0)]
        self.assertAlmostEqual(rows, expected)

    def test_find_rewatched_video(self):
        prev_list = kwatched.get_watched_rows(self.db)

        current_list = [
            ('I.like.programming', 1, '2015-08-13 21:15:00'),
            ]

        result = kwatched.find_rewatched_video(prev_list, current_list)
        self.assertEqual(result, self.updated_list)

    def test_update_files_table(self):
        kwatched.update_files_table(self.db, self.updated_list)
        updated_watched = kwatched.get_watched_rows(self.db)
        self.assertEqual(updated_watched, self.updated_list)


if __name__ == '__main__':
    unittest.main()
