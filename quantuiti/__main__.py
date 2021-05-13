import argparse
from os import system
from subprocess import Popen, DEVNULL
from multiprocessing import Process
from time import sleep
import sys

sys.path.insert(1, '/home/dylan/Desktop/quantuiti/python-quantuiti')

from quantuiti import run_api

def main():
    parser = argparse.ArgumentParser(prog ='quantuiti', 
                                    description ='Quantuiti is a platform designed for automated trading .') 
  
    parser.add_argument('-run', type=str, help="run algorithm")

    args = parser.parse_args() 
  
    

    if args.run:

        def run_file(file_path):
            system(f'python {file_path}')
            

        file_path = args.run

        threads = list()

        main = Process(target=run_file,  args=(file_path, ), daemon=True)
        main.start()

        api = Process(target=run_api, daemon=True)
        api.start()

        main.join()
        api.join()
  
                


       
  
if __name__ == "__main__":
    main()