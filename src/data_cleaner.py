# Extract numbers from a string - Return 0 if no number found

# Standard library imports - built-in modules that come with Python
import re

def clean_number(text):
    match = re.search(r"\d+\.\d+|\d+",text)
    if match:
        value = match.group()
    else:
        value = 0

    return value


def clean_repository_name(name):
    return re.sub(r'[\W_]+', '-', name.lower()).strip('-')




