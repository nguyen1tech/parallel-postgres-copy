# Parallel Postgres COPY

A simple python script to run Postgres COPY command in parallel, no external packages required.

# How to

## 1. Update the `config.ini` file, eg:

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

## 2. Run

```
python src/main.py
```

# Notes

- Currently only `csv` format is supported.
