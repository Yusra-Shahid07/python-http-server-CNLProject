# 🚀 Python HTTP/1.1 Server

A robust, multi-threaded HTTP/1.1 server implemented from scratch using Python's low-level `socket` library. This project demonstrates the core principles of networking, the TCP/IP stack, and the HTTP protocol.

## 🌟 Key Features

- **Multi-threaded Architecture**: Uses Python's `threading` module to handle multiple client connections concurrently.
- **HTTP Keep-Alive (Persistent Connections)**: Implements connection reuse, allowing multiple requests to be served over a single TCP connection for improved performance.
- **Robust MIME Support**: Correctly identifies and serves various file types (HTML, CSS, JS, Images, etc.) using a dedicated MIME mapping system.
- **Security-First Design**: Includes built-in protection against directory traversal attacks, ensuring files are only served from the authorized `www` directory.
- **Proof of Persistence**: Explicit logging system that tracks and displays connection reuse in the terminal for educational/demonstration purposes.
- **Custom Error Handling**: Professional, styled HTML error pages for 404, 400, 405, and 500 status codes.

## 🏗️ Technical Stack

- **Language**: Python 3.x
- **Transport Layer**: TCP (via `socket.SOCK_STREAM`)
- **Application Layer**: HTTP/1.1
- **Concurrency**: Thread-per-connection model

## 📂 Project Structure

```text
http-server-project/
├── src/
│   ├── server.py       # Main entry point and listener
│   ├── connection.py   # Connection/Request handling logic
│   ├── parser.py       # HTTP request/response parsing
│   └── mime.py         # MIME type definitions
├── www/                # Web root directory
│   ├── index.html      # Landing page
│   └── (other assets)
└── README.md           # Project documentation
```

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have Python 3 installed on your system.

### 2. Run the Server
Open your terminal in the project root and run:
```bash
python src/server.py
```

### 3. Access the Webpage
Once the server is running, open your browser and navigate to:
`http://127.0.0.1:8080`

## 📊 Demonstrating Persistence

To witness the **Persistent Connections** in action:
1. Open the browser's Developer Tools (**F12**).
2. Go to the **Network** tab.
3. Refresh the page.
4. Check the terminal logs; you will see:
   `🔄 [PERSISTENCE] Reusing connection for request #2`
   This proves that the browser is using the same TCP pipe for secondary assets (like CSS or images).

## 🛡️ Security
The server implements a strict path validation check. Any attempt to access files outside the `www` directory (e.g., `../../etc/passwd`) will be blocked with a security warning in the logs and a 404 error for the client.
