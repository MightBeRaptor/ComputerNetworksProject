import pandas as pd
import time
import os

FILE_STORAGE_PATH = "./file_storage"

# function to obtain start time before file transfer
def start_time():
    return time.time()

# function to initially create dataframe
def initialize_stats_dataframe():
    file_path = os.path.join(FILE_STORAGE_PATH, "statistics_dataframe.csv")
    if not os.path.exists(file_path):
        columns = ["file_name", "file_size", "transfer_time", "data_rate"]
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

# function to obtain and log the statistics for analysis in a .csv file
def log_statistics(starting_time, file_path):
    # finds end time and calculates transfer time
    ending_time = time.time()
    transfer_time = ending_time - starting_time

    # finds file size
    file_size = os.path.getsize(file_path)

    # find data rate
    if transfer_time > 0:
        data_rate = file_size / transfer_time
    else:
        data_rate = 0

    # establishes desired statistics to be logged
    new_stats = {
        "file_name": os.path.basename(file_path),
        "file_size": file_size,
        "transfer_time": transfer_time,
        "data_rate": data_rate
    }

    # appends new statistics into csv
    stats_df = pd.DataFrame([new_stats])
    stats_file_path = os.path.join(FILE_STORAGE_PATH, "statistics_dataframe.csv")
    stats_df.to_csv(stats_file_path, mode="a", header=not os.path.exists(stats_file_path),index=False)