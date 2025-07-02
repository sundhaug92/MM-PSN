import model

pots = [pf.strip() for pf in open('secrets2.pot', 'r').readlines()]

def get_end_bit_by_length(length):
    pots_by_length = {}
    for pot in pots:
        _, bits = pot.split(':')
        pots_by_length[len(bits)] = bits.strip()

    # print('Pots by length:', pots_by_length)
    if length not in pots_by_length.keys():
        print(f'Assuming 1 for {length}')
        return '1'
    return pots_by_length[length][-1]

def get_current_odds():
    min_length = min(len(pot.split(':')[1]) for pot in pots)
    print('Min length:', min_length)
    max_length = max(len(pot.split(':')[1]) for pot in pots)
    print('Max length:', max_length)
    known_bits = ''
    for i in range(min_length, max_length + 1):
        known_bits += get_end_bit_by_length(i)
    print('Known bits:', known_bits)
    model.model(known_bits)

get_current_odds()