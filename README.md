# Assignment
Python Challenge

Please explain: how you solved the problem and how it would behave based on the different parameters (number of team members, longer meeting times, many rooms with random booking times). 

Answer: I have used pandas library for this code for analysis
Assumptions:
    1) If no single room is available for the entire duration, then this algorithm will return None.
    2) If there are more than one room available with same proximity, then this algorithm can return any room. example: If the team resides on 3 floor and the meeting room is available on 4 and 2 floor, it can return any room
 
 I have divided this code into 3 parts where in first part is to extract the data from the rooms.csv file in the resources folder, 2nd part is to transform the data into a data frame in the ascending order and returns the transformed data frame and the 3rd part is to return the closest room number
 
 
How would you test the program to ensure it always produced the correct results?
I have written a test.py file to ensure the outcomes in different scenarios, there are 8 test scenarios and if the input doesn't match the output the test case fails

