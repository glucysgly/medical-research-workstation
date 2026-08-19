from __future__ import annotations

import re


def route_query(query: str) -> dict[str, object]:
    text = query.casefold().strip()
    if re.search(r"系统综述|meta[- ]?analysis|systematic review|prisma|正式综述|正式检索", text):
        mode = "FORMAL_REVIEW"
        routes = ["formal-literature-search", "trial-registry-search", "search-recall-qa"]
    elif re.search(r"引用真假|核验引用|verify.*(citation|doi)|citation verification|doi.*核验", text):
        mode = "CITATION_VERIFY"
        routes = ["citation-verification"]
    elif re.search(r"正在招募|临床试验|clinical trial|trial registry|clinicaltrials", text):
        mode = "TRIAL_LANDSCAPE"
        routes = ["trial-registry-search"]
    elif re.search(r"沿.*文章|后续研究|forward citation|backward citation|snowball|引文雪球|citation trace", text):
        mode = "SEED_EXPANSION"
        routes = ["citation-tracing", "search-recall-qa"]
    elif re.search(r"深度检索|全面找|所有相关|deep discovery|comprehensive search", text):
        mode = "DEEP_DISCOVERY"
        routes = ["formal-literature-search", "trial-registry-search", "citation-tracing", "search-recall-qa"]
    else:
        mode = "QUICK"
        routes = ["formal-literature-search"]
    return {"mode": mode, "routes": routes, "challenger": mode in {"DEEP_DISCOVERY", "FORMAL_REVIEW"}}
