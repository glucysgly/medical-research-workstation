---
name: trial-registry-search
description: Search and normalize ClinicalTrials.gov with optional registry fallbacks.
---

# Call when

Call for registered, recruiting, ongoing, completed-but-unpublished, or
trial-publication mapping questions.

# Do not call when

Do not substitute registry records for published-paper retrieval, and do not
bypass CAPTCHA or registry access controls.

# Provider order

Use the official ClinicalTrials.gov API v2 thin adapter as the fallback. Keep
ISRCTN and WHO ICTRP explicitly optional/experimental.
