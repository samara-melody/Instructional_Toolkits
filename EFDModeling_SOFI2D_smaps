# This is an instructive toy example for running SOFI2D (https://gitlab.kit.edu/kit/gpi/ag/software/sofi2d) through Slurm

1. Use the python notebook **1_build_models+aquisition_files** to generate a simple layered model (Vp, Vs, and density) and define the acquisition geometry (sources and receivers). Once the inset plots look correct, export the models, sources, and receiver information to their respective folders at the end of the notebook.

2. Set your parameters in **2_setparmsSOFI2D.json** for your forward simulation. See the SOFI2D documentation for detailed guidance.

3. In **3_runSOFI2D.sh**, define how you will execute this program using SLURM, then run this script using "sbatch ./3_runSOFI2D.sh". Use "tail -f slurm-########.out" to view a live verbose of your slurm output log.

4. The data are output to **data_rawout** as shot gathers. In **4_preprocess_shots.sh**, you can preprocess the data if needed — downsample, define header fields, and perform any additional conditioning.
