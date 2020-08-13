'''
    Tashlin Reddy
    August 2020
    Parse Units and Values from CSV column 
'''



import re 


def parse_string(some_string):
    # find the values: 
        # any whole number or decimal 
        # positive or negative
    #find the unit
        # the alpha characters
    processed_string = preprocess(some_string)
    unit = " ".join(re.findall("[a-zA-Z]+", processed_string))
    value = " ".join(re.findall(r"-?\d*\.{0,1}\d+", processed_string))
    
    return value, unit


def preprocess(some_string):
    #quick string clean up, remove commas and spaces
    some_string = some_string.replace(" ", "").replace(",", "")
    return some_string




""" uncomment below for quick test """
# test_string = "-500.1 metres"
# print(parse_string(test_string))

