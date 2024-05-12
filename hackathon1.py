import numpy as np
import pandas as pd
from PIL import Image
from scipy.fft import fft
import os
from skyfield.api import load

# Function to convert text to ASCII binary
def text_to_ascii_binary(text):
    binary_list = [format(ord(char), '08b') for char in text]
    return ''.join(binary_list)

# Function to shift ASCII data
def shift_ascii_data(ascii_data, shift_amount):
    shifted_data = ''.join(chr((ord(char) + shift_amount) % 256) for char in ascii_data)
    return shifted_data

# Function to generate random image (replace with your actual image generation method)
def generate_random_image():
    image = Image.new('RGB', (128, 128))  # Example: creating a black image
    return image

# Function to perform XOR encryption
def xor_with_key(data, key):
    data_bytes = data.encode()  # Convert data to bytes for XOR
    key_bytes = key.encode() if isinstance(key, str) else key  # Convert key to bytes if it's a string
    padded_data = data_bytes[:len(key_bytes)] + bytes([0] * (len(key_bytes) - len(data_bytes))) if len(data_bytes) < len(key_bytes) else data_bytes
    return ''.join(chr(a ^ b) for a, b in zip(padded_data, key_bytes))

# Function to get the position of Mars at a specific date
def get_mars_position(year, month, day):
    # Load ephemeris data (assuming it's already done)
    eph = load('de421.bsp')

    # Select the date
    ts = load.timescale()
    t = ts.utc(year, month, day)

    # Get the position of Mars
    astrometric = eph['mars'].at(t).observe(eph['earth'])
    apparent = astrometric.apparent()
    ra, dec, distance = apparent.radec()

    # Convert RA and Dec to byte arrays for encryption (example)
    ra_bytes = int(ra.hours * 3600).to_bytes(4, byteorder='big')
    dec_bytes = abs(int(dec.degrees * 3600)).to_bytes(4, byteorder='big')  # Convert to absolute value
    mars_position = ra_bytes + dec_bytes

    return mars_position

# Prompt user to enter the data
user_data = input("Enter the data you want to encrypt: ")

# Sample date
year = 2024
month = 5
day = 11

# Convert user data to ASCII binary
ascii_binary_data = text_to_ascii_binary(user_data)

# Shift ASCII data
shifted_ascii_data = shift_ascii_data(ascii_binary_data, 5)  # Example shift amount

# Generate random image
generated_image = generate_random_image()

# Convert image data to string for encryption
image_data_str = generated_image.tobytes().decode('latin-1')

# Save the generated image used for noise
output_dir = r'C:\Users\hayth\OneDrive\Desktop\hackathon'
os.makedirs(output_dir, exist_ok=True)
generated_image_path = os.path.join(output_dir, "generated_image.png")
generated_image.save(generated_image_path)

# Get the position of Mars for the sample datej

mars_position = get_mars_position(year, month, day)

# Combine both keys
composite_key = (image_data_str, mars_position)

# Encrypt data using composite key (XOR on bytes)
encrypted_data = xor_with_key(shifted_ascii_data, composite_key[0])  # XOR with image data
encrypted_data = xor_with_key(encrypted_data, composite_key[1])  # XOR with Mars position
print(encrypted_data)

# Apply Fourier transform on encrypted data
encrypted_data_bytes = encrypted_data.encode('utf-8')  # Convert to bytes for FFT
fourier_transform = fft(np.frombuffer(encrypted_data_bytes, dtype=np.uint8))  # Convert bytes to numpy array for FFT

# Print encrypted Fourier coefficients (placeholder for actual encrypted data)
print("Encrypted data (placeholder for actual encrypted data):", fourier_transform)

# Save encrypted data to Excel file
data_to_save = {'Encrypted_Data': fourier_transform}
df = pd.DataFrame(data_to_save)
excel_path = os.path.join(output_dir, "encrypted_data.xlsx")
df.to_excel(excel_path, index=False)

print("Done")
