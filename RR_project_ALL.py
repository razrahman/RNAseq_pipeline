#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: raziurrahman
"""

import os, sys
import argparse
import subprocess
import pandas as pd


if __name__ == "__main__":
    #modelling input parameters 
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-g', help='directory for gene annotation file *.gff', required=True) # e.g., /RNAseq_processing/GENCODE/gencode.v33.chr_patch_hapl_scaff.annotation.gtf
    parser.add_argument('-index', help='directory for HISAT2 indices', required=True) #e.g. /RNAseq_processing/GENCODE/GRCh38_GENCODE

    
    if len(sys.argv) ==1:
        parser.print_help()
        sys.exit(2)
    map_args = parser.parse_args()
    
    genome_dirs=os.path.abspath(map_args.g)
    hisat_indexes = os.path.abspath(map_args.index)

    DF1 = pd.ExcelFile('All_SRA_samples.xlsx') # excel file containing all SRR samples with each sheet contains SRR samples from different projects 
    for PRJ in DF1.sheet_names:
        df = DF1.parse(PRJ)   # PRJ is the sheet name, which is the project name
        output_dir=os.path.abspath('./'+PRJ) 
        if not os.path.isdir(output_dir):
            subprocess.call(["mkdir","-p",output_dir]) # create project directory e.g. ./PRJNA123456

        All_SRA = df['SRR Accession Number']

        for II1 in range(len(All_SRA)):
            SRA = All_SRA[II1]
            print(SRA)
            output_dir1 = output_dir+'/'+SRA  # e.g. /PRJNA123456/SRR7890
            output_dir2 = output_dir+'/'+'ballgown'+'/'+SRA
            if not (os.path.isdir(output_dir1) or os.path.isdir(output_dir2)):
                subprocess.call(["mkdir","-p",output_dir1])
                SAM_out = output_dir1+'/'+SRA+'.sam' #/PRJNA123456/SRR7890/SRR7890.sam
                BAM_out = output_dir1+'/'+SRA+'.bam' #/PRJNA123456/SRR7890/SRR7890.bam
                GTF_out  = output_dir2+'/'+SRA+'.gtf' #PRJNA123456/ballgown/SRR7890/SRR7890.gtf
                Gene_out = output_dir2+'/'+SRA+'.tab' #PRJNA123456/ballgown/SRR7890/SRR7890.tab
                subprocess.call(["hisat2","-p","12","--dta","-x",hisat_indexes,"--sra-acc",SRA,"-S",SAM_out])
                subprocess.call(["samtools","sort","-@","12","-o",BAM_out,SAM_out])
                subprocess.call(["stringtie","-e","-B","-p","12","-G",genome_dirs,"-A",Gene_out,"-o",GTF_out,BAM_out])
                
                subprocess.call(["rm","-rf",output_dir1]) # deleting SAM and BAM files

# python3 RR_project_ALL.py -g /RNAseq_processing/GENCODE/gencode.v33.chr_patch_hapl_scaff.annotation.gtf -index /RNAseq_processing/GENCODE/GRCh38_GENCODE
