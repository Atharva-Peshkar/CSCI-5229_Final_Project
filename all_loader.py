import numpy as np
import os
import trimesh
import time
import pickle 
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Script for loading all the meshes and creating a pkl file.")

# Define command-line arguments
parser.add_argument("--input", "-i", help="Input folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", required=True)

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
save_path = args.input
output_path = args.output

frames = os.listdir(save_path)
frames = sorted([j for j in frames if j.endswith('.obj')])
total_frames = len(frames)
meshes = dict() 

def load_all(dir):
    global meshes
    global total_frames
    global frames
    
    print(f"Found {total_frames} meshes.\n")
    print(frames)

    for i in range(total_frames):
        start = time.time()
        vertices, faces, normals = load_mesh(frames[i])
        meshes[f'{i}'] = {'vertices':vertices,'faces':faces,'normals':normals}
        end = time.time()
        elapsed = end-start
        print(f"Mesh {i} loaded in {elapsed} seconds.\n")


# Function to load a single mesh
def load_mesh(frame):

    file_path = os.path.join(save_path,frame)
    mesh = trimesh.load(file_path)
    vertices = mesh.vertices
    faces = mesh.faces
    normals = []

    # Calculate per-vertex normals
    normals = np.zeros_like(vertices)   # Array of the same shape and type as of the vertices.
    for face in faces:
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]

        edge1 = np.subtract(v1,v0)
        edge2 = np.subtract(v2,v0)

        normal = np.cross(edge1, edge2)
        normals[face] += normal

    # Normalize the normals
    norms = np.linalg.norm(normals, axis=1)
    norms[norms == 0] = 1.0  # Avoid division by zero
    normals /= norms[:, np.newaxis]

    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.uint32), np.array(normals, dtype=np.float32)

load_all(save_path)

with open(os.path.join(output_path,'meshes.pkl'), 'wb') as f:
    pickle.dump(meshes, f)