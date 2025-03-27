#!/usr/bin/python3
'''
Created on 03-02-2024

@author: Kyllian Cuevas, Thomas Mirbey
@version: 1

Positioning System - N Lateration exercise (3D version)
'''

#------------------
# Import
#------------------

import matplotlib.pyplot as plt

from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import random
import json

#------------------
# Functions
#------------------

class AccessPoint:
    def __init__(self, id, x, y, z, radius, color):
        """
        @args:
        id (int): Identifier for the access point.
        x (float): x-coordinate of the access point.
        y (float): y-coordinate of the access point.
        z (float): z-coordinate of the access point.
        radius (float): Distance from the access point to the phone.
        color (str): Color of the sphere to draw.
        """
        # Assert that inputs are valid types
        assert isinstance(id, int), "Access point id must be an integer"
        assert isinstance(x, (int, float)), "x-coordinate must be a number"
        assert isinstance(y, (int, float)), "y-coordinate must be a number"
        assert isinstance(z, (int, float)), "z-coordinate must be a number"
        assert isinstance(radius, (int, float)) and radius > 0, "radius must be a positive number"
        assert isinstance(color, str), "color must be a string"
        
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.color = color

    def draw_sphere(self, ax):
        """
        @args:
        ax (matplotlib.axes._subplots.Axes3DSubplot): The 3D Axes object to draw the sphere on.
        """
        try:
            # Use scatter points
            phi = np.linspace(0, np.pi, 100)
            theta = np.linspace(0, 2 * np.pi, 100)
            phi, theta = np.meshgrid(phi, theta)
            x = self.radius * np.sin(phi) * np.cos(theta) + self.x
            y = self.radius * np.sin(phi) * np.sin(theta) + self.y
            z = self.radius * np.cos(phi) + self.z
            
            # Draw sphere
            ax.plot_surface(x, y, z, color=self.color, alpha=0.2)

            # Draw a cross at the center of the sphere
            cross_size = self.radius * 0.2  
            ax.plot([self.x - cross_size, self.x + cross_size], [self.y, self.y], [self.z, self.z], color=self.color, linewidth=2)
            ax.plot([self.x, self.x], [self.y - cross_size, self.y + cross_size], [self.z, self.z], color=self.color, linewidth=2)
            ax.plot([self.x, self.x], [self.y, self.y], [self.z - cross_size, self.z + cross_size], color=self.color, linewidth=2)
        except Exception as e:
            print(f"Error in drawing sphere for AccessPoint {self.id}: {e}")

def draw(phone, access_points):
    """
    @args:
    phone (dict): Dictionary containing 'x', 'y', and 'z' coordinates of the phone.
    access_points (list): List of AccessPoint objects.
    """
    try:
        # Assert that phone coordinates are valid
        assert isinstance(phone, dict), "Phone data should be a dictionary"
        assert all(coord in phone for coord in ['x', 'y', 'z']), "Phone dictionary must contain 'x', 'y', and 'z' keys"
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Draw each access point's sphere
        for ap in access_points:
            ap.draw_sphere(ax)
            # Label for each AccessPoint
            ax.text(ap.x, ap.y, ap.z, f'AP{ap.id}', color='black', fontsize=10)

        # Draw the phone's position
        cross_size = 0.1
        ax.plot([phone['x'] - cross_size, phone['x'] + cross_size], [phone['y'], phone['y']], [phone['z'], phone['z']], color='purple', linewidth=2)
        ax.plot([phone['x'], phone['x']], [phone['y'] - cross_size, phone['y'] + cross_size], [phone['z'], phone['z']], color='purple', linewidth=2)
        ax.plot([phone['x'], phone['x']], [phone['y'], phone['y']], [phone['z'] - cross_size, phone['z'] + cross_size], color='purple', linewidth=2)

        # Label for the phone
        ax.text(phone['x'], phone['y'], phone['z'], 'Phone', color='purple', fontsize=12)

        # Adjust plot limits 
        all_x = [ap.x for ap in access_points]
        all_y = [ap.y for ap in access_points]
        all_z = [ap.z for ap in access_points]
        all_r = [ap.radius for ap in access_points]

        # Minimal and Maximal dimension
        x_min, x_max = min(all_x) - max(all_r) - 1, max(all_x) + max(all_r) + 1
        y_min, y_max = min(all_y) - max(all_r) - 1, max(all_y) + max(all_r) + 1
        z_min, z_max = min(all_z) - max(all_r) - 1, max(all_z) + max(all_r) + 1

        # Resize
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)
        
        ax.set_title("3D N lateration exercise")
        plt.show()
    except AssertionError as e:
        print(f"Input error: {e}")
    except Exception as e:
        print(f"Error in drawing: {e}")


def calculate_error(position, access_points):
    """
    @args:
    position (list): Estimated position of the phone [x, y, z].
    access_points (list): List of AccessPoint objects containing the positions and radius.
    
    @return:
    float: The sum of squared errors between calculated and actual distances from the phone
           to each access point.
    """
    try:
        assert len(position) == 3, "Position should be a list of 3 coordinates [x, y, z]"
        x, y, z = position
        error = 0
        for ap in access_points:
            distance = np.sqrt((x - ap.x)**2 + (y - ap.y)**2 + (z - ap.z)**2)
            error += (distance - ap.radius)**2 
        return error
    except Exception as e:
        print(f"Error in error calculation: {e}")
        return float('inf')  # Return a large error value in case of an issue

def trilaterate(access_points):
    """
    @args:
    access_points (list): List of AccessPoint objects.

    @return:
    list: Estimated position [x, y, z] of the phone.
    
    Estimate the phone's position by minimizing the error between
    the measured and calculated distances from the access points.
    """
    try:
        # Assert that there are at least 3 access points
        assert len(access_points) >= 3, "At least 3 access points are required for trilateration"
        
        initial_guess = [0, 0, 0]  # Initial guess for the position in 3D
        result = minimize(calculate_error, initial_guess, args=(access_points,))
        estimated_position = result.x
        return estimated_position
    except AssertionError as e:
        print(f"Input error in trilaterate: {e}")
    except Exception as e:
        print(f"Error in trilateration: {e}")
        return [0, 0, 0]  # Return a default position in case of an error

#------------------
# Main
#------------------

if __name__ == '__main__':
    try:
        access_points = [
            AccessPoint(id=0, x=0.5, y=0.5, z=0.5, radius=3, color='blue'),
            AccessPoint(id=1, x=4, y=0, z=0, radius=2, color='red'),
            AccessPoint(id=2, x=4, y=5, z=5, radius=4.2, color='green'),
            AccessPoint(id=3, x=3, y=3, z=3, radius=2.5, color='yellow'),
        ]

        # Estimate the phone's position
        position = trilaterate(access_points)
        phone = {"x": position[0], "y": position[1], "z": position[2]}
        print(f"Estimated phone position is : {position}")
        
        # Draw the access points and phone
        draw(phone, access_points)

    except Exception as e:
        print(f"Error in main execution: {e}")
