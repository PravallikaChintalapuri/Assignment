from room_finder import find_closest_meeting_room

"""
This is a test file, which currently has 8 test cases, you can add as per your convenience.
"""


data_file_index_list = [1, 2, 2, 2, 2, 2, 2, 2]
expected_output_of_test_cases = ["9.547", "5.547", "5.123", None, "8.43", "8.43", "5.123", "9.547"]
input_for_test_cases = ["5,8,10:30,11:30", "5,8,10:30,11:30", "5,8,1:30,2:30", "5,9,1:30,2:30", "9,4,11:30,12:30", "9,7,11:30,12:30", "9,8,11:30,12:30", "9,6,13:45,14:30"]

assert len(data_file_index_list) == len(expected_output_of_test_cases) == len(input_for_test_cases), "Invalid setup!!"

for test_case_number, (input_requirement, input_data_index, expected_output) in \
        enumerate(zip(input_for_test_cases, data_file_index_list, expected_output_of_test_cases), 1):
    formatted_input_data_file_number = str(input_data_index).zfill(3)
    formatted_test_case_number = str(test_case_number).zfill(3)
    test_data_file_name = "./resources/{}_test_case_no_rooms.csv".format(formatted_input_data_file_number)
    actual_output = find_closest_meeting_room(input_requirement, test_data_file_name)
    if (expected_output == actual_output):
        print("Test Case: {} :: passed!".format(formatted_test_case_number))
    else:
        print("Test Case: {} :: FAILED << Expected:{}, Actual:{} >>".format(formatted_test_case_number, expected_output, actual_output))
