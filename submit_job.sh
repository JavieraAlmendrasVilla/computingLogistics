#!/bin/bash
#SBATCH --job-name= VRPTW         # Job name
#SBATCH --ntasks=1                    # Number of tasks
#SBATCH --cpus-per-task=1             # Number of CPU cores per task
#SBATCH --mem=200M                    # Memory per node
#SBATCH --time=01:00:00               # Time limit hrs:min:sec
#SBATCH --clusters=inter                # Cluster name
#SBATCH --partition=cm2_inter_large_mem  # Partition name
#SBATCH --error=error-logs/vrp/slurm-%j.err        # SLURM error file
#SBATCH --output=slurm-logs/vrp/slurm-%j.out        # SLURM output file


# Ensure logs and error-logs directories exist
mkdir -p logs error-logs error-logs/vrp
mkdir -p logs output-logs slurm-logs/vrp

# Load modules or environment if needed
#module unload python
module load miniconda3
conda init bash > /dev/null 2>&1
# shellcheck disable=SC1090
source ~/.bashrc > /dev/null 2>&1

conda activate cl > /dev/null 2>&1


# Print out the host ID
echo "Host ID: $(hostid)"

# Run the script for each experiment listed in run_list.csv
pids=()
while IFS=',' read -r run_name arg1 arg2; do
    echo "Running job: $run_name with arguments: $arg1 $arg2"

    # Create subdirectories for logs and error-logs based on the job name
    mkdir -p logs/$run_name error-logs/$run_name slurm-logs/$run_name

    # Run the job and save output and error logs in the respective subfolders
    srun --job-name=$run_name \
         --output=logs/$run_name/output-%j.log \
         --error=error-logs/$run_name/error-%j.log \
         python run.py "$arg1" "$arg2" "$run_name" &


    # Capture the PID of the srun command
    pids+=($!)

done < run_list.csv


# Move the SLURM output file to the appropriate job log directory
#mv slurm-job.out slurm-logs/linear_nodes_5_trips_2/
#mv slurm-error.err error-logs/linear_nodes_5_trips_2/

# Wait for all background jobs to finish
for pid in "${pids[@]}"; do
    wait $pid
done
