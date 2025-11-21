# I/O option for internal voltage. Gets data from internal_voltage and displays it. 
# Inputs: B_MAX, B_ROC.
# Outputs: V_INT, Max E-field, Max current, power density.

import math
import pandas as pd

# Head/brain ellipsoid dimensions (approximate adult brain in meters)
head_a = 0.09  # semi-axis a (lateral) - 9 cm
head_b = 0.09  # semi-axis b (anterior-posterior) - 9 cm  
head_c = 0.065  # semi-axis c (superior-inferior) - 6.5 cm

def calculate_induced_voltage(dB_dt, a, b, c):
    """
    Calculate induced voltage in an ellipsoidal conductor in a changing magnetic field.
    
    Patient is lying down, so B field is parallel to y-axis (anterior-posterior direction).
    
    Using Faraday's law: V = |dΦ/dt| = |dB/dt| * A_max
    where A_max = π * a * c (cross-sectional area perpendicular to y-axis)
    """
    A_max = math.pi * a * c
    V_induced = abs(dB_dt) * A_max
    return V_induced

def calculate_max_electric_field(dB_dt, a, c):
    """
    Calculate maximum induced electric field strength.
    With B parallel to y-axis, E_max occurs at the maximum radius from the y-axis.
    """
    r_max = max(a, c)
    E_max = (r_max / 2) * abs(dB_dt)
    return E_max

def get_user_input():
    """Get and validate user input for simulation parameters."""
    print("=" * 60)
    print("MRI INDUCED VOLTAGE CALCULATOR - I/O SCRIPT")
    print("=" * 60)
    
    while True:
        try:
            max_dB_dt = float(input("\nEnter maximum dB/dt value (T/s): "))
            if max_dB_dt <= 0:
                print("Error: dB/dt must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")
    
    while True:
        try:
            B_max = float(input("Enter maximum B field strength (T): "))
            if B_max <= 0:
                print("Error: B_max must be positive. Please try again.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")
    
    return max_dB_dt, B_max

def run_simulation(max_dB_dt, B_max):
    """Run the MRI voltage simulation and return results DataFrame."""
    NUM_STEPS = 1000
    
    print("\n" + "=" * 60)
    print("SIMULATION PARAMETERS")
    print("=" * 60)
    print(f"Ellipsoid dimensions:")
    print(f"  a (lateral): {head_a*100:.1f} cm")
    print(f"  b (anterior-posterior): {head_b*100:.1f} cm")
    print(f"  c (superior-inferior): {head_c*100:.1f} cm")
    print(f"  Cross-sectional area (a*c): {math.pi * head_a * head_c * 10000:.2f} cm²")
    print(f"\nB field orientation: Parallel to y-axis (patient lying down)")
    print(f"Maximum B field: {B_max} T")
    print(f"Maximum dB/dt: {max_dB_dt} T/s")
    print(f"Number of steps: {NUM_STEPS}")
    print(f"dB/dt increment: {max_dB_dt/NUM_STEPS:.6f} T/s")
    print("=" * 60)

    # Calculate increment
    dB_dt_increment = max_dB_dt / NUM_STEPS
    
    # Store results
    results = []
    
    # Calculate for different dB/dt values
    for i in range(NUM_STEPS + 1):
        B_ROC = i * dB_dt_increment  # dB/dt in Tesla/second
        
        # Calculate induced voltage
        V_INT = calculate_induced_voltage(B_ROC, head_a, head_b, head_c)
        
        # Calculate maximum electric field
        E_max = calculate_max_electric_field(B_ROC, head_a, head_c)
        
        # Estimate maximum current density (assuming brain conductivity σ ≈ 0.33 S/m)
        sigma_brain = 0.33  # S/m
        J_max = sigma_brain * E_max
        
        results.append({
            'Step': i,
            'dB/dt (T/s)': B_ROC,
            'Induced Voltage (V)': V_INT,
            'Max E-field (V/m)': E_max,
            'Max Current Density (A/m²)': J_max,
            'Power Density (W/m³)': sigma_brain * E_max**2
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Biological considerations

    if B_max == 7:
        print("***Caution! High Field***")
    #if B_ROC == :
    
    if 0.1 <= E_max <= 1:
        print("Subtle Neuromodulation")
    elif 1 < E_max <= 10:
        print("***PERIPHERAL NERVE STIMULATION***")
        if 1 < E_max <= 5.8:
            print("!!! Sensory Perception - tingling !!!")
        if 5.8 < E_max <= 10:
            print("!!! Sensory Perception - PAINFUL !!!")    
    
    #if J_max==      

    # Display summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Maximum dB/dt: {df['dB/dt (T/s)'].max():.6f} T/s")
    print(f"Maximum induced voltage: {df['Induced Voltage (V)'].max():.6f} V")
    print(f"Maximum E-field: {df['Max E-field (V/m)'].max():.6f} V/m")
    print(f"Maximum current density: {df['Max Current Density (A/m²)'].max():.6f} A/m²")
    print("=" * 60)
    
    return df

def save_to_csv(df, max_dB_dt, B_max):
    """Save results to CSV file."""
    # Generate filename based on parameters
    filename = f'mri_results_dBdt_{max_dB_dt}Ts_Bmax_{B_max}T.csv'
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"\n✓ Results saved to: {filename}")
    print(f"✓ Total data points: {len(df)}")
    
    # Display summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Maximum dB/dt: {df['dB/dt (T/s)'].max():.6f} T/s")
    print(f"Maximum induced voltage: {df['Induced Voltage (V)'].max():.6f} V")
    print(f"Maximum E-field: {df['Max E-field (V/m)'].max():.6f} V/m")
    print(f"Maximum current density: {df['Max Current Density (A/m²)'].max():.6f} A/m²")
    print("=" * 60)
    
    return filename

def main():
    """Main execution function."""
    # Get user input
    max_dB_dt, B_max = get_user_input()
    
    # Run simulation
    df = run_simulation(max_dB_dt, B_max)
    
    # Save results
    filename = save_to_csv(df, max_dB_dt, B_max)
    
    print(f"\nSimulation complete! Check {filename} for detailed results.")

if __name__ == "__main__":
    main()
