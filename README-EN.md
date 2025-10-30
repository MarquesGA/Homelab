# 🧠 HomeLab & Raspberry Pi Project — Gabriel Marques

> **Legal Notice:**  
> This project is for **personal and educational use only**.  
> It is not intended for commercial purposes, and the author **assumes no responsibility for misuse**.  
> All sensitive data (IPs, tokens, credentials) have been **intentionally redacted**.
---
> This project was developed over many months as a hobby. I’m not an expert in the field, just a curious person who enjoys solving problems. The entire project was designed to be free or as inexpensive as possible — the only expenses were for hardware parts, an optional domain for SSL, an optional (but highly recommended) VPN subscription, and free time.
>
> The hardware was mostly purchased used or at great discounts — you don’t need anything similar to get started. I began with an IPX3060E, a 2-core / 2-thread processor from 2016 and 1 gb of ram, running CasaOS. The total cost was about R$50, and the case was literally the box it came in.
---
### 💾 Hardware Setup

- **CPU:** AMD Ryzen 5 5600  
- **RAM:** 32 GB DDR4 (2x16GB 3200)  
- **Placa-mãe:** MSI A520 A-PRO  
- **GPU:** RTX 3050 (used for Jellyfin/Immich transcoding)  
- **Storage:**  
  - SSD SanDisk Ultra 3D 500 gb → Proxmox + VMs + LXC  
  - SSD SanDisk 1 TB → Immich data
  - SSD SanDisk 500 gb → Backup and Snapshots
  - HDD 4TB → Media (Jellyfin)
- Raspberry Pi 3 model B+
  - SSD Kingston 120 gb
  - MicroSD 64gb

---
## 🎯 Purpose

This repository documents the process of building and maintaining a **HomeLab** using **Proxmox VE**, **unprivileged LXC containers**, a **virtualized pfSense**, and a **Raspberry Pi** as an auxiliary node.  
It aims to help **Portuguese-speaking beginners** who often find resources only available in English.  
👉 [Read the Portuguese version (README-PT.md)](./README-PT.md)

---

## 🧩 System Overview

| Type | Name | Function | Notes |
|------|------|-----------|-------|
| VM | pfSense | Firewall, VLANs, DHCP, IP blocking | 2 vCPUs / 8GB RAM, WAN passthrough |
| LXC | Jellyfin | Media server with GPU acceleration | HDD 4TB |
| LXC | ARR Stack | qBittorrent + Gluetun (VPN), Radarr, Sonarr, Prowlarr, Bazarr, Jellyseerr | Linked to Jellyfin and Discord using API |
| LXC | Immich | AI photo backup | SSD 1TB and GPU acceleration |
| LXC | Tailscale | Remote private access | Secure, no port forwarding, for remote access |
| LXC | AdGuard (prod) | DNS filtering | Integrated with VLANs |
| LXC | AdGuard (test) | DNS testing | Used for testing purposes, such as Unbound latency, filters, etc. |
| LXC | Unbound | Recursive DNS with DNSSEC | Upstream for AdGuard |
| LXC | Caddy | Reverse proxy + HTTPS via Cloudflare (Grey Cloud) | Certbot automated |
| LXC | Backup-Server | Automated backups | Snapshot and rsync scripts |

---

## 🍓 Raspberry Pi Node

### 🔹 Phase 1 — Learning with PINN
- Used **PINN** for experimenting with multiple OS boots (DietPi, Raspberry Pi OS, LibreELEC).  
- Learned partitioning, boot logic, and system recovery.

### 🔹 Phase 2 — SSD + DietPi + Kodi
- Installed **DietPi** on an external SSD via USB (faster and reliable).  
- Deployed **Kodi** as media center connected to TV (CEC-enabled).  
- Mounted Jellyfin media shares (SMB/NFS).  
- Using tailscale to have external access
- Testing integrations with **Home Assistant** and **Pi-hole**.

---

## ⚙️ Configuration & Scripts

- Most services use Docker Compose or native LXC containers.  
- Community setup scripts adapted from:  
  🔗 [Proxmox VE Community Scripts](https://community-scripts.github.io/ProxmoxVE/)  
- Sensitive data is redacted with placeholders `<REDACTED_...>`.

---

## 🌐 References & Acknowledgements

### 📺 YouTube Channels
- [Jim’s Garage](https://www.youtube.com/@Jims-Garage)  
- [Wolfgang’s Channel](https://www.youtube.com/@WolfgangsChannel)  
- [Hardware Haven](https://www.youtube.com/@HardwareHaven)  
- [Techno Tim](https://www.youtube.com/@TechnoTim)  
- [SauberLab](https://www.youtube.com/@SauberLab)

### 💬 Communities
- [Reddit — GPU passthrough for Jellyfin LXC](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)  
- [StackOverflow](https://stackoverflow.com)  
- [Proxmox Forums](https://forum.proxmox.com)  
- [r/homelab](https://www.reddit.com/r/homelab)  
- [r/selfhosted](https://www.reddit.com/r/selfhosted)

### 📘 Official Docs
- [Proxmox VE](https://www.proxmox.com)  
- [Immich](https://immich.app)  
- [DietPi](https://dietpi.com)  
- [PINN](https://github.com/procount/pinn)  
- [Jellyfin](https://jellyfin.org)  
- [Radarr](https://radarr.video) / [Sonarr](https://sonarr.tv) / [Prowlarr](https://prowlarr.com)

---

## 🙌 Community Purpose

This project’s main mission is to provide **clear, Portuguese-accessible documentation** for HomeLab enthusiasts, bridging the language gap and empowering new learners in tech and self-hosting.

> 💡 If this helped you, please contribute with improvements, translations or community support.

---

## 📜 License

Released under the **MIT License** — free for educational and personal use, with attribution to the original author.

**Author:** Gabriel Marques 🇧🇷  
📍 Brazil  
