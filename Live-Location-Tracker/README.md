# Live Location Tracker 📍📡

[![Node.js](https://img.shields.io/badge/Node.js-v16+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-4.x-000000?style=for-the-badge&logo=express&logoColor=white)](https://expressjs.com/)
[![Socket.io](https://img.shields.io/badge/Socket.io-4.x-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
[![Leaflet](https://img.shields.io/badge/Leaflet-Map%20API-199900?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)
[![Cloudflare Tunnel](https://img.shields.io/badge/Cloudflare-Tunnel-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://www.cloudflare.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

An educational cybersecurity demonstration platform and social engineering reconnaissance simulator. This project illustrates how browser-based Geolocation APIs can be leveraged in security awareness assessments, phishing simulations, and red team demonstrations to pinpoint physical GPS coordinates in real-time.

---

## 📑 Table of Contents

- [Overview](#overview)
- [How It Works (Attack Vector Simulation)](#how-it-works-attack-vector-simulation)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Demonstration & Usage](#demonstration--usage)
- [Security & Ethical Disclaimer](#security--ethical-disclaimer)
- [Defenses & Countermeasures](#defenses--countermeasures)
- [Credits & License](#credits--license)

---

## 🎯 Overview

Modern web browsers implement the W3C Geolocation API, allowing web applications to request high-accuracy GPS coordinates, cellular triangulation data, or Wi-Fi BSSID locations from devices. 

In cybersecurity assessments, attackers frequently disguise geolocation requests within believable bait applications (e.g., weather forecasts, delivery trackers, event check-ins). This project simulates an ethical red-team scenario:

1. **The Bait**: A harmless-looking "Weather Application" prompts the user to verify weather conditions, requesting location permission.
2. **The Reconnaissance**: If granted, high-accuracy GPS coordinates are polled continuously and transmitted back to the command-and-control server.
3. **The Control Dashboard**: An authenticated administrator dashboard receives live coordinates via WebSockets and visualizes the target's precise location on an interactive OpenStreetMap Leaflet interface.

---

## 🔄 How It Works (Attack Vector Simulation)

```
+------------------+         1. Opens Bait URL (/weather)        +--------------------+
|                  | ------------------------------------------> |                    |
|   Target Device  |         2. Prompts "Allow Location"         | Express & SocketIO |
|  (Mobile/Desktop)| <------------------------------------------ |    Backend Server  |
|                  |         3. Streams GPS lat/long updates     |                    |
+------------------+ ------------------------------------------> +--------------------+
                                                                            |
                                                                   4. Emits WebSocket
                                                                      Coordinates
                                                                            v
                                                                 +--------------------+
                                                                 |   Admin Dashboard  |
                                                                 |  (/map?id=target)  |
                                                                 |  Live Leaflet Map  |
                                                                 +--------------------+
```

---

## ✨ Key Features

- **⚡ Real-Time Bidirectional Sync**: Utilizes Socket.io WebSockets to transmit and display location updates with sub-second latency.
- **🗺️ Interactive Map Visualization**: Integrates Leaflet.js with OpenStreetMap to display markers, track coordinate movement, and automatically center the view.
- **🌐 Zero-Port-Forwarding Tunneling**: Integrates `cloudflared` to automatically create a secure, publicly accessible HTTPS tunnel URL on server launch.
- **🔐 Session-Based Admin Authentication**: Protects target management and map viewing routes using secure cookie-based tokens.
- **🎯 Multi-Target Tracking**: Unique client identification enables tracking and toggling between multiple targets simultaneously.
- **📱 Responsive Bait Interface**: Clean, mobile-optimized weather widget styled for modern mobile browsers.

---

## 🛠️ Tech Stack

- **Runtime**: [Node.js](https://nodejs.org/) (v16+)
- **Server Framework**: [Express.js](https://expressjs.com/)
- **Real-Time Communication**: [Socket.io](https://socket.io/)
- **Templating Engine**: [Tarkine](https://www.npmjs.com/package/tarkine)
- **UI Frameworks**: [Bulma CSS](https://bulma.io/) & Custom Responsive CSS
- **Mapping Library**: [Leaflet.js](https://leafletjs.com/) & OpenStreetMap
- **Public Tunneling**: [Cloudflare Tunnel (`cloudflared`)](https://github.com/cloudflare/cloudflared)

---

## 📂 Directory Structure

```
Live-Location-Tracker/
├── public/
│   └── weather.png             # Static weather illustration asset
├── views/
│   ├── home.html               # Authenticated admin panel listing active targets
│   ├── login.html              # Admin login page
│   ├── map.html                # Interactive Leaflet live map view
│   └── weather.html            # Target bait page simulating a weather forecast app
├── .env.example                # Example environment variables
├── .gitignore                  # Git exclusion rules
├── config.js                   # Application port, credentials, and token settings
├── package.json                # Dependencies and project metadata
├── router.js                   # Express route handlers and auth middleware
└── server.js                   # HTTP server, socket initialization, & Cloudflare tunnel
```

---

## 📋 Prerequisites

- **Node.js**: `v16.0.0` or higher
- **npm**: `v7.0.0` or higher
- An active Internet connection (required for OpenStreetMap tiles, CDN scripts, and Cloudflare Tunneling)

---

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdulrehmanazeem23-coder/CyberSecurity-Projects.git
   cd CyberSecurity-Projects/Live-Location-Tracker
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment (Optional)**:
   Copy `.env.example` to `.env` or customize `config.js` to change the administrator credentials and port:
   ```bash
   cp .env.example .env
   ```

4. **Start the application**:
   ```bash
   npm start
   ```

   Upon launch, the terminal will display both local and public tunnel endpoints:
   ```
   LOCAL  : http://localhost:6589
   REMOTE : https://<random-subdomain>.trycloudflare.com
   ```

---

## ⚙️ Configuration

Environment variables can be defined in a `.env` file or passed at runtime:

| Variable | Default Value | Description |
|---|---|---|
| `PORT` | `6589` | Local TCP listening port |
| `ADMIN_USERNAME` | `admin` | Administrator login username |
| `ADMIN_PASSWORD` | `admin` | Administrator login password |
| `AUTH_TOKEN` | `ca978112ca1...` | Session cookie verification token |

Default admin credentials:
- **Username**: `admin`
- **Password**: `admin`

---

## 🎮 Demonstration & Usage

1. Open `LOCAL` or `REMOTE` URL in your browser and log in at `/login`.
2. Once logged into `/`, you will see the administrative dashboard showing the list of tracked sessions.
3. In a separate browser tab or mobile device (simulating the victim), navigate to `/weather`.
4. Click **"Check Weather"** and click **Allow** on the browser's location permission prompt.
5. In the admin dashboard at `/`, a new target ID will appear in real-time.
6. Click the target ID to view their precise GPS coordinates dynamically plotted on the Leaflet map.

---

## 🛡️ Defenses & Countermeasures

Understanding how this reconnaissance vector operates is essential for implementing organizational defenses:

1. **Browser Permission Hygiene**: Never grant location permissions to untrusted websites or random URLs.
2. **Strict Geolocation Policies**: Enterprise administrators can use Group Policy Objects (GPO) or MDM profiles to restrict geolocation prompt permissions across corporate browsers.
3. **VPN & Location Spoofing**: Using VPN services masks IP-based geolocation; however, device-level GPS queries can bypass IP protections unless GPS hardware access is toggled off.
4. **Security Awareness Training**: Train users to identify pretexting schemes where unrelated applications request high-privilege device APIs.

---

## ⚠️ Security & Ethical Disclaimer

> [!WARNING]
> **This tool is developed strictly for authorized educational purposes, defensive research, cybersecurity demonstrations, and ethical red-team exercises.**
>
> Unauthorized tracking of individuals or collecting location data without explicit consent is illegal under various privacy laws (including GDPR, CCPA, and national computer misuse acts). The author does not condone, encourage, or accept responsibility for unauthorized or malicious use of this software.

---

## 📜 Credits & License

- Original implementation concept by [madhanmaaz](https://github.com/madhanmaaz/live-location-tracker).
- Maintained and expanded as part of the [CyberSecurity-Projects](https://github.com/abdulrehmanazeem23-coder/CyberSecurity-Projects) portfolio by [Abdul Rehman Azeem](https://github.com/abdulrehmanazeem23-coder).
- Licensed under the [MIT License](LICENSE).
