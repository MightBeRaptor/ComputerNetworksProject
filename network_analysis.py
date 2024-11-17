import pandas as pd
import time
import os

# function to obtain start time before file transfer
def start_time():
    return time.time()

# function to initially create dataframe
def initialize_stats_dataframe():
    columns = ["file_name", "file_size", "transfer_time", "data_rate"]
    dataframe = pd.DataFrame(columns=columns)
    dataframe.to_csv("statistics_dataframe.csv", index=False)

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

    # read csv into dataframe
    stats_dataframe = pd.read_csv("statistics_dataframe.csv")

    # add statistics into dataframe
    stats_dataframe = pd.concat([stats_dataframe, pd.DataFrame([new_stats])], ignore_index=True)

    # use dataframe for updated csv
    stats_dataframe.to_csv("statistics_dataframe.csv", index=False)

