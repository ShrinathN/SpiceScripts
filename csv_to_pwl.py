#!/bin/python3
import argparse

'''
This script will convert any given .csv file with a current/voltage waveform with timestamp and convert it to a PWL (piecewise linear) file
'''
parser = argparse.ArgumentParser(description="This script will convert any given .csv file with a current/voltage waveform with timestamp and convert it to a PWL (piecewise linear) file")
parser.add_argument("input_file", type=str, help="Input file name")

#optional functionality
parser.add_argument("-O", "--output", type=str, help="Output file name", required=False)
parser.add_argument("-s", "--start_row", type=int, help="Row where the data starts in the csv file (default = 1)", required=False)
parser.add_argument("-d", "--data", type=int, help="Data column number (default=1)", required=False)
parser.add_argument("-t", "--timestamp", type=int, help="Timestamp column number (default=2)", required=False)
parser.add_argument("-dm", "--data_multiplier", type=str, help="Data multiplier (Giga = 1e12, Mega = 1e9, Milli = 1e-3, No multiplier = 1e0) (default = no multiplier)", required=False)
parser.add_argument("-tm", "--timestamp_multiplier", type=str, help="Timestamp multiplier (No multiplier = 1e0, Milli = 1e-3, Micro = 1e-6) (default = no multiplier)", required=False)
parser.add_argument("-da", "--data_append", type=str, help="String to append after each data sample. Can be used to add a unit (default = nothing)", required=False)
parser.add_argument("-ta", "--time_append", type=str, help="String to append after each timestamp. Can be used to add a unit (default = nothing)", required=False)

parser.add_argument("-of", "--offset", type=str, help="Reset time to start from a given timestamp. Unit is seconds (default = 0s)", required=False)
# parser.add_argument("-st", "--starting_time", type=str, help="New starting time. Unit is seconds (default = 0s)", required=False)

args = parser.parse_args()

#reading csv
f = open(args.input_file, "r")
data = f.read()
f.close()

#splitting into rows
data_rows = data.split()

#copying data into internal buffer
starting_row = 0
if(args.start_row is not None):
    starting_row = args.start_row - 1

#data column
data_col_number = 0
if(args.data is not None):
    data_col_number = args.data - 1

#timstamp column
timestamp_col_number = 0
if(args.timestamp is not None):
    timestamp_col_number = args.timestamp - 1

#getting multiplier for data
data_multiplier = 1e0
if(args.data_multiplier is not None):
    data_multiplier = float(eval(args.data_multiplier))

#getting multiplier for timestamp
timestamp_multiplier = 1e0
if(args.timestamp_multiplier is not None):
    timestamp_multiplier = float(eval(args.timestamp_multiplier))

#getting offset
offset = 0
if(args.offset is not None):
    offset = float(eval(args.offset))

# #getting starting point
# starting_time = 0
# if(args.starting_time is not None):
#     starting_time = eval(args.starting_time)

#getting data_append
data_append = ""
if(args.data_append is not None):
    data_append = args.data_append

#getting time_append
timestamp_append = ""
if(args.time_append is not None):
    timestamp_append = args.time_append

output = ""
if(args.output is not None):
    output_buffer = ""
    output = args.output

#looping through all the data and copying to internal buffer
data_buffer = []
for i in range(starting_row, len(data_rows)):
   temp_raw_data_holder = data_rows[i].split(",")
   temp_data_dict = {"data" : float(temp_raw_data_holder[data_col_number]) * data_multiplier,
                    "timestamp" : float(temp_raw_data_holder[timestamp_col_number]) * timestamp_multiplier
   }
   data_buffer.append(temp_data_dict)

#outputting the data
for i in range(0, len(data_buffer)):
    current_data = data_buffer[i]
    if(offset != 0):
        temp_timestamp = str((current_data["timestamp"] - data_buffer[0]["timestamp"]) + offset)
    else:
        temp_timestamp = str(current_data["timestamp"])


    if(output == ""):
        print(f"{temp_timestamp}{timestamp_append} {str(current_data['data'])}{data_append}")
    else:
        output_buffer += f"{temp_timestamp}{timestamp_append} {str(current_data['data'])}{data_append}\n"

if(output != ""):
    f = open(output, "w")
    f.write(output_buffer)
    f.close()
exit(0)