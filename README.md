# MRI-EM-Threshold
Overview: This project simulates how changing magnetic fields in MRI scanners 
induce electrical effects in the human brain. By modeling the brain as an 
ellipsoid and applying electromagnetic principles, we can calculate induced 
voltages, electric fields, and current densities to assess patient safety during
MRI procedures. The software provides quantitative tools to evaluate safety 
parameters across different MRI field strengths and operational settings.

Objective: 
Calculate the electrical effects induced in brain tissue when exposed to 
time-varying magnetic fields during MRI scanning, providing data to assess 
patient safety and regulatory compliance.

Specific Objectives:

    Geometric Modeling:
    - Create a realistic three-dimensional representation of the human brain and 
    skull.
    - Use mathematical surfaces that allow for analytical calculations.
    - Enable easy modification of dimensions for different patient populations.

    Electromagnetic Analysis:
    - Apply Faraday's Law to calculate how changing magnetic fields create 
    electric fields in tissue.
    - Determine induced voltages around closed loops within the brain.
    - Calculate current densities based on tissue conductivity.

    Safety Assessment:
    - Evaluate multiple safety parameters simultaneously.
    - Test wide ranges of magnetic field parameters.
    - Compare calculated values against established safety thresholds.

    Clinical Applications:
    - Understand peripheral nerve stimulation risks.
    - Assess cardiac pacemaker interference potential.
    - Quantify tissue heating effects.
    - Help establish safe operational limits for new MRI sequences.


Assumptions:
    - The human brain is roughly egg-shaped, making an ellipsoid an appropriate 
    first approximation. This shape is defined by three measurements specified 
    in the code.
    - The model assumes a patient lying on their back with the main magnetic 
    field running along the length of their body (through the chest). This is 
    the standard orientation in most MRI scanners.
    - The critical measurement for our calculations is the cross-sectional area 
    perpendicular to the magnetic field direction. This area determines how much 
    magnetic flux passes through the tissue, which directly relates to the 
    induced electrical effects.

In progress: 
    - Classification of different resulting EM field, current density, induced
    voltage as safe, unsafe, OK. 
    - Assumes uniform conductivity of the brain. Must implement feature that 
    distinguishes different areas of conductivity. (Skull, scalp, brain, etc.)
    - Non-uniform magnetic field funcitonality.
    - Implementing variable surface from Claude website, and integrating over
    that. 


Version: 1.0 (11/12/2025)