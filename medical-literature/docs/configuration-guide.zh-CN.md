# MLRO V2 通用配置指南

本指南只描述通用配置，不包含任何个人路径、API key、学校账号或私人全文。

## 1. 安装核心模块

在仓库的 `medical-literature` 目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python scripts/medlit.py doctor --json
```

核心代码使用 Python 标准库；如果只运行离线 E2E，不需要安装商业数据库客户端或大型全文环境。

## 2. PubMed

必须提供一个可接收 NCBI 联系邮件的邮箱；API key 是可选的，但建议用于批量检索。请把值放在操作系统用户环境变量或密钥管理器中，不要写进仓库：

```powershell
[Environment]::SetEnvironmentVariable('NCBI_EMAIL', 'your.email@example.org', 'User')
[Environment]::SetEnvironmentVariable('NCBI_API_KEY', '<your NCBI API key>', 'User')
```

新建 PowerShell 窗口后验证：

```powershell
python scripts/medlit.py capabilities --json
python scripts/medlit.py search --query 'cervical cancer AND immunotherapy' --json
```

输出只应显示 `api_key_configured: true/false`，不应显示密钥正文。

## 3. 商业数据库、CNKI 和 CENTRAL

Embase、Web of Science、Scopus、CNKI 和 CENTRAL 不应被伪装成自动可用：

- 有合法账号/API 或导出权限时，使用对应数据库的原生检索并保存 RIS/CSV；
- 没有权限时，工作站生成检索式并标记 `AUTH_REQUIRED` 或 `MANUAL_REQUIRED`；
- 人工导入必须保留数据库名、完整检索式、检索日期、命中数和文件 SHA-256；
- 不绕过验证码、访问控制或出版社权限。

## 4. ClinicalTrials.gov

默认使用官方 API fallback：

```powershell
python scripts/medlit.py trials --query 'locally advanced cervical cancer pembrolizumab' --json
```

注册试验与论文是不同实体，必须通过 trial-publication provenance 关联。

## 5. Zotero

Zotero 桌面端本地读取和 Web API 写入属于可选 downstream 集成。推荐配置：

```text
ZOTERO_LOCAL=true
ZOTERO_API_KEY=<local secret, never commit>
ZOTERO_LIBRARY_ID=<numeric user or group library id>
ZOTERO_LIBRARY_TYPE=user|group
```

本地 API 只能在用户明确开启 Zotero 设置中的“允许其他应用在此计算机上与 Zotero 通信”后使用。写入时必须先 DOI 去重；默认只导入元数据，不自动下载全文。

## 6. MinerU

MinerU 应安装在独立环境。将可执行文件路径放入当前用户环境变量：

```powershell
[Environment]::SetEnvironmentVariable('MEDLIT_MINERU_BIN', 'C:\path\to\mineru.exe', 'User')
```

只处理用户明确授权的本地 PDF 或合法开放获取 PDF。不要把私人全文上传到未知服务。

## 7. PaperQA2 与 DeepSeek

PaperQA2 需要一个 LiteLLM 兼容的模型提供方，不强制使用 OpenAI。可以使用 DeepSeek 兼容接口，但 key 只应存在于本地环境：

```powershell
[Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', '<your DeepSeek key>', 'User')
```

模板位于 `config/paperqa.deepseek.example.json`。运行时可把 `DEEPSEEK_API_KEY` 映射为当前进程的 `OPENAI_API_KEY`，不要把 key 写进 JSON 或脚本。可使用：

```powershell
$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'User')
python scripts/paperqa_deepseek_local.py --input .\runs\mineru-output --question 'What are the main outcomes and limitations?'
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
```

## 8. 验收与状态

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/medlit.py e2e --output-root .\runs\offline-e2e
```

`CORE_READY` 表示确定性核心和离线契约可用；不表示所有商业数据库、全文、偏倚风险或证据综合链路已经完成。所有 `AUTH_REQUIRED`、`MANUAL_REQUIRED`、`OPTIONAL_UNVERIFIED` 和 `PENDING_DOWNSTREAM_INTEGRATION` 都必须在报告中保留。
