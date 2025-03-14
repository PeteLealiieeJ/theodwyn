import  numpy                                  as np
from    rohan.common.logging                   import Logger
from    rohan.common.base_controllers          import ControllerBase
from    numpy.typing                           import NDArray
from    typing                                 import Union, TypeVar, List, Optional
from    dataclasses                            import dataclass

@dataclass
class VFB_Setpoints:
    pos_xy  : Optional[NDArray]             = None
    vel_xy  : Optional[NDArray]             = None
    ang_yaw : Optional[Union[NDArray,int]]  = None


SelfViconFeedback = TypeVar("SelfViconFeedback", bound="ViconFeedback" )
class ViconFeedback(ControllerBase):
    """
    Class for handling Vicon Feedback Control
    :param logger: rohan Logger() context
    """

    process_name : str = "ViconFeedback Controller"
    
    p_gain              : NDArray
    a_gain              : float
    traj_start_time     : Optional[float]      = None

    def __init__(
        self,
        p_gain              : NDArray          = np.zeros((2,2)),
        a_gain              : NDArray          = 0.,
        logger              : Optional[Logger] = None, 
        **kwargs,
    ):
        super().__init__(
            logger=logger,
        )
        self.p_gain = p_gain
        self.a_gain = a_gain
    
    def init_controller( self ):
        pass

    def deinit_controller( self ):
        pass

    def determine_control( 
        self, 
        pos_xy_vicon : Optional[NDArray]                = None,
        ang_yaw_vicon: Optional[float]                  = None,
        set_points   : Optional[VFB_Setpoints]          = None
    ) -> Union[ List[float], NDArray ]:
    
        v_out = np.zeros((3,))
        if set_points is None: return v_out

        if not set_points.vel_xy is None:
            v_out[0]    = set_points.vel_xy[0]
            v_out[1]    = set_points.vel_xy[1]

        if (not ang_yaw_vicon is None) and (not set_points.ang_yaw is None):
            a_err       = set_points.ang_yaw - ang_yaw_vicon 
            v_out[2]    = self.a_gain * a_err

        if (not pos_xy_vicon is None) and (not set_points.pos_xy is None):
            p_err       =  set_points.pos_xy - pos_xy_vicon
            v_out[0:2] += ( self.p_gain @ p_err ).flatten()
        
        return v_out