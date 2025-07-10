import json, os, sys, time, subprocess

def main():
    while True:
        j = None
        try:
            with open('jobs.json') as f:
                j = json.load(f)

                os.chdir('C:\\Users\\Sundh\\Desktop\\pentest\\hashcat-6.2.5')
                jobs_done = []
                for job in j:
                    if job in jobs_done:
                        continue
                    (digest, left, right) = job
                    cmd = r'hashcat -m 1400 -a 1 --potfile-path C:\Users\Sundh\Desktop\dev\PeterSchmidtNielsen\secrets2.pot '
                    cmd += f'{digest} {left} {right}'
                    subprocess.run(cmd, shell=True)
                    jobs_done.append(job)

                os.chdir('C:\\Users\\Sundh\\Desktop\\dev\\PeterSchmidtNielsen')
        except FileNotFoundError as e:
            print(e)
            time.sleep(5)
        except json.JSONDecodeError as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(0)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)