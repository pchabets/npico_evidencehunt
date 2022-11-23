mkdir out.03.merged
cat out.01.converted/training.txt out.01.converted.epi/training.txt > out.03.merged/comb_training.txt
cat out.01.converted/testing.txt out.01.converted.epi/testing.txt > out.03.merged/comb_testing.txt
cat out.01.converted/validation.txt out.01.converted.epi/validation.txt > out.03.merged/comb_validation.txt

