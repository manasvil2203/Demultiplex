# Assignment the First

## Part 1
1. Be sure to upload your Python script. Provide a link to it here:(Part_1_script.py)[./Part_1_script.py]

| File name | label | Read length | Phred encoding |
|---|---|---|---|
| 1294_S1_L008_R1_001.fastq.gz | read1 | 101 | phred 33 |
| 1294_S1_L008_R2_001.fastq.gz | index1 | 8 | phred 33  |
| 1294_S1_L008_R3_001.fastq.gz | index2 | 8 | phred 33  |
| 1294_S1_L008_R4_001.fastq.gz | read2 | 101 | phred 33  |

2. Per-base NT distribution
    1. Use markdown to insert your 4 histograms here.
        [dist_R1.png](./dist_R1.png)
        [dist_R2.png](./dist_R2.png)
        [dist_R3.png](./dist_R3.png)
        [dist_R4.png](./dist_R4.png)
   
    2. Assuming the downstream analysis is for alignment, for my index reads, I only need them to be valid reads. For them to be valid reads, I just need them to be correctly sequenced, so no N base in the sequence. So I think the cutoff should be 2. Now, one could argue that even if it is read as valid index by my sequencer, it might be a mistake, what if it got some bases wrong and it just happened to be a valid sequence? Well...have you heard of something called Hamming distances?
    Let me define it for you: For two strings of equal length, the Hamming distance is the number of characters that are different at the same position. So the higher the hamming distnce, the more chance that a low quality score will not impact my valid bases.Guess what? We have a pretty high hamming score ranging between 4-8. This means my index which is 8 bases long, will have to have at least 4 bases called wrong, so 50%, to be another valid sequence. Thus, I think it is safe to say that I a quality score of 2 is justified.


    For my biological reads, I would not have a cutoff. All my quality scores look pretty good and so if there are any bad quality, my aligner can deal with them.
    3. zcat 1294_S1_L008_R2_001.fastq.gz| sed -n '2~2p'| grep "N" | wc -l (3976613)
       zcat 1294_S1_L008_R2_001.fastq.gz| sed -n '2~2p'| grep "N" | wc -l (3328051)
       zcat 1294_S1_L008_R2_001.fastq.gz 1294_S1_L008_R3_001.fastq.gz| sed -n '2~2p'| grep "N" | wc -l (7304664)
## Part 2
1. Define the problem
2. Describe output
3. Upload your [4 input FASTQ files](../TEST-input_FASTQ) and your [>=6 expected output FASTQ files](../TEST-output_FASTQ).
4. Pseudocode
5. High level functions. For each function, be sure to include:
    1. Description/doc string
    2. Function headers (name and parameters)
    3. Test examples for individual functions
    4. Return statement
