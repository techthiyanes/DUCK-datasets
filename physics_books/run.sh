#!/usr/bin/env bash

# em_quals
echo -e "\e[1mem_quals\e[0m"
python preprocess.py --output tmp.txt --input data/em_quals.txt
python extract_problems.py --input tmp.txt \
                           --output data/em_quals_output.json \
                           --book "Problems and Solutions on Electromagnetism" \
                           --topic "Electrostatics" 1001 1108 \
                           --topic "Magnetostatic Field and Quasi-Stationary Electromagnetic Fields" 2001 2119 \
                           --topic "Circuit Analysis" 3001 3090 \
                           --topic "Electromagnetic Waves" 4001 4067 \
                           --topic "Relativity, Particle-Field Interactions" 5001 5056
echo --------------------------------

# mechanics_quals
echo -e "\e[1mmechanics_quals\e[0m"
python preprocess.py --output tmp.txt --input data/mechanics_quals.txt
python extract_problems.py --input tmp.txt \
                           --output data/mechanics_quals_output.json \
                           --book "Problems and Solutions on Mechanics" \
                           --topic "Newtonian Mechanics" 1001 1272 \
                           --topic "Analytical Mechanics" 2001 2084 \
                           --topic "Special Relativity" 3001 3054
echo --------------------------------

# optics
echo -e "\e[1moptics\e[0m"
python preprocess.py --output tmp.txt --input data/optics.txt
python extract_problems.py --input tmp.txt \
                           --output data/optics_output.json \
                           --book "Problems and Solutions on Optics" \
                           --topic "Geometrical Optics" 1001 1041 \
                           --topic "Wave Optics" 2001 2089 \
                           --topic "Quantum Optics" 3001 3030
echo --------------------------------

# quantum
echo -e "\e[1mquantum\e[0m"
python preprocess.py --output tmp.txt --input data/quantum.txt
python extract_problems.py --input tmp.txt \
                           --output data/quantum_output.json \
                           --book "Problems and Solutions on Quantum Mechanics" \
                           --topic "Basic Principles and One-dimensional Motions" 1001 1072 \
                           --topic "Central Potentials" 2001 2023 \
                           --topic "Spin and Angular Momentum" 3001 3048 \
                           --topic "Motion in Electromagnetic Fields" 4001 4016 \
                           --topic "Perturbation Theory" 5001 5083 \
                           --topic "Scattering Theory and Quantum Transitions" 6001 6061 \
                            --topic "Many-Particle Systems" 7001 7037 \
                            --topic "Miscellaneous Topics" 8001 8040
echo --------------------------------

# statmech
echo -e "\e[1mstatmech\e[0m"
python preprocess.py --output tmp.txt --input data/statmech.txt
python extract_problems.py --input tmp.txt \
                           --output data/statmech_output.json \
                           --book "Problems and Solutions on Thermodynamics and Statistical Mechanics" \
                           --topic "Thermodynamics" 1001 1159 \
                           --topic "Statistical Physics" 2001 2208
echo --------------------------------

# solid_state
echo -e "\e[1msolid_state\e[0m"
python preprocess.py --output tmp.txt --input data/solid_state.txt
python extract_problems.py --input tmp.txt \
                           --output data/solid_state_output.json \
                           --book "Problems and Solutions on Solid State Physics, Relativity and Miscellaneous Topics" \
                           --topic "Solid State Physics" 1001 1081 \
                           --topic "Relativity" 2001 2028 \
                           --topic "Miscellaneous Topics" 3001 3056
