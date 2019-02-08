#!/usr/bin/env bash

# NAMES
# cut -f1,2 'data/program-committee.txt'
# awk -F '\t' '{ print $1 " " $2 }' < 'data/program-committee.txt'
# awk '{ split($0,a,"\t"); print a[0]; }' < 'data/program-committee.txt'
# Collate, order and get NAMES
echo "NAMES"
awk -F '\t' '{
   a=$1 " " $2; 
   my_dict[a] += 1; 
} END { 
   for (key in my_dict) { 
      print key, my_dict[key] } 
}' < 'data/program-committee.txt' | sort

# COUNTRIES
# cut -f3 < 'data/program-committee.txt'
# Collate, order and get COUNTRIES
echo "COUNTRIES"
awk -F '\t' '{ 
   a=$1 " " $2; 
   my_dict[a] = $4;
}
END { 
   for (key in my_dict) { 
      print key, my_dict[key] } 
}' < 'data/program-committee.txt' | sort | cut -d ' ' -f 3-

# UNIS
# cut -f6 < 'data/program-committee.txt'
# Collate, order and get UNIS
echo "UNIS"
awk -F '\t' '{ 
a=$1 " " $2; 
my_dict[a] = $5;
}
END { 
for (key in my_dict) { 
print key, my_dict[key] } 
}' < 'data/program-committee.txt' | sort | cut -d ' ' -f 3-


