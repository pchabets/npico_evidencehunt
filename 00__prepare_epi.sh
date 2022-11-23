# The raw output of Doccano contains 'data' and 'label'
# this needs to be converted to 'text' and 'labels'

############
# 1. convert
############

# copy and set NERDA required fields
cp data_epi/final.jsonl data_epi/final_cleaned.jsonl 

# change fields
sed -i '' 's|"data"|"text"|' data_epi/final_cleaned.jsonl 
sed -i '' 's|"label"|"labels"|' data_epi/final_cleaned.jsonl 

###########
# 2. rename
###########

# replace all instances of PICO terminology in more simple version
sed -i '' 's|"Patient/population"|"Patient"|g' data_epi/final_cleaned.jsonl
sed -i '' 's|"Intervention/treatment"|"Intervention"|g' data_epi/final_cleaned.jsonl


######################
# 3. shuffle sentences
######################

awk 'BEGIN{srand() }
{ lines[++d]=$0 }
END{
    while (1){
    if (e==d) {break}
        RANDOM = int(1 + rand() * d)
        if ( RANDOM in lines  ){
            print lines[RANDOM]
            delete lines[RANDOM]
            ++e
        }
    }
}' data_epi/final_cleaned.jsonl > data_epi/final_cleaned_shuffled.jsonl

############################################
# 4. separate in training/validation/testing
############################################

# in total N = 610 (450, 80, 80)

cat data_epi/final_cleaned_shuffled.jsonl | head -n 450 > data_epi/data_training.jsonl
cat data_epi/final_cleaned_shuffled.jsonl | head -n 530 | tail -n 80 > data_epi/data_validation.jsonl
cat data_epi/final_cleaned_shuffled.jsonl | head -n 610 | tail -n 80 > data_epi/data_testing.jsonl
