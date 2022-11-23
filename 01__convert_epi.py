#!/usr/bin/env python3
# 
# Wim Otte (w.m.otte@umcutrecht.nl)
#
# Doccano jsonl contains single abstract lines (with 'id', 'data' and 'label')
# Required is: 'id', 'text' and 'labels'
#
# CoNLL-U Format: https://universaldependencies.org/format.html
#################################################################################
import os
import csv

from doccano_transformer.datasets import NERDataset
from doccano_transformer.utils import read_jsonl
from itertools import compress

#################################################################################
# BEGIN FUNCTIONS
#################################################################################

###
# Process data
##
def convert_dataset( type, outdir ):
    
    # source of data
    src_path = 'data_epi/data_' + type + '.jsonl'

    # each row should contain: 'id', 'text' and 'labels'
    dataset = read_jsonl( filepath = src_path, dataset = NERDataset, encoding = 'utf-8' )

    # output file
    outfile = outdir + '/' + type + '.txt'

    with open( outfile, 'w' ) as f:
        # loop over all entries and write to file
        for single_entry in dataset.to_conll2003( tokenizer = str.split ):
            f.write( single_entry[ 'data' ] )
            f.write( '\n' )

    f.close()

#################################################################################
# END FUNCTIONS
#################################################################################

# create output dir
outdir = 'out.01.converted.epi'
if not os.path.exists( outdir ): 
    os.mkdir( outdir )

##############################
# TRAINING
##############################

# convert dataset
convert_dataset( 'validation', outdir )
convert_dataset( 'testing', outdir )
convert_dataset( 'training', outdir )
