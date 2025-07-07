import sys, os.path, glob, re

def get_filename(left_bits_cnt, rem_bits):
    if rem_bits == '':
        return f'alts.{left_bits_cnt}.txt'
    return f'alts.{left_bits_cnt}.{rem_bits}.txt'


def do_regen(total_bits_cnt, selector_bits):
    if total_bits_cnt < 50:
        raise ValueError('Not enough bits')

    left_bits_cnt = total_bits_cnt - 25

    out_fn = get_filename(left_bits_cnt, selector_bits)
    if os.path.exists(out_fn):
        print(f'# {out_fn} already exists, skipping regeneration.')
        return True

    # print(f'LBC: {left_bits_cnt}')

    gave_gen = False


    for base_lbc_cnt in range(left_bits_cnt, 24, -1):
        # print(f'DEBUG: base_lbc_cnt={base_lbc_cnt}, left_bits_cnt={left_bits_cnt}, selector_bits={selector_bits}')
        for rev_i in range(len(selector_bits) -1, -2, -1):
            rem_bits = ''
            if rev_i >= 0:
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

                cmd += f' > {out_fn} &'

                print(cmd)
                gave_gen = True
                break
            if gave_gen:
                break
        if gave_gen:
            break
    if not gave_gen:
        print(f'# Unable to generate {out_fn} from existing files.')
    return gave_gen

if __name__ == '__main__':
    if len(sys.argv) == 1:
        alt_files = []
        for fn in glob.glob('run*.bat'):
            with open(fn) as f:
                alt_files += re.findall(r'alts\.(\d+)\.(\d+)\.txt', f.read())
        alt_files = sorted(set(alt_files))
        
        for (lbc, prefix) in alt_files:
            lbc_i = int(lbc)
            # print(lbc_i - len(prefix))
            do_regen(lbc_i+25, prefix)


    elif len(sys.argv) < 3:
        print('Usage: regen2.py [<total_bits_cnt> <selector_bits>]')
        sys.exit(1)

    else:
        total_bits_cnt = int(sys.argv[1])

        for sbc_arg in range(2, len(sys.argv)):
            selector_bits = sys.argv[sbc_arg]
            do_regen(total_bits_cnt, selector_bits)
        