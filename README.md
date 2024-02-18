# Parallel Postgres COPY

A simple python script to run Postgres COPY command in parallel, no external packages required.

## Motivation

As we know, when we want to load a large amount of data into Postgres we usually use the COPY command and here is an example command to load `songs.csv` file to the `songs` table: `\COPY songs FROM '../data/songs.csv' WITH DELIMITER ',' CSV HEADER;`. But how about if we have many CSV files and want to run COPY in parallel to speed things up?

Let's say we have many songs splited cross mulitple `songs_*.csv` files under `/home/data` folder and we want to load these data into the `songs` table in Postgres:

```
ls /home/data
 - songs_01.csv
 - songs_02.csv
 ...
```

Normally, we run the COPY command for each `songs.csv` file but it's too much manual and seqential.

**Solution**: The idea is to load a whole data folder rather than individual files and utilize the multi-processing power for speed things up.

## How to

### 1. Update the `config.ini` file, eg:

```
[Source]:
  data_dir = /home/data/parallel-postgres-copy/datasets
[Target]:
  hostname = localhost
  port = 5432
  user = postgres
  password = changeme
  database = copy-test-db
  schema = music
  table = songs
[Resource]
  max_workers = 3   --> The number of processes, parallelism
```

### 2. Run

```
python src/main.py
```

## Notes

- Currently only `csv` format is supported.
