import tkinter as tk
from tkinter import messagebox

# Import your existing code functions
import cv2
import webbrowser
import time
from tkinter import filedialog

# Define your existing functions (Do not modify these)

# Function to display the popup window
def show_popup(url):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    response = messagebox.askyesno("QR Code Detected", f"QR Code found! Do you want to open the URL: {url}?")

    if response:
        webbrowser.open(url)
        print(f"Opening URL: {url}")
    else:
        print("User chose not to open the URL.")
    
    root.destroy()

# Function to scan QR codes from an image selected by the user
def scan_qr_from_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Could not read image.")
            return

        img_resized = cv2.resize(img, (640, 480))
        qr_detector = cv2.QRCodeDetector()
        value, pts, qr_code = qr_detector.detectAndDecode(img_resized)

        if value:
            print(f"Scanned QR Code: {value}")
            show_popup(value)
        else:
            print("No QR Code detected in the image.")

    except Exception as e:
        print(f"Error during image scan: {e}")

# Function to open file dialog and select image from PC
def open_image():
    file_path = filedialog.askopenfilename(title="Select QR Code Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        print(f"Selected image path: {file_path}")
        scan_qr_from_image(file_path)

# Function to scan QR codes using the webcam in real-time
def scan_qr_using_webcam():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam.")
            return

        print("Starting webcam for QR code scanning...")

        start_time = time.time()
        max_duration = 60  # Max webcam duration in seconds

        qr_detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame_resized = cv2.resize(frame, (640, 480))
            value, pts, qr_code = qr_detector.detectAndDecode(frame_resized)

            if value:
                print(f"Scanned QR Code: {value}")
                cv2.putText(frame_resized, f"QR Code: {value}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                show_popup(value)
                break
            else:
                print("No QR Code detected")
                cv2.putText(frame_resized, "No QR Code detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("QR Code Scanner", frame_resized)

            elapsed_time = time.time() - start_time
            if elapsed_time > max_duration:
                print("Webcam time limit reached.")
                break

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Exiting on 'Q' key press.")
                break
        
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Error during webcam scan: {e}")

# GUI Interface Code (Tkinter)

# Create the main window
def create_interface():
    root = tk.Tk()
    root.title("QR Code Scanner")

    # Function for Image option
    def scan_from_image():
        open_image()

    # Function for Webcam option
    def scan_from_webcam():
        scan_qr_using_webcam()

    # Add a label
    label = tk.Label(root, text="Choose a QR Code scanning method:", font=("Arial", 14))
    label.pack(pady=10)

    # Add buttons for the two options
    button_image = tk.Button(root, text="Scan from Image", width=20, height=2, command=scan_from_image)
    button_image.pack(pady=5)

    button_webcam = tk.Button(root, text="Scan from Webcam", width=20, height=2, command=scan_from_webcam)
    button_webcam.pack(pady=5)

    # Run the main loop
    root.mainloop()

# Run the interface
create_interface()
