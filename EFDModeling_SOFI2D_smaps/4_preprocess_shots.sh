#!/bin/bash

mkdir -p data_preprocessed
mkdir -p data_preprocessed/allshots
mkdir -p data_preprocessed/separatedshots

dirs=$(find ./data_rawout* -type d)

### Define header information which will be mapped to SU files 
### This is based on the parameters of the forward simulation
D1=.0005 # input sampling interval can be determined from: DT * NDT for output seismograms
NT=1000  # input no. of time samples: TIME / D1

# We set a fine sampling to overcome numerical artifacts in simulation
# However, we will not have frequencies in the data that require
# this high density of sampling / data size
# So we define a reasonable downsampled interval and no. of time samples
DTOUT=.00125  # 1.25 ms is still 'overkill' for seismic data, 2 or 4 ms might be more reasonabl
scalar=$(echo "scale=2; $DTOUT/$D1" | bc)
NTOUT=$(echo "scale=2; $NT/$scalar" | bc)
# Calculate Nyquist frequencies in and out so we can apply a high-pass filter on data
Ny_DTIN=$(echo "scale=2; 1/($D1*2)" | bc)
Ny_DTOUT=$(echo "scale=2; $Ny_DTIN/$scalar" | bc)


## For all files in the output directory (SU)
for j in $dirs; do
    for i in $(ls "$j"); do
        echo "$j ---- $i"

        # Each shot gather component (e.g. p, vy, vz, div and curl) are saved with suffix: ".shot#"
        # A more helpful labeling would be to associate these gathers with the shot X position.
        # This renaming is done in the block of code below.
        suwind < "$j/$i" key=tracl min=2 max=2 | sugethw key=sx > tmp
        x=$(sed -n -e 's/^.*=//p' tmp)
        echo "$i" > tmp2
        o=$(sed -n -e 's/^.*_//p' tmp2)
        div=1000
        sx=$(expr $x / $div)
        var=$(echo "$i" | sed -r -e 's/.su.*//')
        var="${var}_${sx}.su"

        # Correct and set header information. Below I...
        # ... scale the offset, source and receiver locations (suchw...)
        # ... reset the scale factors (sushw...)
        # ... shift my gathers in time to account for the wavelet-peak delay (sushw tstat and sustatic)
        # ... calculate and set signed-offsets (suazimuth...)
        # ... resample the data and reset associated header (suresamp...sushw...)
        # ... window shot gathers to reasonable offsets, spacing and time extents

        suchw < "$j/$i" key1=offset,sx,gx,sdepth,gelev,swdep key2=offset,sx,gx,sdepth,gelev,swdep  key3=offset,sx,gx,sdepth,gelev,swdep  b=.001,.001,.001,.001,.001,.001 | \
        sushw key=scalco,scalel,tstat a=0,0,190 | sustatic hdrs=1 | \
        suazimuth offset=1 signedflag=1 | \
        suresamp dt=$DTOUT nt=$NTOUT | \
	    sushw key=d1 a=$DTOUT | \
	    sudipfilt dx=1 slopes=0,.0004,.0005,.0006 amps=0,0,1,1 | \
        suwind key=offset min=10 max=400 j=10 itmax=240 > ./data_preprocessed/separatedshots/$var

        echo "Finished creating shot file: $var"
        echo
        echo
    done
done

# List of components to concatenate
components=("vx" "vy" "p" "curl" "div" "r")
# Concatenate all shots for each component
for comp in "${components[@]}"; do
    cat ./data_preprocessed/separatedshots/*$comp*.su > ./data_preprocessed/allshots/$comp.su
done

# Rotate horizontal component X into radial if needed
./suRotHor2c in1="./data_preprocessed/allshots/vx.su" in2="./data_preprocessed/allshots/vx.su" o1="./data_preprocessed/allshots/r.su" o2="tmp" aziIn=0.0

rm ./tmp*