
import sys
from scanner.widgets import MainWindow, Application
from scanner.engine import ScannerEngine
from simulation.ranges_wrapper import RangesWrapper
#from scanner.simu

# create components
app = Application([])
win = MainWindow()
exp_ranges = RangesWrapper()
sim_ranges = RangesWrapper()
engine = ScannerEngine(sim_ranges, exp_ranges)

# open and save project routines
#def open_project(filename):
#    with open(filename, 'rb') as f:
        #sim.deserialize(f)
#        exp.deserialize(f)

#def save_project(filename):
 #   with open(filename, 'wb') as f:
        # sim.serialize(f)
 #       exp.serialize(f)


# connect components
exp_ranges.sigUpdated.connect(win.pan.plotUpper)
exp_ranges.sigAdded.connect(win.expDock.addItems)
win.expDock.sigAddItems.connect(exp_ranges.add_data_files)
win.expDock.sigRemoveItem.connect(exp_ranges.remove)
win.expDock.sigItemChecked.connect(exp_ranges.set_visibility)
win.expDock.sigCurrentRowChanged.connect(exp_ranges.make_info)
exp_ranges.sigInfo.connect(win.expDock.setInfoSheet)

# execute
win.show()
sys.exit(app.exec_())