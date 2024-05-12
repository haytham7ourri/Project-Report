import numpy as np
import pandas as pd
from PIL import Image
from scipy.fft import ifft
import os
from skyfield.api import load

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
def decrypt_and_convert_to_text(encrypted_data, image_path, mars_position):
    try:
        # Load image data
        image = Image.open(image_path)
        image_data_str = image.tobytes().decode('latin-1')

        # Combine both keys
        composite_key = (image_data_str, mars_position)

        # Decrypt data using composite key (XOR decryption)
        decrypted_data = xor_decrypt(encrypted_data, composite_key)

        # Shift ASCII data back to original
        shifted_ascii_data = shift_ascii_data(decrypted_data, -5)  # Assuming a shift of 5 was applied during encryption

        # Convert ASCII binary back to text
        original_text = ""
        for i in range(0, len(shifted_ascii_data), 8):
            byte = shifted_ascii_data[i:i+8]
            original_text += chr(int(byte, 2))

        return original_text
    except Exception as e:
        print("Error during decryption and conversion:", e)
        return None

# Path to the encrypted data Excel file
excel_path = input("Enter the path to the encrypted data Excel file: ")

# Load encrypted data
encrypted_data = load_encrypted_data(excel_path)

# Path to the generated image
image_path = r'C:\Users\hayth\OneDrive\Desktop\hackathon\generated_image.png'

# Sample date for Mars position
year = 2024
month = 5
day = 11

# Get the position of Mars for the sample date
mars_position = get_mars_position(year, month, day)

# Decrypt and convert encrypted data to text
decrypted_text = decrypt_and_convert_to_text(encrypted_data, image_path, mars_position)

# Print decrypted text
if decrypted_text is not None:
    print("Decrypted original text:", decrypted_text)
else:
    print("Failed to decrypt and convert to text.")
