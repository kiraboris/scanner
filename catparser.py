# parsers for files from old CDMS version (Pickett .cat output)
import math
from collections import defaultdict

class Line:
    def __init__(self, line):
        try:
            self.valid = True
            self.freq = float(line[0:13])        # Frequency of the line v (usually in MHz)   
            self.freqErr = float(line[15:21])
            self.Elow = float(line[31:41])       # lower state energy (in cm-1)
            self.intensity = float(line[21:29])  # base 10 logarithm of the integrated intensity at 300 K (in nm2MHz);
            self.g = int(line[41:44])
            self.pressureAlpha = 0.0             # pressure broadening, alpha: dv=p*alpha*(T/296)^delta
            self.pressureDelta =0.0              # pressure broadening, delta: dv=p*alpha*(T/296)^delta 
            self.EinsteinA = 0.0        
            self.qUpper = []
            self.qLower = []
            for i in range(0, 6):
                self.qUpper.append(line[55 + i * 2 : 55 + i * 2 + 2])
                self.qLower.append(line[67 + i * 2: 67 + i * 2 + 2])
            self.strLowerState = ','.join(self.qLower)
            self.strUpperState = ','.join(self.qUpper)
        except:
            self.valid = False
    
    simplifyMapping = [ ('a', '1'), ('b', '2'), ('c', '3'), ('d', '4'), ('e', '5'), ('-', ' '), ('f', '6'), ('g', '7'), ('h', '8'), ('i', '9'), ('j', '10'), ('k', '11'), ('l', '12'), ('m', '13'), ('n', '14'), ('o', '15'), ('p', '16'), ('A', '10'), ('B', '11'), ('C', '12'), ('D', '13'), ('E', '14'), ('F', '15'), ('G', '16'), ('H', '17'), ('I', '18'), ('J', '19'), ('K', '20'), ('L', '21'), ('M', '22'), ('N', '23'), ('O', '24'), ('P', '25') ]    
    def simplified(self):
        newline = self
        for i in range(0, 6):
            for k, v in Line.simplifyMapping:
                newline.qUpper[i] = newline.qUpper[i].replace(k, v)
                newline.qLower[i] = newline.qLower[i].replace(k, v)
        newline.strLowerState = ','.join(newline.qLower)
        newline.strUpperState = ','.join(newline.qUpper)
        return newline
        
    def toString(self):
        data = [str(self.freq), str(self.freqErr), str(self.intensity), str(self.Elow), str(self.g), self.strUpperState, self.strLowerState, str(self.pressureAlpha), str(self.pressureDelta), str(self.EinsteinA) ]
        return ' '.join(data)
       
class State:
    def __init__(self):
        self.E = None
        self.g = None
       
# initialize example:
# CatParser('CH3CN', [{'label': ';v=0;', 'cat': 'v0.cat', 'pressure': 'v0.p', 'AE': True],
#                     {'label': ';v=1;', 'cat': 'v1.cat'}])
class CatParser: 
    def __init__(self, filenames):
        self.lines = defaultdict(list)
        self.flagPressure = defaultdict(bool)
        for bundle in filenames:
            catfilename = bundle.get('cat')
            if(catfilename is None):
                continue
            else:
                label = bundle.get('label', catfilename)
                AEflag = bundle.get('AE', False)
                if(AEflag): # separate ortho/para isomers or A/E line symmetry
                    labels = [label + 'A', label + 'E']
                    filters = [lambda line: line.valid and int(line.qUpper[1]) % 3 == 0, 
                               lambda line: line.valid and int(line.qUpper[1]) % 3 != 0]
                else:
                    labels = [label]
                    filters = [lambda line: line.valid]
                
                for (lab, filt) in zip(labels, filters):
                    self.__readCat(lab, catfilename, filt)
                    self.__blend(lab)
                    pressurefilename = bundle.get('pressure')
                    if(not pressurefilename is None):
                        self.__readPressure(lab, pressurefilename)
                        self.flagPressure[lab] = True
                    else:
                        self.flagPressure[lab] = False          
        self.__buildStatesAndEinstein()
                    
    def __blend(self, label):
        lines = self.lines[label]
        newlines = []
        blends = []
        flagLastLine = False
        for i in range(1, len(lines) + 1):
            prevline = lines[i - 1]
            if(i < len(lines)):
                line = lines[i]
            else:
                flagLastLine = True

            if(not flagLastLine and prevline.freq == line.freq):
                blends.append(prevline)
            else:
                if(len(blends) == 0):
                    newlines.append(prevline)
                else:
                    blends.append(prevline)
 
                    I_bl = map(lambda x: 10 ** x.intensity, blends)
                    g_bl = map(lambda x: x.g if 10 ** x.intensity == max(I_bl) else 0, blends)   # max-only weight
                    #g_bl = map(lambda x: int(x.g * (10 ** x.intensity / max(I_bl))), blends)     # effective weight
                    
                    prevline.intensity = math.log10(sum(I_bl))
                    prevline.g = sum(g_bl);

                    newlines.append(prevline)
                    blends = []
        self.lines[label] = newlines
    
    def __readCat(self, label, filename, filterFunc):
         with open(filename, 'r') as file:
            for str_line in file:
                line = Line(str_line).simplified() # ! simplified goes here, 12.06.
                if(filterFunc(line)):  # test line against provided filter
                    self.lines[label].append(line)  
                    
    def __readPressure(self, label, filename):
        with open(filename, 'r') as file:
            flagFirstIteration = True            
            for str_line in file:
                if(flagFirstIteration):
                    flagFirstIteration = False
                    indices = map(int, str_line.split())
                else:
                    ppp = str_line.split()
                    for line in self.lines[label]:
                        flagMatch = True
                        for (i, idx) in enumerate(indices):
                            try:
                                if(idx >= 6 and (int(line.qLower[idx - 6])!=int(ppp[i]))):
                                    flagMatch = False
                                    break
                                elif(idx < 6 and (int(line.qUpper[idx])!=int(ppp[i]))):
                                    flagMatch = False
                                    break   
                            except:
                                flagMatch = False
                        if(flagMatch):
                            line.pressureAlpha = float(ppp[-2])
                            line.pressureDelta = float(ppp[-1])
                            continue
                    
    def write(self, filename):
        with open(filename, 'w') as file:
            for label,lines in self.lines.iteritems():
                for line in lines:
                    file.write(label + ': ' + line.toString() + '\n')

    def __buildStatesAndEinstein(self):
        self.states = defaultdict(State)
        for label,lines in self.lines.iteritems():
            for line in lines:
                lkey = label + line.strLowerState
                ukey = label + line.strUpperState
                self.states[lkey].E = line.Elow
                if(self.states[ukey].g is None):
                    self.states[ukey].g = line.g
                else:
                    self.states[ukey].g += line.g
                    
        Tref = 300
        Qrs = self.partition(Tref) # ~15000 for CH3CN

        for label,lines in self.lines.iteritems():
            bad_line_ind = []
            for (i,line) in enumerate(lines):
                ukey = label + line.strUpperState
                intensity = 10 ** line.intensity
                Elower = line.Elow
                Eupper = self.states[ukey].E
                if(not Eupper is None):
                    line.EinsteinA = intensity * line.freq ** 2 * (Qrs / line.g) / (math.exp(-1.43877696 * Elower / Tref) - math.exp(-1.43877696 * Eupper / Tref)) * 2.7964E-16
                else:
                    bad_line_ind.append(i)
            for index in sorted(bad_line_ind, reverse = True):
                del lines[index]
            
   
    def partition(self, temperature):
        pf_value = 0.0
        err_counter = 0
        for state in self.states.values():
            if(not state.E is None and not state.g is None):
                pf_value += state.g * math.exp(-1.43877696 * state.E / temperature)  
            else:
                err_counter += 1
  
        if(float(err_counter) / len(self.states) > 0.05):
            print 'CatParser warning: more than 5% of microstates cannot be used for Q(T) calculation!'
    
        return pf_value           