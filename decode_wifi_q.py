import cv2
from pyzbar.pyzbar import decode

def decode_hotspot_qr(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not read image from {image_path}. Please check the file path.")
        return
    
    # Attempt to decode using pyzbar
    decoded_objects = decode(img)

    if decoded_objects:
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print("Decoded QR Code Data:", qr_data)  # Print the decoded data
            password = extract_wifi_password(qr_data)
            if password:
                print(f"Extracted Password: {password}")
                return
    print("No valid QR code found or no Wi-Fi credentials present.")

def extract_wifi_password(qr_data):
    if qr_data.startswith("WIFI:"):
        params = qr_data.split(';')
        password = None
        for param in params:
            if param.startswith("P:"):
                password = param[2:]  # Extract password
                return password
    return None

decode_hotspot_qr('C:/Users/JOSEPH/Documents/GitHub/python/hotspot_qr.jpeg')  # Ensure the filename has .jpeg or .jpg
