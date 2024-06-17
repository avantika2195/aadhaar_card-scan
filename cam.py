import cv2
import pytesseract
import re
import json

# Path to the Tesseract executable (change this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to capture an image using the camera
def capture_image():
    camera = cv2.VideoCapture(0)  # 0 represents the default camera (you can change it if you have multiple cameras)

    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return None

    ret, frame = camera.read()
    if not ret:
        print("Error: Could not capture an image.")
        camera.release()
        return None

    camera.release()
    return frame

# Function to extract information from the captured image
def extract_information(image):
    # Preprocess the image (resize, grayscale, and adaptive thresholding)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Perform OCR using Tesseract
    aadhaar_data = pytesseract.image_to_string(thresholded)

    # Define regular expressions for extracting Name, Date of Birth (DOB), and Aadhar Number
    name_pattern = r"([A-Za-z ]+)"
    dob_pattern = r"(?:DOB|D0B|D08)[:\s]*([\d/:-]+)"
    aadhar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    # Extract Name
    name_matches = re.findall(name_pattern, aadhaar_data)
    if name_matches:
        name = " ".join(name_matches).strip()
    else:
        name = "Name not found"

    # Extract DOB
    dob_matches = re.findall(dob_pattern, aadhaar_data, re.IGNORECASE)
    if dob_matches:
        dob = dob_matches[0].strip()
    else:
        dob = "DOB not found"

    # Extract Aadhar Number
    aadhar_matches = re.findall(aadhar_pattern, aadhaar_data)
    if aadhar_matches:
        aadhar = aadhar_matches[0].replace(" ", "")
    else:
        aadhar = "Aadhar Number not found"

    # Create a JSON object to store the extracted data
    aadhar_info = {
        "Name": name,
        "DOB": dob,
        "Aadhar Number": aadhar
    }

    return aadhar_info

# Main loop to continuously capture and process images
while True:
    # Capture an image from the camera
    captured_image = capture_image()

    if captured_image is not None:
        # Extract information from the captured image
        extracted_info = extract_information(captured_image)

        # Print the extracted information
        print(extracted_info)

        # Save the extracted information to a JSON file
        with open('aadhar_info.json', 'w') as json_file:
            json.dump(extracted_info, json_file, indent=4)

        # Display the captured image
        cv2.imshow("Captured Image", captured_image)

        # Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('p'):
            break

# Release OpenCV resources
cv2.destroyAllWindows()
