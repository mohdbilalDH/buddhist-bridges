# Controlled Vocabularies — India–Korea Mediators Master Dataset

Version 0.1 · 2026-08-16 · These are the ONLY allowed values for the corresponding fields.

## 1. relationship_type (people.csv, person_person.csv)
| Value | Definition |
|---|---|
| `DIRECT` | Physical encounter/travel: the person travelled between India and Korea (or met an Indian/Korean in person in a third country) |
| `INDIRECT` | Influence or connection without physical travel (e.g., wrote about the other country, was read there, shaped perceptions) |
| `MEDIATED` | Influence through an intermediary: another person, a language, a text, a translation, an institution |
| `UNCERTAIN` | Evidence insufficient to classify; record uncertainty explicitly in notes |

## 2. exchange_types (people.csv)
`RELIGIOUS` · `LITERARY` · `INTELLECTUAL` · `POLITICAL` · `ARTISTIC` · `LINGUISTIC` · `CULTURAL` · `DIPLOMATIC` · `ECONOMIC` · `MILITARY` · `ACADEMIC` · `MUSICAL` · `CINEMATIC` · `HUMANITARIAN` · `JOURNALISM` · `OTHER`
(multi-value: semicolon-separated; `HUMANITARIAN` added for peacekeeping/medical missions, `JOURNALISM` for media figures — v0.1.1, 2026-08-16)

## 3. period
| Value | Range (approx.) |
|---|---|
| `ANCIENT` | before 900 CE (Three Kingdoms / Silla / Gaya / early Goryeo) |
| `MEDIEVAL` | 900–1392 (Goryeo) |
| `EARLY_MODERN` | 1392–1900 (Joseon) |
| `MODERN` | 1900–1945 (colonial era) |
| `CONTEMPORARY` | 1945–2026 |

## 4. direction_of_influence
`INDIA_TO_KOREA` · `KOREA_TO_INDIA` · `BIDIRECTIONAL` · `UNCERTAIN`

## 5. confidence
| Value | Definition |
|---|---|
| `HIGH` | Multiple independent authoritative sources; primary evidence |
| `MEDIUM` | One authoritative source or consistent secondary sources |
| `LOW` | Single secondary/popular source; details uncertain |
| `SPECULATIVE` | Scholarly hypothesis or legend; explicitly flagged |

## 6. source_type (sources.csv)
`PRIMARY` (contemporary document, inscription, letter, travelogue) · `SECONDARY` (scholarly monograph/article) · `TERTIARY` (encyclopedia, reference work) · `ARCHIVAL` (archive holding) · `DATABASE` (structured database: Wikidata, OpenAlex, DBpedia) · `NEWS` (newspaper/periodical) · `WEBSITE` (institutional website) · `OTHER`

## 7. reliability (sources.csv)
`AUTHORITATIVE` (national academy, university press, peer-reviewed) · `ACADEMIC` · `INSTITUTIONAL` (museum, embassy, government) · `POPULAR` (press, blogs) · `UNVERIFIED`

## 8. nationality_region (people.csv)
`KOREAN` (Silla/Goryeo/Joseon/Korean) · `INDIAN` (incl. historical: Gandhara, Serindia, Ayodhya) · `CHINESE` · `JAPANESE` · `BRITISH` · `OTHER` · `UNCERTAIN`
(For pre-modern figures use the historical polity in parentheses in the free-text field, e.g. `KOREAN (Silla)`.)

## 9. place_type (places.csv)
`CITY` · `REGION` · `KINGDOM` · `MONASTERY` · `PORT` · `MOUNTAIN` · `COUNTRY` · `UNIVERSITY` · `OTHER`

## 10. purpose (travels.csv)
`PILGRIMAGE` · `DIPLOMATIC` · `STUDY` · `TRADE` · `EXILE` · `MISSIONARY` · `WAR` · `BUSINESS` · `ACADEMIC` · `OTHER` · `UNKNOWN`

## 11. text_type (texts.csv)
`TRAVELOGUE` · `COMMENTARY` · `POEM` · `LETTER` · `TREATISE` · `BIOGRAPHY` · `TRANSLATION` · `NEWSPAPER_ARTICLE` · `SUTRA` · `HISTORY` · `MEMOIR` · `OTHER`

## 12. institution_type (institutions.csv)
`MONASTERY` · `UNIVERSITY` · `GOVERNMENT` · `EMBASSY` · `COMPANY` · `NGO` · `MEDIA` · `MILITARY` · `OTHER`

## 13. relationship_kind (person_person.csv)
`TEACHER_STUDENT` · `CONTEMPORARY` · `CORRESPONDENT` · `TRANSLATOR_OF` · `SUBJECT_OF` · `COLLEAGUE` · `FAMILY` · `MET_IN_PERSON` · `INFLUENCED` · `DOCUMENTED` · `OTHER`

## 14. link_type (person_place.csv)
`BIRTH` · `RESIDENCE` · `VISITED` · `STUDIED` · `WORKED` · `LEGENDARY_ORIGIN` · `DIED` · `OTHER`

## 15. link_type (person_text.csv)
`AUTHOR` · `TRANSLATOR` · `SUBJECT` · `MENTIONED_IN` · `COMMENTATOR` · `OTHER`

## 16. status (people.csv)
`VERIFIED` · `PARTIAL` (some fields verified, others uncertain) · `UNRESOLVED` (open questions) · `LEGENDARY` (mythic/traditional figure, documented as legend)

## 17. date precision
`YEAR` · `MONTH` · `DAY` · `CENTURY` · `APPROX` · `UNKNOWN`

## 18. physically_traveled
`YES` · `NO` · `UNCERTAIN`

## 19. languages (free-text, ISO 639-1 codes preferred)
`ko` Korean · `zh` Chinese (Classical Chinese `lzh`) · `sa` Sanskrit · `pi` Pali · `hi` Hindi · `bn` Bengali · `en` English · `ja` Japanese · `fa` Persian · `ar` Arabic · `ta` Tamil · `ml` Malayalam · `ur` Urdu · `fr` French · `de` German · `ru` Russian · `other` (specify)

## 20. geographic locations (free-text but standardised)
Use modern country names + historical polity in parentheses, e.g. `India (Gandhara)`, `Korea (Silla)`, `China (Tang)`, `Japan`, `Sri Lanka (Ceylon)`, `Myanmar (Burma)`, `Indonesia (Srivijaya)`, `Central Asia (Serindia)`.