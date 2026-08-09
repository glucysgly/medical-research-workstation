# WSL Repair Before Snapshot

Captured 2026-08-09 before the minimal repair.

- Hardware: ASUS ProArt P16 H7606WI, AMD Ryzen AI 9 HX 370.
- CPU virtualization firmware: enabled.
- WSL distribution: Ubuntu, Stopped, version 2.
- WSL bridge result: HYPERV_NOT_INSTALLED.
- Windows boot registry: SystemStartOptions contained HYPERVISORLAUNCHTYPE=OFF.
- WSL/Lxss and Virtual Machine Platform component packages: present.
- Planned change: bcdedit /set hypervisorlaunchtype auto.
- Not planned: BIOS changes, Secure Boot changes, feature installation, WSL
  unregister/reset, distribution deletion, or automatic restart.
