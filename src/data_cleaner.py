# Extract numbers from a string
# Return 0 if no number found

import re

def clean_number(text):
    match = re.search(r"\d+\.\d+|\d+",text)
    if match:
        value = match.group()
    else:
        value = 0

    return value






