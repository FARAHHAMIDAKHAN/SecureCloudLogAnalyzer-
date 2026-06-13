from collections import defaultdict

# SPLIT (file ko lines mein divide karna)
def split_file(lines):
    return [line.strip() for line in lines if line.strip()]

# MAP (key-value banانا)
def mapper(line):
    parts = line.split()

    if len(parts) < 5:
        return []

    status = parts[3]
    hour = parts[4]

    return [
        (status, 1),
        (hour, 1)
    ]

# SHUFFLE + REDUCE
def reducer(mapped_data):
    result = defaultdict(int)

    for key, value in mapped_data:
        result[key] += value

    return result

# MAIN MAPREDUCE FUNCTION
def run_mapreduce(file_content):
    lines = split_file(file_content.split("\n"))

    mapped = []

    for line in lines:
        mapped.extend(mapper(line))

    reduced = reducer(mapped)

    return reduced