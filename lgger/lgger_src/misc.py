from os import getcwd, environ
from os.path import isfile
from typing import Optional


# Function to check if character is a dot/period "."
def is_period(input_char):
    return input_char == "."


# Function to check if character is a minus/dash "-"
def is_minus(input_char):
    return input_char == "-"


# Return number of occurrences of comparison function in string
def count_x(compare_func, input_string):
    return len(list(filter(compare_func, input_string)))


# Checks if string is a valid number (negative, float or number)
def valid_number(input_string: str):
    # Remove redundant spaces (strip spaces from front and back)
    input_string = input_string.strip()

    # Check if string is empty
    if len(input_string) == 0:
        return False

    # Check if string is empty
    for char in input_string:
        if (char != "-") and (char != ".") and (not char.isdigit()):
            return False

    # String has no more than 1 "-" signs
    if count_x(is_minus, input_string) > 1:
        return False

    # String has a "-" sign at the start, if "-" is in the string
    if (count_x(is_minus, input_string) == 1) and (input_string[0] != "-"):
        return False

    # Check if the string has any digits
    if count_x(str.isdigit, input_string) == 0:  # post-refactor
        return False

    # Check if string has more than one dot "."
    if count_x(is_period, input_string) > 1:
        return False

    # Check if string starts or ends in a dot "."
    if (input_string[0] == ".") or (input_string[-1] == "."):
        return False

    # Check if string has a dot "." after negative sign "-"
    if (input_string[0] == "-") and (input_string[1] == "."):
        return False

    if count_x(is_period, input_string) == 1:
        return float(input_string)
    return int(input_string)


# Format directory path to standard.
# Current rules are:
#   - Replace backslash with forward slash
#   - Add forward slash at end of string if none is present
def normalize_dir(dir_str: Optional[str]):
    if not dir_str:
        return ''
    dir_str = dir_str.replace('\\', '/')
    if dir_str[-1] != '/':
        dir_str += '/'
    if dir_str[:2] == "./":
        dir_str = dir_str.replace("./", environ.get('LGGER_CWD', getcwd()))
    return dir_str


# Format file name to standard.
# Current rules are:
#   - Append "_n" to string, where n is the number of files with the same file name
#     Example: file.txt will be file_1.txt if file.txt already exists in dir_str
def normalize_filename(dir_str, file_str, **kwargs):
    file_cnt = 1
    file_str_bak = file_str
    if count_x(is_period, file_str):
        while isfile(dir_str + file_str):
            file_str = f"_{str(file_cnt)}.".join(file_str_bak.rsplit('.', 1))
            file_cnt += 1
    else:
        while isfile(dir_str + file_str):
            file_str = f"{file_str_bak}_{file_cnt}"
            file_cnt += 1
    return file_str
