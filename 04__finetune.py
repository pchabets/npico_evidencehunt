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

#################################################################################
# END FUNCTIONS
#################################################################################

# create output dir
outdir = 'out.04.finetune'
if not os.path.exists( outdir ): 
    os.mkdir( outdir )

#################
# 1. Get data
#################

# input dir
indir = 'out.03.merged'

# input files (CoNLL-U Format)
training_file = indir + '/comb_training.txt'
validation_file = indir + '/comb_validation.txt'
testing_file = indir + '/comb_testing.txt'

# get training, testing and validation data 
data_training = get_data( training_file )
data_validation = get_data( validation_file )
data_testing = get_data( testing_file )

print( len( data_training.get( 'sentences' ) ) )
print( len( data_validation.get( 'sentences' ) ) )
print( len( data_testing.get( 'sentences' ) ) )

# print one sentence
sentence = data_training.get( 'sentences' )[ 0 ]
tags = data_training.get( 'tags' )[ 0 ]
print( "\n".join( [ "{} ----- {}".format( word, tag ) for word, tag in zip( sentence, tags ) ] ) )

# get unique labels in sentence
unique = list( dict.fromkeys( tags ) ) 
print( unique )

#################
# 2. Build model
#################

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

# hyperparameters
hyperparameters = { 'epochs' : 20,
                    'warmup_steps' : 400,
                    'train_batch_size': 16,
                    'learning_rate': 0.0001 }

# convert to lower case
tokenizer_parameters = {'do_lower_case' : True }

# max length of abstract
max_len = 512

# define model
model = NERDA( dataset_training = data_training,
               dataset_validation = data_validation,
               tag_scheme = tag_scheme,
               tag_outside = tag_outside,
               max_len = max_len,
               transformer = transformer_name,
               hyperparameters = hyperparameters,
               dropout = 0.1,
               tokenizer_parameters = tokenizer_parameters )

# train model
model.train()

# output file
model_outfile = outdir + '/trained_ner_model.bin'

# save model
model.save_network( model_outfile )

# evaluate on external testing data
print( model.evaluate_performance( data_validation ) )
print( model.evaluate_performance( data_testing ) )

# predict example sentence
#text = "A total of 110 patients with epilepsy entered the study on MRI-testing."
#print( model.predict_text( text ) )

