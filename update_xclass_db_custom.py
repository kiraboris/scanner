import sys;

dbFilename = "/home/borisov/software/moeller/Database/cdms_sqlite.db"
modulesPath = ["/home/borisov/software/moeller/programs/Update_VAMDC"]

# 'web' (vadmcd) or 'files' (old cdms) mode 
mode = 'files'  

#settings for web mode
specificName = 'CH3CN;v=0;A'
onlyInsert = False
onlyUpdate = True
onlySimulate = True
deleteArchived = False

# settings for file mode
name = '3MBN-HX-HFS'
filenames = [{'label': '-1', 'cat': name + '.cat'}]
#filenames = [{'label': '', 'cat': name + '.cat', 'pressure': name + 'v=0.p', 'AE': True},
#             {'label': ';v=1;', 'cat': name + 'v=1.cat'}, {'label': ';v=2;', 'cat': name + 'v=2.cat'}]


flagUpdate = True

#--------------------------------------------------------------------------
## check if sys.path variable is already updated and modify if neccessary
for NewModulesPath in modulesPath:                                                 
    already_included_flag = "false"
    for entries in sys.path:
        if (entries == NewModulesPath):
            already_included_flag = "true"
            break
    if (already_included_flag == "false"):
        sys.path.append(NewModulesPath)

## try to import update package
try:
    import database
    db = database.Database(dbFilename)
    
    if(mode == 'web'):
        db.update_database(None, onlyInsert, onlyUpdate, deleteArchived, specificName, onlySimulate)
    elif(mode == 'files'):
        db.insert_species_data_files(name, filenames, flagUpdate)
    
except ImportError:
    print " "
    print "Error in subroutine UpdateDatabase:"
    print " "
    print "Can not import update package."

