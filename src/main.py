import os
from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from time import time

from config import Config, load_config
from copy_cmd import run_copy_cmd


def run_copy_parallel(config: Config) -> None:
    """Runs Postgres COPY command in parallel, the level of parallelism
    is defined in the config.ini file under resource.max_workers.

    Args:
        config (Config): The config.
    """
    start = time()
    inserted_rows = 0
    successes = 0
    failures = 0
    csv_files = [
        os.path.abspath(os.path.join(config.source.data_dir, file))
        for file in os.listdir(config.source.data_dir)
        if file.endswith(".csv")
    ]
    with ProcessPoolExecutor(max_workers=config.resource.max_workers) as executor:
        results = executor.map(run_copy_cmd, csv_files, repeat(config.target))
        for result in results:
            splits = result.split("-")
            if splits[0] == "F":
                failures += 1
            else:
                successes += 1
                inserted_rows += int(splits[1])

    end = time()
    print(f"Processed {len(csv_files)} files took: {end - start} seconds")
    print(f"Sucesses: {successes} files")
    print(f"Failures: {failures} files")
    print(f"Inserted rows: {inserted_rows}")


if __name__ == "__main__":
    # Load config
    app_config = load_config()
    # Run the copy cmd in parallel
    run_copy_parallel(config=app_config)
