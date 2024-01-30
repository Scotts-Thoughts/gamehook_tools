import requests
import json
import sys
import datetime

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

def generate_test(prop, game_name, game_version):
    print(f"Generating test for property {prop.get('path')}...")
    path = prop.get('path')
    address = prop.get('address')
    bytes_value = prop.get('bytes')
    bytes_str = f"[{', '.join(map(str, bytes_value))}]" if bytes_value else None
    value = prop.get('value')

    if path is not None:
        test_method = f"""
    [TestMethod]
    public async Task {path.replace('.', '_').replace('[', '_').replace(']', '_')}()
    {{
        await Load_{game_name}({game_version});

        var mapper = await GameHookClient.GetMapperAsync();
    """

        if address and bytes_value:
            test_method += f'\n        mapper.AssertAreEqual("{path}", 0x{address:X}, {bytes_str},'
        if value is not None:
            test_method += f' {json.dumps(value)});'
        else:
            test_method += ' null);'

        test_method += "\n    }\n"

        print(f"Generated test for property {prop.get('path')}")
        return test_method

    print(f"Failed to generate test for property {prop.get('path')}")
    return None

# URL of the server
url = "http://localhost:8085/mapper"

# Fetch the data from the server
data = fetch_data(url)

# Get the game name and version from the command line arguments
game_name = sys.argv[1] if len(sys.argv) > 1 else "GB_PokemonYellow"
game_version = sys.argv[2] if len(sys.argv) > 2 else "0"

if data:
    # Get the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Open the file with the current date in the name
    with open(f'tests/{game_name}_{game_version}_tests_{current_date}.txt', 'w') as f:
        # Generate and write each test
        for prop in data['properties']:
            test = generate_test(prop, game_name, game_version)
            if test:
                f.write(test)
