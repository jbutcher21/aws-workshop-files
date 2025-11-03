**File Type:** jsonl
**Root Records:** 70
**List Elements (Tables):** 25
**Total Fields:** 53

**Data Elements (All Lists):**
- properties.name: 38 records
- properties.address: 29 records
- properties.entity: 17 records
- properties.program: 17 records
- properties.authority: 17 records
- properties.reason: 17 records
- properties.listingDate: 17 records
- properties.status: 17 records
- properties.firstName: 14 records
- properties.lastName: 14 records
- properties.role: 14 records
- properties.phone: 10 records
- properties.birthDate: 9 records
- properties.email: 9 records
- properties.owner: 8 records
- properties.asset: 8 records
- properties.country: 7 records
- properties.director: 6 records
- properties.organization: 6 records
- properties.percentage: 5 records
- properties.previousName: 5 records
- properties.idNumber: 3 records
- properties.jurisdiction: 3 records
- properties.middleName: 1 records
- properties.gender: 1 records

## Document: ftm

### Fields

| # | Field Name | Type | Records | Pop % | Unique % | Table Context | Sample 1 | Sample 2 | Sample 3 | Sample 4 | Sample 5 |
|---|------------|------|---------|-------|----------|---------------|----------|----------|----------|----------|----------|
| 1 | id | str | 70 | 100.0% | 100.0% | root (70) | sanctions-person-1006 (1) | sanctions-sanction-1006 (1) | sanctions-person-1007 (1) | sanctions-sanction-1007 (1) | sanctions-person-1008 (1) |
| 2 | schema | str | 70 | 100.0% | 7.1% | root (70) | Person (33) | Sanction (17) | Ownership (8) | Company (6) | Directorship (6) |
| 3 | properties | dict | 70 |  |  | root (70) | 6 items (20) | 3 items (18) | 4 items (17) | 5 items (6) | 2 items (5) |
| 4 | properties.firstName | list | 14 |  |  | root (70) | 1 items (14) |  |  |  |  |
| 5 | properties.firstName.firstName | str | 14 | 100.0% | 71.4% | firstName (14) | Robert (2) | Eddie (2) | Maria (2) | John (2) | Patricia (1) |
| 6 | properties.lastName | list | 14 |  |  | root (70) | 1 items (14) |  |  |  |  |
| 7 | properties.lastName.lastName | str | 14 | 100.0% | 78.6% | lastName (14) | Smith (4) | Smith Sr (1) | Kusha (1) | Knight (1) | Antoun (1) |
| 8 | properties.middleName | list | 1 |  |  | root (70) | 1 items (1) |  |  |  |  |
| 9 | properties.middleName.middleName | str | 1 | 100.0% | 100.0% | middleName (1) | E (1) |  |  |  |  |
| 10 | properties.name | list | 38 |  |  | root (70) | 1 items (38) |  |  |  |  |
| 11 | properties.name.name | str | 38 | 100.0% | 97.4% | name (38) | John Smith (2) | Robert E Smith Sr (1) | Patricia Smith (1) | Robert Smith (1) | Eddie Kusha (1) |
| 12 | properties.birthDate | list | 9 |  |  | root (70) | 1 items (9) |  |  |  |  |
| 13 | properties.birthDate.birthDate | str | 9 | 100.0% | 66.7% | birthDate (9) | 1970-03-01 (2) | 1980-01-07 (2) | 1973-12-11 (2) | 1954-03-31 (1) | 1993-09-14 (1) |
| 14 | properties.idNumber | list | 3 |  |  | root (70) | 1 items (3) |  |  |  |  |
| 15 | properties.idNumber.idNumber | str | 3 | 100.0% | 100.0% | idNumber (3) | 112233 (1) | 294-66-9999 (1) | 201-77-7719 (1) |  |  |
| 16 | properties.address | list | 29 |  |  | root (70) | 1 items (29) |  |  |  |  |
| 17 | properties.address.address | str | 29 | 100.0% | 86.2% | address (29) | 638 Downey St, Salem, OR (2) | 3212 W. 32nd St Palm Harbor, FL 60527 (2) | Jia Musa Shahdara Sheikhupura Road, Lahore, Pakist (2) | Fieldstrasse 10, FL-2198 Triesen, Lichtenstein (2) | 123 Main St, Las Vegas  (1) |
| 18 | properties.entity | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 19 | properties.entity.entity | str | 17 | 100.0% | 100.0% | entity (17) | sanctions-person-1006 (1) | sanctions-person-1007 (1) | sanctions-person-1008 (1) | sanctions-person-1012 (1) | sanctions-person-1014 (1) |
| 20 | properties.program | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 21 | properties.program.program | str | 17 | 100.0% | 5.9% | program (17) | SANCTIONS (17) |  |  |  |  |
| 22 | properties.authority | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 23 | properties.authority.authority | str | 17 | 100.0% | 5.9% | authority (17) | Sanctions Authority (17) |  |  |  |  |
| 24 | properties.reason | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 25 | properties.reason.reason | str | 17 | 100.0% | 17.6% | reason (17) | Category: Fraud (13) | Category: Sanctioned (2) | Category: PEP (2) |  |  |
| 26 | properties.listingDate | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 27 | properties.listingDate.listingDate | str | 17 | 100.0% | 82.4% | listingDate (17) | 2019-03-05 (2) | 2015-05-07 (2) | 2019-04-03 (2) | 2017-01-03 (1) | 2020-02-04 (1) |
| 28 | properties.status | list | 17 |  |  | root (70) | 1 items (17) |  |  |  |  |
| 29 | properties.status.status | str | 17 | 100.0% | 17.6% | status (17) | Active (11) | Current (4) | Inactive (2) |  |  |
| 30 | properties.email | list | 9 |  |  | root (70) | 1 items (9) |  |  |  |  |
| 31 | properties.email.email | str | 9 | 100.0% | 77.8% | email (9) | msentosa@fmail.com (2) | kjones@universal.com (2) | psmith@email.com (1) | robert.smith@email.com (1) | Kusha123@hmail.com (1) |
| 32 | properties.gender | list | 1 |  |  | root (70) | 1 items (1) |  |  |  |  |
| 33 | properties.gender.gender | str | 1 | 100.0% | 100.0% | gender (1) | M (1) |  |  |  |  |
| 34 | properties.phone | list | 10 |  |  | root (70) | 1 items (10) |  |  |  |  |
| 35 | properties.phone.phone | str | 10 | 100.0% | 100.0% | phone (10) | 42-7925774 (1) | (4812)85-62-34 (1) | +92 42-7925774 (1) | +7(4812)85-62-34 (1) | 800-111-1234 (1) |
| 36 | properties.country | list | 7 |  |  | root (70) | 1 items (7) |  |  |  |  |
| 37 | properties.country.country | str | 7 | 100.0% | 71.4% | country (7) | Pakistan (2) | Singapore (2) | Germany (1) | RUS (1) | Lichtenstein (1) |
| 38 | properties.jurisdiction | list | 3 |  |  | root (70) | 1 items (3) |  |  |  |  |
| 39 | properties.jurisdiction.jurisdiction | str | 3 | 100.0% | 66.7% | jurisdiction (3) | Singapore (2) | Germany (1) |  |  |  |
| 40 | properties.owner | list | 8 |  |  | root (70) | 1 items (8) |  |  |  |  |
| 41 | properties.owner.owner | str | 8 | 100.0% | 75.0% | owner (8) | corp-filings-org-2074 (3) | corp-filings-person-2013 (1) | corp-filings-person-2014 (1) | corp-filings-person-2061 (1) | corp-filings-person-2081 (1) |
| 42 | properties.asset | list | 8 |  |  | root (70) | 1 items (8) |  |  |  |  |
| 43 | properties.asset.asset | str | 8 | 100.0% | 75.0% | asset (8) | corp-filings-org-2011 (2) | corp-filings-org-2074 (2) | corp-filings-org-2041 (1) | corp-filings-org-2071 (1) | corp-filings-org-2141 (1) |
| 44 | properties.role | list | 14 |  |  | root (70) | 1 items (14) |  |  |  |  |
| 45 | properties.role.role | str | 14 | 100.0% | 50.0% | role (14) | Principal (5) | Global Parent (3) | Owns 50% (2) | Owns 60% (1) | Owns 40% (1) |
| 46 | properties.percentage | list | 5 |  |  | root (70) | 1 items (5) |  |  |  |  |
| 47 | properties.percentage.percentage | str | 5 | 100.0% | 80.0% | percentage (5) | 50 (2) | 60 (1) | 40 (1) | 100 (1) |  |
| 48 | properties.previousName | list | 5 |  |  | root (70) | 1 items (5) |  |  |  |  |
| 49 | properties.previousName.previousName | str | 5 | 100.0% | 40.0% | previousName (5) | Universal Exports (4) | Autowerkz (1) |  |  |  |
| 50 | properties.director | list | 6 |  |  | root (70) | 1 items (6) |  |  |  |  |
| 51 | properties.director.director | str | 6 | 100.0% | 100.0% | director (6) | corp-filings-person-2051 (1) | corp-filings-person-2101 (1) | corp-filings-person-2111 (1) | corp-filings-person-2121 (1) | corp-filings-person-2131 (1) |
| 52 | properties.organization | list | 6 |  |  | root (70) | 1 items (6) |  |  |  |  |
| 53 | properties.organization.organization | str | 6 | 100.0% | 33.3% | organization (6) | corp-filings-org-2071 (5) | corp-filings-org-2041 (1) |  |  |  |