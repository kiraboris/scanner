"""Help script for Nadine's fitting: removes duplicate lines from .fit.

Script will find lines in *.fit file that have all same quantum numbers 
and remove FIRST (older) copy.

INPUT: 
1) xxx for xxx.lin (as command line argument or console input).
Additional command line parameters:
2) number of lines to be skipped from beginning of .lin file (useful to ignore "older" lines).
OUTPUT: xxx.lin will be modified, original version backuped in xxx.lin.pre
Python version: 3.4.4"""

from sys import argv as ARGV;
from shutil import copyfile; 

# input filenames
if len(ARGV) < 2: 
	name_file = input("Enter xxx for xxx.lin, please: ")
else:
	name_file = ARGV[1];
	
count_ignorez = 0;
if len(ARGV) >= 3:
	count_ignorez = int(ARGV[2]);

if name_file.endswith((".lin", ".fit")):
	name_file = name_file[:-4]; 
	
name_lin_file = name_file + ".lin";
name_lin_old_file = name_lin_file + ".pre";

# accumulate quantum numbers to string
def grabLineFromFit(line) -> str:
	const_ind_begin_col = 0;
	const_ind_end_col_plus_one = 10;
	str_cols = line.split();
	if(len(str_cols) < const_ind_end_col_plus_one):
		return '';
		
	for i in range(const_ind_begin_col, const_ind_end_col_plus_one):
		if len(str_cols[i]) < 2:
			str_cols[i] = '0' + str_cols[i];
	#end loop
	str_result = str.join('', str_cols[const_ind_begin_col:const_ind_end_col_plus_one]);
	return str_result;

quantum_dict = {}; # {quantum_numbers->repcount}
with open(name_lin_file, 'r') as file:
	for (i, line) in enumerate(file):
		if(i >= count_ignorez):
			str_key = grabLineFromFit(line);
			
			if(not str_key):
				continue;
				
			count_rep_old = quantum_dict.get(str_key, 0);
			quantum_dict[str_key] = count_rep_old + 1;
	#end loop

# intermediate
copyfile(name_lin_file, name_lin_old_file);

# find and remove duplicates
count_removed = 0;
with open(name_lin_old_file, 'r') as file_old, open(name_lin_file, 'w') as file_new:
	for (i, line) in enumerate(file_old):
		if(i < count_ignorez):
			file_new.write(line);
			continue;
			
		str_key = grabLineFromFit(line);
		
		if(not str_key):
			file_new.write(line);
			continue;
		
		count_rep_old = quantum_dict.get(str_key, 0);
		if(count_rep_old >= 2):
			quantum_dict[str_key] = count_rep_old - 1;
			count_removed = count_removed + 1;
			# line not written 
		else:
			file_new.write(line);
	#end loop

# results
print("Lines removed as duplicates: ", count_removed);