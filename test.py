def parse_value(value):
    if 'OPEN' in value:
        return float('inf')

    # If there's a '/', consider the value after it.
    if '/' in value:
        value = value.split('/')[1]
    print(value)
    # if there is a '###' consider the value before it
    if '###' in value:
        value = value.split('###')[0]
    print(value)

    #remove whitespace from the D.### 

    value = value.strip()

    # Extracting numbers.
    numbers = [int(n) for n in value.split('.') if n.isdigit()]
    if numbers:
        return numbers[-1]
    return None


def sort_interfaces(interfaces):
    for i, interface in enumerate(interfaces):
        value = parse_value(interface[6])
        if value is None:
            user_input = input(
                f"Cannot determine value for {interface[6]}. Please enter a number or type 'open': ").strip().lower()
            if user_input == 'open':
                value = float('inf')
            else:
                value = int(user_input)
        interface.append(value)
    return sorted(interfaces, key=lambda x: x[-1])


def verify_duplicates(sorted_interfaces):
    seen = {}
    for interface in sorted_interfaces:
        if interface[6] in seen:
            user_input = input(f"Please verify: {interface[2]}")
            if not user_input:
                continue
        seen[interface[6]] = True
    return sorted_interfaces


def split_sides(interfaces):
    left, right = [], []
    for i, interface in enumerate(interfaces):
        if (interface[-1] - 1) % 24 < 12:
            left.append(interface)
        else:
            right.append(interface)
    return left, right


def process_patch_panel(sides):
    # Combine right and left interfaces.
    combined = sides[0] + sides[1]

    # Sort interfaces.
    sorted_interfaces = sort_interfaces(combined)

    # Check and verify duplicates.
    verified_interfaces = verify_duplicates(sorted_interfaces)

    # Split sides.
    left, right = split_sides(verified_interfaces)

    # Return as required: right as 0th item and left as 1st.
    return [right, left]


# Test
sides_input = [
    [["Port1", "", "", "", "", "", "D.270 ###39103", "", "", ""],
     ["Port2", "", "", "", "", "", "D.016", "", "", ""],
     ["Port3", "", "", "", "", "", "OPEN", "", "", ""]],
    [["Port4", "", "", "", "", "", "D.270.1", "", "", ""],
     ["Port5", "", "", "", "", "", "270/D.215.13", "", "", ""],
     ["Port6", "", "", "", "", "", "UNKNOWN", "", "", ""],
     ["Port7", "", "", "", "", "", "RM 240 D.215", "", "", ""]]
]

print(process_patch_panel(sides_input))
