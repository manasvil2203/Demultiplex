#!/usr/bin/env python

# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
You should update this docstring to reflect what you would like it to say'''

__version__ = "0.1"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = None
RNA_bases = None

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33
    

def qual_score(phred_score: str) -> float:
    """The function takes a phred score sequence and returns the mean of all the integer values."""
    total = 0
    for letter in phred_score:
        total += convert_phred(letter)
    return total/len(phred_score)
        

def validate_base_seq(seq: str, RNAflag: bool=False) -> bool:
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    seq = seq.upper()
    return len(seq) == seq.count("A") + seq.count("U" if RNAflag else "T") + seq.count("G") + seq.count("C")

def gc_content():
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()         
    Gs = DNA.count("G")       
    Cs = DNA.count("C")       
    return (Gs+Cs)/len(DNA)

def calc_median(lst):
    '''Given a sorted list, returns the median value of the list'''
    i = len(lst)
    if i%2 == 0:
        mid_a = (i//2) -1 
        mid_b = i//2
        med = (lst[mid_a] + lst[mid_b])/2
    else:
        mid = (i +1)//2
        mid = mid - 1
        med = lst[mid]

    return med

def oneline_fasta(input_file, output_file):
    '''docstring'''
    with open(output_file, 'w') as out_fh:
        with open(input_file, 'r') as in_fh:
            sequence_line = ''
            for line in in_fh:
                if ">" in line:
                    if sequence_line == "":
                        out_fh.write(line)
                    else:
                        
                        sequence_line += "\n"
                        out_fh.write(sequence_line)
                        sequence_line = ""
                        out_fh.write(line)
                else:
                    line = line.strip("\n")
                    sequence_line += line
            out_fh.write(sequence_line)

if __name__ == "__main__":
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    # These tests are run when you execute this file directly (instead of importing it)
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")

    assert validate_base_seq("AATAGAT") == True, "Validate base seq does not work on DNA"
    assert validate_base_seq("AAUAGAU", True) == True, "Validate base seq does not work on RNA"
    print("Passed DNA and RNA tests")
    print("testing RNA:")
    assert validate_base_seq("AAUAGAU", True), "RNA test failed"
    print("RNA test passed!")
    print("testing DNA:")
    assert validate_base_seq("AATAGAT"), "DNA test failed"
    print("DNA test passed!")
    print("testing non-nucleic acid:")
    assert validate_base_seq("R is the best!")==False, "R sux"
    print("non-nucleic test passsed!")

    assert gc_content("GCGCGC") == 1
    assert gc_content("AATTATA") == 0
    assert gc_content("GCATCGAT") == 0.5
    print("correctly calculated GC content")

    assert calc_median([1,2,100]) == 2, "calc_median function does not work for odd length list"
    assert calc_median([1,2]) == 1.5, "calc_median function does not work for even length list"
    assert calc_median([1,1,1,1,1,1,1,1,1,5000]) == 1
    assert calc_median([1,2,3,4,5,6,7,13]) == 4.5
    print("Median successfully calculated")

    assert qual_score("EEE") == 36
    assert qual_score("#I") == 21
    assert qual_score("EJ") == 38.5
    assert qual_score(phred_score) == 37.62105263157895, "wrong average phred score"
    print("You calcluated the correct average phred score")
