import os
import subprocess
from time import time
from config import DatabaseConfig, TargetConfig


def run_copy_cmd(
    database_config: DatabaseConfig, target_config: TargetConfig, data_file: str
) -> None:
    start = time()
    copy_cmd = f"""PGPASSWORD="{database_config.password}" \
        psql -h "{database_config.hostname}" \
            -p "{database_config.port}" \
            -U "{database_config.user}" \
            -d "{database_config.database}" \
            -c "\COPY {target_config.schema}.{target_config.table} FROM '{data_file}' WITH DELIMITER ',' CSV HEADER;"
        """
    process_id = os.getpid()
    result = subprocess.run([copy_cmd], shell=True, capture_output=True, text=True)
    if result.stderr:
        print(
            f"[Process ID]:{process_id} - Run COPY on data file: {data_file}, status: Failed, exit_code: {result.returncode}, error: {result.stderr}"
        )
    else:
        inserted_rows = result.stdout[:-1]
        print(
            f"[Process ID]:{process_id} - Run COPY on data file: {data_file}, status: Succeeded, exit_code: {result.returncode}, output: {inserted_rows} rows, took: {time() - start} seconds"
        )
