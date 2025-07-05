import sys, os.path, glob

def get_filename(left_bits_cnt, rem_bits):
    if rem_bits == '':
        return f'alts.{left_bits_cnt}.txt'
    return f'alts.{left_bits_cnt}.{rem_bits}.txt'


def do_regen(total_bits_cnt, selector_bits):
    if total_bits_cnt < 50:
        raise ValueError('Not enough bits')

    left_bits_cnt = total_bits_cnt - 25

    if os.path.exists(get_filename(left_bits_cnt, selector_bits)):
        return True

    # print(f'LBC: {left_bits_cnt}')

    gave_gen = False

    for base_lbc_cnt in range(left_bits_cnt, 24, -1):
        for rev_i in range(len(selector_bits) -1, -1, -1):
            rem_bits = selector_bits[:rev_i]

            from_fn = get_filename(base_lbc_cnt, rem_bits)
            # print(f'Checking {from_fn} for {selector_bits}...')
            if os.path.exists(from_fn):
                cmd = ''
                if selector_bits == rem_bits:
                    cmd = f'cat {from_fn} '
                else:
                    cmd = f'rg "^{selector_bits}" {from_fn} '
                bits_to_add_cnt = left_bits_cnt - base_lbc_cnt
                
                if bits_to_add_cnt > 0:
                    sed_bits = [f'\\1{bin(i)[2:].zfill(bits_to_add_cnt)}' for i in range(1<<(bits_to_add_cnt))]
                    # print(bits_to_add_cnt, sed_bits)
                    cmd += r" | sed -E 's/(.*)/" + '\\n'.join(sed_bits) + "/g'"

                cmd += f' > alts.{left_bits_cnt}.{selector_bits}.txt &'

                print(cmd)
                gave_gen = True
                break
    
    return gave_gen

if __name__ == '__main__':
    if len(sys.argv) == 1:
        for fn in glob.glob('alts.*.*.txt'):
            left_bits_cnt, rem_bits, _ = fn.split('.', maxsplit=3)[1:]
            # if rem_bits is not a number, skip
            if not rem_bits.isdigit():
                continue
            for next_bit in ['0', '1']:
                do_regen(25 + int(left_bits_cnt), rem_bits + next_bit)
    elif len(sys.argv) < 3:
        print('Usage: regen2.py [<total_bits_cnt> <selector_bits>]')
        sys.exit(1)

    else:
        total_bits_cnt = int(sys.argv[1])

        for sbc_arg in range(2, len(sys.argv)):
            selector_bits = sys.argv[sbc_arg]
            do_regen(total_bits_cnt, selector_bits)
        