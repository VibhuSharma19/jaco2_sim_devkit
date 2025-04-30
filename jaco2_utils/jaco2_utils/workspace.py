#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R

class Manipulator7DOF:
    """
    Class to plot and visualize the workspace of 7-dof Jaco2 manipulator
    """

    def __init__(self):
        """
        Initiate the variables required for defining the manipulator using D-H parameters and joint limits.
        """

        self.d = np.array([-0.2755, 0, -0.41, -0.0098, -0.311, 0, -0.2638])
        self.alpha = np.array([np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi/2, np.pi])
        self.a = np.zeros(7)
        self.joint_limits = np.array([[-2*np.pi, 2*np.pi],
                                      [0.261*np.pi, 1.7389*np.pi],
                                      [-2*np.pi, 2*np.pi],
                                      [0.1667*np.pi, 1.833*np.pi],
                                      [-2*np.pi, 2*np.pi],
                                      [0.361*np.pi, 1.6389*np.pi],
                                      [-2*np.pi, 2*np.pi]])

    def dh_transform(self, theta:float, d:float, a:float, alpha:float):
        """
        Compute individual transformation matrix using DH parameters
        
        Args:
            theta: joint angles. variable for rotational joints
            d: joint offset, variable for prismatic joints
            a: link length
            alpha: link angle
        """
        return np.array([[np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
                         [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
                         [0, np.sin(alpha), np.cos(alpha), d],
                         [0, 0, 0, 1]])

    def forward_kinematics(self, joint_angles: list[float]):
        """
        Compute the forward kinematics of the manipulator.
        
        Args:
            joint_angles: list of joint angles for a single configuration
        """
        T_base = np.array([[1, 0, 0, 0],
                           [0, -1, 0, 0],
                           [0, 0, -1, 0],
                           [0, 0, 0, 1]])
        T = T_base
        for i in range(7):
            T = np.dot(T, self.dh_transform(joint_angles[i], self.d[i], self.a[i], self.alpha[i]))
        return T[:3, 3]  # Extract end-effector position

    def generate_workspace(self, num_samples: int =9000):
        """
        Generate and plot the workspace of the manipulator.
        
        Args:
            num_samples: number of random manipulator configuration
        """

        workspace_points = []
        for _ in range(num_samples):
            joint_angles = [np.random.uniform(low, high) for low, high in self.joint_limits]
            position = self.forward_kinematics(joint_angles)
            workspace_points.append(position)
        workspace_points = np.array(workspace_points)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(workspace_points[:, 0], workspace_points[:, 1], workspace_points[:, 2], s=1, alpha=0.5)
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        ax.set_title("Jaco2 7-DOF Manipulator Workspace")
        plt.show()

def main():
    manipulator = Manipulator7DOF()
    manipulator.generate_workspace()

if __name__ == "__main__":
    main()
