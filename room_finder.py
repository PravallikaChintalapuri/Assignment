import re

import pandas as pd
from dateutil.parser import parse as time_parser

pd.set_option("display.max_columns", 8)
pd.set_option('max_colwidth', 300)

DELIMITER = ","

"""
Assumptions:
    1) If no single room is available for the entire duration, then this algorithm will return None.
    2) If there are more than one room available with same proximity, then this algorithm can return any room. 
"""

def get_rooms_data_frame(room_details_file):
    """
    It simply extract data from input file in a way that every record/line has only one time slot with other details such as room_no, capacity, time_slot (start_time & end_time)
    :param room_details_file: relative path of input data file
    :return: extracted dataframe
    """
    df = pd.DataFrame(columns=["room_no", "capacity", "start_time", "end_time"])
    with open(room_details_file, "r") as f:
        for line_number, line in enumerate(f.readlines()):
            if line.endswith("\n"):
                line = line[:-1]
            delimit_split_array = re.split(",", line)
            if len(delimit_split_array) % 2 != 0:
                raise ValueError("Incorrect data in provided file, number of elements in each row must be even [line_number: {}]".format(line_number))
            room_no = delimit_split_array[0]
            capacity = int(delimit_split_array[1])
            start_time, end_time = [], []
            for index in range(2, len(delimit_split_array), 2):
                start_time.append(time_parser(delimit_split_array[index]).time())
                end_time.append(time_parser(delimit_split_array[index + 1]).time())
            number_of_time_availability_durations = len(start_time)
            df = pd.concat([df, pd.DataFrame(
                {"room_no": [room_no] * number_of_time_availability_durations, "capacity": [capacity] * number_of_time_availability_durations, "start_time": start_time,
                 "end_time": end_time})])
    return df


def transform_data_frame(rooms_data_frame):
    """
    It takes raw input data frame and add new column floor for easy calculation and sort the records/lines by floor number in ascending order
    :param rooms_data_frame: raw input data frame
    :return: transformed dataframe
    """
    rooms_data_frame['floor'] = rooms_data_frame["room_no"].apply(lambda x: int(x.split(".")[0]))
    rooms_data_frame.sort_values(["floor"], inplace=True)
    rooms_data_frame.reset_index(inplace=True, drop=True)
    return rooms_data_frame


def get_closest_room_no(rooms_data_frame, current_floor, team_size, meeting_start_time, meeting_end_time):
    """
    It takes transformed data frame and other details to return closest room number
    :param rooms_data_frame: transformed data frame
    :param current_floor: current_floor where team is sitted
    :param team_size: team size
    :param meeting_start_time: when team wants to start the meeting
    :param meeting_end_time: when team meeting will end
    :return: closest room number [for tie scenarios, it will return any value]
    """
    total_records, _ = rooms_data_frame.shape
    df_with_satisfied_current_floor = rooms_data_frame[
        (rooms_data_frame['floor'] == current_floor) & (rooms_data_frame['capacity'] >= team_size) & (rooms_data_frame['start_time'] <= meeting_start_time) & (
                    meeting_end_time <= rooms_data_frame['end_time'])]
    number_of_rows_in_df_with_satisfied_current_floor_df = df_with_satisfied_current_floor.shape[0]
    if number_of_rows_in_df_with_satisfied_current_floor_df != 0:
        return df_with_satisfied_current_floor.iloc[0, 0]
    else:
        upper_df = rooms_data_frame[
            (rooms_data_frame['floor'] < current_floor) & (rooms_data_frame['capacity'] >= team_size) & (rooms_data_frame['start_time'] <= meeting_start_time) & (
                        meeting_end_time <= rooms_data_frame['end_time'])]
        lower_df = rooms_data_frame[
            (rooms_data_frame['floor'] > current_floor) & (rooms_data_frame['capacity'] >= team_size) & (rooms_data_frame['start_time'] <= meeting_start_time) & (
                        meeting_end_time <= rooms_data_frame['end_time'])]
        total_records_in_upper_df = upper_df.shape[0]
        total_records_in_lower_df = lower_df.shape[0]
        if (total_records_in_lower_df == 0) and total_records_in_upper_df == 0:
            return None
        elif (total_records_in_lower_df == 0):
            return rooms_data_frame.iloc[upper_df.index[-1], 0]
        elif (total_records_in_upper_df == 0):
            return rooms_data_frame.iloc[lower_df.index[0], 0]

        upper_pointer_iter = range(total_records_in_upper_df - 1, -1, -1)
        lower_pointer_iter = range(0, total_records_in_lower_df, 1)
        upper_index = next(upper_pointer_iter)
        lower_index = next(lower_pointer_iter)

        if ((current_floor - upper_df.iloc[upper_index, 4]) <= (lower_df.iloc[lower_index, 4] - current_floor)):
            return upper_df.iloc[upper_index, 0]
        else:
            return lower_df.iloc[lower_index, 0]


def find_closest_meeting_room(requirement, room_details_file="./resources/rooms.csv"):
    """
    It is the main function which executes all the steps (extracting data, transforming data and extracting available meeting room)
    :param requirement: input string
    :param room_details_file: data_file which has list of room details
    :return: closest room number [for tie scenarios, it will return any value]
    """
    current_floor, team_size, meeting_start_time, meeting_end_time = requirement.split(DELIMITER)
    meeting_start_time, meeting_end_time = time_parser(meeting_start_time).time(), time_parser(meeting_end_time).time()
    current_floor = int(current_floor)
    team_size = int(team_size)
    rooms_data_frame = get_rooms_data_frame(room_details_file)
    # print(rooms_data_frame)
    rooms_data_frame = transform_data_frame(rooms_data_frame)
    # print(rooms_data_frame)
    return get_closest_room_no(rooms_data_frame, current_floor=current_floor, team_size=team_size, meeting_start_time=meeting_start_time, meeting_end_time=meeting_end_time)


if __name__ == "__main__":
    print(find_closest_meeting_room("5,8,10:30,11:30"))
