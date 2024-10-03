import cv2
from pyzbar.pyzbar import decode

def decode_qr(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if img is None:
        print(f"Error: Could not read image from {image_path}. Please check the file path.")
        return
    
    # Decode the QR code using pyzbar
    decoded_objects = decode(img)
    
    if not decoded_objects:
        print("No QR code found in the image.")
        return

    for obj in decoded_objects:
        # Print the decoded data
        print("QR Code Data:", obj.data.decode("utf-8"))

# Replace 'your_image.png' with the path to your QR code image
decode_qr('your_image.png')
