# NaraGo Music

A lightweight, self-hosted music web app that provides access to songs, lyrics, charts, and mood-based discovery via the Rich Music API. Features a clean, dark UI built with vanilla HTML/CSS/JS and a Python proxy server to bypass CORS restrictions.

![NaraGo Music Screenshot](https://via.placeholder.com/800x450/111/fff?text=NaraGo+Music+Screenshot) <!-- Optional: replace with actual screenshot -->

## ✨ Features

- **Search & Autocomplete** – Find songs, artists, albums
- **Home Feed** – Curated sections (quick picks, throwbacks, etc.)
- **Charts** – Top playlists and trending content
- **Mood Categories** – Discover music by vibe (e.g., Bepergian, Fokus, Chill)
- **Audio Player** – YouTube-based hidden iframe playback with controls
- **Synced Lyrics** – Fetch and display timed lyrics when available
- **Queue Management** – Add to queue, shuffle, repeat, next/prev
- **Responsive Design** – Works on mobile & desktop (PWA-ready)
- **CORS Proxy** – Lightweight Python server to bypass API restrictions
- **Offline Installable** – Includes web app manifest for PWA install

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **API Proxy**: Python 3 + `http.server` (standard library)
- **Styling**: Custom CSS (CSS variables, Flexbox/Grid)
- **Fonts**: [DM Sans](https://fonts.google.com/specimen/DM+Sans), [Space Mono](https://fonts.google.com/specimen/Space+Mono)
- **Icons**: Inline SVG (no external icon fonts)
- **YouTube Player**: YouTube IFrame API (hidden 1x1px iframe)

## 📦 Installation

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- A domain or subdomain pointing to your server (optional but recommended for HTTPS)
- Ports 80 (HTTP) and/or 443 (HTTPS) open
- (Optional) [Nginx](https://nginx.org/) or similar reverse proxy for SSL termination & port 80/443 binding
- (Optional) [Cloudflare](https://www.cloudflare.com/) or other CDN for SSL & caching

### Local Development / Testing

1. Clone or copy the project files:
   ```bash
   git clone <your-repo-url>
   cd narago-music
   # or copy index.html, server.py, manifest.json to a folder
   ```

2. Install no Python dependencies (uses only standard library).

3. Start the proxy server:
   ```bash
   python3 server.py
   ```
   The server will start on `http://0.0.0.0:8080` by default.

4. Open your browser and visit:
   ```
   http://localhost:8080
   ```

### Production Deployment (VPS with Nginx & Systemd)

This setup assumes you have a VPS (e.g., Ubuntu/Debian) with a domain pointed to it.

#### 1. Prepare the server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python3 and Nginx if not present
sudo apt install -y python3 nginx
```

#### 2. Place the application files

```bash
sudo mkdir -p /var/www/narago-music
sudo cp index.html server.py manifest.json /var/www/narago-music/
sudo chown -R $USER:$USER /var/www/narago-music
```

#### 3. Configure Nginx as a reverse proxy

Create `/etc/nginx/sites-available/narago-music`:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name music.narago.web.id; # <-- change to your domain/subdomain

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }
}
```

Enable the site and test:
```bash
sudo ln -sf /etc/nginx/sites-available/narago-music /etc/nginx/sites-enabled/narago-music
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Create a Systemd service for the Python proxy

Create `/etc/systemd/system/narago-music.service`:

```ini
[Unit]
Description=NaraGo Music Proxy Server
After=network.target

[Service]
Type=simple
User=www-data   # or your non-root user
WorkingDirectory=/var/www/narago-music
ExecStart=/usr/bin/python3 server.py
Restart=on-failure
RestartSec=5
Environment=PORT=8080

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable narago-music
sudo systemctl start narago-music
sudo systemctl status narago-music
```

#### 5. (Optional) Configure SSL with Cloudflare

- Point your DNS (e.g., `music.narago.web.id`) to your VPS IP via an **A record** in Cloudflare.
- Set SSL/TLS mode to **Full (strict)** in Cloudflare SSL/TLS settings.
- Ensure your origin server (VPS) accepts HTTP on port 80 (Nginx will handle it).
- Cloudflare will handle HTTPS → HTTP termination.

Your app will now be accessible at `https://music.narago.web.id` (if using Cloudflare) or `http://music.narago.web.id` (HTTP only).

#### 6. Verify

Visit your domain:
- `http://music.narago.web.id` (or `https://` if SSL configured)
- Test API: `http://music.narago.web.id/api/search?q=test`

## 🖥️ Usage

Once running:
- Use the search bar to find music.
- Click on Home, Charts, or Mood pills to browse categories.
- Click a song to play it in the bottom player.
- Click the lyric button (📜) to view synced lyrics.
- Use the queue controls to manage playback.

## 🔧 API Proxy Notes

The `server.py` file is a minimal proxy that:
- Serves static files (`index.html`, etc.) from the same directory.
- Proxies all `/api/*` requests to `https://richmusic.vercel.app`.
- Adds `Access-Control-Allow-Origin: *` header to allow browser requests.
- Includes a realistic `User-Agent` and headers to mimic a browser request.

No API key is required; it relies on the public Rich Music API.

## 📱 PWA Install

The site includes a basic web app manifest (`manifest.json`). To install:
1. Visit the site on Chrome/Android.
2. Tap the browser menu → **Install** (or **Add to Home screen**).
3. The app will launch in standalone mode (no address bar).

*Note*: Background audio playback via PWA depends on browser policy; true background audio may require a native wrapper.

## 🧹 Project Structure

```
narago-music/
├── index.html          # Main application (SPA)
├── server.py           # Python HTTP server + API proxy
├── manifest.json       # Web app manifest for PWA
└── README.md           # This file
```

## 🤝 Contributing

Feel free to fork and submit pull requests. For major changes, open an issue first to discuss.

## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

> **Disclaimer**: This project is for educational and personal use. It relies on the public Rich Music API and does not host any copyrighted audio. Respect the API's terms of service and rate limits.