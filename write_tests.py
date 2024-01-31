import requests
import json
import sys
import datetime
import re

# Get the current date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

def fetch_data(url):
    print("Fetching data...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def generate_assertion(prop):
    path = prop.get('path')
    address = prop.get('address')
    bytes_value = prop.get('bytes')
    bytes_str = f"[{', '.join(map(str, bytes_value))}]" if bytes_value else None
    value = prop.get('value')

    if path is not None:
        # Replace any characters that are not letters, numbers, or underscores with underscores
        sanitized_path = re.sub(r'\W', '_', path)

        assertion = ''
        if address and bytes_value:
            assertion = f'mapper.AssertAreEqual("{path}", 0x{address:X}, {bytes_str},'
        elif value is not None:
            assertion = f'mapper.AssertAreEqual("{path}",'
        else:
            return None

        assertion += f' {json.dumps(value)});'
        return assertion

    return None

# URL of the server
url = "http://localhost:8085/mapper"

# Fetch the data from the server
print("Fetching data...")
data = fetch_data(url)

# Get the game name and version from the command line arguments
game_name = sys.argv[1] if len(sys.argv) > 1 else "GB_PokemonYellow"
game_version = sys.argv[2] if len(sys.argv) > 2 else "0"

if data:
    print("Data fetched successfully.")
    # Get the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Open the file with the current date in the name
    with open(f'tests/{game_name}_{game_version}_tests_{current_date}.txt', 'w') as f:
        print("Generating assertions...")
        # Generate and write each assertion
        assertions = []
        for prop in data['properties']:
            assertion = generate_assertion(prop)
            if assertion:
                assertions.append(assertion)

        print("Assertions generated. Writing to file...")
        # Generate the full test method
        test_method = f"""
[TestMethod]
public async Task All_Properties()
{{
    await Load_{game_name}({game_version});

    var mapper = await GameHookClient.GetMapperAsync();
"""
        for assertion in assertions:
            test_method += f'\n    {assertion}'

        test_method += "\n}\n"
        f.write(test_method)

    print("File written successfully.")
