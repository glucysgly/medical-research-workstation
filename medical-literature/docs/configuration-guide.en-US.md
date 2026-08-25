# MLRO V2 Generic Configuration Guide

This guide contains generic configuration only. It does not contain personal paths, API keys, institutional credentials, or private full text.

## 1. Install the core module

From the repository's `medical-literature` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
python scripts/medlit.py doctor --json
```

The core uses the Python standard library. Offline E2E does not require commercial database clients or a large full-text environment.

## 2. PubMed

Provide a contact email for NCBI. An API key is optional but recommended for batch retrieval. Store values in the operating-system user environment or a secret manager, never in the repository:

```powershell
[Environment]::SetEnvironmentVariable('NCBI_EMAIL', 'your.email@example.org', 'User')
[Environment]::SetEnvironmentVariable('NCBI_API_KEY', '<your NCBI API key>', 'User')
```

Open a new PowerShell window and verify:

```powershell
python scripts/medlit.py capabilities --json
python scripts/medlit.py search --query 'cervical cancer AND immunotherapy' --json
```

Output should expose only `api_key_configured: true/false`, never the key itself.

## 3. Commercial databases, CNKI, and CENTRAL

Embase, Web of Science, Scopus, CNKI, and CENTRAL must not be represented as automatically available without authorized access:

- run the native database search when a legal account/API or export permission exists;
- otherwise generate the query and report `AUTH_REQUIRED` or `MANUAL_REQUIRED`;
- preserve database name, exact query, search date, hit count, and SHA-256 for every manual export;
- never bypass CAPTCHA, access controls, or publisher permissions.

## 4. ClinicalTrials.gov

The official API fallback can be exercised with:

```powershell
python scripts/medlit.py trials --query 'locally advanced cervical cancer pembrolizumab' --json
```

Registry records and published papers are separate entities and must be connected through trial-publication provenance.

## 5. Zotero

Zotero desktop local reads and Web API writes are optional downstream integrations. The generic shape is:

```text
ZOTERO_LOCAL=true
ZOTERO_API_KEY=<local secret, never commit>
ZOTERO_LIBRARY_ID=<numeric user or group library id>
ZOTERO_LIBRARY_TYPE=user|group
```

The local API requires the Zotero preference that allows other applications on this computer to communicate with Zotero. Import by DOI only after deduplication; metadata-only import is the default and full-text download is not automatic.

## 6. MinerU

Install MinerU in an isolated environment and expose its executable path through the user environment:

```powershell
[Environment]::SetEnvironmentVariable('MEDLIT_MINERU_BIN', 'C:\path\to\mineru.exe', 'User')
```

Process only local PDFs explicitly authorized by the user or legally open-access PDFs. Do not upload private full text to unknown services.

## 7. PaperQA2 and DeepSeek

PaperQA2 needs an LLM provider compatible with LiteLLM; it does not require an OpenAI account specifically. A DeepSeek-compatible endpoint can be used, but the key must remain local:

```powershell
[Environment]::SetEnvironmentVariable('DEEPSEEK_API_KEY', '<your DeepSeek key>', 'User')
```

The template is `config/paperqa.deepseek.example.json`. At runtime, map `DEEPSEEK_API_KEY` to the current process's `OPENAI_API_KEY`; do not write the key into JSON or scripts:

```powershell
$env:OPENAI_API_KEY = [Environment]::GetEnvironmentVariable('DEEPSEEK_API_KEY', 'User')
python scripts/paperqa_deepseek_local.py --input .\runs\mineru-output --question 'What are the main outcomes and limitations?'
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
```

## 8. Validation and status

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
python scripts/medlit.py e2e --output-root .\runs\offline-e2e
```

`CORE_READY` means that the deterministic core and offline contracts are usable; it does not mean that all commercial databases, full-text, risk-of-bias, or evidence-synthesis steps are complete. Preserve `AUTH_REQUIRED`, `MANUAL_REQUIRED`, `OPTIONAL_UNVERIFIED`, and `PENDING_DOWNSTREAM_INTEGRATION` in reports.
