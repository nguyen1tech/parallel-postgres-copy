# pylint: disable=line-too-long

import os
import subprocess
from time import time
from config import TargetConfig


def run_copy_cmd(data_file: str, target_config: TargetConfig) -> None:
    """Runs Postgres COPY command.

    Args:
        data_file (str): The data file.
        target_config (TargetConfig): The Postgres table config to load data into.
    """
    start = time()
    copy_cmd = f"""PGPASSWORD="{target_config.password}" \
        psql -h "{target_config.hostname}" \
            -p "{target_config.port}" \
            -U "{target_config.user}" \
            -d "{target_config.database}" \
            -c "\\COPY {target_config.schema}.{target_config.table} FROM '{data_file}' WITH DELIMITER ',' CSV HEADER;"
        """
    process_id = os.getpid()
    result = subprocess.run(
        [copy_cmd], shell=True, capture_output=True, text=True, check=False
    )
    if result.stderr:
        print(
            f"[Process ID]:{process_id} - Run COPY on data file: {data_file}, status: Failed, exit_code: {result.returncode}, error: {result.stderr}"
        )
        return "F-0"

    inserted_rows = int(result.stdout.split(" ")[1])
    print(
        f"[Process ID]:{process_id} - Run COPY on data file: {data_file}, status: Succeeded, exit_code: {result.returncode}, output: {inserted_rows} rows, took: {time() - start} seconds"
    )
    return f"S-{inserted_rows}"
