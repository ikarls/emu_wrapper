#!/usr/bin/env python3

import sys
import os
import subprocess
import shutil
import glob

# Outfile to be imported to Geneious
outFile = sys.argv[2]

# Temporary Geneious folder. Example: /Users/user/Geneious 2022.1 Data/transient/1660719270002/x/8/
pathToGeneiousData = sys.argv[4]

pathToDocker = sys.argv[6]

# In/out data folder selected by user
pathToData = sys.argv[8]
mountPath = os.path.join(pathToData, ":/geneious")

# List of fasta files in data folder
inFiles = []
for file in os.listdir(pathToData):
    if file.endswith(".fasta"):
        inFiles.append(os.path.join("/geneious",file))

# Run emu abundance for each sample
for inFile in inFiles:
    subprocess.run( [pathToDocker, "run", "--rm", "-v", mountPath, "emu3.4.4_image", \
        "emu", "abundance", inFile, \
        "--db", "/tmp/geneious/emu-database", \
        "--keep-counts", "--keep-files", "--keep-read-assignments", "--output-unclassified", \
        "--output-dir", "/geneious"] )

# Run emu combine-outputs for selected folder - both relative abundance and counts
combineOutputs = ("emu combine-outputs /geneious species; emu combine-outputs --counts /geneious species")

subprocess.run( [pathToDocker, "run", "--rm" ,"-v", mountPath, \
    "emu3.4.4_image", "/bin/bash", "-c", combineOutputs] )

# Copy combined output file to Geneious tmp folder
shutil.copyfile(os.path.join(pathToData, outFile), os.path.join(pathToGeneiousData, outFile))