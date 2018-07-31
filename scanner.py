
import sys
from scanner.gui import MainWindow, Application
from scanner.ranges_wrapper import RangesWrapper
#from scanner.simu

# create components
app = Application([])
win = MainWindow()
exp = RangesWrapper()
#sim = Simulation()

# open and save project routines
def open_project(filename):
    with open(filename, 'rb') as f:
        #sim.deserialize(f)
        exp.deserialize(f)

def save_project(filename):
    with open(filename, 'wb') as f:
        # sim.serialize(f)
        exp.serialize(f)

# connect components
exp.sigUpdated.connect(win.pan.update)
win.expDock.sigAddFile.connect(exp.add_data_file)
win.expDock.sigRemoveItem.connect(exp.remove)


# execute
win.show()
sys.exit(app.exec_())