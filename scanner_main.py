import sys
from scanner_widgets import MainWindow, Application
# from scanner.engine import ScannerEngine
from simulation.ranges_wrapper import RangesWrapper
from simulation.simulation_group import SimulationGroup

# create components
app = Application([])
win = MainWindow()
exp_ranges = RangesWrapper(flag_no_division=False)
sim_ranges = RangesWrapper(flag_no_division=True)
sim = SimulationGroup()
# engine = ScannerEngine(sim_ranges, exp_ranges)

sim_defaults= {"resolution":0.025, "min_freq":90000.0, "max_freq":140000.0,
                 "threshold":-4.0, "intensity_factor":1.0, "sigma":0.2}

pan_defaults= {"plot_background_color": 'ddd', "plot_axes_color": 'k',
               'plot_pen_color': 'k'}

# set defaults
sim.set_defaults(**sim_defaults)
win.pan.setConfig(pan_defaults)

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
exp_ranges.log.connect(win.log)
exp_ranges.sigUpdated.connect(win.pan.plotUpper)
exp_ranges.sigAdded.connect(win.expDock.addItems)
exp_ranges.sigBoundaries.connect(sim.set_boundaries)
win.expDock.sigAddItems.connect(exp_ranges.add_data_files)
win.expDock.sigRemoveItem.connect(exp_ranges.remove)
win.expDock.sigItemChecked.connect(exp_ranges.set_visibility)

sim.log.connect(win.log)
sim.sigUpdateRange.connect(sim_ranges.update)
sim.sigRemoveRange.connect(sim_ranges.remove)
sim.sigLockRanges.connect(sim_ranges.lock)
sim.sigAdded.connect(win.simDock.addItem)
sim_ranges.sigUpdated.connect(win.pan.plotLower)
win.simDock.sigAddItem.connect(sim.add_rotor)
win.simDock.sigRemoveItem.connect(sim.remove_rotor)
win.simDock.sigItemChecked.connect(sim_ranges.set_visibility)

sim.sigInfo.connect(win.stgDock.setSheet)
sim.sigInfo2.connect(win.parDock.setItems)
win.simDock.sigCurrentRowChanged.connect(sim.get_settings)
win.simDock.sigCurrentRowChanged.connect(sim.get_rotor_params)
win.simDock.sigCurrentTextChanged.connect(win.stgDock.setTitle)
win.simDock.sigCurrentTextChanged.connect(win.parDock.setTitle)
win.simDock.sigCurrentTextChanged.connect(win.fitDock.setTitle)
win.simDock.sigApplySettings.connect(sim.apply_settings)
win.stgDock.sigSheetChanged.connect(win.simDock.apply_settings_proxy)


# execute
win.show()
sys.exit(app.exec_())
