import re
import sys
import time
import random
import string
import argparse
import datetime

class Variables():
    def __init__(self):
        self.final_password = 0
        self.weak = string.ascii_letters
        self.normal = string.ascii_letters + string.digits
        self.strong = string.ascii_letters + string.digits + string.punctuation
        self.parser = argparse.ArgumentParser("Password Generator", description='A simple command line password generator by itsthooor', usage='password_generatory.py -l LENGTH [1 or higher] -m MODE [weak, normal, strong] -sm SAFEMODE [(y)es or (n)o]', epilog='Github -> https://github.com/itsthooor')
        self.parser.add_argument('-l' ,'--length', dest='length' , metavar='LENGTH', help='Length of the password', type=int, default=8)
        self.parser.add_argument('-m' ,'--mode' , dest='mode', metavar='MODE', help='Sets the passwords security level', type=str, default='normal', choices=['weak', 'normal', 'strong'])
        self.parser.add_argument('-sm' ,'--safemode', dest='safemode' , metavar='SAFEMODE', help='Activate to let an algorythm make the password more secure. Needs much more time the higher the length. Preferred use with good CPU', type=str, default='n')
        self.args = self.parser.parse_args()

class Timers():
    def __init__(self):
        self.timer_start = None
        self.timer_time = None

variables = Variables()
timer1 = Timers()
timer2 = Timers()

def timer_start(mode):
    if mode == 'generate':
        timer1.timer_start = time.perf_counter()
    if mode == 'print':
        timer2.timer_start = time.perf_counter()
 
def timer_stop(mode):
    if mode == 'generate':
        timer_gen_end = time.perf_counter()
        timer_gen_eq = timer_gen_end - timer1.timer_start
        timer1.timer_time = str(datetime.timedelta(seconds=round(timer_gen_eq)))
    if mode == 'print':
        timer_print_end = time.perf_counter()
        timer_print_eq = timer_print_end - timer2.timer_start
        timer2.timer_time = str(datetime.timedelta(seconds=round(timer_print_eq)))

def generate(mode, chars, length, safemode):
    timer_start('generate')
    if safemode in ('Yes', 'yes', 'Y', 'y'):
        print('Safemode activated!')
        password = ''.join(random.choice(chars) for x in range(length))
        if mode == 'normal':
            intgen = re.findall(r'\d+', str(password))
            while len(intgen) < (length / 3):
                password = ''.join(random.choice(chars) for x in range(length))
                intgen = re.findall(r'\d+', str(password))
        if mode == 'strong':
            lettergenerator = re.findall("[A-Z]+", str(password))
            intgen = re.findall(r'\d+', str(password))
            while len(lettergenerator) < (length / 3):
                password = ''.join(random.choice(chars) for x in range(length))
                lettergenerator = re.findall("[A-Z]+", str(password))
            while len(intgen) < (length / 3):
                password = ''.join(random.choice(chars) for x in range(length))
                intgen = re.findall(r'\d+', str(password))
        variables.final_password = password
    else:
        password = ''.join(random.choice(chars) for x in range(length))
        variables.final_password = password
    timer_stop('generate')
    timer_start('print')
    return password

if __name__ == "__main__":
    if variables.args.mode == 'weak':
        print('Weak Password with', variables.args.length,'characters =', generate('weak', variables.weak, variables.args.length, variables.args.safemode), '\nGenerated in', timer1.timer_time)
    elif variables.args.mode == 'normal':
        print('Normal Password with', variables.args.length,'characters =', generate('normal', variables.normal, variables.args.length, variables.args.safemode), '\nGenerated in', timer1.timer_time)
    else:
        print('Strong Password with', variables.args.length,'characters =', generate('strong', variables.strong, variables.args.length, variables.args.safemode), '\nGenerated in', timer1.timer_time)
    timer_stop('print')
    print('Time for printing:',timer2.timer_time)
    answer = input('Wanna print it to a text file? [y/n] -> ')
    if answer == 'y':
        with open('password.txt', 'w') as f:
            f.write(str(variables.final_password))
    f.close()