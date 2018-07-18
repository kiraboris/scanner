"""Help script for Nadine's fitting: sorts lines the way Holger said to do it.

INPUT: 
1) xxx for xxx.lin (as command line argument or console input).
OUTPUT: 
1) xxx sorted.lin
2) xxx classification.txt (same as above, but with additional line class information)

Python version: 3.4.4"""

from sys import argv as ARGV;

# input filenames
if len(ARGV) < 2: 
	name_file = input("Enter xxx for xxx.lin, please: ")
else:
	name_file = ARGV[1];
	
if name_file.endswith((".lin", ".fit")):
	name_file = name_file[:-4]; 

name_lin_file = name_file + ".lin";
name_sort_file = name_file + " sorted.lin";
name_class_file = name_file + " classification.txt"; 

# line info class (additional info as methods)
class Line:
	def __init__(self, sline: str):
		self.sline = sline;
		str_cols = sline.split();
		if(len(str_cols) < 10):
			self.valid = False; 
		else:
			self.valid = True;
			self.J1 = int(str_cols[0]);
			self.Ka1 = int(str_cols[1]);
			self.Kc1 = int(str_cols[2]);
			self.J2 = int(str_cols[5]);
			self.Ka2 = int(str_cols[6]);
			self.Kc2 = int(str_cols[7]);
			self.freq = float(str_cols[10]);
			self.freq_err = float(str_cols[11]);
	
	def dJ(self) -> int:
		return self.J1 - self.J2;
		
	def dKa(self) -> int:
		return self.Ka1 - self.Ka2;

	def dKc(self) -> int:
		return self.Kc1 - self.Kc2;
	
	def branch(self) -> str:
		if(self.dJ() == 0):
			return 'Q';
		elif(self.dJ() == 1):
			return 'R';
		elif(self.dJ() == -1):
			return 'P';
	
	def type(self) -> str:
		if(abs(self.dKa()) % 2 == 0):
			return 'a';
		else:
			if(abs(self.dKc()) % 2 == 0):
				return 'c';
			else:
				return 'b';
	
	def classification(self) -> str:
		return self.type() + self.branch() + str(self.dKa()) + 'x';
		
# input
v_lines = [];
with open(name_lin_file, 'r') as file:
	for sline in file:
		line = Line(sline);
		if(line.valid):
			v_lines.append(line);
	#end loop

# sort
def makeKey(line: Line) -> int:
	#by default to the end
	ndig1 = 1;
	ndig2 = 3;
	ndig3 = 3;

	key1 = 10 ** ndig1 - 2; 
	key2 = 10 ** ndig2 - 1; 
	key3 = 10 ** ndig3 - 1; 	

	slinclass = line.classification();
	if(slinclass in {'aR0x'}):
		key1 = 1;
		key2 = line.J1;
		key3 = line.Ka1;
		
	elif(slinclass in {'cR-1x', 'cR1x'}):
		key1 = 3;
		key2 = line.J1;		
		key3 = min(line.Ka1, line.Ka2);
		
	elif(slinclass in {'aR-2x', 'aR2x', 'aQ-2x', 'aQ2x', 'aQ0x'}):
		key1 = 5;
		
	if(line.Ka1 > 3 or line.Ka2 > 3): # then interchange J and Ka keys (sort orders)
		(key2, key3) = (key3, key2);
		key1 = key1 + 1;

	return (key1 * 10 ** (ndig2 + ndig3) + key2 * 10 ** (ndig3) + key3);

keys = [];
for i in range(0, len(v_lines)):
	const_num_blends_max = 3;
	lin_cur = v_lines[i];
	key_new = makeKey(lin_cur);
	
	for j in range(i + 1, min(len(v_lines), i + const_num_blends_max)):
		lin_next = v_lines[j];
		if(lin_cur.freq == lin_next.freq): # blend!
			key_next = makeKey(lin_next);	
			if(key_next > key_new):
				key_new = key_next; # use 'latest' key for blends
		else:
			break;
	#end loop
	
	keys.append(key_new);
#end loop

# actual sort using Schwartzian transform
(keys_sorted, v_lines_sorted) = zip(*sorted(zip(keys, v_lines), key = lambda x: x[0]));

# output
with open(name_class_file, 'w') as file_class, open(name_sort_file, 'w') as file_sorted:
	for (i, line) in enumerate(v_lines_sorted):
		line_with_class =	(line.classification() + 
							' ' * (5 - len(line.classification())) +
							' (' + str(keys_sorted[i]) + ') ' + line.sline);
		file_class.write(line_with_class);
		file_sorted.write(line.sline);
	#end loop

