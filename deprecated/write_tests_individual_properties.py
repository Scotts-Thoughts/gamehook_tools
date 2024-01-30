import requests
import json

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def generate_tests(parent_path, properties):
    test_methods = []

    for prop in properties:
        if prop['path'].startswith(parent_path):
            path = prop['path']
            address = prop['address']
            bytes_value = prop['bytes']
            bytes_str = f"[{', '.join(map(str, bytes_value))}]"
            value = prop['value']
            test_method = f"""
        [TestMethod]
        public async Task {path.replace('.', '_').replace('[', '_').replace(']', '_')}()
        {{
            await Load_GB_PokemonYellow(6);

            var mapper = await GameHookClient.GetMapperAsync();

            mapper.AssertAreEqual("{path}", 0x{address:X}, {bytes_str}, {json.dumps(value)});
        }}
        """
            test_methods.append(test_method)

    return "\n".join(test_methods)

# URL of the server
url = "http://localhost:8085/mapper"

# Fetch the data from the server
data = fetch_data(url)
if data:
    # Filter properties that belong to player.team[0]
    player_team_0_properties = [p for p in data['properties'] if p['path'].startswith('player.team.0')]

    # Generate test methods
    parent_path = 'player.team.0'
    test_methods = generate_tests(parent_path, player_team_0_properties)
    print(test_methods)
else:
    print("Failed to retrieve data from the server.")
