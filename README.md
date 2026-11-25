<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:0a3d2e,100:00ff9c&height=180&section=header&text=Vladyslav%20Krutii&fontSize=48&fontColor=e6edf3&fontAlignY=38&desc=cybersecurity%20%C2%B7%20CTF%20%C2%B7%20DevOps&descSize=18&descAlignY=60&descColor=00ff9c" width="100%"/>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&duration=3000&pause=900&color=00FF9C&center=true&vCenter=true&width=620&lines=%24+whoami;Cybersecurity+student+%40+KSE+%F0%9F%87%BA%F0%9F%87%A6;CTF+player+%E2%80%94+team+KSE_CS1;Reversing+binaries+%26+breaking+web+apps;Signing+images+%26+hardening+K8s" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/vladyslav-krutii-598b64356/"><img src="assets/badge-linkedin.svg" height="34" alt="LinkedIn"/></a>
  <img src="assets/badge-kse.svg" height="34" alt="Kyiv School of Economics"/>
  <img src="assets/badge-ctf.svg" height="34" alt="CTF team KSE_CS1"/>
</p>

---

### `> cat about.txt`

```yaml
name:      Vladyslav Krutii
location:  Ukraine 🇺🇦
study:     BSc Cybersecurity @ Kyiv School of Economics
ctf_team:  KSE_CS1
highlight: Haruul Zangi CTF 2026 Grand Final · Attack & Defense · 10th place · Mongolia 🇲🇳
interests: [reverse engineering, web security, DevSecOps, tooling]
now:       DevSecOps: supply-chain security & Kubernetes hardening
```

### `> ls ~/projects --featured`

<p align="center">
  <a href="https://github.com/vladyslav-krutii/secscan">
    <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/pin-secscan.svg" alt="secscan"/>
  </a>
  <a href="https://github.com/vladyslav-krutii/kse-air-alerts">
    <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/pin-kse-air-alerts.svg" alt="kse-air-alerts"/>
  </a>
  <a href="https://github.com/vladyslav-krutii/k8s-attack-defense-lab">
    <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/pin-k8s-attack-defense-lab.svg" alt="k8s-attack-defense-lab"/>
  </a>
</p>

| Project | What it is | Stack |
|---|---|---|
| 🛡️ [**secscan**](https://github.com/vladyslav-krutii/secscan) | Security-headers scanner API, secured end to end:<br/>• SSRF found & fixed in my own scanner (resolve-then-allowlist, every redirect re-validated)<br/>• Abuse protection: rate limit, concurrency cap, scan deadline<br/>• Value-based header grading, A to F<br/>• Supply chain: SHA-pinned actions, Gitleaks, Semgrep, pip-audit, Trivy, SBOM, Cosign keyless signing<br/>• Kyverno admits only images signed by my CI<br/>• Default-deny NetworkPolicy egress as a second SSRF layer<br/>• STRIDE threat model | FastAPI · Docker · Kubernetes · GitHub Actions · Cosign · Kyverno |
| ☸️ [**k8s-attack-defense-lab**](https://github.com/vladyslav-krutii/k8s-attack-defense-lab) | Kubernetes security lab: one app deployed twice, vulnerable vs hardened:<br/>• 6 misconfigurations exploited, then blocked: privileged pod + hostPath, over-permissive SA token, no NetworkPolicy, secrets in env/ConfigMap, root + writable FS + no limits, mutable image tags<br/>• Every scenario has a `verify.sh`; CI rebuilds the lab on kind and requires 6/6 exploitable vs 6/6 blocked<br/>• Hardening: Pod Security `restricted`, per-workload RBAC, default-deny NetworkPolicy, secrets as files, read-only FS, images pinned by digest<br/>• Kyverno 1.20: 9 CEL `ValidatingPolicy`, 105 offline `kyverno test` cases<br/>• Falco 0.45 (modern eBPF, not privileged) with 6 custom detection rules | kind · Calico · Kyverno · Falco · Kustomize · GitHub Actions |
| 🚨 [**kse-air-alerts**](https://github.com/vladyslav-krutii/kse-air-alerts) | Hourly per-oblast forecast of new air-raid alerts in Ukraine, evaluated walk-forward so no forecast ever sees the future | Python · pandas · scikit-learn |

### `> stack --list`

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,c,cs,ts,js,bash,powershell&theme=dark" alt="languages"/><br/>
  <img src="https://skillicons.dev/icons?i=fastapi,django,nextjs,react,dotnet,tailwind&theme=dark" alt="frameworks"/><br/>
  <img src="https://skillicons.dev/icons?i=docker,kubernetes,githubactions,prometheus,grafana,linux,kali,vercel,git&theme=dark" alt="infra & tools"/>
</p>

<p align="center">
  <img src="assets/tool-ida.svg" height="28" alt="IDA Pro"/>
  <img src="assets/tool-burp.svg" height="28" alt="Burp Suite"/>
  <img src="assets/tool-wireshark.svg" height="28" alt="Wireshark"/>
  <img src="assets/tool-pwntools.svg" height="28" alt="pwntools"/>
  <img src="assets/tool-trivy.svg" height="28" alt="Trivy"/>
  <img src="assets/tool-kyverno.svg" height="28" alt="Kyverno"/>
  <img src="assets/tool-falco.svg" height="28" alt="Falco"/>
  <img src="assets/tool-cosign.svg" height="28" alt="Cosign"/>
</p>

### `> git log --stats`

<p align="center">
  <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/stats.svg" alt="GitHub stats"/>
  <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/top-langs.svg" alt="Top languages"/>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/streak.svg" alt="Streak"/>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/snake-dark.svg?v=3" />
    <img alt="contribution snake" src="https://raw.githubusercontent.com/vladyslav-krutii/vladyslav-krutii/output/snake.svg?v=3" />
  </picture>
</p>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ff9c,50:0a3d2e,100:0d1117&height=100&section=footer" width="100%"/>
