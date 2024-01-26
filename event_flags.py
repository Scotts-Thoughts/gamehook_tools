import re

# Constants
BASE_ADDRESS = 0xd7b7
END_ADDRESS = 0xdfff
BITS_PER_BYTE = 8
INPUT_FILE = "C:/Users/scott/OneDrive/Desktop/gold_event_flags.js"
OUTPUT_FILE = 'gold_event_flags.xml'

# Regex to match event, skip, and next lines
event_regex = re.compile(r'^\s*const\s+(EVENT_[A-Z0-9_]+)')
skip_regex = re.compile(r'^\s*const_skip\s*(\d*)')
next_regex = re.compile(r'^\s*const_next\s+\$(\w+)')

# Initialize counters
byte_offset = 0
bit_position = 0

# Open the input and output files
with open(INPUT_FILE, 'r') as infile, open(OUTPUT_FILE, 'w') as outfile:
    # Write the XML header
    outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outfile.write('<root>\n')

    # Process each line in the input file
    for line in infile:
        event_match = event_regex.match(line)
        skip_match = skip_regex.match(line)
        next_match = next_regex.match(line)
        if event_match:
            # Calculate the address and bit position
            address = BASE_ADDRESS + byte_offset
            position = bit_position

            # Convert the event flag name to lowercase
            name = event_match.group(1).lower()

            # Write the XML element
            outfile.write(f'  <property name="{name}" type="bit" address="0x{address:X}" position="{position}" />\n')

            # Update the counters
            bit_position += 1
            if bit_position == BITS_PER_BYTE:
                bit_position = 0
                byte_offset += 1
        elif skip_match:
            # Update the counters by the number of bits to skip
            skip_bits = int(skip_match.group(1)) if skip_match.group(1) else 1
            bit_position += skip_bits
            while bit_position >= BITS_PER_BYTE:
                bit_position -= BITS_PER_BYTE
                byte_offset += 1
        elif next_match:
            # Update the byte offset and bit position by the number of bits to skip
            next_bit_offset = int(next_match.group(1), 16)
            byte_offset = next_bit_offset // BITS_PER_BYTE
            bit_position = next_bit_offset % BITS_PER_BYTE

    # Write the XML footer
    outfile.write('</root>\n')