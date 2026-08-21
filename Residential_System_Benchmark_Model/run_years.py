import os
import numpy as np
import subprocess as sp

home = '//'.join(os.path.dirname(os.path.abspath(__file__)).split('//'))
print(home)
years=np.arange(2010,2020)

for year in years:
	cd_path = home + "//" + str(year) + " Residential System Benchmark Model//python//main.py"
	os.system(('python "' + cd_path +'"' ))
