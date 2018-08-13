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
sim.set_defaults(resolution=0.05, min_freq=1000.0, max_freq=200000.0,
                 threshold=-4.0, intensity_factor=1.0, sigma=0.2)

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
exp_ranges.sigSettings.connect(win.expSettings.setSheet)
win.expDock.sigAddItems.connect(exp_ranges.add_data_files)
win.expDock.sigRemoveItem.connect(exp_ranges.remove)
win.expDock.sigItemChecked.connect(exp_ranges.set_visibility)
win.expDock.sigSettingsRequest.connect(exp_ranges.get_settings)
win.expDock.sigSettingsRequest.connect(win.expSettings.show)

sim.sigUpdateRange.connect(sim_ranges.update)
sim.sigRemoveRange.connect(sim_ranges.remove)
sim.sigAdded.connect(win.simDock.addItem)
sim.sigSettings.connect(win.simSettings.setSheet)
sim_ranges.sigUpdated.connect(win.pan.plotLower)
win.simDock.sigAddItem.connect(sim.add_rotor)
win.simDock.sigRemoveItem.connect(sim.remove_rotor)
win.simDock.sigSettingsRequest.connect(sim.get_settings)
win.simDock.sigSettingsRequest.connect(win.simSettings.show)
win.simDock.sigItemChecked.connect(sim_ranges.set_visibility)
win.simSettings.sigSheetChanged.connect(sim.apply_settings)

# execute
win.show()
sys.exit(app.exec_())
