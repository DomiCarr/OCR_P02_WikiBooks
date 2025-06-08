#----------------------------------------------------------------------
# data_cleaner.py
#
# Utility functions for text processing and data cleaning.
#----------------------------------------------------------------------

# Standard library imports - built-in modules that come with Python
import re

def clean_number(text):
    """
    Extract the first number found in the input string.
    Supports integers and decimals.
    Returns the number as a string, or 0 if no number is found.

    Regex explanation:
    - \d+      : matches one or more digits (0-9)
    - \.       : matches a literal dot (decimal point)
    - \d+      : matches one or more digits (decimal part)
    """
    match = re.search(r"\d+\.\d+|\d+", text)
    if match:
        value = match.group()
    else:
        value = 0
    return value

def clean_repository_name(name):
    """
    Normalize a string to create a repository-friendly name:
    - Convert to lowercase
    - Replace any non-alphanumeric characters or underscores with hyphens
    - Remove leading/trailing hyphens

    Regex explanation:
    - [\W_] matches any character that is NOT a letter or digit (non-alphanumeric) and also underscores,
    - + means one or more occurrences of these characters,
    - so all groups of such characters are replaced by one hyphen.
    """
    return re.sub(r'[\W_]+', '-', name.lower()).strip('-')



