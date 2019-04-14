# Sparkify Song Play Analysis ETL Pipeline

## Purpose
The purpose of this project is to create a pipeline that is able to 
extract data from log files, transform the data to match required formats,
and load the transformed data into postgres database tables to allow for
efficient data analysis by the music startup, Sparkify.

### Busines Value
Sparkify expects to write queries against this database to gain insights
into the behavior and trends of its users in order to better serve them 
in the future.

## Database Schema
The database tables are laid our in a star schema, with central songplays fact table:

### songplays
`songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent`

and 4 supporting dimension tables, users, songs, artists, and time:

### users
`user_id, first_name, last_name, gender, level`

### songs
`song_id, title, artist_id, year, duration`

### artists
`artist_id, name, location, lattitude, longitude`

### time
`start_time, hour, day, week, month, year, weekday`

The star schema design allows for efficient querying of the songplay data across many different dimensons
(see [Example Queries](#Example\ Queries))

## ETL Pipeline
The ETL pipeline works in 3 steps:

1. Extract- The file structure is walked, and relevant files are read in a pandas dataframes
1. Transform- The required data is pulled out of the dataframes and formatted as required by the database.  In addition, any additional required data is pulled in from external sources.
1. Load - The formatted data is inserted into their destination tables

### ETL Notes
The song/artist data and the songplay data (which references songs/artists) were loaded from different data sources (`data/song_data` and `data/log_data`, respectively). These example data sources are just examples and therefore not all songs/artists referenced in the songplays logs are represented.

Therefore, when a song/artist combination were not found in the data, new rows in these tables were added to make the data as complete as possible.

## Example Queries

Question: How many users are listening to the Backstreet Boys on Thursdays?

```SQL
SELECT COUNT(*) 
FROM songplays sp
JOIN artists a on sp.artist_id = a.artist_id
JOIN time t on sp.start_time = t.start_time
WHERE a.name = 'Backstreet Boys' AND  t.weekday = 3
```

Question: Who are the top 5 users with the most listening time?

```SQL
SELECT TOP 5 u.*, SUM(s.duration) as total_time
FROM songplays sp
JOIN artists a on sp.artist_id = a.artist_id
JOIN users u on sp.user_id = u.user_id
GROUP BY u.user_id
ORDER BY total_time DESC
```

## Setup
1. Install PostgreSQL
1. Open pgAdmin
    1. Add user with appropriate permissions (ability to create database)
    1. Create database `studentdb`, a default table that we will use to make an initial connection to our server.
1. Run `pip install -r requirements.txt` to install required libraries from `requirements.txt`
1. Run `python create_tables.py` to create the `sparkifydb` database and the empty tables.
2. Run `python etl.py` to run the etl pipeline, reading the data and populating the tables created in the previous step.