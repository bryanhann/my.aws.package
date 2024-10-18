import sys
import subprocess

from colorama import Fore, Back, Style

def stderr(txt):
    sys.stderr.write(str(txt) + '\n')
    sys.stderr.flush()

def stdout(txt):
    sys.stdout.write(str(txt) + '\n')
    sys.stdout.flush()

def bold(text):
    return Style.BRIGHT + Fore.RED + text + Style.RESET_ALL

def cli(line):
    stderr( '\nExecute the following:' )
    stderr(f'    {bold(line)}')

def run(line):
    stderr( '\nRunning:')
    stderr(f'    {bold(line)}')
    subprocess.run( line.split() )

def ezrun(line, capture=True, show=False):
    if show:
        stderr(bold(line))
    it=subprocess.run(line.split(), capture_output=capture)
    if capture:
        it.stdout = it.stdout.decode('utf-8')
        it.stderr = it.stderr.decode('utf-8')
    return it

