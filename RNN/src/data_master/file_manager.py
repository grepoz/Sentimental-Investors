from pathlib import Path

from data_master import DIRECTORY_NAME


class FileManager:
    directory_name = DIRECTORY_NAME

    @staticmethod
    def compose_filename(params):
        return params.ticker + "_" + params.start_time + "_" + params.end_time

    @staticmethod
    def compose_filename_of_csv(params):
        return FileManager.directory_name + "/" + FileManager.compose_filename(params) + ".csv"

    @staticmethod
    def find_full_datafile_name(token: str, directory: Path) -> Path:
        files = [file for file in directory.glob(f"{token}*.csv")]
        if len(files) != 1:
            raise Exception(f"There should be exactly one data file for {token} in {directory}")
        return files[0]
