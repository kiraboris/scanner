import sys
from scanner.widgets import MainWindow, Application
# from scanner.engine import ScannerEngine
from simulation.ranges_wrapper import RangesWrapper
from simulation.simulation_group import SimulationGroup

# create components
app = Application([])
win = MainWindow()
exp_ranges = RangesWrapper()
sim_ranges = RangesWrapper()
sim = SimulationGroup()
# engine = ScannerEngine(sim_ranges, exp_ranges)

# set defaults
sim.set_defaults(resolution=0.1, min_freq=1000, max_freq=200000, threshold=-10.0, intensity_factor=1.0)

# open and save project routines
# def open_project(filename):
#    with open(filename, 'rb') as f:
# sim.deserialize(f)
#        exp.deserialize(f)

# def save_project(filename):
#   with open(filename, 'wb') as f:
# sim.serialize(f)
#       exp.serialize(f)


# connect components
exp_ranges.sigUpdated.connect(win.pan.plotUpper)
exp_ranges.sigAdded.connect(win.expDock.addItems)
exp_ranges.sigInfo.connect(win.expDock.setInfoSheet)
win.expDock.sigAddItems.connect(exp_ranges.add_data_files)
win.expDock.sigRemoveItem.connect(exp_ranges.remove)
win.expDock.sigItemChecked.connect(exp_ranges.set_visibility)
win.expDock.sigCurrentRowChanged.connect(exp_ranges.make_info)

sim.sigUpdateRange.connect(sim_ranges.update)
sim_ranges.sigUpdated.connect(win.pan.plotLower)
win.simDock.sigAddItem.connect(sim.add_rotor)

# execute
win.show()
sys.exit(app.exec_())
