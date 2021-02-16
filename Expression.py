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
        
    DF1 = pd.ExcelFile('All_SRA_samples.xlsx')
    for PRJ in DF1.sheet_names:
        df = DF1.parse(PRJ)   # PRJ is the sheet name, which is the project name
        output_dir=os.path.abspath('./'+PRJ) 

        GeneCount = pd.read_csv(output_dir+'/'+'gene_count_matrix.csv')
        TranscriptCount = pd.read_csv(output_dir+'/'+'transcript_count_matrix.csv')
        All_SRA = df['SRR Accession Number']
        
        for II1 in range(len(All_SRA)):
            SRA = All_SRA[II1]
            print(SRA)
            output_dir1 = output_dir+'/'+'ballgown'+'/'+SRA
            
            #GeneCount = GeneCount.rename(columns={SRA: SRA })
            #TranscriptCount = TranscriptCount.rename(columns={SRA: SRA })

            # writing Gene ID and Gene Name in the expression file
            if II1==0:
                SRA_READ = pd.read_csv(output_dir1+'/'+SRA+'.tab',sep='\t')
                SRA_GeneID = SRA_READ['Gene ID']
                SRA_GeneNAME = SRA_READ['Gene Name']

                DFobj =pd.DataFrame(columns=['Gene ID','Gene Name'])
                DFobj['Gene ID'] = SRA_GeneID
                DFobj['Gene Name'] = SRA_GeneNAME
                DFobj2 =DFobj.copy()

            SRA_READ1 = pd.read_csv(output_dir1+'/'+SRA+'.tab',sep='\t')
            SRA_READ1.drop_duplicates(subset ="Gene ID",keep = 'first', inplace = True) 
            
            SRA_READ2 = SRA_READ1[['Gene ID','FPKM']]
            DFobj = pd.merge(DFobj, SRA_READ2, on='Gene ID')
            DFobj = DFobj.rename(columns={"FPKM": SRA})
            
            SRA_READ3 = SRA_READ1[['Gene ID','TPM']]
            DFobj2 = pd.merge(DFobj2, SRA_READ3, on='Gene ID')
            DFobj2 = DFobj2.rename(columns={"TPM": SRA})

        fileName= output_dir+'/'+PRJ+ '_Expression_FPKM.csv'
        DFobj.to_csv(fileName, index=False)
        
        fileName2= output_dir+'/'+PRJ+ '_Expression_TPM.csv'
        DFobj2.to_csv(fileName2, index=False)
        
        fileName3= output_dir+'/'+PRJ+ '_gene_count_matrix.csv'
        GeneCount.to_csv(fileName3, index=False)
        
        fileName4= output_dir+'/'+PRJ+ '_transcript_count_matrix.csv'
        TranscriptCount.to_csv(fileName4, index=False)

# python3 Expression.py
