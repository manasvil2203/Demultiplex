#!/usr/bin/env python
import bioinfo
import gzip
import matplotlib.pyplot as plt

#Define my variable in argparse
import argparse 
def get_args():
    parser = argparse.ArgumentParser(description="A program that takes a fasta fie and gives another fasta file with each records longest reads")
    parser.add_argument("-f", "--file", help="Specify the fatsa file to be used", required=True)
    parser.add_argument("-l", "--length", help="Specify the length of the list to be created", required=True)
    return parser.parse_args()  

args = get_args()

#Globalize my variables
f: str = args.file
l: int = int(args.length)


def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    for i in range(l):
        lst.append(value)
    return lst

my_list: list = []
my_list = init_list(my_list)


def populate_list(file: str) -> tuple[list, int]:
    """This function will take a fastq file. Loop through every record and convert quality scores to integers. It will keep an ongoing sum of that in a list.Returns the list and counter of total number of lines in the file."""
    my_list: list = []
    my_list = init_list(my_list)
    with gzip.open(file , "rt") as fh:
        for num_line,line in enumerate(fh):
            line = line.strip()
            if num_line%4 == 3:
                for score_index, score_letter in enumerate(line):
                    my_list[score_index] += bioinfo.convert_phred(score_letter)
            
    return my_list, num_line + 1


#Populating my list
my_list, num_lines = populate_list(f)


# Calculating and printing my means
print(f'{"# Base Pair"}\t{"Mean Quality Score"}')
for score_index,score in enumerate(my_list):
    my_list[score_index] = score/(num_lines/4)


positions = list(range(len(my_list)))  # x-axis: base positions

# Create the plot
plt.plot(positions, my_list, marker= '*', color= "purple")  
plt.title("Mean Phred Quality Score by Base Position")
plt.xlabel("Base Position in Read")
plt.ylabel("Mean Quality Score")
plt.grid(True)
plt.savefig("hist_quality.png")



