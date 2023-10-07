import re

def match_dynamic_url(input_string, url_to_match):
    # Escape special characters in the input_string and convert it to a regex pattern
    pattern = re.escape(input_string)
    
    # Replace the placeholders (e.g., :u, :x) with regex capture groups
    pattern = re.sub(r'\\:([a-zA-Z_][a-zA-Z0-9_]*)', r'(?P<\1>[^/]+)', pattern)
    
    # Add anchors to the pattern to ensure it matches the entire string
    pattern = f'^{pattern}$'

    # Attempt to match the URL using the regex pattern
    match = re.match(pattern, url_to_match)

    if match:
        # If there's a match, extract the captured values into a dictionary
        captured_values = match.groupdict()
        return captured_values
    else:
        return None

def extract_variables(input_string, url_to_match):
    captured_values = match_dynamic_url(input_string, url_to_match)
    
    if captured_values:
        # Filter out the captured values that were originally placeholders
        variables = {key: value for key, value in captured_values.items() if key not in ['prefix']}
        return variables
    else:
        return None

# Example usage:
input_string = '/:prefix/:u/string/:x/'
url_to_match = '/admin/dashboard/more/user123/string/42/'
variables = extract_variables(input_string, url_to_match)

if variables:
    print("Variables extracted:")
    print(variables)
else:
    print("No match.")
