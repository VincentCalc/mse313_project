import csv
from scipy.stats import linregress
import math as m
from matplotlib import pyplot 

strain_rates = [0.1, 0.3, 0.6, 0.9, 1.2, 1.5]
strain_dict = {}
stress_dict = {}
for x in range(1, 19):
    fname = "sample " + str(x) + ".csv"
    with open(fname, 'r') as f:
        reader = csv.reader(f)
        strain_dict[x] = []
        stress_dict[x] = []
        for i in reader:
            strain_dict[x].append(float(i[0]))
            stress_dict[x].append(float(i[1]))
print stress_dict, strain_dict
res = {}
for x in range(1,19):
    num = len(strain_dict[x])
    max_r = 0.0
    temp_res = None
    start = 0
    for i in range(0, num-4):
        temp = linregress(strain_dict[x][i:i+4], stress_dict[x][i:i+4])
        if temp.rvalue > max_r and temp.slope > 5000.0:
            max_r = temp.rvalue
            temp_res = temp
            start = i
    res[x] = (temp_res, start, start + 4)
print res
print_lis = []
for x in range(1,19):
    strain_data = strain_dict[x]
    stress_data = stress_dict[x]
    modulus, start, end = res[x]
    slope = modulus.slope
    pt = start + 1
    disp = strain_data[pt]
    offset = 0.002
    temp = float('inf')
    yield_stress = 0 
    for i in range(len(strain_data)):
        diff = abs(slope*strain_data[i] + stress_data[pt] - (disp+offset)*slope - stress_data[i])
        if temp > diff:
            temp = diff
            yield_stress = stress_data[i]
    print_lis.append((x, strain_rates[(x-1)/3], slope, yield_stress))
with open("output.csv", 'w') as f:
    csv_w = csv.writer(f)
    csv_w.writerow(("sample", "strain rate", "modulus", "yield_stress"))
    csv_w.writerows(print_lis)
