# Provider roles

| Role | Examples | Can affect formal count? | Current status |
|---|---|---:|---|
| FORMAL_DATABASE | PubMed, Embase, Web of Science, Scopus, CNKI, CENTRAL | Yes, independently | PubMed fallback exists; commercial auth pending |
| DISCOVERY_ENGINE | Paper Search, OpenAlex | No by itself | Vendor integration unverified |
| TRIAL_REGISTRY | ClinicalTrials.gov, optional ISRCTN/WHO ICTRP | Separate registry count | Official API fallback exists |
| CITATION_FORWARD/BACKWARD | Semantic Scholar, optional OpenAlex | No; logged as snowball | Thin S2 adapter + fixture contract |
| CHALLENGER | scholar-megasearch | No | Explicitly degradable |
| VERIFIER | DOI MCP, Crossref/PubMed fallback | No; gates bibliography | Fallback policy + fixtures |
| LOCAL_LIBRARY | Zotero | No | Read-first boundary |
| MANUAL_IMPORT | CENTRAL export, CNKI export | Only with recorded import | Human action required |

No upstream is promoted merely because it has stars or a successful install.
License, API behavior, contract tests, limits, and live smoke evidence remain
separate acceptance evidence.
