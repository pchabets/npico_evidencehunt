
# change fields [i.e., remove secondary outcome and sample size]

sed -i '' 's|B-Outcome_2nd|O|g' out.01.converted.epi/training.txt
sed -i '' 's|I-Outcome_2nd|O|g' out.01.converted.epi/training.txt
sed -i '' 's|B-N|O|g' out.01.converted.epi/training.txt
sed -i '' 's|I-N|O|g' out.01.converted.epi/training.txt

sed -i '' 's|B-Outcome_2nd|O|g' out.01.converted.epi/testing.txt
sed -i '' 's|I-Outcome_2nd|O|g' out.01.converted.epi/testing.txt
sed -i '' 's|B-N|O|g' out.01.converted.epi/testing.txt
sed -i '' 's|I-N|O|g' out.01.converted.epi/testing.txt

sed -i '' 's|B-Outcome_2nd|O|g' out.01.converted.epi/validation.txt
sed -i '' 's|I-Outcome_2nd|O|g' out.01.converted.epi/validation.txt
sed -i '' 's|B-N|O|g' out.01.converted.epi/validation.txt
sed -i '' 's|I-N|O|g' out.01.converted.epi/validation.txt


sed -i '' 's|B-TOREMOVE|O|g' out.01.converted/training.txt
sed -i '' 's|B-TOREMOVE|O|g' out.01.converted/validation.txt
sed -i '' 's|B-TOREMOVE|O|g' out.01.converted/testing.txt

sed -i '' 's|I-TOREMOVE|O|g' out.01.converted/training.txt
sed -i '' 's|I-TOREMOVE|O|g' out.01.converted/validation.txt
sed -i '' 's|I-TOREMOVE|O|g' out.01.converted/testing.txt

