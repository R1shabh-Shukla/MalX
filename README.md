# 🚀 MalX
### A Cybersecurity Project for IIT Dhanbad Infosec Club

---

## Project Overview
**MalX** is a proof-of-concept malware project designed to demonstrate cyberattack techniques for educational purposes. The project operates with two main scripts: one for infecting a target machine and one for controlling the system remotely via an admin panel.

---

## 🛠️ Installation and Setup

1. **Clone this repository**:
  git clone https://github.com/<your-username>/MalwareX.git

2. Install dependencies on target machine:
pip install -r requirements.txt  

Run the Scripts:

To run the target machine script (malware) on target pc:
python malwrae.py

To run the admin panel script on admin pc:
python admin_panel.py

📦 Dependencies
1.Target Machine (Malware Script)
 requests
 opencv-python (cv2)
 pynput
 Pillow (ImageGrab)
 scapy
 win32gui
 winreg

2.Admin Panel Script
  bottle

🌟 Core Functionalities
Keylogger: Targets specific websites like Instagram and Facebook.

Network Sniffing: Captures network packets and sends them to the admin panel.

Webcam Capture: Takes real-time photos from the target’s webcam.

Screenshot Capture: Captures the target’s desktop screenshots.

Wi-Fi Password Extraction: Retrieves saved Wi-Fi credentials.

Remote Shutdown: Shuts down the target machine remotely.


⚠️ Ethical Disclaimer
This project is for educational purposes only. Unauthorized use is illegal and unethical. Obtain permission before deploying this on any network or machine.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
