
import sys
import argparse
import subprocess
import os
import shutil

# Paths to scripts and directories
main_script = "demo.py"
mesh_loader = "all_loader.py"
vibe_defualt_output = "/VIBE/output/"

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Script for generating MOCAP meshes using VIBE.")

# Define command-line arguments
parser.add_argument("--input", "-i", help="Video input - file/youtube link", required=True)
parser.add_argument("--output", "-o", help="Output folder", required=True)

# Parse the command-line arguments
args = parser.parse_args()

# Access the values of the arguments
input_path = args.input
output_path = args.output

vibe_fit_command = f"python {main_script} --vid_file {input_path} --output_folder /VIBE/output/ --save_obj"
# Run VIBE script
try:
    subprocess.run([vibe_fit_command], shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running {main_script}: {e}")

video_folder = os.path.join(vibe_defualt_output,os.listdir(vibe_defualt_output)[0])
os.rename(video_folder,os.path.join(vibe_defualt_output,"video_demo"))
video_folder = os.path.join(vibe_defualt_output,os.listdir(vibe_defualt_output)[0])
meshes = os.path.join(video_folder,"meshes")
mesh = os.path.join(meshes,sorted(os.listdir(meshes))[0])

pkl_generate_command = f"python {mesh_loader} --input {mesh} --output {output_path}"
try:
    subprocess.run([pkl_generate_command], shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running {mesh_loader}: {e}")

shutil.rmtree(video_folder)
