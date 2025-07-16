import json

min_left_side_bits = None
extra_bits = 0

with open('jobs.json') as f:
    j = json.load(f)

    for job in j:
        digest, left, right = job
        left_side_bits_str = left.split('.')[1]
        left_side_bits = int(left_side_bits_str)
        left_side_prefix = left.split('.')[2]

        if min_left_side_bits is None:
            min_left_side_bits = left_side_bits

        if left_side_bits < min_left_side_bits:
            continue

        for i in range(left_side_bits - min_left_side_bits + 1):
            print(f'python3 regen2.py $(({left_side_bits}+25)) {left_side_prefix}' + '{0..1}' * i)
