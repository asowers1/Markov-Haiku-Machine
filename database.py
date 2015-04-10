__author__ = 'Andrew Sowers'

import sqlite3
import re
import os
from collections import defaultdict

class haikuTweetDB(object):

    def __init__(self, dbfile):
        """
        Connect to the database specified by dbfile.  Assumes that this
        dbfile already contains the tables specified by the schema.
        """
        self.dbfile = dbfile
        self.cxn = sqlite3.connect(dbfile)
        self.cur = self.cxn.cursor()


        self.execute("""CREATE TABLE IF NOT EXISTS tweetCollection (
                                 id  INTEGER PRIMARY KEY,
                                 text VARCHAR,
                                 screen_name VARCHAR,
                                 created_at VARCHAR,
                                 source VARCHAR
                            );""")
                            
        self.execute("""CREATE TABLE IF NOT EXISTS haikuCollection (
                                 id  INTEGER PRIMARY KEY,
                                 text VARCHAR,
                                 screen_name VARCHAR,
                                 created_at VARCHAR,
                                 source VARCHAR
                            );""")



    def _quote(self, text):
        """
        Properly adjusts quotation marks for insertion into the database.
        """

        text = re.sub("'", "''", text)
        return text

    def _unquote(self, text):
        """
        Properly adjusts quotations marks for extraction from the database.
        """

        text = re.sub("''", "'", text)
        return text


    def execute(self, sql):
        """
        Execute an arbitrary SQL command on the underlying database.
        """
        res = self.cur.execute(sql)
        self.cxn.commit()

        return res
        
        
    def insertHaiku(self, text, screen_name, created_at, source):
	    """ 
	    Inserts text that is assumed to be a haiku into the haikuCollection table
	    """
	    sql = """INSERT INTO haikuCollection (text, screen_name, created_at, source) VALUES ('%s', '%s', '%s', '%s')""" % (self._quote(text), self._quote(screen_name), self._quote(created_at), self._quote(source))
	    res = self.execute(sql)
	    return self.cur.lastrowid
    

    def insertTweet(self, text, screen_name, created_at, source):
        """
        Inserts a tweet into the tweetCollection table, returning the id of the
        row.
        """

        sql = """INSERT INTO tweetCollection (text, screen_name, created_at, source) VALUES ('%s', '%s', '%s', '%s')""" % (self._quote(text), self._quote(screen_name), self._quote(created_at), self._quote(source))

        res = self.execute(sql)
        return self.cur.lastrowid

   