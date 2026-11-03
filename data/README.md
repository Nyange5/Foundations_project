# ETIKE data guide

**Status:** Sprint 1 draft, updated as the collection progresses

This folder holds everything about the **real data** behind ETIKE: where it comes from, how we clean it, and how it reaches the database. 

```
data/
├── README.md     ← this file: rules and process
├── sources.md    ← log of every source we collect from
└── raw/          ← original files exactly as received (NOT committed to Git)
```

## 1. Rules

1. **Real data only.** We do not use dummy or invented data. If a value is unknown, leave it empty; never guess it.
2. **Every source is logged.** Nothing enters the database unless it has a row in `sources.md`.
3. **Explain before you ask.** Tell every source why we need the data, how it is used and how it is protected, before collecting anything.
4. **Consent first.** The source agrees (in writing or by message, noted in `sources.md`) and may withdraw at any time. Withdrawn data is deleted.
5. **Collect the minimum.** Only the fields in section 3. Personal data (a driver's phone number, licence number, a person's name) is collected only when the person agrees and the feature needs it, in line with Rwanda's Law No. 058/2021 on personal data protection.
6. **Raw files stay out of Git.** `data/raw/` is git-ignored, so personal details never reach the repository. Only `README.md`, `sources.md` and the cleaning/loading scripts are committed.
7. **Cleaned data is reproducible.** Anyone can rebuild the database data by re-running the loading script on the raw files.

## 2. Pipeline

```
Collect  →  Record in sources.md  →  Clean  →  Load by script  →  Verify
```

| Step | What happens | 
| --- | --- | 
| Collect | Visit, call or interview the source; photograph or copy the timetable/price list; save the original into `data/raw/` | 
| Record | Add a row to `sources.md` the same day | 
| Clean | Standardise names, times and prices (section 4) | 
| Load | Run the loading script to fill `bus_companies`, `routes` and `bus_trips` | 
| Verify | Spot-check 10% of rows against the original source; run the checklist in section 5 | 

## 3. What we collect

### Bus companies → `bus_companies`

| Field | Example | 
| --- | --- | 
| `name` | (company name as it prints it) | 
| `phone` | (public office number) | 

### Routes → `routes`

| Field | Example |     
| --- | --- | 
| `from_district` | Kigali | 
| `to_district` | Musanze | 

### Bus trips → `bus_trips`

| Field | Example | 
| --- | --- | 
| `company` | (must match a `name` above) | 
| `route` | from + to district | Required |
| `departs_at` | 07:00 | 
| `seats_total` | 30 | 
| `fare_rwf` | 3000 | 

### Private and shared rides

Prices for private cars and drivers' interest in shared seats are collected through short interviews with drivers. Record only what the driver agrees to share. Vehicle and driver details are stored only after the driver consents, and drivers are approved through the app later, not from this folder.


## 4. Cleaning rules

- **Districts:** use the official English spelling, capitalised (Kigali, Musanze, Huye, Rubavu, ...). One spelling per district everywhere.
- **Times:** 24-hour `HH:MM`.
- **Prices:** whole numbers in RWF, no `RWF`, commas or spaces (`3000`, not `3,000 RWF`).
- **Company names:** exactly as the company writes them; remove duplicates (same company, different spelling).
- **Missing values:** leave empty. Do not write `N/A`, `0` or a guess.
- **Dates:** record the date the data was collected, since fares and timetables change.
- **Phone numbers:** digits only, local format (`078xxxxxxx`).

## 5. Verification checklist

Before a cleaned file is handed over for loading:

- [ ] Every row has a matching entry in `sources.md`
- [ ] No row contains personal data the person did not agree to share
- [ ] District names, times and prices follow section 4
- [ ] No duplicate company, route or trip
- [ ] About 10% of rows re-checked against the original source
- [ ] Original file saved in `data/raw/` (not committed)

## 6. Keeping `raw/` out of Git

Add this to the root `.gitignore`. The `.gitkeep` exception keeps the folder in the repository:

```
data/raw/*
!data/raw/.gitkeep
```

## 7. If a source asks us to remove their data

1. Delete their files from `data/raw/`.
2. Remove their rows from the cleaned files and from the database .
3. Mark the entry in `sources.md` as **Withdrawn** (keep the row, remove the data).
