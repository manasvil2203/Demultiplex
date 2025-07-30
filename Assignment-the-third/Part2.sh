#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=bgmp                  #REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 #optional: number of cpus, default is 1
#SBATCH --mem=52GB                        #optional: amount of memory, default is 4GB per cpu
#SBATCH --mail-user=manasvil@uoregon.edu     #optional: if you'd like email
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --job-name=Demultiplex           #optional: job name
#SBATCH --output=Demultiplex_%j.out       #optional: file to store stdout from job, %j adds the assigned jobID
#SBATCH --error=Demultiplex_%j.err        #optional: file to store stderr from job, %j adds the assigned jobID

mamba activate bgmp-demultiplex

/usr/bin/time -v  ./Part2.py -r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz\
                             -r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
                             -r3 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz \
                             -r4 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
                             > matrix.txt