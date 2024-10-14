import sys
import subprocess

from colorama import Fore, Back, Style

def stderr(out):
    out=str(out) + '\n'
    sys.stderr.write(out)
    sys.stderr.flush()

def bold(text):
    return Style.BRIGHT + Fore.RED + text + Style.RESET_ALL

def cli(line):
    #print(Back.GREEN + 'and with a green background')
    #print(Style.DIM + 'and in dim text')
    #print(Style.RESET_ALL)
    #print('back to normal now')
    stderr( '\nExecute the following:' )
    stderr(f'    {bold(line)}')
def run(line):
    stderr( '\nRunning:')
    stderr(f'    {bold(line)}')
    #stderr('forcing: ' + line)
    subprocess.run( line.split() )
