import numpy as np
from MRUVFunctionsUtils import setup_time_range

take_off_start_s = 0
take_off_end = 60
take_off_accel_const = 3.38

cruise_start_s = take_off_end
cruise_end = 3944.77
cruise_start_position_meters = 6084
cruise_speed_const = 202.8
cruise_accel_const = 0

landing_start_s = cruise_end
landing_end_s = 4004.77
landing_start_position_meters = 793916
landing_initial_speed = cruise_speed_const
landing_accel_const = -3.38


take_off_domain, take_off_position, take_off_velocity, take_off_accel = setup_time_range(take_off_start_s, take_off_end,
                                                                                         a0=take_off_accel_const)

cruise_domain, cruise_position, cruise_velocity, cruise_accel = setup_time_range(cruise_start_s, cruise_end,
                                                                                 # frames_scale=0.025,
                                                                                 t0=cruise_start_s,
                                                                                 x0=cruise_start_position_meters,
                                                                                 v0=cruise_speed_const)

landing_domain, landing_position, landing_velocity, landing_accel = setup_time_range(landing_start_s, landing_end_s,
                                                                                     t0=landing_start_s,
                                                                                     x0=landing_start_position_meters,
                                                                                     v0=cruise_speed_const,
                                                                                     a0=landing_accel_const)

time_domain = np.concatenate([take_off_domain, cruise_domain, landing_domain])
accel_values = np.concatenate([take_off_accel, cruise_accel, landing_accel])
velocity_values = np.concatenate([take_off_velocity, cruise_velocity, landing_velocity])
position_values = np.concatenate([take_off_position, cruise_position, landing_position])
