# RNAseq_pipeline
It is a detailed RNA-seq data processing pipeline

This processing pipeline have used "New Tuxedo" package with HISAT2, StingTie (https://www.nature.com/articles/nprot.2016.095).

Input: 
  1. Excel file with each sheet indicates a project ID and in the project sheet a list of SRR accession numbers, this pipeline will be able to download the raw          sequece files of the samples from SRA and process those to get gene read count, transcript read count, FPKM and TPM. 
     Sample Excel file ( .......) is added
     
  2. Human (or others) gene annotation file (e.g. gencode.v33.chr_patch_hapl_scaff.annotation.gtf). I have downloaded my file from GENCODE              (https://www.gencodegenes.org/human/). I have used comprehensive gene annotation file for all regions with .gtf format (download link:      ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_33/gencode.v33.chr_patch_hapl_scaff.annotation.gtf.gz)
  
  3. HISAT2 indexes in a directory. prebuilt HISAT2 indexes for the human genomes and many other organisms are available in HAT website. But I have built these indices. For that, you need genome sequence file (e.g., GRCh38.p13.genome.fa; downloaded from Gencode, ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_37/GRCh38.p13.genome.fa.gz) and gene annotation file (.gtf mentioned in Input 2). Detailed steps are included in Box 2 of Tuxedo nature protocol (https://www.nature.com/articles/nprot.2016.095).


Code files:
  1. RR_project_ALL.py
  2. prepDE.py
  3. Expression.py

Make sure your machines have following softwares installed.
  1. Python
  2. Python3 (including pandas package)
  3. hisat2 (version- 2.0.5; using updated version may cause problem downloading file from SRA)
  4. samtools (version- 1.3.1)
  5. stringtie (version- 2.0.6)

The steps of processing the data:

Step 1:

Run the following code in command line from your main directory which have your excel file containing SRR list (from Input 1)
      "python3 RR_project_ALL.py -g {..gene annotation file (from Input 2) address...} -index {..hisat2 index folder (built in Input 3) address}"

In this step, 3 program runs

 A. HISAT2 downloads SRR files from SRA, do the "alignment of the reads to the genome" using hisat_indices and output sam file.
 
 B. samtools converts sam file to bam file
 
 C. StringTie takes the gene annotation file (.gtf) and bam file. It then assembles of the alignments into full-length transcripts and quantifies of the expression     levels of each gene and transcript. It produces mainly two file (I) a GTF file containing the assembled transcripts (e.g. in /RNA_seq Processing Main   folder/Project1/Ballgown/SRR_Sample1/SRR_Sample1.gtf) (II) Gene abundances in tab-delimited format (III) Ballgown/DEseq Input Table Files, which contains coverage    data for all transcripts.
 

Step 2:

Go inside each project file repeatedly (e.g., RNA_seq Processing Main folder/Project1/ ) and run
   "python {.../prepDE.py} " # mention where your prepDE.py file is (e.g. RNA_seq Processing Main folder/prepDE.py).

prepDE.py file contains ways to extract gene_read_count and transcript_read_count

Step 3:

Run the following command again from your main directory
   
"python3 Expression.py"

Expression.py file contains ways to extract FPKM and TPM data from the .tab file

Your RNA-seq processing folder will ultimately look like this:

RNA_seq Processing Main folder
	RR_project_ALL.py
  prepDE.py
  Expression.py
  SRR_list.xlsx
  Project1
    Ballgown
      SRR_Sample1
        SRR_Sample1.tab
        SRR_Sample1.gtf
        t_data.ctab
        e_data.ctab
        i_data.ctab
      SRR_Sample2
        ...
        ...
    gene_read_count.csv
    transcript_count_matrix.csv
    Project1_Expression_FPKM.csv
    Project1_Expression_TPM.csv
  Project2
    ...
    ...
      ...
      ...
  GENCODE data
    gencode.v33.chr_patch_hapl_scaff.annotation.gtf
    GRCh38.p13.genome.fa
    GRCh38_GENCODE.1.ht2
    GRCh38_GENCODE.2.ht2
    ...
    ...
    
  

