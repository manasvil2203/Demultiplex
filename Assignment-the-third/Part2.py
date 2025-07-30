#!/usr/bin/env python

import argparse 
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="Demultiplexes four gzip-compressed FASTQ files using index barcodes and categorizes reads into matched, hopped, or unknown.")
    parser.add_argument("-r1", "--read1", help="Specify the fatsa file to be used", required=True)
    parser.add_argument("-r2", "--index1", help="Specify the fatsa file to be used", required=True)
    parser.add_argument("-r3", "--index2", help="Specify the fatsa file to be used", required=True)
    parser.add_argument("-r4", "--read2", help="Specify the fatsa file to be used", required=True)
    return parser.parse_args()

args = get_args()

#Globalize my variables
r1: str = args.read1
r2: str = args.index1
r3: str = args.index2
r4: str = args.read2


#Set for all valid indexes
valid_indexes = {
    "GTAGCGTA", "CGATCGAT", "GATCAAGG",
    "AACAGCGA", "TAGCCATG", "CGGTAATC",
    "CTCTGGAT", "TACCGGAT", "CTAGCTCA",
    "CACTTCAC", "GCTACTCT", "ACGATCAG",
    "TATGGCAC", "TGTTCCGT", "GTCCTAAG",
    "TCGACAAG", "TCTTCGAC", "ATCATGCG",
    "ATCGTGGT", "TCGAGAGT", "TCGGATTC",
    "GATCTTGC", "AGAGTCCA", "AGGATAGC"
}

#Initialize dictionaries for matched and hopped
matched_dict = {}
hopped_dict = {}

#Initialize counters for counting up the total number of reads for hopped and unknown
total_hopped = 0
total_unknown = 0 

#Make a function for reverse complimenting index 2
def reverse_complement(barcode : str) -> str :
        ''' Takes index2 from R3 and outputs its reverse complements'''
        # Define the complement rules
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
        
        # Create an empty string to store the reverse complement
        rev_comp = ""

        # Go through the barcode in reverse order
        for base in reversed(barcode):
            # Look up the complement base and add it to the result
            if base in complement:
                rev_comp += complement[base] 
            else:
                rev_comp += 'N'  # If an unknown base is found, default to 'N'        
        return rev_comp


#Make function for storing 48 file handles for matching dictionary

output_handle_dict = {} #Empty dictionary to store file handles

def get_output_handles(index: str):
    '''Return file handles for writing matched reads for a given index. If handles don’t exist yet, create and store them in a global dictionary'''

    if index not in output_handle_dict: #if it does not exist in the dictionary
        r1_filename = f"{index}_R1.fq" #making R1 file
        r2_filename = f"{index}_R2.fq" #making R2 file
        r1_handle = open(r1_filename, "w") #Opening file for R1
        r2_handle = open(r2_filename, "w") #Opening file for R2
        output_handle_dict[index] = (r1_handle, r2_handle) #Putting in dictionary
    return output_handle_dict[index]


#Initializing list to store each record
r1_record = []
r2_record = []
r3_record = []
r4_record = []

#Opening files for unknown and hopped.
with open("unknown_R1.fq", "w") as unknown_r1, \
     open("unknown_R2.fq", "w") as unknown_r2, \
     open("hopped_R1.fq", "w") as hopped_r1, \
     open("hopped_R2.fq", "w") as hopped_r2:
#Opening all 4 files to read 
    with gzip.open(r1, "rt") as R1, \
         gzip.open(r2, "rt") as R2, \
         gzip.open(r3, "rt") as R3, \
         gzip.open(r4, "rt") as R4: 

        while True:
             # Read 4 lines per file (one FASTQ record)
                r1_record = [R1.readline().strip() for i in range(4)]
                r2_record = [R2.readline().strip() for i in range(4)]
                r3_record = [R3.readline().strip() for i in range(4)]
                r4_record = [R4.readline().strip() for i in range(4)]

                if not r1_record[0] or not r2_record[0] or not r3_record[0] or not r4_record[0]:
                    break

                    
                #print(r1_record)
                # print(r2_record)
                # print(r3_record)
                # print(r4_record)

                #Extracting the sequences and indexes from each file
                read1 = r1_record[1] 
                read2 = r4_record[1]
                index1 = r2_record[1]
                index2 = r3_record[1]

                #print(read1)
                #break

                # Using the reverse_complement function to reverse complement index 2
                index2 = reverse_complement(index2)
                #print(index2)
                
                #Modify the headers of the sequence files
                r1_record[0] = r1_record[0] + f" {index1}-{index2}"
                r4_record[0] = r4_record[0] + f" {index1}-{index2}"

                #print(r4_record[0])
                

                if index1 in valid_indexes and index2 in valid_indexes:
                     if index1 == index2:
                          r1_handle, r2_handle = get_output_handles(index1)
                          r1_handle.writelines(line + "\n" for line in r1_record)
                          r2_handle.writelines(line + "\n" for line in r4_record)

                          # Define the index pair
                          index_pair = (index1, index2)

                          #UPdating count for the dictionary
                          if index_pair in matched_dict:
                            matched_dict[index_pair] += 1  # Increment the count
                          else:
                            matched_dict[index_pair] = 1   # Initialize with 1 if it's the first time seeing it

                     else:
                          #Writing into my files
                          hopped_r1.writelines(line + "\n" for line in r1_record)
                          hopped_r2.writelines(line + "\n" for line in r4_record) 

                           # Define the index pair
                          index_pair = (index1, index2)

                          #UPdating count for the dictionary
                          if index_pair in hopped_dict:
                            hopped_dict[index_pair] += 1  # Increment the count
                          else:
                            hopped_dict[index_pair] = 1   # Initialize with 1 if it's the first time seeing it

                          #Updating counter
                          total_hopped +=1
                else:
                    #Writing into files
                    unknown_r1.writelines(line + "\n" for line in r1_record)
                    unknown_r2.writelines(line + "\n" for line in r4_record)
                    #Updating my total counter
                    total_unknown += 1

# Close all matched file handles
for r1_handle, r2_handle in output_handle_dict.values():
    r1_handle.close()
    r2_handle.close()


#Sorting valid indexes set for a proper order
valid_indexes = sorted(valid_indexes)

#Printing the headerS
#Making sure to leave a gap first
print("".ljust(10) + "".join(idx.rjust(10) for idx in valid_indexes))


#Looping through matched and hopped to extract respective values for the matrix
for row in valid_indexes: #Through each row index
    row_str = row.ljust(10)  #Left align the barcode to width 10

    for col in valid_indexes: #Through each coloumn
        if col == row: #if they match 
            count = matched_dict.get((row, col), 0) #get value from matched dictionary else put zero
        else: #if not 
            count = hopped_dict.get((row, col), 0) #get value from hopped sictionary, if not 0

        row_str += str(count).rjust(10) #convert the count to a string and right align to width 10 
    print(row_str)
 
with open("results.txt", "w") as r:
    #print(matched_dict, file =r)
    total_matched = sum(matched_dict.values())
    print(f"Total no.of matcheded:{total_matched}", file =r)
    #print(hopped_dict, file =r)
    print(f"Total no.of hopped:{total_hopped}", file =r)
    print(f"Total no.of unknown:{total_unknown}", file =r)