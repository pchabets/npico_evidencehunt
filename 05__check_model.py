#!/usr/bin/env python3
# 
# Wim Otte (w.m.otte@umcutrecht.nl)
#
# TODO before script run:
#
# export TOKENIZERS_PARALLELISM=false
# export PYTHONWARNINGS="ignore"
# 
# Fit NER model
#################################################################################
import os
import csv
import pandas as pd

from itertools import compress
from NERDA.models import NERDA

#################################################################################
# BEGIN FUNCTIONS
#################################################################################

###
# Read data.
##
def get_data( file_path, limit = None ):
    # read data from file.
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ' ')
        for row in reader:
            data.append([row])

    sentences = []
    sentence = []
    entities = []
    tags = []

    for row in data:
        # extract first element of list.
        row = row[0]
        # TO DO: move to data reader.
        if len(row) > 0 and row[0] != '-DOCSTART-':
            sentence.append(row[0])
            tags.append(row[-1])        
        if len(row) == 0 and len(sentence) > 0:
            # clean up sentence/tags.
            # remove white spaces.
            selector = [word != ' ' for word in sentence]
            sentence = list( compress( sentence, selector ) )
            tags = list( compress( tags, selector ) )
            # append if sentence length is still greater than zero..
            if len(sentence) > 0:
                sentences.append(sentence)
                entities.append(tags)
            sentence = []
            tags = []
            
    if limit is not None:
        sentences = sentences[:limit]
        entities = entities[:limit]
    
    return {'sentences': sentences, 'tags': entities}

###
# Load finetuned model
##
def load_finetuned_model():

    # model file
    finetuned_model = 'out.04.finetune/trained_ner_model.bin'
    
    # the IOB tagging scheme implies, that words that are beginning of named entities 
    # are tagged with 'B-' and words 'inside' (=continuations of) named entities 
    # are tagged with 'I-'.
    tag_scheme = [ 'B-Patient',
               'I-Patient',
               'B-Intervention',
               'I-Intervention',
               'B-Control',
               'I-Control',
               'B-Outcome',
               'I-Outcome' ]

    # outside text
    tag_outside = 'O'

    # transformer model
    transformer_name = 'microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract'

    # max length of abstract
    max_len = 512

    # define model
    model = NERDA( 
               tag_scheme = tag_scheme,
               tag_outside = tag_outside,
               max_len = max_len,
               transformer = transformer_name )

    # load from file
    model.load_network_from_file( finetuned_model )

    return( model )

#################################################################################
# END FUNCTIONS
#################################################################################

# create output dir
outdir = 'out.05.check.model'
if not os.path.exists( outdir ): 
    os.mkdir( outdir )

#################
# 1. Get data
#################

# input files (CoNLL-U Format)
testing_file = 'out.03.merged/comb_testing.txt'

# get testing data 
data_testing = get_data( testing_file )

print( len( data_testing.get( 'sentences' ) ) )


######################################################
# 2. Load finetuned model and apply to single abstract
######################################################

# load finetuned model
model = load_finetuned_model()

# evaluate on test set
print( model.evaluate_performance( data_testing ) )

# abstract file
pred_outfile = outdir + '/pred_abstract.tsv'

# abstract from new RCT
text = 'Background: High-level evidence for using steroids in epileptic encephalopathy (EE), other than West syndrome (WS), is lacking. This study investigated the efficacy and safety of pulse intravenous methylprednisolone (IVMP) in EE other than WS. Methods: This is an open-label evaluator-blinded randomised controlled study. Children aged 6 months or more with EE other than WS were included. Eighty children were randomised into intervention and non-intervention groups with 40 in each group. At the first visit (T1) seizure frequency, electroencephalographic (EEG) and Vineland Social Maturity Scale (VSMS) were obtained, and antiseizure medication (ASM) were optimised. After 1 month (T2), subjects were randomised to intervention (ASM+3 months IVMP pulse) or non-intervention group (only ASM) with 40 subjects in each group. They were followed up for 4 months (T3) and assessed. Results: After 4 months of follow-up, 75% of patients receiving IVMP had >50% seizure reduction versus 15.4% in control group (χ2=28.29, p<0.001) (RR 4.88, 95% CI 2.29 to 10.40), median percentage change in seizure frequency (91.41% vs 10%, p<0.001), improvement in EEG (45.5% vs 9.4%, χ2=10.866, p=0.001) and social age domain of VSMS scores (Z=-3.62, p<0.001) compared with baseline. None of the patients in the intervention group had any serious side-effects. Discussion: Three-month pulse IVMP therapy showed significant improvement in seizure frequency, EEG parameters and VSMS scores, with no steroid-related serious adverse effects. It can be considered as a safe and effective add on treatment in children with EE other than WS.'

# predict labels for text
pred = model.predict_text( text )

# make data.frame and write to disk
df = pd.DataFrame( pred )
df.to_csv( pred_outfile )

