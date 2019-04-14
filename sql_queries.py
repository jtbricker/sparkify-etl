""" This module contains string constants which contain SQL scripts for
creating/dropping tables and inserting data into those tables.

These constants are imported by other python scripts in order to perform
the ETL work.
"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
    user_id VARCHAR NOT NULL REFERENCES users(user_id),
    level VARCHAR NOT NULL,
    song_id VARCHAR NOT NULL REFERENCES songs(song_id),
    artist_id VARCHAR NOT NULL REFERENCES artists(artist_id),
    session_id VARCHAR NOT NULL,
    location VARCHAR,
    user_agent VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR PRIMARY KEY, 
    first_name VARCHAR NOT NULL, 
    last_name VARCHAR NOT NULL, 
    gender VARCHAR, 
    level VARCHAR NOT NULL 
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY, 
    title VARCHAR NOT NULL, 
    artist_id VARCHAR NOT NULL REFERENCES artists(artist_id), 
    year INT, 
    duration DECIMAL NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    location VARCHAR, 
    latitude DECIMAL, 
    longitude DECIMAL
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY, 
    hour INT NOT NULL, 
    day INT NOT NULL, 
    week INT NOT NULL, 
    month INT NOT NULL, 
    year INT NOT NULL, 
    weekday INT NOT NULL
);
""")


# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO 
        UPDATE SET 
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            gender = EXCLUDED.gender,
            level = EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO 
        UPDATE SET 
            title = EXCLUDED.title,
            artist_id = EXCLUDED.artist_id,
            year = EXCLUDED.year,
            duration = EXCLUDED.duration
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO 
        UPDATE SET 
            name = EXCLUDED.name,
            location = EXCLUDED.location,
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")


# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id 
FROM songs s 
JOIN artists a on s.artist_id = a.artist_id
WHERE s.title = %s AND a.name = %s AND s.duration = %s
""")

# QUERY LISTS
# Note: We need to create any tables with foreign keys before tables that reference those keys.
#       We also need to drop tables that use foreign keys before tables that have those keys.
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]