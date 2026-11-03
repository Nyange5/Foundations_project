# Sources log

Every source of real data is recorded here **the day we collect from it**. See `README.md` for the rules.

**Last updated:** 2 November 2026

## Status key

| Status | Meaning |
| --- | --- |
| Not started | Identified, not yet contacted |
| Contacted | We reached out and are waiting for a reply |
| Agreed | Source agreed to share; data not yet received |
| Collected | Data received and saved in `data/raw/` |
| Cleaned | Data cleaned and ready to load |
| Loaded | Data is in the database |
| Declined | Source declined; do not contact again without a new reason |
| Withdrawn | Source withdrew consent; data deleted |

## Log

Nothing has been collected yet. The sources below are ones we plan to approach. They are **not** confirmed, and no data from them is in the project.

| ID | Source | Type | Data we want | How we collect | Consent | Date | Raw file | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S-001 | RITCO | Bus company | Routes, timetable, fares | Website, then office/staff visit | — | — | — | Not started | Public website exists; staff confirmation needed |
| S-002 | Volcano Express | Bus company | Routes, timetable, fares | Visit at Nyabugogo | — | — | — | Not started | |
| S-003 | Horizon | Bus company | Routes, timetable, fares | Visit at Nyabugogo | — | — | — | Not started | |
| S-004 | Drivers at Nyabugogo | Private drivers | Typical private-car prices per route; interest in shared seats | Short interviews | — | — | — | Not started | No names stored unless the driver agrees |
| S-005 | RURA transport statistics | Public report | Registered operators, general context | Download public PDF | Not needed (public) | — | — | Not started | Cite the report; do not copy private data |

## How to add an entry

Copy this block, fill it in, and add a row to the table above:

```
ID:            S-00X
Source:        (company / person's role / document)
Type:          Bus company | Driver | Public document | Observation
Contact:       (role and how we reached them; no private numbers in this file)
Collected by:  (team member)
Date:          YYYY-MM-DD
Consent:       Verbal | Written | Message | Not needed (public)
Data received: (what we actually got)
Raw file:      data/raw/<filename>
Cleaning done: (what we changed)
Status:        Collected
Notes:         (hesitations, restrictions on use, follow-up date)
```

## Rules for this file

- Do **not** write private phone numbers, personal names of drivers, or licence numbers here. Refer to a source by company or role.
- Keep rows even when a source declines or withdraws; change the status instead of deleting the row.
- If a source restricts how we use their data, write the restriction in **Notes**.
