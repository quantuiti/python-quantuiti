import argparse
from os import system
from subprocess import Popen, DEVNULL
from multiprocessing import Process
from time import sleep

import sys
import os
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, dir_path)

from quantuiti import run_api

def run_file(file_path):
    system(f'python {file_path}')

def main():
    parser = argparse.ArgumentParser(prog ='quantuiti', 
                                    description ='Quantuiti is a platform designed for automated trading .') 
  
    parser.add_argument('-run', type=str, help="run algorithm")

    args = parser.parse_args() 
  
    

    if args.run:


        file_path = args.run

        threads = list()
        api = Process(target=run_api, daemon=False)
        main = Process(target=run_file,  args=(file_path, ), daemon=False)
        
        api.start()
        main.start()


        api.join()
        main.join()
  
                


       
  
if __name__ == "__main__":
    main()