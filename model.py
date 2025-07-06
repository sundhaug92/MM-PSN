import sys


def main():
    known_bits = sys.argv[1]
    model(known_bits)

def model(known_bits):
    print('Z0', known_bits.count('0'))
    print('O1', known_bits.count('1'))
    s_kb = ''.join(sorted(known_bits))
    print(s_kb, len(s_kb))
    wins, losses = 0, 0
    
    strings = []

    for ones in range(66-24):
        string_to_add = '1' * ones + '0' * (41 - ones)
        string_to_add = ''.join(sorted(string_to_add[:41]))
        # print(len(string_to_add), string_to_add)
        strings.append(string_to_add)

    print('S', len(strings))
    print('S0', len(strings[0]))

    relevant_strings = [s for s in strings if s_kb in s]

    print('RS:', len(relevant_strings))

    for rs in relevant_strings:
        print(rs, rs.count('1'), rs.count('0'))

    wins = len([rs for rs in relevant_strings if rs.count('1') > rs.count('0')])
    losses = len([rs for rs in relevant_strings if rs.count('1') <= rs.count('0')])

    print(f"Wins: {wins}, Losses: {losses}, WL = {wins + losses}, Win Rate: {100 * wins / (wins + losses) if (wins + losses) > 0 else 0:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python model.py <known_bits>")
        sys.exit(1)
    main()
