import requests
import json
import argparse

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def generate_single_test_method(parent_path, properties):
    test_method = """
    [TestMethod]
    public async Task Yellow_Active_Pokemon()
    {
        await Load_GB_PokemonYellow(9);

        var mapper = await GameHookClient.GetMapperAsync();
    """

    for prop in properties:
        if prop['path'].startswith(parent_path):
            path = prop['path']
            address = prop.get('address')
            bytes_value = prop.get('bytes')
            value = prop['value']

            if address is not None and bytes_value is not None:
                bytes_str = f"[{', '.join(map(str, bytes_value))}]"
                test_method += f"""
        mapper.AssertAreEqual("{path}", 0x{address:X}, {bytes_str}, {json.dumps(value)});"""
            elif address is not None:
                test_method += f"""
        mapper.AssertAreEqual("{path}", 0x{address:X}, {json.dumps(value)});"""
            else:
                test_method += f"""
        mapper.AssertAreEqual("{path}", {json.dumps(value)});"""

    test_method += "\n    }\n"
    return test_method

# Set up the argument parser
parser = argparse.ArgumentParser(description='Generate test methods based on a given parent path.')
parser.add_argument('parent_path', type=str, help='The parent path to filter properties by.')

# Parse the command line arguments
args = parser.parse_args()

# URL of the server
url = "http://localhost:8085/mapper"

# Fetch the data from the server
data = fetch_data(url)
if data:
    # Filter properties based on the user-defined parent path
    filtered_properties = [p for p in data['properties'] if p['path'].startswith(args.parent_path)]

    # Generate a single test method
    test_method = generate_single_test_method(args.parent_path, filtered_properties)
    print(test_method)
else:
    print("Failed to retrieve data from the server.")
