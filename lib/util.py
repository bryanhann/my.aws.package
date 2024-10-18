import sys
import subprocess

from colorama import Fore, Back, Style

def stderr(txt):
    sys.stderr.write(str(txt) + '\n')
    sys.stderr.flush()

def bold(text):
    return Style.BRIGHT + Fore.RED + text + Style.RESET_ALL

def cli(line):
    stderr( '\nExecute the following:' )
    stderr(f'    {bold(line)}')

def run(line):
    stderr( '\nRunning:')
    stderr(f'    {bold(line)}')
    subprocess.run( line.split() )

