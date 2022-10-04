import logging
from typing import List
from off.turbine import Turbine
lg = logging.getLogger(__name__)


class WindFarm:
    time_step = -1
    settings_sol: dict()
    turbines: List[Turbine]

    def __init__(self, turbines: List[Turbine], settings_sol: dict):
        """
        Object which hosts the turbine array as well as parameters, constants & variables important to the simulation.

        Parameters
        ----------
        turbines : Turbine object list
            List of turbines in the wind farm
        settings_sol : dict
            Solver settings
        """
        self.turbines = turbines
        self.settings_sol = settings_sol

