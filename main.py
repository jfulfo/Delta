import os
import subprocess
import sys

def main(cli):
    args = ' '.join(sys.argv[1:])
    if cli:
        os.system(f'python3 cli.py {args}')
    else:
        pass

if __name__ == "__main__":
    main(True)
    #cli = input("Is this a CLI app? (y/n): ")
    #if cli.lower() == "y":
    #    main(True)
    #else:
    #    main(False)


