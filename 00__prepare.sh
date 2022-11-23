# The raw output of Doccano contains 'data' and 'label'
# this needs to be converted to 'text' and 'labels'

############
# 1. convert
############

# copy and set NERDA required fields
cp data/final.jsonl data/final_cleaned.jsonl 

# change fields
sed -i '' 's|"data"|"text"|' data/final_cleaned.jsonl 
sed -i '' 's|"label"|"labels"|' data/final_cleaned.jsonl 

###########
# 2. rename
###########

# replace all instances of PICO terminology in more simple version
sed -i '' 's|"P"|"Patient"|g' data/final_cleaned.jsonl
sed -i '' 's|"I"|"Intervention"|g' data/final_cleaned.jsonl
sed -i '' 's|"C"|"Control"|g' data/final_cleaned.jsonl
sed -i '' 's|"X"|"Outcome"|g' data/final_cleaned.jsonl
sed -i '' 's|"B"|"O"|g' data/final_cleaned.jsonl


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
}' data/final_cleaned.jsonl > data/final_cleaned_shuffled.jsonl

############################################
# 4. separate in training/validation/testing
############################################

# in total N = 789 (600, 95, 94)

cat data/final_cleaned_shuffled.jsonl | head -n 600 > data/data_training.jsonl
cat data/final_cleaned_shuffled.jsonl | head -n 695 | tail -n 95 > data/data_validation.jsonl
cat data/final_cleaned_shuffled.jsonl | head -n 789 | tail -n 94 > data/data_testing.jsonl
