#!/bin/bash

#SBATCH -p rcp
#SBATCH --job-name="my_run"
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=10
# #SBATCH --ntasks=40

#SBATCH --time=6:00:00
#SBATCH --exclusive
#SBATCH --export=ALL



#supress warning message for some versions of MPI
export LD_LIBRARY_PATH=/opt/lib/extras:$LD_LIBRARY_PATH

# Go to the directory from which our job was launched
#cd $SLURM_SUBMIT_DIR

module purge
module load mpi/openmpi/gcc
module load libs/fftw3/gcc-openmpi
module load apps/denise_black_edition/gcc-openmpi/1.4

srun ../bin/sofi2D ./2_setparmsSOFI2D.json 
