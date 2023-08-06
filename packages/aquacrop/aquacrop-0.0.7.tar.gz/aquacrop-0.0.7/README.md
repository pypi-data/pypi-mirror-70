# AquaCrop-OS
> Python version of AquaCropOS 


## Install

`pip install aquacrop`

AquaCropOS is an environment built for the design and testing of irrigation stratgeies. We are still in early development and so ensure you have downloaded the latest version.

It is built upon the AquaCropOS crop-growth model (written in Matlab `link`) which itself itself is based on the FAO AquaCrop model. Comparisons to both base models are shown in `link`

### to do:

 - Adjust dz so that it covers whole root zone. [0.1]*12 is default. if max_root>1.2 then keep 0.1m to final layer until last layer =0.3 or max_root is inside the root zone. If not add 0.1 to the second last layer and so on. 
 
 - finish jit conversions
 
 - fix func docstrings
 
 - change NewCond class to struct
 
 - create struct for other classes
 
 - tutorials (comparisson)
 
 - batch tutorials
 
 - optimisation
 
 - calibration
 
 - custom irrigation decisions
 
 - env.gym style wrapper
 
 - add a display_full_outputs arg so we dont create a pandas dataframe after each model end
