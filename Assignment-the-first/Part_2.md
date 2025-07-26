### Problem: 
I have 4 different files which contain my biological read 1, biological read 2, index 1 and index. Beware that index 2 is reverse complemented, so I need to make sure that they it is fixed. I need to add the indexes to the end of each header of each record. Now I need to check if each barcode is even valid, if it is valid, I need to check if it is a matched index or hopped index. If it is not valid I just assign it to unkown(because regardless of it not meeting my qulaity score threshold or being incorrectly sequenced with N, it will be in unkknown). I then need to write all these into their respective files. There should be a total of 52 files. 48 of which are going to be the matched index pairs.

### Informative Output
1. I am going to first table all possible matched index pair.This will help show us how many reads were assigned to each valid sample and in detecting imbalance across barcodes...maybe.
2. Next, a table of all observed mismatched index pairs. This will be useful for detecting index hopping, checking which barcode pairs are most frequently misassigned and estimating contamination rate.
3.  Table for unknown sequences, to help diagnose sequencing errors.
4. Maybe have a summary stats table? Total read pairs processed, Total matched index-pairs (all samples), Total index-hopped reads, Total unknown reads, Percent index-hopped, Percent unknown. Just for an overview

### Pseudocode
I would first argparse all 4 of my fastq files.Then I would globalize said variable.
```
    Say the variables are the following:
    R1 - for bio read 1
    R2 - for index 1 
    R3 - for index 2
    R4 - for bio read 2
```
```
I would make a set with all the valid indexes
```

I would also initialize things here...like:
```
    Initialize dictionary for counting the possible permuatations
    Initialize file for index hopping R1 and R2
    Initialize file for unkown R1 and R2
```
```
Initialize dictionary for storing matched file handles

def get_output_handles(index1: str, index2: str):
    """
    Returns file handles for writing matched reads corresponding to a given index-pair.
    
    If the file handles for the given (index1, index2) pair have not yet been created,
    this function opens the corresponding R1 and R2 output files in write mode, stores
    them in a global dictionary, and returns the handles. If they already exist in the dictionary, it just gives those file handles.
    """
    returns (r1_handle, r2_handle)
    Input: "ACGTA" "ACGTA"
    Output: (ACGTA_R1.fq, ACGTA_R1.fq )
```
```
  Initialize counters for:
            Each valid index-pair.
            Total index-hopped pairs.
            Total unknown pairs.

```
```
Then I would open all 4 of my files using with open in the 'r' mode
    Then in a while True loop:
        I would read each record(so loop through 4 lines) of each file.
        So I would have 4 different variables for each readline.

        Then break out of the loop if the line does not exist anymore

        Then I would extract  index 1 from R2 and index2 from R3 and also read1 from R1 and read2 from R4
        and then the quality scores for the indexes

        I would then reverse complement index2 from R3
            def reverse_complement(barcode : str) -> str :
            ''' Takes index2 from R3 and outputs its reverse complements"
            return rev_comp

            Input: "AGCTG"
            Output: "TCGAC"

        Then I would modify both my Fastq headers and add my barcodes to the end in the order(index1- reverse compliment(index2)) 
            Increment the permutations dictionary using the barcode pair if it exists and add one if it does not exist.
            
         Now I would check if my indexes are even part of the valid indexes
           
                If yes then I would check and store in respective variables:
                        Matched: index1 == reverse_complement(index2) and both are valid
                        Hopped: both are valid but don’t match each other

                If not:
                    Chuck them in unknown
        
        Write it to the respective file that it fits in 
            If it is matched:
                Call get_output_handles(index1, index2) to get the R1 and R2 file handles
                Write the full FASTQ record for read1 to the matched R1 output file:
                header with index pair
                read1 sequence
                "+"
                read1 quality scores

                Write the full FASTQ record for read2 to the matched R2 output file:
                header with index pair
                read2 sequence
                "+"
                read2 quality scores

                Increment counter +1 

            If it is hoppped:
                Write the read1 FASTQ record to hopped_R1 file (same format as above)
                Write the read2 FASTQ record to hopped_R2 file (same format as above)

                Increment index_hopped_count by 1
            If it is unknown:
                Write the read1 FASTQ record to unknown_R1 file
                Write the read2 FASTQ record to unknown_R2 file

                Increment unknown_count by 1

        Close my files

```