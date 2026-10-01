# Advanced Infrastructure & Virtualization Lab — Gabriel Marques

A production-grade, highly available enterprise-adjacent home infrastructure environment designed to test advanced concepts in virtualization, network isolation, security governance, and recursive DNS management. This repository documents the architecture, automation scripts, and design decisions powering a hybrid Proxmox VE and ARM-based infrastructure.

---

### Engineering Methodology & Self-Directed R&D

This entire infrastructure was architected and deployed through a **100% self-taught and self-directed R&D approach**. Built entirely without formal courses, corporate training, or external bootcamps, the project serves as a practical testing ground for reverse-engineering complex environments, reading official documentation, and mastering production-grade systems engineering. 

It stands as a testament to autonomous problem-solving, advanced troubleshooting, and the ability to implement enterprise-level architectural patterns independently.

---

### Architectural Overview & Network Topology

The infrastructure is segregated using strict virtual networking topologies managed by a virtualized pfSense enterprise firewall. High-performance compute tasks utilize hardware translation (GPU passthrough), while core infrastructure services run within lightweight, unprivileged virtualization layers.

| Deployment Type | Host Service | Core Functionality | Infrastructure & Architecture Notes |
| :--- | :--- | :--- | :--- |
| **Virtual Machine** | pfSense | Core Routing, Firewall, VLAN Segmentation, DHCP, IP Blocking | Provisioned with Dedicated WAN Passthrough; manages isolated network zones. |
| **LXC Container** | Caddy | Reverse Proxy & Automated Edge SSL Termination | Integrated with Cloudflare DNS (Grey Cloud) via automated Certbot API challenges. |
| **LXC Container** | Tailscale | Secure Overlay Mesh Network & Remote Private Access | Zero-Port-Forwarding configuration acting as the secure ingress gateway for remote administration. |
| **LXC Container** | AdGuard (Prod) | Enterprise-grade DNS Filtering & Ad-Blocking | Core DNS upstream sinkholing integrated natively across production VLANs. |
| **LXC Container** | Unbound | Upstream Recursive DNS Resolver with DNSSEC Validation | Hardened recursive resolver deployed as the authoritative upstream for AdGuard layers. |
| **LXC Container** | Home Assistant | Centralized Smart Home Automation Engine | Core state machine managing multi-protocol IoT orchestration and internal telemetry. |
| **LXC Container** | Hermes Agent | Event-Driven System Agent & Monitoring Daemon | Lightweight communication agent deployed to orchestrate state reporting and automated workflows. |
| **LXC Container** | Immich | AI-Powered Asset Management & Multi-Node Photo Backup | Optimized with PCIe GPU Passthrough for hardware-accelerated AI facial recognition and transcoding. |
| **LXC Container** | Jellyfin | Media Distribution & Real-time Transcoding Engine | Configured with Intel/NVIDIA runtime drivers for direct hardware-accelerated encoding/decoding. |
| **LXC Container** | ARR Stack | Automated Media Ingestion Pipelines | Comprises qBittorrent isolated via a Gluetun VPN gateway, integrated with Radarr/Sonarr via event APIs. |
| **LXC Container** | Backup-Server | Automated Disaster Recovery & Snapshot Lifecycle | Custom crontab automated backup logic executing rsync policies and incremental Proxmox snapshots. |

---

### Hardware Provisioning & Bare-Metal Layer

A balanced compute-to-storage architecture deployed to achieve optimal power efficiency while sustaining high IOPS workloads across multiple SSD pools.

* **Compute:** AMD Ryzen 5 5600 (6 Cores / 12 Threads) on an MSI A520 A-PRO motherboard
* **Memory:** 32 GB DDR4 RAM (2x16GB 3200 MHz)
* **Graphics & AI Compute:** NVIDIA RTX 3050 (Dedicated to Jellyfin/Immich transcoding and AI pipelines)
* **Storage Pools:**
  * `Pool-0 (System):` 500 GB SanDisk Ultra 3D SSD (Proxmox VE OS, VM storage, active LXC runtimes)
  * `Pool-1 (Data/AI):` 1 TB SanDisk SSD (Dedicated high-speed storage for Immich processing)
  * `Pool-2 (Backup):` 500 GB SanDisk SSD (Local disaster recovery, hot snapshots, and configuration state retention)
  * `Pool-3 (Cold/Media):` 4 TB Mechanical HDD (High-capacity block storage for media libraries)

---

### Cloud Offsite Backup & Disaster Recovery Architecture

To ensure strict compliance with data resilience standards, the infrastructure implements a hybrid backup model combining local state tracking with offsite cloud replication.

* **Proxmox Backup Server (PBS):** Deployed to manage automated, incremental, client-side encrypted, and deduplicated snapshots of all critical virtualized instances and volumes.
* **Google Cloud Storage Integration:** Local backup pools are securely replicated and synchronized to a Google Cloud Storage cold tier. This ensures high durability, end-to-end encryption, and geographical isolation for full disaster recovery scenarios.

---

### Secondary Auxiliary Node: Raspberry Pi

An edge-computing node running DietPi Linux deployed on external solid-state storage to ensure high read/write reliability and mitigate micro-SD hardware degradation.

* **Bare Metal:** Raspberry Pi 3 Model B+ boot-configured to a 120 GB Kingston External SSD.
* **Capabilities & Current Testing:**
  * Isolated Kodi Media Station running CEC-enabled television protocols.
  * Multi-protocol file shares utilizing secure network mounts (SMB/NFS) back-hauling to the main storage pool.
  * Active integration environment testing failover scenarios for Home Assistant and high-availability Pi-hole clustering.

---

### Automation & Governance

* All microservices are managed and maintained via declarative Docker Compose manifests or natively isolated Linux Containers (LXC).
* Deployment strategies are adapted from verified community blueprints and customized to enforce strict security boundaries.
* Security compliance: All internal secrets, tokens, API keys, and public routing structures are strictly sanitized using dynamic environment parameters or placeholders (`<REDACTED_...>`).

---

### Technical References & Communities

* **Documentation & Tools:** Proxmox VE, Home Assistant, Immich, DietPi, Jellyfin, Radarr, Sonarr, Prowlarr.
* **Architecture Blueprints:** Proxmox VE Community Scripts, r/homelab, r/selfhosted, Proxmox Forums.

---

### Technical Compliance & Licensing

Distributed under the MIT License. Open for collaborative review, systemic optimizations, and educational forks.

**Author:** Gabriel Marques
*Platform, Automation & Observability Engineer*
