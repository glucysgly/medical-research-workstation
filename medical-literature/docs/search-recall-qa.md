# Search recall QA

For a formal or deep run, compare formal and challenger canonical IDs and
write `source_overlap.csv` plus `search_qa.json`. Report intersection, formal
unique, challenger unique, verified challenger unique, relevant challenger
unique, and warnings.

Challenger-unique records are classified as query-term gap, indexing gap,
preprint-only, conference-only, database-not-covered, metadata mismatch,
date/language filter, or other. A confirmed query-term gap starts a new search
run and never mutates the previous run.

The formal PRISMA count is always derived from formal source exports and the
freeze manifest. Challenger output is supplementary QA.
