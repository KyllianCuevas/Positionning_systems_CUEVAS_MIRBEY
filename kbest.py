#!/usr/bin/python3
'''
Created on 03-02-2024

@author: Kyllian Cuevas, Thomas Mirbey
@version: 1.1

Positioning System - KBest Neighboors
'''

#------------------
# Import
#------------------

import numpy as np
import matplotlib.pyplot as plt

#------------------
# Functions
#------------------

def compute_similarity(reference_vectors, mp_vector):
    """
        @args:
        reference_vectors (numpy.ndarray): Array of RSS values for different cells.
        mp_vector (numpy.ndarray): RSS values measured by the mobile phone.

        Computes the Euclidean distance between the mobile phone power vector and reference power vectors.
    """
    try:
        assert reference_vectors.shape[1] == mp_vector.shape[0], "Dimension mismatch between reference vectors and mp_vector"
        differences = reference_vectors - mp_vector
        squared_differences = differences ** 2
        metrics = np.sqrt(np.sum(squared_differences, axis=1))  # Euclidean norm
        return metrics
    except Exception as e:
        print(f"Error in compute_similarity: {e}")
        return np.array([])

def find_best_cells(reference_vectors, mp_vector, k=4):
    """
        @args:
        reference_vectors (numpy.ndarray): Array of RSS values for different cells.
        mp_vector (numpy.ndarray): RSS values measured by the mobile phone.
        k (int): Number of best matching cells to select.

        Finds the K best matching cells based on the similarity metric.
    """
    try:
        assert k > 0, "k must be greater than zero"
        metrics = compute_similarity(reference_vectors, mp_vector)
        assert metrics.size > 0, "Metrics computation failed"
        best_indices = np.argsort(metrics)[:k]  # Get indices of K best cells
        return best_indices, metrics[best_indices]
    except Exception as e:
        print(f"Error in find_best_cells: {e}")
        return np.array([]), np.array([])

def compute_barycentric_position(cell_positions, best_indices, metrics):
    """
        @args:
        cell_positions (numpy.ndarray): Array of positions for all cells.
        best_indices (numpy.ndarray): Indices of the best K selected cells.
        metrics (numpy.ndarray): Similarity metrics for the best K selected cells.

        Computes the barycentric position of the mobile phone using the best K cells.
    """
    try:
        assert len(best_indices) == len(metrics), "Mismatch in best indices and metrics length"
        weights = 1 / metrics  # Inverse of metric as weight (lower metric = higher weight)
        weights /= np.sum(weights)  # Normalize
        estimated_position = np.sum(cell_positions[best_indices] * weights[:, np.newaxis], axis=0)
        return estimated_position
    except Exception as e:
        print(f"Error in compute_barycentric_position: {e}")
        return np.array([None, None])

def plot_map(cell_positions, best_indices, estimated_position):
    """
        @args:
        cell_positions (numpy.ndarray): Array of positions for all cells.
        best_indices (numpy.ndarray): Indices of the best K selected cells.
        estimated_position (numpy.ndarray): Computed position of the mobile phone.

        Plots the map with cell positions, best cells, and estimated position.
    """
    try:
        plt.figure(figsize=(6,6))
        plt.scatter(cell_positions[:,0], cell_positions[:,1], c='blue', label='Cells')
        plt.scatter(cell_positions[best_indices,0], cell_positions[best_indices,1], c='red', label='Best Cells')
        plt.scatter(estimated_position[0], estimated_position[1], c='green', marker='x', s=100, label='Estimated Position')
        
        for i, pos in enumerate(cell_positions):
            label = f"C{i+1}"
            if i in best_indices:
                label += " (Best)"
            plt.text(pos[0]+0.1, pos[1]+0.1, label, fontsize=12)
        
        plt.xlabel("X Position")
        plt.ylabel("Y Position")
        plt.title("Positioning Map")
        plt.legend()
        plt.grid()
        plt.show()
    except Exception as e:
        print(f"Error in plot_map: {e}")

#------------------
# Variables
#------------------

reference_vectors = np.array([
    [50, 60, 70],  # Cell 1 RSS values
    [55, 65, 75],  # Cell 2 RSS values
    [40, 50, 60],  # Cell 3 RSS values
    [45, 55, 65],  # Cell 4 RSS values
    [30, 40, 50],  # Cell 5 RSS values
])

mp_vector = np.array([48, 58, 68])  # Mobile phone measured RSS

cell_positions = np.array([
    [0, 0],  # Position of Cell 1
    [1, 0],  # Position of Cell 2
    [0, 1],  # Position of Cell 3
    [1, 1],  # Position of Cell 4
    [2, 2],  # Position of Cell 5
])

#------------------
# Main
#------------------

if __name__ == '__main__':
    best_indices, best_metrics = find_best_cells(reference_vectors, mp_vector, k=4)
    position = compute_barycentric_position(cell_positions, best_indices, best_metrics)

    print("Estimated Position:", position)
    plot_map(cell_positions, best_indices, position)