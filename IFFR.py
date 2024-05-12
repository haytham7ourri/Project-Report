import numpy as np
import pandas as pd  # Import pandas
from scipy.fft import ifft

# Function to load only complex numbers from Excel file
def load_encrypted_data(excel_path):
    try:
        # Read Excel file with Pandas
        df = pd.read_excel(excel_path)
        
        # Convert the 'Encrypted_Data' column to complex numbers
        encrypted_data = df['Encrypted_Data'].astype(complex)
        
        return encrypted_data
    except Exception as e:
        print("Error during data loading:", e)
        return None

# Function to decrypt the data and convert it to text
def decrypt_and_convert_to_text(encrypted_data):
    try:
        # Convert encrypted data to a NumPy array of complex numbers
        encrypted_data_array = np.array(encrypted_data)
        
        # Apply IFFT
        decrypted_data = ifft(encrypted_data_array)
        
        # Print IFFT coefficients
        print("IFFT coefficients before modification:")
        for coef in decrypted_data:
            # Round coefficients to the nearest integer
            rounded_coef = np.round(coef.real)
            print(rounded_coef)
        
        # Remove the third, fourth, and fifth terms
        decrypted_data[3:6] = 0
        
        # Round coefficients to the nearest integer
        decrypted_data = np.round(decrypted_data.real)
        
        # Convert the real part to ASCII text
        ascii_text = ''.join([chr(int(byte)) for byte in decrypted_data])
        
        # Replace "Â" with "ð"
        ascii_text = ascii_text.replace("Â", "ð")
        
        return ascii_text
    except Exception as e:
        print("Error during decryption and conversion:", e)
        return None

# Path to the Excel file containing encrypted data
excel_path = r'C:\Users\hayth\OneDrive\Desktop\hackathon\encrypted_data.xlsx'

# Load encrypted data
encrypted_data = load_encrypted_data(excel_path)

if encrypted_data is not None:
    # Decrypt and convert to text
    decrypted_text = decrypt_and_convert_to_text(encrypted_data)
    
    if decrypted_text is not None:
        # Print decrypted text
        print("Decrypted text:", decrypted_text)
    else:
        print("Failed to decrypt and convert to text.")
else:
    print("Failed to load encrypted data.")
