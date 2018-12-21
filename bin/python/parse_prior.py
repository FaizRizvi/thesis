#!/usr/bin/env python
from __future__ import print_function

Usage = """
priorsTable2Sparse.py
convert a prior in table format (columns = regulators, rows = gene targets) into a sparse,
3-column format (regulator, row, interaction strength)
Usage: python ${scriptHome}/priorsTable2Sparse.py
INPUTS:
	priorTable -- tab-delimited file, columns = regulators, rows = gene targets, values = 
		interaction strengths 
	outFileName -- name for output file	
OUTPUTS:
	priorTable_sp -- sparse, 3-column output: 
		regulator, target, and interaction strength
"""	

import pandas as pd
import seaborn as sns
import os
import sys
import argparse
import pybedtools
import numpy as np
import snippets
from shutil import copyfile

parser = argparse.ArgumentParser()

parser.add_argument("-p", "-IN_PRIOR", dest='IN_PRIOR', help="Input PRIOR", required=True, nargs='+')
parser.add_argument("-o", "-OUT_DIR", dest='OUT_DIR', help="Output directory", required=True)

# set the arguments from the command line to variables in the args object
args = parser.parse_args()

if not os.path.exists(args.OUT_DIR):
        os.makedirs(args.OUT_DIR)

os.chdir(args.OUT_DIR)

for prior in args.IN_PRIOR:
	base = os.path.basename(prior)
	prior_basename = os.path.splitext(base)[0]
	print("Basename is " + prior_basename)

	df = snippets.priorTable2Sparse(prior, prior_basename, args.OUT_DIR)
	
	snippets.mergeDegeneratePriorTFs(df, prior_basename)