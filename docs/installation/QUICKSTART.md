# Quick start / 快速开始

## English

From the repository root:

```bash
python scripts/bootstrap.py --dry-run
python scripts/researchctl.py doctor --json
python scripts/researchctl.py skills audit --json
python scripts/researchctl.py projects --json
python examples/synthetic/run_synthetic_smoke.py
```

For a local project, use an ASCII project id and keep restricted data outside
the public repository. The control plane creates metadata and manifest files;
it does not download raw data or install a complete bioinformatics stack.

## 中文

在仓库根目录执行：

```bash
python scripts/bootstrap.py --dry-run
python scripts/researchctl.py doctor --json
python scripts/researchctl.py skills audit --json
python scripts/researchctl.py projects --json
python examples/synthetic/run_synthetic_smoke.py
```

本地项目请使用英文、数字、连字符或下划线组成的项目 ID。受限数据应保存在公开
仓库之外。控制层只创建项目元数据和 manifest，不下载原始数据，也不自动安装完整
生信环境。
