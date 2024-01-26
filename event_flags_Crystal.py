# import re
# import sys

# # Starting address and position
# address = 0xda7d
# position = 0

# # Open the file
# with open(sys.argv[1], 'r') as f:
#     # Process each line
#     for line in f:
#         line = line.strip()
#         if line.startswith('const '):
#             # This is a constant definition
#             event_name = line[6:]
#             if event_name != 'skip':
#                 # Generate XML property
#                 print(f'<property name="{event_name.lower()}" type="bool" address="0x{address:04X}" bit="{position}" />')
#             # Update position and possibly address
#             position += 1
#             if position == 8:
#                 position = 0
#                 address += 1
#         elif line.startswith('const_next '):
#             # This is a const_next directive
#             skip_bits = int(line[11:])
#             skip_bytes, position = divmod(skip_bits, 8)
#             address += skip_bytes
#             if position >= 8:
#                 position -= 8
#                 address += 1

import re
import sys

# Starting address and position
address = 0xda7d
position = 0

# Open the file
with open(sys.argv[1], 'r') as f:
    # Process each line
    for line in f:
        line = line.strip()
        if line.startswith('const '):
            # This is a constant definition
            event_name = line[6:]
            if event_name != 'skip':
                # Generate XML property
                print(f'<property name="{event_name.lower()}" type="bool" address="0x{address:04X}" bit="{position}" />')
            # Update position and possibly address
            position += 1
            if position == 8:
                position = 0
                address += 1
        elif line.startswith('const_next '):
            # This is a const_next directive
            position = int(line[11:])
            address = 0xda7d + position // 8
            position = position % 8
        elif line.startswith('; Unused'):
            # This is an unused directive, do nothing
            continue