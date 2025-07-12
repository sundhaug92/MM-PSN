from datetime import datetime, timedelta
import random

start_time = datetime.now()
start_bit_cnt = 60
hash_rate = 4_400_000_000

def do_experiment():
    end_date = start_time

    bit_solved = start_bit_cnt

    while bit_solved < 65:
        bits_known = (end_date - datetime(2025, 7, 1)).days + 1
        difficulty = random.randint(1, 2 ** (bit_solved - bits_known))
        # print(f"Difficulty: {difficulty} for {bit_solved} bits")
        delta_time = timedelta(seconds=difficulty / hash_rate)
        if delta_time.days > 1:
            continue
        # print(f"Delta time: {delta_time} for {bit_solved} bits")
        end_date += delta_time
        bit_solved += 1
        # print()

    print((end_date - start_time).total_seconds())

if __name__ == "__main__":
    for i in range(10_000):
        do_experiment()