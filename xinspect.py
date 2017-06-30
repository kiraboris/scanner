# import LoadASCIIFile and GetTransitions packages
import task_LoadASCIIFile
import task_GetTransitions

def inspect(FileName, FreqMin, FreqMax, SelectMolecule):
    NumHeaderLines = 0
    RestFreq = 0.0
    vLSR = 0.0
    expdata = task_LoadASCIIFile.LoadASCIIFile(FileName, NumHeaderLines, \
    RestFreq, vLSR)
    FrequencyWidth = 5.0
    ElowMin = 0.0
    ElowMax = 2000.0
    task_GetTransitions.GetTransitions(expdata, FreqMin, FreqMax, \
    SelectMolecule, FrequencyWidth, \
    ElowMin, ElowMax)