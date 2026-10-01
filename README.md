> **Aviso Legal:**  
> Este projeto foi criado **exclusivamente para uso pessoal e educacional**.  
> Não há qualquer intuito comercial, e o autor **não se responsabiliza por qualquer uso indevido** do material aqui descrito.  
> Todos os dados sensíveis (IPs, tokens, chaves, senhas) foram **intencionalmente ocultados ou substituídos**.
___
> Este projeto foi desenvolvimento durante muitos meses, como hobby, eu não sou especialista na área, apenas uma pessoa curiosa e que gosta de resolver problemas. Todo o projeto foi pensado para ser gratuito ou o mais barato possivel, o gasto feito foi apenas em peças de hardware, um domínio para SSL (Opcional), assinatura da VPN (Opcional mas altamente recomendado) e tempo livre.
---
# Laboratório Avançado de Infraestrutura & Virtualização — Gabriel Marques

Este repositório documenta a arquitetura, os scripts de automação e as decisões de design que sustentam uma infraestrutura híbrida baseada em Proxmox VE e arquitetura ARM. O ambiente foi projetado seguindo padrões de nível de produção para homologar conceitos avançados de virtualização, isolamento de redes, governança de segurança e gerenciamento de DNS recursivo.

---

### Metodologia de Engenharia e P&D Autodidata

Toda esta infraestrutura foi arquitetada e implantada por meio de uma abordagem de Pesquisa e Desenvolvimento (P&D) **100% autodidata**. Construído integralmente sem cursos formais, treinamentos corporativos ou bootcamps externos, o projeto funciona como um campo de testes prático para engenharia reversa de ambientes complexos, análise de documentações oficiais e domínio de engenharia de sistemas em escala real. 

Este laboratório reflete capacidade autônoma de resolução de problemas, diagnóstico avançado de falhas (troubleshooting) e competência para implementar de forma independente padrões arquiteturais complexos.

---

### Visão Geral da Arquitetura & Topologia de Rede

A infraestrutura é segregada utilizando topologias rígidas de rede virtual gerenciadas por um firewall corporativo pfSense virtualizado. Tarefas de computação de alto desempenho utilizam tradução direta de hardware (GPU passthrough), enquanto os serviços de infraestrutura principal rodam em camadas de virtualização leves e contêineres não privilegiados.

| Tipo de Implantação | Serviço Hospedado | Funcionalidade Core | Notas de Infraestrutura e Arquitetura |
| :--- | :--- | :--- | :--- |
| **Máquina Virtual** | pfSense | Roteamento, Firewall, Segmentação de VLANs, DHCP, Bloqueio de IP | Provisionado com passthrough exclusivo de rede WAN; gerencia zonas isoladas. |
| **Contêiner LXC** | Caddy | Proxy Reverso e Terminação SSL Automatizada na Borda | Integrado ao DNS da Cloudflare (Grey Cloud) via desafios automatizados de API do Certbot. |
| **Contêiner LXC** | Tailscale | Rede Mesh Privada e Acesso Remoto Seguro | Configuração de encaminhamento zero de portas (Zero-Port-Forwarding) atuando como gateway de ingresso seguro. |
| **Contêiner LXC** | AdGuard (Prod) | Filtragem de DNS de Nível Corporativo e Bloqueio de Anúncios | Resolução e sumidouro (sinkhole) de DNS integrado nativamente nas VLANs de produção. |
| **Contêiner LXC** | Unbound | Resolvedor DNS Upstream Recursivo com Validação DNSSEC | Resolvedor recursivo endurecido (hardened) implantado como upstream autoritativo para as camadas AdGuard. |
| **Contêiner LXC** | Home Assistant | Motor Central de Automação Residencial e IoT | Máquina de estado core gerenciando orquestração multiprotocolo e telemetria interna. |
| **Contêiner LXC** | Hermes Agent | Agente de Sistema Orientado a Eventos e Daemon de Monitoramento | Agente leve implantado para orquestrar relatórios de estado e fluxos de trabalho automatizados. |
| **Contêiner LXC** | Immich | Gestão de Ativos por IA e Backup de Fotos Multino | Otimizado com PCIe GPU Passthrough para aceleração de hardware em reconhecimento facial por IA. |
| **Contêiner LXC** | Jellyfin | Distribuição de Mídia e Motor de Transcoding em Tempo Real | Configurado com drivers de runtime NVIDIA para codificação/decodificação direta via hardware. |
| **Contêiner LXC** | ARR Stack | Pipelines Automatizados de Ingestão de Mídia | Composto por qBittorrent isolado através de um gateway VPN Gluetun, integrado via APIs de eventos. |
| **Contêiner LXC** | Backup-Server | Recuperação de Desastres e Ciclo de Vida de Snapshots | Lógica automatizada via crontab executando políticas de rsync e snapshots incrementais locais. |

---

### Provisionamento de Hardware e Camada Bare-Metal

Uma arquitetura equilibrada de computação e armazenamento implantada para obter eficiência energética ideal, sustentando altas cargas de IOPS em múltiplos pools de SSD.

* **Processamento (CPU):** AMD Ryzen 5 5600 (6 Cores / 12 Threads) em uma placa-mãe MSI A520 A-PRO
* **Memória RAM:** 32 GB DDR4 (2x16GB 3200 MHz)
* **Processamento Gráfico e IA (GPU):** NVIDIA RTX 3050 (Dedicada aos pipelines de IA do Immich e transcoding do Jellyfin)
* **Pools de Armazenamento:**
  * `Pool-0 (Sistema):` SSD SanDisk Ultra 3D de 500 GB (Proxmox VE OS, armazenamento de VMs e runtimes ativos de LXC)
  * `Pool-1 (Dados/IA):` SSD SanDisk de 1 TB (Armazenamento dedicado de alta velocidade para processamento do Immich)
  * `Pool-2 (Backup):` SSD SanDisk de 500 GB (Recuperação de desastres local, snapshots a quente e retenção de estado)
  * `Pool-3 (Mídia):` HDD Mecânico de 4 TB (Armazenamento em bloco de alta capacidade para bibliotecas de mídia)

---

### Arquitetura de Backup em Nuvem Offsite e Recuperação de Desastres

Para garantir conformidade estrita com os padrões de resiliência de dados, a infraestrutura implementa um modelo de backup híbrido que combina o rastreamento de estado local com a replicação externa em nuvem.

* **Proxmox Backup Server (PBS):** Implantado para gerenciar snapshots automatizados, incrementais, criptografados no lado do cliente e desduplicados de todas as instâncias e volumes virtualizados críticos.
* **Integração com Google Cloud Storage:** Os pools de backup locais são replicados de forma segura e sincronizados com uma camada fria (cold tier) do Google Cloud Storage. Isso garante alta durabilidade, criptografia de ponta a ponta e isolamento geográfico para cenários completos de recuperação de desastres (Disaster Recovery).

---

### Nó Secundário Auxiliar: Raspberry Pi

Um nó de computação de borda rodando DietPi Linux, implantado em armazenamento externo de estado sólido para garantir alta confiabilidade de leitura/gravação e mitigar a degradação de hardware de cartões micro-SD.

* **Bare Metal:** Raspberry Pi 3 Model B+ configurado para inicialização em um SSD externo Kingston de 120 GB.
* **Capacidades e Testes Atuais:**
  * Estação de mídia isolada Kodi executando protocolos de televisão habilitados para CEC via HDMI.
  * Compartilhamento de arquivos multiprotocolo utilizando montagens de rede seguras (SMB/NFS) interligadas ao pool principal.
  * Ambiente ativo de testes de cenários de failover para Home Assistant e agrupamento (clustering) de alta disponibilidade do Pi-hole.

---

### Automação & Governança

* Todos os microsserviços são gerenciados e mantidos por meio de manifestos declarativos do Docker Compose ou contêineres Linux nativamente isolados (LXC).
* As estratégias de implantação são adaptadas de blueprints validados pela comunidade e customizadas para impor limites estritos de segurança de rede.
* Conformidade de segurança: Todos os segredos internos, tokens, chaves de API e estruturas de roteamento público são estritamente higienizados usando parâmetros de ambiente dinâmicos ou placeholders (`<REDACTED_...>`).

---

### Referências Técnicas & Comunidades

* **Documentação e Ferramentas:** Proxmox VE, Home Assistant, Immich, DietPi, Jellyfin, Radarr, Sonarr, Prowlarr.
* **Blueprints de Arquitetura:** Proxmox VE Community Scripts, r/homelab, r/selfhosted, Fóruns Oficiais Proxmox.

---

### Conformidade Técnica & Licença

Distribuído sob a licença **MIT**. Aberto para revisão colaborativa, otimizações sistêmicas e forks educacionais.

**Autor:** Gabriel Marques
*Engenheiro de Plataforma, Automação & Observabilidade*


---

## 📜 Licença

Distribuído sob a licença **MIT** — uso e modificação livres para fins pessoais e educacionais, mantendo créditos ao autor.

**Autor:** Gabriel Marques 🇧🇷  
