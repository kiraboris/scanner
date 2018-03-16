"""Help script for Nadine's fitting: moves bad lines to end of .lin file.

New in version 3:
Lines are no longer moved to end, but are marked with an asterix.
Additional command line parameter: number of sigmas (default 3).

New in version 2:
Additional command line parameter: number of lines to be skipped 
from beginning of .lin file (useful to ignore "older" lines)

Script will find lines in *.fit file that have discrepancies more than 
3*sigma_estimate and mark them in the *.lin file with an asterix,
whereby indicating the deviation.

INPUT: 
1) xxx for xxx.lin and xxx.fit 
(as command line argument or console input).
Additional command line parameters:
2) number of sigmas (default 3)
3) number of lines to be skipped from beginning of .lin file (useful to ignore "older" lines).
OUTPUT: xxx.lin will be modified, original version back-upped in xxx.lin.pst
Python version: 3.4.4"""

from sys import argv as ARGV;
from shutil import copyfile; 

# input filenames
if len(ARGV) < 2: 
	name_file = input("Enter xxx for xxx.lin and xxx.fit, please: ")
else:
	name_file = ARGV[1];
	
count_ignorez = 0;
count_sigmas = 3;
if len(ARGV) >= 3:
	count_sigmas = int(ARGV[2]);
if len(ARGV) >= 4:
	count_ignorez = int(ARGV[3]);

if name_file.endswith((".lin", ".fit")):
	name_file = name_file[:-4]; 
	
name_lin_file = name_file + ".lin";
name_fit_file = name_file + ".fit";
name_lin_old_file = name_lin_file + ".pst";

# find boundaries of last fitting iteration in *.fit
i_end_line = 0;
i_start_line = -1;
with open(name_fit_file, 'r') as file:
	for (i, line) in enumerate(file):
		line_trimmed = line.lstrip();
		if line_trimmed.startswith('NORMALIZED DIAGONAL'):
			i_end_line = i - 1;
		elif line_trimmed.startswith('EXP.FREQ.'):
			i_start_line = i + 1;

num_lines_in_fit = i_end_line - i_start_line + 1;
if(i_start_line < 0 or num_lines_in_fit == 0):
	print(name_fit_file + ": seems like there's nothing to parse..");
	exit();
	
if(count_ignorez >= num_lines_in_fit):
	print("Warning! All lines in .lin file are ignored.");

# accumulate 'estimated frequencies' of 'wrong' lines from *.fit
def testLineFromFit(line, wrong_frequences_dict):
	const_ind_estfreq_col = 11;
	const_ind_error_col = 13;
	const_ind_sigma_col = 14;
	str_cols = line.split();
	freq_error = float(str_cols[const_ind_error_col]);
	freq_sigma = float(str_cols[const_ind_sigma_col]);
	if freq_error > count_sigmas * freq_sigma:
		frequency = float(str_cols[const_ind_estfreq_col]);
		wrong_frequences_dict[frequency] = freq_error;

wrong_frequences_dict = {};
with open(name_fit_file, 'r') as file:
	for (i, line) in enumerate(file):
		if(i >= i_start_line and i <= i_end_line):
			testLineFromFit(line, wrong_frequences_dict);

# intermediate
copyfile(name_lin_file, name_lin_old_file);

# find 'wrong' lines in *.lin
def formLineFromLin(line, wrong_frequences_dict) -> str:
	const_ind_estfreq_col = 10;
	str_cols = line.split();
	if(len(str_cols) <= const_ind_estfreq_col):
		return line;
	frequency = float(str_cols[const_ind_estfreq_col]);
	if(frequency in wrong_frequences_dict):
		return ('*' + str(wrong_frequences_dict[frequency]) + '* ' + line);
	else:
		return line;

flag_interperting = False;
with open(name_lin_old_file, 'r') as file_old, open(name_lin_file, 'w') as file_new:
	for (i, line) in enumerate(file_old):
		flag_commented = False;
		if(i == count_ignorez):
			flag_interperting = True;
	
		line_strip = line.strip();
		if not line_strip:
			flag_interperting = False;  # stop processing if empty line found 
		elif line_strip[0] == '*': # commented line
			flag_commented = True;
		
		if(not flag_interperting or flag_commented):
			file_new.write(line);
		else:
			file_new.write(formLineFromLin(line, wrong_frequences_dict));
	#end loop

# results
print("Deviating lines (.fit):", sorted(wrong_frequences_dict.items(),
	reverse=True, key=lambda x: x[1]));
print("Good lines count (.fit):", num_lines_in_fit - len(wrong_frequences_dict));


