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
    csv_files = [
        os.path.abspath(os.path.join(config.source.data_dir, file))
        for file in os.listdir(config.source.data_dir)
        if file.endswith(".csv")
    ]
    with ProcessPoolExecutor(max_workers=config.resource.max_workers) as executor:
        executor.map(run_copy_cmd, csv_files, repeat(config.target))


if __name__ == "__main__":
    # Load config
    app_config = load_config()
    # Run the copy cmd in parallel
    start = time()
    run_copy_parallel(config=app_config)
    end = time()
    print(f"Took {end - start} seconds")
