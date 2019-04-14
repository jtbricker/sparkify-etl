import os
import glob
import uuid
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime

def process_song_file(cur, filepath):
    """Read in the data from a single song data file and insert the
    relevant data into the song and artists tables.

    Arguments:
        cur {cursor} -- psycopg2 object that allows for interactions with the DB
        filepath {str} -- file location
    """

    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = list(df[['song_id','title','artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)

def process_log_file(cur, filepath):
    """Read in the data from a single log data file and insert the relevant data into the time, 
    users, songs, artists and songplays tables.

    Arguments:
        cur {cursor} -- psycopg2 object that allows for interactions with the DB
        filepath {str} -- file location
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = (df.ts/1000).apply(datetime.fromtimestamp)
    
    # insert time data records
    time_data = (t.apply(lambda x: x.isoformat()), t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame({k:v for (k,v) in zip(column_labels, time_data)})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            # If artist and song id not in tables, add them
            artistid = uuid.uuid4().hex[:18].upper()
            songid = uuid.uuid4().hex[:18].upper()
            cur.execute(artist_table_insert, (artistid, row.artist, None, None, None))
            cur.execute(song_table_insert, (songid, row.song, artistid, None, row.length))

        # insert songplay record
        songplay_data = songplay_data = (datetime.fromtimestamp(row.ts/1000), \
                                         row.userId, row.level, songid, artistid, \
                                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Parses a given directory for data files and uses the provided function to extract
    the data and insert it into an appropriate database table
    
    Arguments:
        cur {cursor} -- psycopg2 object representing connection to PostgreSQL DB
        conn {connection} -- psycopg2 object that allows for interactions with the DB
        filepath {str} -- file location
        func {function(cursor, filepath)} -- A function extracts the data from a given filepath,
        tranforms the data into an apropriate format and uses the cursor to insert the data into a db table
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ Extracts the song and log data and insert data into the relevant tables
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
