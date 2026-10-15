# REFERENCE AUDIT (final pass, 14 Oct 2026)
Method: all 24 bib entries checked against Crossref (DOI lookup, or bibliographic search where no DOI exists), comparing title, year, volume and pages; key literature claims checked against abstracts/publisher pages/full text as listed.

| Key | Metadata check | Claim check |
|---|---|---|
| ring2019, engelen2021, apruzzese2022, kuang2014, waghmode2025, emirmahmutoglu2025, abdelrahman2026, scholkopf1998, cortes1995, cover1967, quinlan1986, chicco2020, nadeau2003, abdulhammed2019 | Crossref match: title 1.0, year/volume/pages agree | Abstract/publisher level (earlier rounds) |
| sharafaldin2018 | Crossref (search): title, year, pp 108-116 agree; no DOI in bib | Abstract |
| patil2025 | DOI matches; Informatica 49(4), Dec 2025; issue number added this pass | 99.98 % ET+IG (24 features) from publisher abstract; 99.58-99.96 % PCA range from full paper (author-supplied re-check) |
| abdelaziz2025 | DOI matches; J. Netw. Syst. Manage. 33(1), art. 2; online 22 Oct 2024, volume year 2025 (bib uses 2025) | 99.8 % weighted-F1, 93.31 % macro-F1 (source abstract) |
| chavan2025 | DOI matches; IJCA 187(3), pp 17-22 (pages added this pass) | Table 4 RF 97.20 % in publisher PDF (read in full this session); 80/20 split |
| xu2025 | arXiv:2506.19877v2 confirmed (title, authors, v2 dated 11 Aug 2025); not on Crossref as a journal | Table II MLP 0.9775 on overall test set confirmed this pass |
| emirmahmutoglu2025 | DOI matches; P2P Netw. Appl. 18(3), art. 161 | Abstract: 0.99987 F1 confirmed; 99.9965 % accuracy location is from an external re-check, not independently re-read by me |
| panigrahi2018, arp2022, pedregosa2011, breiman2001, demsar2006 | No DOI; Crossref search did not return the right record (venues without DOIs). Volume/pages match my knowledge of the publications but are NOT machine-verified | Panigrahi/Arp abstracts checked earlier; textbook references used only for method attribution |

Unverified: IEEE Xplore pages (not accessible), Emirmahmutoglu full text, the five non-DOI entries' page numbers, and any sentence not listed above.
