#!/usr/bin/python3

import math

class Conversions:

   """
     The class used to converts angles from one type to another type representation.
     available conversions are:
     - Quaternion to Euler
     - Euler to Quaternion
     - Quaternion to Axis-Angle
     - Axis-Angle to Quaternion
     - Euler angles to Axis-Angle
     - Axis-Angle to Euler

     Reference: "https://www.euclideanspace.com/maths/geometry/rotations/euler/index.htm"
    """
   
   @staticmethod
   def euler_to_quaternion(euler_angles:list)->list :
      """
      euler_to_quaternion:
       Converts the euler angles (roll, pitch, yaw) to quaternion

      Args:
          euler_angles (list): [roll, pitch, yaw] (in radians)
      
      Returns:
         quaternion form as list [x, y, z, w]
      """

      roll, pitch, yaw = euler_angles
        
      cy = math.cos(yaw * 0.5)
      sy = math.sin(yaw * 0.5)
      cp = math.cos(pitch * 0.5)
      sp = math.sin(pitch * 0.5)
      cr = math.cos(roll * 0.5)
      sr = math.sin(roll * 0.5)
      
      w = cr * cp * cy + sr * sp * sy
      x = sr * cp * cy - cr * sp * sy
      y = cr * sp * cy + sr * cp * sy
      z = cr * cp * sy - sr * sp * cy
      
      return [x, y, z, w]
   
   @staticmethod
   def quaternion_to_euler(quaternion:list, in_degree:bool = False)-> list :
      """
      quaternion_to_euler:
       Converts the given quaternion angle representation to euler angle representation

      Args:
          quaternion (list): [x, y, z, w]
          in_degree (bool): set wether to get euler angles in degree or in radians. (default - False)

      Returns:
          list: euler angles as [roll, pitch, yaw]
      """
      x, y, z, w = quaternion
        
      t0 = 2.0 * (w * x + y * z)
      t1 = 1.0 - 2.0 * (x * x + y * y)
      roll = math.atan2(t0, t1)
      
      t2 = 2.0 * (w * y - z * x)
      t2 = max(-1.0, min(1.0, t2))
      pitch = math.asin(t2)
      
      t3 = 2.0 * (w * z + x * y)
      t4 = 1.0 - 2.0 * (y * y + z * z)
      yaw = math.atan2(t3, t4)
      
      if in_degree == True:
         roll = math.degrees(roll)
         pitch = math.degrees(pitch)
         yaw = math.degrees(yaw)

         return [roll, pitch, yaw]
      
      else:
         return [roll, pitch, yaw]
   
   @staticmethod
   def quaternion_to_axis_angle(quaternion:list, in_degree:bool = False) -> dict :
      """
      quaternion_to_axis_angle:
      Converts the given quaternion to axis-angle representation

      Args:
          quaternion (list): the quaternion to convert [x, y, z, w]
          in_degree (bool, optional): sets the angle output unit to degree or radian. Defaults to False.

      Returns:
          dict: a dict of axis and angle
      """
      x, y, z, w = quaternion
      angle = 2.0 * math.acos(w)
      s = math.sqrt(1 - w * w) if w * w < 1 else 1e-6
      
      if s < 1e-6:
          axis = [1.0, 0.0, 0.0]
      else:
          axis = [x / s, y / s, z / s]
      
      if in_degree == True:
         angle = math.degrees(angle)
      else:
         angle = angle

      return { "axis": axis, "angle": angle }
   
   @staticmethod
   def axis_angle_to_quaternion(axis_angle:dict) -> list:
      """
      axis_angle_to_quaternion:
      Converts the given axis-angle representation to q quaternion 

      Args:
          axis_angle (dict): a dictionary of form {'axis':[], 'angle':angle(rad)}

      Returns:
          list: a quaternion of form [x, y, z, w]
      """
      axis, angle = axis_angle["axis"], axis_angle["angle"]
      half_angle = angle / 2.0
      s = math.sin(half_angle)
      x = axis[0] * s
      y = axis[1] * s
      z = axis[2] * s
      w = math.cos(half_angle)

      return [x, y, z, w]
   
   @staticmethod
   def euler_to_axis_angle(euler_angles:list, in_degree:bool = False)-> dict:
      """
      euler_to_axis_angle:
      Converts the given euler angles (RPY) to axis-angle representation

      Args:
          euler_angles (list): euler angles as [Roll, Pitch, Yaw]
          in_degree (bool, optional): sets the angle output unit to degree or radian. Defaults to False.


      Returns:
          dict: axis-angle dict as {'axis':axis, 'angle':angle}
      """
      quat = Conversions.euler_to_quaternion(euler_angles)
      return Conversions.quaternion_to_axis_angle(quat, in_degree)
   
   @staticmethod
   def axis_angle_to_euler(axis_angle:dict, in_degree:bool = False)->list:
      """
      axis_angle_to_euler:
      Converts the given axis-angle representation to euler angles (RPY) 

      Args:
          axis_angle (dict):a dictionary of form {'axis':[], 'angle':angle(rad)}
          in_degree (bool, optional): sets the angle output unit to degree or radian. Defaults to False.

      Returns:
          list: outputs the euler angles as [roll, pitch, yaw]
      """
      quat = Conversions.axis_angle_to_quaternion(axis_angle)
      return Conversions.quaternion_to_euler(quat, in_degree)

   @staticmethod
   def quaternion_to_matrix(quaternion:list)-> list:
      """
      quaternion_to_matrix:
      Covert a quaternion into a full three-dimensional rotation matrix.
 
      Args:
         quaternion (list): A 4 element array representing the quaternion (x, y, z, w) 
 
      Returns:
         list: A 3x3 element matrix representing the full 3D rotation matrix. 
             This rotation matrix converts a point in the local reference 
             frame to a point in the global reference frame.
      """
      q0 = quaternion[0]
      q1 = quaternion[1]
      q2 = quaternion[2]
      q3 = quaternion[3]

      # First row of the rotation matrix
      r00 = 2 * (q0 * q0 + q1 * q1) - 1
      r01 = 2 * (q1 * q2 - q0 * q3)
      r02 = 2 * (q1 * q3 + q0 * q2)

      # Second row of the rotation matrix
      r10 = 2 * (q1 * q2 + q0 * q3)
      r11 = 2 * (q0 * q0 + q2 * q2) - 1
      r12 = 2 * (q2 * q3 - q0 * q1)

      # Third row of the rotation matrix
      r20 = 2 * (q1 * q3 - q0 * q2)
      r21 = 2 * (q2 * q3 + q0 * q1)
      r22 = 2 * (q0 * q0 + q3 * q3) - 1

      # 3x3 rotation matrix
      rot_matrix = [[r00, r01, r02],
                     [r10, r11, r12],
                     [r20, r21, r22]]
      return rot_matrix
   
   @staticmethod
   def euler_to_matrix(euler_angles:list)->list:
      """
      euler_to_matrix:
      Converts the given euler angles to a 3x3 rotation matrix

      Args:
          euler_angles (list): euler angles as [roll, pitch, yaw] (in rads)

      Returns:
          list: A 3x3 element matrix representing the full 3D rotation matrix.
      """
      quat = Conversions.euler_to_quaternion(euler_angles)
      return Conversions.quaternion_to_matrix(quat)
   
