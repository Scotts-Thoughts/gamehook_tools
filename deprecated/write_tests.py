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

def generate_test(prop):
    path = prop.get('path')
    address = prop.get('address')
    bytes_value = prop.get('bytes')
    bytes_str = f"[{', '.join(map(str, bytes_value))}]" if bytes_value else None
    value = prop.get('value')
    if path and address and bytes_value and value:
        test_method = f"""
    [TestMethod]
    public async Task {path.replace('.', '_').replace('[', '_').replace(']', '_')}()
    {{
        await Load_GB_PokemonYellow(6);

        var mapper = await GameHookClient.GetMapperAsync();

        mapper.AssertAreEqual("{path}", 0x{address:X}, {bytes_str}, {json.dumps(value)});
    }}
    """
        return test_method
    return None

# URL of the server
url = "http://localhost:8085/mapper"

# Fetch the data from the server
data = fetch_data(url)
if data:
    # Open the file
    with open('tests.txt', 'w') as f:
        # Generate and write each test
        for prop in data['properties']:
            try:
                test = generate_test(prop)
                if test:
                    f.write(test)
                    print(f"Generated test for property {prop.get('path')}")
                    if prop.get('path') == 'input_a':
                        print("Generated test for input_a property")
            except Exception as e:
                print(f"Error generating test for property {prop}: {e}")
else:
    print("Failed to retrieve data from the server.")