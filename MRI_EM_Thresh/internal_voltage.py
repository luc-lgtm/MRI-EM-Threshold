# Calculator for internal voltage given B_ROC, B_MAX, outputting internal
# voltage and whether or not its afe given biological constraints. Also measures
# how B field from MRI interacts with brain's EM
# All units in meters, tesla. 

import math
import pandas as pd

# Constants (all in SI units)
B_MAX = 7  # Tesla - maximum field strength
B_ROC_INCREMENT = 0.05  # Tesla/second increment for rate of change
NUM_STEPS = 100  # Number of dB/dt values to test

# Head/brain ellipsoid dimensions (approximate adult brain in meters)
head_a = 0.09  # semi-axis a (lateral) - 9 cm
head_b = 0.09  # semi-axis b (anterior-posterior) - 9 cm  
head_c = 0.065  # semi-axis c (superior-inferior) - 6.5 cm

def calculate_induced_voltage(dB_dt, a, b, c):
    """
    Calculate induced voltage in an ellipsoidal conductor in a changing magnetic field.
    
    Patient is lying down, so B field is parallel to y-axis (anterior-posterior direction).
    For a uniform field B parallel to y-axis changing at rate dB/dt,
    the induced electric field at radius r from axis is: E = -(r/2) * dB/dt
    
    The maximum loop is perpendicular to the y-axis.
    
    Using Faraday's law: V = dΦ/dt = dB/dt * pi(a)(c)
    """
    # Maximum cross-sectional area (perpendicular to B field along y-axis)
    # This is the lateral (a) × superior-inferior (c) cross-section
    A_max = math.pi * a * c
    
    # Induced voltage (EMF) around the maximum loop
    V_induced = abs(dB_dt) * A_max
    
    return V_induced

def calculate_max_electric_field(dB_dt, a, c):
    """
    Calculate maximum induced electric field strength from the MRI.
    With B parallel to y-axis, E_max occurs at the maximum radius from the y-axis.
    Maximum radius is in the a-c plane.
    """
    r_max = max(a, c)  # Maximum distance from y-axis
    E_max = (r_max / 2) * abs(dB_dt)
    return E_max

def main():
    print("=" * 80)
    print("MRI INDUCED VOLTAGE CALCULATOR")
    print("=" * 80)
    print(f"\nEllipsoid Parameters:")
    print(f"  Semi-axis a (lateral): {head_a*100:.1f} cm")
    print(f"  Semi-axis b (anterior-posterior): {head_b*100:.1f} cm")
    print(f"  Semi-axis c (superior-inferior): {head_c*100:.1f} cm")
    print(f"  Maximum cross-sectional area: {math.pi * head_a * head_c * 10000:.2f} cm²")
    print(f"\nMagnetic Field Parameters:")
    print(f"  B field orientation: Parallel to y-axis (patient lying down)")
    print(f"  Maximum field strength (B_MAX): {B_MAX} T")
    print(f"  Rate of change increment: {B_ROC_INCREMENT} T/s")
    print(f"  Number of test points: {NUM_STEPS}")
    print("=" * 80)
    
    # Store results
    results = []
    
    # Calculate for different dB/dt values
    for i in range(NUM_STEPS + 1):
        B_ROC = i * B_ROC_INCREMENT  # dB/dt in Tesla/second
        
        # Calculate induced voltage
        V_INT = calculate_induced_voltage(B_ROC, head_a, head_b, head_c)
        
        # Calculate maximum electric field
        E_max = calculate_max_electric_field(B_ROC, head_a, head_c)
        
        # Estimate maximum current density (assuming brain conductivity σ ≈ 0.33 S/m)
        sigma_brain = 0.33  # S/m
        J_max = sigma_brain * E_max
        
        results.append({
            'dB/dt (T/s)': B_ROC,
            'Induced Voltage (V)': V_INT,
            'Max E-field (V/m)': E_max,
            'Max Current Density (A/m²)': J_max,
            'Power Density (W/m³)': sigma_brain * E_max**2
        })
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Display sample of results (first 10, middle 10, last 10)
    print("\n" + "=" * 80)
    print("RESULTS - First 10 values:")
    print("=" * 80)
    print(df.head(10).to_string(index=False))
    
    print("\n" + "=" * 80)
    print(f"RESULTS - Middle 10 values (around {NUM_STEPS//2 * B_ROC_INCREMENT:.3f} T/s):")
    print("=" * 80)
    mid_start = NUM_STEPS//2 - 5
    print(df.iloc[mid_start:mid_start+10].to_string(index=False))
    
    print("\n" + "=" * 80)
    print("RESULTS - Last 10 values:")
    print("=" * 80)
    print(df.tail(10).to_string(index=False))
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS:")
    print("=" * 80)
    print(f"Maximum dB/dt tested: {df['dB/dt (T/s)'].max():.3f} T/s")
    print(f"Maximum induced voltage: {df['Induced Voltage (V)'].max():.6f} V")
    print(f"Maximum E-field: {df['Max E-field (V/m)'].max():.6f} V/m")
    print(f"Maximum current density: {df['Max Current Density (A/m²)'].max():.6f} A/m²")
    
    # Safety context
    print("\n" + "=" * 80)
    print("SAFETY CONTEXT:")
    print("=" * 80)
    print("Typical MRI gradient slew rates: 20-200 T/m/s")
    print("Peripheral nerve stimulation threshold: ~20-80 V/m (depends on pulse duration)")
    print("FDA limit for dB/dt: Varies by pulse duration and location")
    print("=" * 80)
    
     # Option to save to CSV
    save_option = input("\nWould you like to save the complete results to CSV? (yes/no): ")
    if save_option.lower() in ['yes', 'y']:
        filename = 'mri_induced_voltage_results.csv'
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")
    
    return df

if __name__ == "__main__":
    df_results = main()