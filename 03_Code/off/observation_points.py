import numpy as np
from abc import ABC, abstractmethod
from off.states import States
from off.utils import OFFTools as OT


class ObservationPoints(States, ABC):
    """
    ObservationPoints is the abstract base class for a list of wake tracers / particles
    The class inherits get, set & iterate methods from the abstract States class, init is overwritten
    """

    def __init__(self, number_of_time_steps: int, number_of_states: int):
        """
        ObservationPoints is the abstract base class for a list of wake tracers / particles
        The class inherits get, set & iterate methods from the abstract States class, init is overwritten

        Parameters
        ----------
        number_of_time_steps : int
            number of time steps the states should go back / chain length
        number_of_states : int
            number of states per time step
        """
        super(ObservationPoints, self).__init__(number_of_time_steps, number_of_states)

    @abstractmethod
    def get_world_coord(self) -> np.ndarray:
        """ Returns the x, y, z coordinates of all OPs

        Returns
        -------
        np.ndarray
            m x 3 matrix where the columns are the x,y,z coordinates
        """       
        pass

    @abstractmethod
    def init_all_states(self, wind_speed: float, wind_direction: float, rotor_pos: np.ndarray, time_step: float):
        """
        Creates a downstream chain of OPs
        Overwrites the base method of the States class

        Parameters
        ----------
        wind_speed : float
            Wind speed in m/s
        wind_direction : float
            Wind direction in deg
        rotor_pos : np.ndarray
            1 x 3 vector with x,y,z location of the rotor in the world coordinate system
        time_step : float
            simulation time step in s
        """
        pass


class FLORIDynOPs4(ObservationPoints):

    def __init__(self, number_of_time_steps: int):
        """
        FLORIDynOPs have four states, three in the world coordinate system (x,y,z) and one in the wake coordinate system
        (downstream).

        Parameters
        ----------
        number_of_time_steps : int
            equivalent to OP chain length
        """
        super(FLORIDynOPs4, self).__init__(number_of_time_steps, 4)

    def get_world_coord(self) -> np.ndarray:
        """
        Returns the world coordinates of the OPs

        Returns
        -------
        np.ndarray
            [x, y, z] coordinates in world coordinate system
        """
        return self.states[:, 0:3]

    def init_all_states(self, wind_speed: float, wind_direction: float, rotor_pos: np.ndarray, time_step: float):
        """        
        Creates a downstream chain of OPs
        Overwrites the base method of the States class

        Parameters
        ----------
        wind_speed : float
            Wind speed in m/s
        wind_direction : float
            Wind direction in deg
        rotor_pos : np.ndarray
            1 x 3 vector with x,y,z location of the rotor in the world coordinate system
        time_step : float
            simulation time step in s
        """       
        ot = OT()

        dw = np.arange(self.n_time_steps) * wind_speed
        self.states[:, 0] = np.cos(ot.deg2rad(wind_direction)) * dw + rotor_pos[0]
        self.states[:, 1] = np.sin(ot.deg2rad(wind_direction)) * dw + rotor_pos[1]
        self.states[:, 2] = rotor_pos[2]
        self.states[:, 3] = dw


class FLORIDynOPs6(ObservationPoints):

    def __init__(self, number_of_time_steps: int):
        """
        FLORIDyn OPs with six states, three in the world coordinate system (x,y,z) and one in the wake coordinate system
        (x,y,z). This method requires more memory but less calculations at runtime.

        Parameters
        ----------
        number_of_time_steps : int
            equivalent to OP chain length
        """
        super(FLORIDynOPs6, self).__init__(number_of_time_steps, 6)

    def get_world_coord(self) -> np.ndarray:
        """
        Returns the world coordinates of the OPs

        Returns
        -------
        np.ndarray
            [x, y, z] coordinates in world coordinate system
        """
        return self.op_list[:, 0:3]

    def init_all_states(self, wind_speed: float, wind_direction: float, rotor_pos: np.ndarray, time_step: float):
        """
        Creates a downstream chain of OPs
        Overwrites the base method of the States class

        Parameters
        ----------
        wind_speed : float
            Wind speed in m/s
        wind_direction : float
            Wind direction in deg
        rotor_pos : np.ndarray
            1 x 3 vector with x,y,z location of the rotor in the world coordinate system
        time_step : float
            simulation time step in s
        """
        ot = OT()

        dw = np.arange(self.n_time_steps) * wind_speed
        self.states[:, 0] = np.cos(ot.deg2rad(wind_direction)) * dw + rotor_pos[0]
        self.states[:, 1] = np.sin(ot.deg2rad(wind_direction)) * dw + rotor_pos[1]
        self.states[:, 2] = rotor_pos[2]
        self.states[:, 3] = dw
