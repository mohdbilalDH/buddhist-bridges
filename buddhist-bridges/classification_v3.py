# -*- coding: utf-8 -*-
"""Buddhist Bridges V3 classification (source of truth), v0.2 - 2026-08-17.

Every record of the V2 India-Korea Mediators dataset is classified for the
Buddhist-only V3 dataset. v0.2 replaces the binary scope with the user's
graded relevance scale and adds multi-valued connection types and movement
statuses:

    relevance (buddhist_relevance, graded - the V3 decision mechanism):
             PRIMARY    - Buddhist identity: monks/nuns/ordained practitioners,
                          Buddhist institutions, sacred sites, core Buddhist texts
             SECONDARY  - significant Buddhist activity, primary identity elsewhere
                          (scholars of Buddhism, Buddhist-themed writers, partly
                          Buddhist institutions/texts)
             MEDIATOR   - not Buddhist themselves, but a documented channel in the
                          India-Korea Buddhist exchange (Tagore, Gandhi, Vinoba,
                          translators of Buddhist-relevant works, hosts)
             CONTEXTUAL - relevant background/context, no direct Buddhist channel
                          (legends, literary circles, partly-relevant surveys)
             NONE       - no Buddhist relevance (V2-only records)

    scope (carry decision, derived from relevance and validated by the generator):
             KEEP    - PRIMARY: carry into V3 as-is
             ADAPT   - SECONDARY/MEDIATOR: carry with reframing
             CONTEXT - CONTEXTUAL: carry as reference-only context rows
             EXCLUDE - NONE: stays in V2 dataset only
             REVIEW  - pending research before a final decision (P-0068, P-0070)

    period_band (user's continuous historical framework):
             B1 Ancient/early-medieval (<900)
             B2 Silla/Goryeo (900-1392)
             B3 Joseon (1392-1900)
             B4 Modern/colonial (1900-1945)
             B5 1945-1990
             B6 1990-2026

    conns (connection-type ladder, weak->strong by documentation; MULTIPLE
          allowed per record, joined with "; " in the CSV):
             LEGENDARY            - traditional/legendary narrative
             INDIRECT_INFLUENCE   - documented influence, no direct channel
             TEXTUAL_TRANSMISSION - texts/teachings/translations as the channel
             PERSON_ENCOUNTER     - documented person-to-person contact
             INSTITUTIONAL        - institutional/organizational channel
             PHYSICAL_MOVEMENT    - documented physical travel/movement

    movement (movement status of the person relative to the India-Korea
              exchange; "-" when not applicable):
             planned / visited / worked / studied / legendary

Generator: build_classification.py -> classification_v3.csv
"""

RELEVANCE = ("PRIMARY", "SECONDARY", "MEDIATOR", "CONTEXTUAL", "NONE")

SCOPES = ("KEEP", "ADAPT", "CONTEXT", "EXCLUDE", "REVIEW")

# relevance -> scope mapping (validated by the generator; REVIEW is an override)
SCOPE_DERIVED = {
    "PRIMARY": "KEEP",
    "SECONDARY": "ADAPT",
    "MEDIATOR": "ADAPT",
    "CONTEXTUAL": "CONTEXT",
    "NONE": "EXCLUDE",
}

MOVEMENT = ("planned", "visited", "worked", "studied", "legendary", "-")

BANDS = {
    "B1": "B1 Ancient/early-medieval (<900)",
    "B2": "B2 Silla/Goryeo (900-1392)",
    "B3": "B3 Joseon (1392-1900)",
    "B4": "B4 Modern/colonial (1900-1945)",
    "B5": "B5 1945-1990",
    "B6": "B6 1990-2026",
}

CONN = {
    "LEGENDARY": "LEGENDARY",
    "INDIRECT": "INDIRECT_INFLUENCE",
    "TEXTUAL": "TEXTUAL_TRANSMISSION",
    "ENCOUNTER": "PERSON_ENCOUNTER",
    "INSTITUTIONAL": "INSTITUTIONAL",
    "PHYSICAL": "PHYSICAL_MOVEMENT",
}

# ----------------------------------------------------------------------------
# PEOPLE  (pid -> (relevance, scope, band, conns, movement, rationale))
# ----------------------------------------------------------------------------
PERSON = {
    "P-0001": ("PRIMARY", "KEEP", "B1", ("PHYSICAL", "TEXTUAL"), "visited",
               "Core record: Silla pilgrim-monk; Wang ocheonchukguk jeon is the primary 8th-c. source on India"),
    "P-0002": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "-",
               "Silla Yogacara master; India link via Indian doctrine studied in Chang'an (no travel)"),
    "P-0003": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "-",
               "Silla philosopher; commentaries on Indian-origin texts (Awakening of Faith)"),
    "P-0004": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "-",
               "Silla exegete of Indian sutra heritage (Pure Land / Golden Light commentaries)"),
    "P-0005": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "-",
               "Silla Yogacara commentator (Cheng Weishi Lun lineage)"),
    "P-0006": ("PRIMARY", "KEEP", "B1", ("PHYSICAL", "INSTITUTIONAL"), "worked",
               "Earliest documented Buddhist arrival in Korea (384 CE); founder of Baekje Buddhism"),
    "P-0007": ("CONTEXTUAL", "CONTEXT", "B1", ("LEGENDARY",), "legendary",
               "Legendary queen from 'Ayuta'; non-Buddhist cultural narrative (context row)"),
    "P-0008": ("CONTEXTUAL", "CONTEXT", "B1", ("LEGENDARY",), "-",
               "Legendary founder-king; non-Buddhist (context row)"),
    "P-0009": ("PRIMARY", "KEEP", "B2", ("TEXTUAL",), "-",
               "Seon monk-historian; Samguk Yusa preserves the early Buddhist traditions"),
    "P-0010": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "-",
               "Esoteric master; Amoghavajra-lineage transmission to Silla"),
    "P-0011": ("PRIMARY", "KEEP", "B1", ("PHYSICAL", "TEXTUAL"), "studied",
               "Baekje Vinaya master; documented sea pilgrimage to Central India 526-531; 5 yrs Sanskrit at Sangana"),
    "P-0012": ("PRIMARY", "KEEP", "B1", ("PHYSICAL", "TEXTUAL"), "worked",
               "Indian Tripitaka master resident in Baekje (531); bearer of Sanskrit texts"),
    "P-0013": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "studied",
               "Silla monk at Nalanda (Yijing record)"),
    "P-0014": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Silla monk at Bodh Gaya/Nalanda (Yijing record)"),
    "P-0015": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Silla pilgrim to India (Yijing record)"),
    "P-0016": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Silla monk who died at Bodh Gaya (Yijing record)"),
    "P-0017": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Silla pilgrim to India (Yijing record)"),
    "P-0018": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Silla monk in Yijing's India network (identification debated)"),
    "P-0020": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Esoteric monk; reached Central India, died in Tibet"),
    "P-0021": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "visited",
               "Unified Silla monk; India via Tang"),
    "P-0022": ("PRIMARY", "KEEP", "B1", ("PHYSICAL",), "studied",
               "Goguryeo monk ordained in Sri Lanka (South Asian Buddhist world; not mainland India)"),
    "P-0023": ("PRIMARY", "KEEP", "B2", ("PHYSICAL", "INSTITUTIONAL", "ENCOUNTER"), "worked",
               "Flagship record: last great Indian monk in Korea; Nalanda -> Goryeo; founded Hoeamsa 1328; Naong's teacher"),
    "P-0024": ("PRIMARY", "KEEP", "B2", ("ENCOUNTER",), "-",
               "Goryeo Seon master; personal transmission from Indian master Jikong"),
    "P-0025": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "-",
               "Joseon encyclopedist; India via Ming geography, not Buddhist"),
    "P-0026": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "-",
               "India entries unverified; not Buddhist"),
    "P-0027": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "-",
               "Silhak world geography; not Buddhist"),
    "P-0028": ("SECONDARY", "ADAPT", "B4", ("TEXTUAL",), "-",
               "Father of Korean religious studies; Choson Pulgyo T'ongsa (1918) - scholar of Buddhism, not a practitioner"),
    "P-0029": ("SECONDARY", "ADAPT", "B4", ("TEXTUAL", "ENCOUNTER"), "-",
               "Wrote Choson Pulgyo (1930) arguing Buddhism reached Korea directly from India; nationalist framing; Tagore meeting 1916"),
    "P-0030": ("MEDIATOR", "ADAPT", "B4", ("INDIRECT", "ENCOUNTER"), "planned",
               "Channel figure: Lamp of the East (1929) invoked Korea's Buddhist heritage; influenced Han Yong-un; Seoul visit planned 1929, never made"),
    "P-0031": ("CONTEXTUAL", "CONTEXT", "B4", ("ENCOUNTER",), "-",
               "Tagore circle; literary meeting in Japan (context row)"),
    "P-0032": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "-",
               "Tagore translator; literary (context row)"),
    "P-0033": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "-",
               "Tagore translator; literary (context row)"),
    "P-0034": ("PRIMARY", "KEEP", "B4", ("INDIRECT", "TEXTUAL"), "-",
               "Buddhist monk-poet (PRIMARY identity); India link via Tagore's spiritual lyricism (literary-religious reception with critical distance)"),
    "P-0035": ("CONTEXTUAL", "CONTEXT", "B4", ("INDIRECT",), "-",
               "Novelist; Tagore review; 1930s Buddhist conversion not tied to India (context row)"),
    "P-0036": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "-",
               "Tagore message translator; literary (context row)"),
    "P-0037": ("CONTEXTUAL", "CONTEXT", "B5", ("INDIRECT",), "-",
               "Quaker 'Korean Gandhi'; Gandhi channel but non-Buddhist (context row)"),
    "P-0038": ("MEDIATOR", "ADAPT", "B4", ("INDIRECT",), "-",
               "Channel figure: Gandhi's words open Popchong's Muso-yu; influence on Korea's independence movement"),
    "P-0039": ("NONE", "EXCLUDE", "B5", ("INDIRECT",), "-",
               "PM of India; diplomatic"),
    "P-0040": ("NONE", "EXCLUDE", "B5", ("INDIRECT",), "-",
               "Diplomat; UN Korea policy"),
    "P-0041": ("NONE", "EXCLUDE", "B5", ("INDIRECT",), "-",
               "Ambassador; Korean War diplomacy"),
    "P-0042": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "UNTCOK chairman; electoral mission"),
    "P-0043": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "NNRC chairman; military"),
    "P-0044": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "ICF commander; military"),
    "P-0045": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "NNRC alternate chairman; military-diplomatic"),
    "P-0046": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "60 PFA commander; military-medical"),
    "P-0047": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "First Indian ambassador to the ROK"),
    "P-0048": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "worked",
               "First ROK ambassador to India"),
    "P-0049": ("NONE", "EXCLUDE", "B6", ("PHYSICAL",), "visited",
               "Daewoo chairman; economic"),
    "P-0050": ("NONE", "EXCLUDE", "B6", ("INDIRECT",), "-",
               "Samsung chairman; corporate only (personal travel unverified)"),
    "P-0051": ("SECONDARY", "ADAPT", "B6", ("PHYSICAL", "TEXTUAL"), "visited",
               "Poet, ordained monk 1952-62; India travels 1990s/2019; Little Pilgrim (Buddha novel)"),
    "P-0052": ("PRIMARY", "KEEP", "B5", ("PHYSICAL", "ENCOUNTER"), "visited",
               "Monk-essayist; 1971 India pilgrimage, met Vinoba Bhave; Muso-yu"),
    "P-0053": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "TEXTUAL"), "visited",
               "Career Buddhist-studies Indologist; India-Korea interflow monograph; Seoul 2016"),
    "P-0054": ("SECONDARY", "ADAPT", "B6", ("TEXTUAL",), "-",
               "Korean scholar of Indian/Buddhist philosophy (domestic academic tradition, not India-trained)"),
    "P-0055": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"), "studied",
               "Lay Buddhist-studies scholar; Delhi University MA/PhD; Korean lecturer at DU"),
    "P-0056": ("NONE", "EXCLUDE", "B6", ("PHYSICAL",), "studied",
               "Hindi professor/translator; not Buddhist"),
    "P-0057": ("NONE", "EXCLUDE", "B6", ("PHYSICAL",), "worked",
               "Korean-studies scholar; not Buddhist"),
    "P-0058": ("NONE", "EXCLUDE", "B6", ("PHYSICAL",), "studied",
               "Korean-language pedagogue; not Buddhist"),
    "P-0059": ("CONTEXTUAL", "CONTEXT", "B6", ("PHYSICAL",), "studied",
               "Korean-studies scholar; co-editor of partly-Buddhist India-Korea survey (context row)"),
    "P-0060": ("NONE", "EXCLUDE", "B6", ("TEXTUAL",), "-",
               "Korean-studies scholar; not Buddhist"),
    "P-0061": ("CONTEXTUAL", "CONTEXT", "B6", ("PHYSICAL",), "studied",
               "Korean studies; cultural-religious history, not Buddhist-specific (context row)"),
    "P-0062": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"), "worked",
               "Jogye monk; Bunhwangsa India abbot; BGICBS chancellor; Delhi University MOU 2026"),
    "P-0063": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"), "studied",
               "Jogye bhikkhuni; Pune MA + Delhi PhD"),
    "P-0064": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "TEXTUAL"), "studied",
               "Jogye bhikkhuni; Delhi University Buddhist studies (5+ years); temple-food master"),
    "P-0065": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"), "studied",
               "Jogye monk; Delhi University 1992-98; 4,500 km solo pilgrimage of Indian Buddhist sites"),
    "P-0066": ("NONE", "EXCLUDE", "B6", ("TEXTUAL",), "-",
               "Korean-poetry translator into Hindi; literary"),
    "P-0067": ("NONE", "EXCLUDE", "B5", ("PHYSICAL",), "visited",
               "Poet; 1986 Korea gathering; literary"),
    "P-0068": ("SECONDARY", "ADAPT", "B5", ("ENCOUNTER",), "-",
               "Documented meeting with Indian poet Sitanshu Yashaschandra at Dongguk University (literary exchange; compassion theme)"),
    "P-0069": ("NONE", "EXCLUDE", "B6", ("INDIRECT",), "-",
               "No India link found; non-Buddhist"),
    "P-0070": ("NONE", "EXCLUDE", "B5", ("INDIRECT",), "-",
               "No verifiable Gandhi/India influence; thought rooted in Donghak/Buddhism/Christianity (Hani 2026-07-03); popular Gandhi association unverified"),
    "P-0071": ("MEDIATOR", "ADAPT", "B5", ("ENCOUNTER",), "-",
               "Gandhian leader; documented Indian counterpart in Popchong's 1971 encounter"),
    "P-0072": ("PRIMARY", "KEEP", "B4", ("PHYSICAL", "TEXTUAL"), "planned",
               "First modern-era Korean Buddhist pilgrimage attempt (1925-27); died in Ceylon en route; travelogues 도석기/남국기/석란의 불교"),
    "P-0073": ("PRIMARY", "KEEP", "B5", ("PHYSICAL",), "visited",
               "Hwang Su-yŏng: Dongguk professor; 1962-63 field survey of Indian Buddhist sites following Hyecho's route; visited Nalanda"),
    "P-0074": ("MEDIATOR", "ADAPT", "B2", ("INDIRECT",), "-",
               "Muhak Chach'o: Jikong's disciple per tradition; T'aejo's royal preceptor; co-led the Nalanda-modeled Hoeamsa; no India travel"),
    "P-0075": ("SECONDARY", "ADAPT", "B2", ("INDIRECT",), "-",
               "Baegun Gyeonghan: Jikji author; received Jikong's inka per tradition; no India travel"),
    "P-0076": ("SECONDARY", "ADAPT", "B5", ("ENCOUNTER",), "-",
               "Sitanshu Yashaschandra: Indian poet; documented counterpart in Sŏ Chŏng-ju's Dongguk encounter"),
    "P-0077": ("SECONDARY", "ADAPT", "B2", ("INDIRECT",), "-",
               "Ch'ukwŏn Chijŏn: Jikong's disciple per tradition; National Preceptor Chŏngji (정지국사); no India travel"),
}

# ----------------------------------------------------------------------------
# PLACES  (place_id -> (relevance, scope, band, conns, rationale))
# ----------------------------------------------------------------------------
PLACE = {
    "PL-0001": ("PRIMARY", "KEEP", "B1", ("-",), "Silla: home kingdom of the core ancient monks"),
    "PL-0002": ("PRIMARY", "KEEP", "B1", ("-",), "Baekje: Marananta, Gyeomik, Baedalta"),
    "PL-0003": ("CONTEXTUAL", "CONTEXT", "B1", ("-",), "Recorded relevance is the Heo Hwang-ok legend (non-Buddhist; context row)"),
    "PL-0004": ("PRIMARY", "KEEP", "B1", ("-",), "Goguryeo: Hyonyu"),
    "PL-0005": ("PRIMARY", "KEEP", "B2", ("-",), "Goryeo: Iryon, Dhyanabhadra, Naong, Hoeamsa"),
    "PL-0006": ("NONE", "EXCLUDE", "B3", ("-",), "Recorded relevance is non-Buddhist (Yi Su-gwang, Ch'oe Han-gi, Yi Kyu-gyong)"),
    "PL-0007": ("CONTEXTUAL", "CONTEXT", "B1", ("LEGENDARY",), "Legendary origin site of Heo Hwang-ok (debated; context row)"),
    "PL-0008": ("PRIMARY", "KEEP", "B1", ("-",), "Hyecho itinerary; Buddhist heartland (Gandhara)"),
    "PL-0009": ("PRIMARY", "KEEP", "B1", ("-",), "Nalanda: Silla monks' destination; Dhyanabhadra ordination"),
    "PL-0010": ("PRIMARY", "KEEP", "B1", ("-",), "Bodh Gaya: enlightenment site; Hyeeop, Hyongak; Bunhwangsa India"),
    "PL-0011": ("PRIMARY", "KEEP", "B1", ("-",), "Hyecho itinerary (Kashmir)"),
    "PL-0012": ("PRIMARY", "KEEP", "B1", ("-",), "Sangana Great Vinaya Monastery: Gyeomik's 5-year study site"),
    "PL-0013": ("PRIMARY", "KEEP", "B6", ("-",), "Delhi: Delhi University Buddhist-studies hub (Wookwan, Gakseong, Hyoseok, U Myeong-ju)"),
    "PL-0014": ("SECONDARY", "ADAPT", "B6", ("-",), "Pune: Pune University (Hyoseok MA); study venue on a monk's route"),
    "PL-0015": ("MEDIATOR", "ADAPT", "B1", ("-",), "Chang'an: Woncheuk's Ximing Monastery; transit hub of Buddhist transmission"),
    "PL-0016": ("MEDIATOR", "ADAPT", "B1", ("-",), "Guangzhou: Hyecho's departure port"),
    "PL-0017": ("MEDIATOR", "ADAPT", "B2", ("-",), "Yuan Dadu: Dhyanabhadra's base; Naong meeting"),
    "PL-0018": ("MEDIATOR", "ADAPT", "B1", ("-",), "Kucha: Hyecho itinerary node"),
    "PL-0019": ("MEDIATOR", "ADAPT", "B1", ("-",), "Serindia/Western Regions: Marananta's probable origin; Hyecho route"),
    "PL-0020": ("MEDIATOR", "ADAPT", "B1", ("-",), "Nishapur: Hyecho route node (westernmost point)"),
    "PL-0021": ("MEDIATOR", "ADAPT", "B1", ("-",), "Tibet: Ojin's death site; Dhyanabhadra transit"),
    "PL-0022": ("PRIMARY", "KEEP", "B1", ("-",), "Sri Lanka: Hyonyu ordination; Theravada South Asia"),
    "PL-0023": ("CONTEXTUAL", "CONTEXT", "B4", ("-",), "Tokyo/Yokohama: Tagore literary meetings (context row)"),
    "PL-0024": ("PRIMARY", "KEEP", "B6", ("-",), "Seoul: modern Buddhist hub (Jogye HQ, Dongguk, Bongwonsa)"),
    "PL-0025": ("NONE", "EXCLUDE", "B5", ("-",), "Busan: 60 PFA arrival (military)"),
    "PL-0026": ("NONE", "EXCLUDE", "B5", ("-",), "Panmunjom/Imjingak: armistice site; military memorials"),
    "PL-0027": ("PRIMARY", "KEEP", "B6", ("-",), "New Delhi: Buddhist studies + IBC + GBS 2026 hub"),
    "PL-0028": ("NONE", "EXCLUDE", "B6", ("-",), "Meerut: Lee Jeong-ho PhD (Hindi literature)"),
    "PL-0029": ("PRIMARY", "KEEP", "B1", ("-",), "Gyeongju: Silla Buddhist capital; Yongjangsa (T'aehyon)"),
    "PL-0030": ("MEDIATOR", "ADAPT", "B1", ("-",), "Eastern Jin territory: Marananta's departure point"),
    "PL-0031": ("PRIMARY", "KEEP", "B1", ("-",), "Generic India: destinations of Yijing-recorded monks"),
    "PL-0032": ("PRIMARY", "KEEP", "B6", ("-",), "Sarnath: 2023 Sangwol pilgrimage endpoint; 2022 Jogye delegation; first sermon site"),
    "PL-0033": ("PRIMARY", "KEEP", "B6", ("-",), "Kushinagar: parinirvana site; 2023 Sangwol route; 2014 Jogye itinerary"),
    "PL-0034": ("PRIMARY", "KEEP", "B6", ("-",), "Lumbini: Buddha's birthplace; 2023 Sangwol route via Nepal; 2014 Jogye itinerary"),
    "PL-0035": ("PRIMARY", "KEEP", "B6", ("-",), "Vaishali: 2023 Sangwol route"),
    "PL-0036": ("PRIMARY", "KEEP", "B6", ("-",), "Shravasti: 2023 Sangwol pilgrimage endpoint"),
    "PL-0037": ("PRIMARY", "KEEP", "B6", ("-",), "Rajgir/Vulture Peak: 2023 Sangwol route; near Nalanda"),
    "PL-0038": ("PRIMARY", "KEEP", "B6", ("-",), "Kapilavastu: Buddha's childhood home; 2023 Sangwol route"),
    "PL-0039": ("PRIMARY", "KEEP", "B6", ("-",), "Dharamsala: 2026 KBPF pilgrimage destination (Tibetan Buddhist center)"),
}

# ----------------------------------------------------------------------------
# TRAVELS  (travel_id -> (relevance, scope, movement, rationale));
# band/conn derived by generator
# ----------------------------------------------------------------------------
TRAVEL = {
    "T-0001": ("PRIMARY", "KEEP", "visited", "Hyecho's Five Indias pilgrimage (c. 719/723-727)"),
    "T-0002": ("PRIMARY", "KEEP", "worked", "Marananta's 384 arrival in Baekje; founded Baekje Buddhism"),
    "T-0003": ("PRIMARY", "KEEP", "studied", "Gyeomik's sea pilgrimage 526-531 (Sangana, 5 yrs Sanskrit)"),
    "T-0004": ("PRIMARY", "KEEP", "worked", "Baedalta India -> Baekje by sea, 531"),
    "T-0005": ("PRIMARY", "KEEP", "studied", "Ariyabalma Silla -> Nalanda; died there"),
    "T-0006": ("PRIMARY", "KEEP", "visited", "Hyeeop Silla -> Bodh Gaya/Nalanda; died in India"),
    "T-0007": ("PRIMARY", "KEEP", "visited", "Hyont'ae Silla -> India -> Tang"),
    "T-0008": ("PRIMARY", "KEEP", "visited", "Hyongak Silla -> Bodh Gaya with Xuanzhao; died there"),
    "T-0009": ("PRIMARY", "KEEP", "visited", "Gubon Silla -> India"),
    "T-0010": ("PRIMARY", "KEEP", "visited", "Ojin Silla -> Tang -> Central India -> Tibet"),
    "T-0011": ("PRIMARY", "KEEP", "visited", "Wonpyo Silla -> Tang -> India -> Tang"),
    "T-0012": ("PRIMARY", "KEEP", "studied", "Hyonyu Goguryeo -> Sri Lanka; ordained there"),
    "T-0013": ("PRIMARY", "KEEP", "worked", "Dhyanabhadra Magadha -> Goryeo (1326); Hoeamsa founded 1328"),
    "T-0014": ("MEDIATOR", "ADAPT", "visited", "Tagore's Japan visits 1916-1929; mediator channel (Lamp of the East influence on Korean Buddhism)"),
    "T-0015": ("CONTEXTUAL", "CONTEXT", "visited", "Chin Hak-mun Korea -> Japan; literary meeting with Tagore (context row)"),
    "T-0016": ("SECONDARY", "ADAPT", "visited", "Ch'oe Nam-son Tokyo 1916 Tagore meeting; part of his Buddhist-history channel"),
    "T-0017": ("NONE", "EXCLUDE", "worked", "K.P.S. Menon UNTCOK mission 1947-48"),
    "T-0018": ("NONE", "EXCLUDE", "worked", "Thimayya NNRC chairmanship 1953-54"),
    "T-0019": ("NONE", "EXCLUDE", "worked", "Thorat ICF command 1953-54"),
    "T-0020": ("NONE", "EXCLUDE", "worked", "Chakravarty NNRC alternate chairmanship"),
    "T-0021": ("NONE", "EXCLUDE", "worked", "Rangaraj 60 PFA arrival Busan 1950"),
    "T-0022": ("NONE", "EXCLUDE", "worked", "Aga ambassadorship Seoul 1974-77"),
    "T-0023": ("NONE", "EXCLUDE", "worked", "Park Chan-hyun ambassadorship New Delhi 1974-76"),
    "T-0024": ("NONE", "EXCLUDE", "visited", "Kim Woo-choong business trip 1994"),
    "T-0025": ("SECONDARY", "ADAPT", "visited", "Ko Un's India travels (1990s; 2019 New Delhi); literary-academic"),
    "T-0026": ("PRIMARY", "KEEP", "visited", "Popchong 1971 pilgrimage (Sarnath/Bodh Gaya; Vinoba Bhave ashram)"),
    "T-0027": ("PRIMARY", "KEEP", "visited", "Lokesh Chandra Seoul 2016 (Lotus Sutra exhibition)"),
    "T-0028": ("PRIMARY", "KEEP", "studied", "U Myeong-ju Korea -> Delhi (MA/PhD Buddhist Studies; c. 2001)"),
    "T-0029": ("NONE", "EXCLUDE", "studied", "Lee Jeong-ho Hindi studies (CHI, JNU, Meerut)"),
    "T-0030": ("NONE", "EXCLUDE", "worked", "Pankaj Mohan AKS career"),
    "T-0031": ("NONE", "EXCLUDE", "studied", "Neerja Samajdar SNU PhD (Korean language)"),
    "T-0032": ("NONE", "EXCLUDE", "studied", "Vyjayanti Raghavan SNU MA (Korean history)"),
    "T-0033": ("PRIMARY", "KEEP", "worked", "Buddhavara Korea <-> Bodh Gaya residence; Bunhwangsa India; DU MOU 2026"),
    "T-0034": ("PRIMARY", "KEEP", "studied", "Hyoseok Pune MA -> Delhi PhD"),
    "T-0035": ("PRIMARY", "KEEP", "studied", "Wookwan Delhi University study (5+ years)"),
    "T-0036": ("PRIMARY", "KEEP", "studied", "Gakseong Delhi University 1992-98 + 4,500 km pilgrimage"),
    "T-0037": ("NONE", "EXCLUDE", "visited", "Dileep Jhaveri 1986 poetry gathering in Korea"),
    "T-0038": ("PRIMARY", "KEEP", "planned", "Yi Yŏng-jae Korea -> Ceylon 1925-27; intended India pilgrimage (first modern attempt)"),
    "T-0039": ("PRIMARY", "KEEP", "visited", "Hyeryun Silla -> India (Yijing enumeration)"),
    "T-0041": ("NONE", "EXCLUDE", "worked", "Kaushal Kumar Korea fellowships (Korean studies)"),
    "T-0042": ("PRIMARY", "KEEP", "visited", "Hwang Su-yŏng Seoul -> India 1962-63 (Hyecho-route survey; Nalanda visit)"),
}

# ----------------------------------------------------------------------------
# TEXTS  (text_id -> (relevance, scope, band, conns, rationale))
# ----------------------------------------------------------------------------
TEXT = {
    "TX-0001": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "Hyecho's travelogue; primary source on 8th-c. India"),
    "TX-0002": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "Wonhyo's commentaries on Indian-origin texts"),
    "TX-0003": ("PRIMARY", "KEEP", "B2", ("TEXTUAL",), "Iryon's compendium; primary record of early Buddhist traditions"),
    "TX-0004": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "Joseon world-geography encyclopedia; not Buddhist"),
    "TX-0005": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "India entries unverified; not Buddhist"),
    "TX-0006": ("NONE", "EXCLUDE", "B3", ("INDIRECT",), "Silhak world geography; not Buddhist"),
    "TX-0007": ("PRIMARY", "KEEP", "B4", ("TEXTUAL",), "First comprehensive Korean Buddhist history (Indian origins)"),
    "TX-0008": ("CONTEXTUAL", "CONTEXT", "B4", ("INDIRECT",), "Tagore poetry; literary source text (context row)"),
    "TX-0009": ("CONTEXTUAL", "CONTEXT", "B4", ("INDIRECT",), "Tagore poetry; literary (context row)"),
    "TX-0010": ("MEDIATOR", "ADAPT", "B4", ("INDIRECT",), "Tagore's 1929 message; explicitly invokes Korea's Buddhist heritage - mediator channel"),
    "TX-0011": ("CONTEXTUAL", "CONTEXT", "B4", ("INDIRECT",), "Tagore poem; literary (context row)"),
    "TX-0012": ("PRIMARY", "KEEP", "B4", ("INDIRECT",), "Korean Buddhist resistance poetry (Han Yong-un, a monk); Tagore-influenced"),
    "TX-0013": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "Tagore translation; literary (context row)"),
    "TX-0014": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "Tagore translation; literary (context row)"),
    "TX-0015": ("CONTEXTUAL", "CONTEXT", "B4", ("TEXTUAL",), "Tagore translation; literary (context row)"),
    "TX-0016": ("PRIMARY", "KEEP", "B4", ("TEXTUAL",), "Ch'oe Nam-son's Buddhist history (direct India/Xiyu origin thesis)"),
    "TX-0017": ("NONE", "EXCLUDE", "B4", ("-",), "Modern novel; not India-related"),
    "TX-0018": ("PRIMARY", "KEEP", "B5", ("TEXTUAL",), "Popchong's Buddhist essay collection (Gandhian opening)"),
    "TX-0019": ("PRIMARY", "KEEP", "B6", ("TEXTUAL",), "Wookwan's temple-food book (India-trained author)"),
    "TX-0020": ("PRIMARY", "KEEP", "B6", ("TEXTUAL",), "Lokesh Chandra's India-Korea interflow monograph (2019)"),
    "TX-0021": ("SECONDARY", "ADAPT", "B6", ("TEXTUAL",), "India-Korea historical/cultural survey; partly Buddhist chapters"),
    "TX-0022": ("NONE", "EXCLUDE", "B6", ("INDIRECT",), "Korean poetry in Hindi; literary"),
    "TX-0023": ("NONE", "EXCLUDE", "B6", ("INDIRECT",), "Korean poetry in Hindi; literary"),
    "TX-0024": ("NONE", "EXCLUDE", "B6", ("TEXTUAL",), "Hindi-Korean dictionary; linguistic"),
    "TX-0025": ("NONE", "EXCLUDE", "B6", ("TEXTUAL",), "Hindi novel translation (Tamas); literary"),
    "TX-0026": ("CONTEXTUAL", "CONTEXT", "B6", ("TEXTUAL",), "Gandhi biography in Korean; mediator figure, non-Buddhist (context row)"),
    "TX-0027": ("NONE", "EXCLUDE", "B5", ("TEXTUAL",), "ICF official history; military"),
    "TX-0028": ("PRIMARY", "KEEP", "B2", ("TEXTUAL",), "Samguk Sagi (1145) records Marananta's 384 arrival"),
    "TX-0029": ("PRIMARY", "KEEP", "B1", ("TEXTUAL",), "T'aehyon's Yogacara commentary"),
    "TX-0030": ("NONE", "EXCLUDE", "B4", ("TEXTUAL",), "Duplicate of TX-0016; drop in V3"),
}

# ----------------------------------------------------------------------------
# INSTITUTIONS  (institution_id -> (relevance, scope, band, conns, rationale))
# ----------------------------------------------------------------------------
INSTITUTION = {
    "I-0001": ("CONTEXTUAL", "CONTEXT", "B1", ("INSTITUTIONAL",), "Legendary state; Heo Hwang-ok narrative (context row)"),
    "I-0002": ("PRIMARY", "KEEP", "B1", ("INSTITUTIONAL",), "Nalanda Mahavihara: Silla monks' destination; Dhyanabhadra ordination"),
    "I-0003": ("PRIMARY", "KEEP", "B2", ("INSTITUTIONAL",), "Hoeamsa: founded by Indian master Dhyanabhadra (1328)"),
    "I-0004": ("CONTEXTUAL", "CONTEXT", "B4", ("INSTITUTIONAL",), "Tagore's university; literary-cultural (context row)"),
    "I-0005": ("NONE", "EXCLUDE", "B5", ("INSTITUTIONAL",), "Korean War repatriation commission"),
    "I-0006": ("NONE", "EXCLUDE", "B5", ("INSTITUTIONAL",), "Indian peacekeeping force"),
    "I-0007": ("NONE", "EXCLUDE", "B5", ("INSTITUTIONAL",), "Military medical unit"),
    "I-0008": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "JNU Korean studies centre (non-Buddhist)"),
    "I-0009": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "AKS Korean studies (non-Buddhist)"),
    "I-0010": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Dongguk: Korea's Buddhist university; Indian philosophy program"),
    "I-0011": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "HUFS Hindi department (non-Buddhist)"),
    "I-0012": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Delhi University: main Indian host of Korean Buddhist-studies students"),
    "I-0013": ("SECONDARY", "ADAPT", "B6", ("INSTITUTIONAL",), "Pune University: Hyoseok's anthropology MA; study venue on a monk's route"),
    "I-0014": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Bodh Gaya International College of Buddhist Studies (Korean-led; DU MOU 2026)"),
    "I-0015": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Bunhwangsa India: Korean Jogye temple at Bodh Gaya (groundbreaking 2020-03-28; dedication 2022-05)"),
    "I-0016": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Mahayeon temple-food centre (India-trained founder)"),
    "I-0017": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "Daewoo Group; economic"),
    "I-0018": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "Samsung Electronics India; economic"),
    "I-0019": ("NONE", "EXCLUDE", "B5", ("INSTITUTIONAL",), "Diplomatic mission"),
    "I-0020": ("PRIMARY", "KEEP", "B5", ("INSTITUTIONAL",), "Songgwangsa lineage (Popchong); relevance is B5 despite 1197 foundation"),
    "I-0021": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Bongnyeongsa bhikkhuni college (Hyoseok, Wookwan trained)"),
    "I-0022": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Jogye Order: host of 2023 Sangwol pilgrimage; Bunhwangsa India; 2022 official delegation"),
    "I-0023": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Sangwol Society: organizer of the 2023 1,167-km walking pilgrimage"),
    "I-0024": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Jungto Society: annual India pilgrimage program (36th 2027-01-14~30)"),
    "I-0025": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Yeoraesunwon: Korean-run temple at Bodh Gaya (founded ~2000-01; Wonman abbot; Dharma School)"),
    "I-0026": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "IBC: host of GBS 2023/2026, ICYBS 2025; Bexpo 2026 exchange"),
    "I-0027": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "KBPF (대한불교진흥원): organizer of 2026 India pilgrimage (Dharamsala/Ajanta-Ellora/Sanchi)"),
    "I-0028": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "BBS (불교방송): organizer of Seon Meditation Tour India-Nepal (Dec 2025-Jan 2026)"),
    "I-0029": ("NONE", "EXCLUDE", "B6", ("INSTITUTIONAL",), "Diplomatic mission (ROK Embassy in India); host venue of the 2023 50th-anniversary exchange"),
    "I-0030": ("PRIMARY", "KEEP", "B5", ("INSTITUTIONAL",), "국제불교문제연구소: dispatched the 1981-82 Korean Buddhist delegation to India (PM Gandhi meeting; Tripitaka donation at Nalanda)"),
    "I-0031": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",), "Nalanda University (est. 2014): Dongguk University MOU 2023-02-24; modern revival of the ancient Nalanda channel"),
}

# ----------------------------------------------------------------------------
# PERSON-PERSON  (relationship_id -> (relevance, scope, conns, rationale))
# ----------------------------------------------------------------------------
REL = {
    "R-0001": ("CONTEXTUAL", "CONTEXT", ("LEGENDARY",), "Legendary marriage of Heo Hwang-ok and King Suro (context row)"),
    "R-0002": ("PRIMARY", "KEEP", ("ENCOUNTER",), "Gyeomik-Baedalta in-person travel companionship (531)"),
    "R-0003": ("PRIMARY", "KEEP", ("ENCOUNTER",), "Dhyanabhadra-Naong teacher-student (precepts at 7; meeting at 38)"),
    "R-0004": ("CONTEXTUAL", "CONTEXT", ("ENCOUNTER",), "Tagore-Ch'oe Nam-son literary meeting (context row)"),
    "R-0005": ("CONTEXTUAL", "CONTEXT", ("ENCOUNTER",), "Tagore-Chin Hak-mun literary meeting (context row)"),
    "R-0006": ("CONTEXTUAL", "CONTEXT", ("TEXTUAL",), "Tagore-Kim Ok translation (context row)"),
    "R-0007": ("CONTEXTUAL", "CONTEXT", ("TEXTUAL",), "Tagore-Jeong Ji-yong translation (context row)"),
    "R-0008": ("CONTEXTUAL", "CONTEXT", ("TEXTUAL",), "Tagore-Chu Yo-han translation (context row)"),
    "R-0009": ("MEDIATOR", "ADAPT", ("INDIRECT",), "Tagore influence on Buddhist monk Han Yong-un (with critical distance)"),
    "R-0010": ("CONTEXTUAL", "CONTEXT", ("INDIRECT",), "Tagore-Yi Kwang-su literary reception (context row)"),
    "R-0011": ("CONTEXTUAL", "CONTEXT", ("INDIRECT",), "Gandhi-Ham Sok-hon (Quaker) (context row)"),
    "R-0012": ("MEDIATOR", "ADAPT", ("INDIRECT",), "Gandhi's words -> Popchong's Muso-yu (textual influence on a Buddhist monk)"),
    "R-0013": ("MEDIATOR", "ADAPT", ("ENCOUNTER",), "Popchong-Vinoba Bhave 1971 in-person meeting (Buddhist monk's documented Indian counterpart)"),
    "R-0014": ("NONE", "EXCLUDE", ("-",), "Nehru-Krishna Menon diplomacy"),
    "R-0015": ("NONE", "EXCLUDE", ("-",), "NNRC colleagues"),
    "R-0016": ("NONE", "EXCLUDE", ("-",), "NNRC colleagues"),
    "R-0017": ("NONE", "EXCLUDE", ("-",), "JNU CKS colleagues"),
    "R-0018": ("PRIMARY", "KEEP", ("TEXTUAL",), "Iryon documented Marananta (Samguk Yusa)"),
    "R-0019": ("MEDIATOR", "ADAPT", ("INDIRECT",), "Jikong-Muhak teacher-student per tradition (Jahyeon 2017); lineage carried into Joseon"),
    "R-0020": ("SECONDARY", "ADAPT", ("INDIRECT",), "Jikong-Baegun inka per tradition (Jahyeon 2017)"),
    "R-0021": ("SECONDARY", "ADAPT", ("ENCOUNTER",), "Sŏ Chŏng-ju-Yashaschandra meeting at Dongguk (literary)"),
    "R-0022": ("SECONDARY", "ADAPT", ("INDIRECT",), "Jikong-Ch'ukwŏn teacher-student per tradition (Jahyeon 2017; Hyunbul 2017; Atlas 2025)"),
}

# ----------------------------------------------------------------------------
# PERSON-PLACE  (link_id -> (relevance, scope, rationale));
# conn/movement derived by generator from link type
# ----------------------------------------------------------------------------
PPL = {
    "L-0001": ("PRIMARY", "KEEP", "Hyecho born in Silla"),
    "L-0002": ("PRIMARY", "KEEP", "Hyecho departed Guangzhou by sea"),
    "L-0003": ("PRIMARY", "KEEP", "Hyecho's travelogue ends at Kucha"),
    "L-0004": ("PRIMARY", "KEEP", "Woncheuk at Ximing Monastery, Chang'an"),
    "L-0005": ("PRIMARY", "KEEP", "Wonhyo born in Silla"),
    "L-0006": ("PRIMARY", "KEEP", "Marananta arrival in Baekje (384)"),
    "L-0007": ("CONTEXTUAL", "CONTEXT", "Heo Hwang-ok legendary origin (Ayuta/Ayodhya) (context row)"),
    "L-0008": ("CONTEXTUAL", "CONTEXT", "Heo Hwang-ok legendary residence in Gaya (context row)"),
    "L-0009": ("CONTEXTUAL", "CONTEXT", "Suro legendary residence (context row)"),
    "L-0010": ("PRIMARY", "KEEP", "Gyeomik studied at Sangana monastery"),
    "L-0011": ("PRIMARY", "KEEP", "Ariyabalma at Nalanda"),
    "L-0012": ("PRIMARY", "KEEP", "Dhyanabhadra ordained at Nalanda"),
    "L-0013": ("PRIMARY", "KEEP", "Dhyanabhadra in Goryeo; founded Hoeamsa"),
    "L-0014": ("NONE", "EXCLUDE", "Yi Su-gwang Joseon residence"),
    "L-0015": ("CONTEXTUAL", "CONTEXT", "Tagore Japan visits (context row)"),
    "L-0016": ("CONTEXTUAL", "CONTEXT", "Tagore Seoul (planned 1929, never visited) (context row)"),
    "L-0017": ("NONE", "EXCLUDE", "K.P.S. Menon UNTCOK sessions"),
    "L-0018": ("NONE", "EXCLUDE", "Thimayya NNRC chairmanship"),
    "L-0019": ("NONE", "EXCLUDE", "Thorat ICF command"),
    "L-0020": ("NONE", "EXCLUDE", "Rangaraj arrival at Busan"),
    "L-0021": ("NONE", "EXCLUDE", "Aga ambassadorship in Seoul"),
    "L-0022": ("NONE", "EXCLUDE", "Park Chan-hyun ambassadorship in New Delhi"),
    "L-0023": ("NONE", "EXCLUDE", "Kim Woo-choong Racer launch visit"),
    "L-0024": ("PRIMARY", "KEEP", "Popchong 1971 India visit (Vinoba Bhave ashram)"),
    "L-0025": ("PRIMARY", "KEEP", "Lokesh Chandra Seoul 2016 (Lotus Sutra exhibition)"),
    "L-0026": ("PRIMARY", "KEEP", "U Myeong-ju Delhi University study"),
    "L-0027": ("NONE", "EXCLUDE", "Pankaj Mohan AKS professorship"),
    "L-0028": ("NONE", "EXCLUDE", "Neerja Samajdar SNU PhD"),
    "L-0029": ("NONE", "EXCLUDE", "Vyjayanti Raghavan SNU MA"),
    "L-0030": ("PRIMARY", "KEEP", "Buddhavara at Bodh Gaya (Bunhwangsa India)"),
    "L-0031": ("PRIMARY", "KEEP", "Hyoseok at Pune University"),
    "L-0032": ("PRIMARY", "KEEP", "Wookwan at Delhi University"),
    "L-0033": ("PRIMARY", "KEEP", "Gakseong at Delhi University 1992-98"),
    "L-0034": ("CONTEXTUAL", "CONTEXT", "Tagore born in Calcutta (context row)"),
    "L-0035": ("PRIMARY", "KEEP", "Hwang Su-yŏng visited Nalanda (1962-63 survey)"),
}

# ----------------------------------------------------------------------------
# PERSON-TEXT  (link_id -> (relevance, scope, rationale)); conn derived by generator
# ----------------------------------------------------------------------------
PTX = {
    "L-0101": ("PRIMARY", "KEEP", "Hyecho author of Wang ocheonchukguk jeon"),
    "L-0102": ("PRIMARY", "KEEP", "Wonhyo author of Haedong-so commentaries"),
    "L-0103": ("PRIMARY", "KEEP", "Iryon author of Samguk Yusa"),
    "L-0104": ("NONE", "EXCLUDE", "Yi Su-gwang author (Jibong yuseol)"),
    "L-0105": ("NONE", "EXCLUDE", "Yi Kyu-gyong author (Oju)"),
    "L-0106": ("NONE", "EXCLUDE", "Ch'oe Han-gi author (Jiguyon'gu)"),
    "L-0107": ("PRIMARY", "KEEP", "Yi Nung-hwa author (Buddhist history)"),
    "L-0108": ("CONTEXTUAL", "CONTEXT", "Tagore author (Gitanjali) (context row)"),
    "L-0109": ("CONTEXTUAL", "CONTEXT", "Tagore author (The Gardener) (context row)"),
    "L-0110": ("MEDIATOR", "ADAPT", "Tagore author (Lamp of the East message) - mediator channel"),
    "L-0111": ("CONTEXTUAL", "CONTEXT", "Tagore author (Song of the Defeated) (context row)"),
    "L-0112": ("PRIMARY", "KEEP", "Han Yong-un author (Buddhist resistance poetry)"),
    "L-0113": ("CONTEXTUAL", "CONTEXT", "Kim Ok translator (Gitanjali) (context row)"),
    "L-0114": ("CONTEXTUAL", "CONTEXT", "Jeong Ji-yong translator (Hwimun poems) (context row)"),
    "L-0115": ("CONTEXTUAL", "CONTEXT", "Chu Yo-han translator (4-line message) (context row)"),
    "L-0116": ("PRIMARY", "KEEP", "Ch'oe Nam-son author (Choson Pulgyo 1930)"),
    "L-0117": ("NONE", "EXCLUDE", "Yi Kwang-su author (Mujong)"),
    "L-0118": ("PRIMARY", "KEEP", "Popchong author (Muso-yu)"),
    "L-0119": ("PRIMARY", "KEEP", "Wookwan author (temple food)"),
    "L-0120": ("PRIMARY", "KEEP", "Lokesh Chandra author (Morning Calm)"),
    "L-0121": ("SECONDARY", "ADAPT", "Vyjayanti co-editor (India-Korea survey)"),
    "L-0122": ("NONE", "EXCLUDE", "Divik Ramesh translator (Korean poetry)"),
    "L-0123": ("NONE", "EXCLUDE", "Divik Ramesh translator (Korean poetry)"),
    "L-0124": ("NONE", "EXCLUDE", "Lee Jeong-ho author (Hindi-Korean dictionary)"),
    "L-0125": ("NONE", "EXCLUDE", "Lee Jeong-ho translator (Tamas)"),
    "L-0126": ("NONE", "EXCLUDE", "Lee Jeong-ho author (Gandhi biography)"),
    "L-0127": ("PRIMARY", "KEEP", "Marananta subject of Samguk Sagi"),
    "L-0128": ("CONTEXTUAL", "CONTEXT", "Heo Hwang-ok subject of Samguk Yusa (context row)"),
    "L-0129": ("CONTEXTUAL", "CONTEXT", "Suro subject of Samguk Yusa (context row)"),
    "L-0130": ("PRIMARY", "KEEP", "Marananta subject of Samguk Yusa"),
    "L-0131": ("PRIMARY", "KEEP", "T'aehyon author (Seong yusik non hakki)"),
    "L-0132": ("CONTEXTUAL", "CONTEXT", "Tagore subject (Song of the Defeated) (context row)"),
}

# ----------------------------------------------------------------------------
# EVENTS  (event_id -> (relevance, scope, band, conns, rationale));
# all v0.2 seed events are B6 contemporary India-Korea developments
# ----------------------------------------------------------------------------
EVENT = {
    "EV-0001": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "Jogye/Sangwol 1,167-km walking pilgrimage India-Nepal 2023 (PIB-documented)"),
    "EV-0002": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Bexpo 2026 IBC-Jogye lay exchange, Seoul (Buddha statue gift)"),
    "EV-0003": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "2nd Global Buddhist Summit 2026 New Delhi; Jogye participation confirmed (Munjong as representative, Jinwoo's message read)"),
    "EV-0004": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "Jungto annual India pilgrimage program (36th: 2027-01-14~30)"),
    "EV-0005": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Delhi University - BGICBS academic MOU 2026-04-23"),
    "EV-0006": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "Jogye delegation Sarnath -> Bodh Gaya, May 2022"),
    "EV-0007": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "2014 Jogye pilgrimage to 8 great sites + Nepal incl. Yeoraesunwon"),
    "EV-0008": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Bunhwangsa India groundbreaking 2020-03-28 (Jogye's first India temple)"),
    "EV-0009": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Bunhwangsa India dedication 2022-05 (150-person Jogye delegation, Wonhaeng)"),
    "EV-0010": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Global Buddhist Summit 2023 (20-21 Apr, Ashok Hotel); Jogye participation confirmed (Jeongbeom as representative)"),
    "EV-0011": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "ICYBS 2025 Delhi; Korean participation not documented"),
    "EV-0012": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "KBPF 2026 India pilgrimage (3-11 Oct, Dharamsala/Ajanta-Ellora/Sanchi)"),
    "EV-0013": ("PRIMARY", "KEEP", "B6", ("PHYSICAL", "INSTITUTIONAL"),
                "BBS Seon Meditation Tour 4 India-Nepal (26 Dec 2025 - 4 Jan 2026)"),
    "EV-0014": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Korea-India 50th anniversary cultural exchange 2023 (Jogye + ROK Embassy; NGMA exhibition)"),
    "EV-0015": ("PRIMARY", "KEEP", "B5", ("PHYSICAL", "INSTITUTIONAL"),
                "1981-82 Korean Buddhist delegation to India (국제불교문제연구소; PM Gandhi meeting; Tripitaka donation at Nalanda)"),
    "EV-0016": ("PRIMARY", "KEEP", "B6", ("INSTITUTIONAL",),
                "Dongguk University - Nalanda University MOU 2023-02-24"),
    "EV-0017": ("PRIMARY", "KEEP", "B2", ("PHYSICAL", "INSTITUTIONAL"),
                "1370 relic stupa for Dhyānabhadra at Hoeamsa (Kongmin's order; Naong supervised)"),
    "EV-0018": ("PRIMARY", "KEEP", "B6", ("PHYSICAL",),
                "2024 return of Jikong/Naong + Buddha relics (India provenance) to Hoeamsa from Boston MFA"),
    "EV-0019": ("PRIMARY", "KEEP", "B6", ("TEXTUAL", "INSTITUTIONAL"),
                "World-first public display of the BnF Wang ocheonchukguk jeon manuscript at NMK (2010-11); second loan 2019-20"),
}

# ----------------------------------------------------------------------------
# PERSON-EVENT  (link -> (relevance, scope, band, conns, movement, rationale));
# derived by the generator from the linked event unless overridden here
# ----------------------------------------------------------------------------
PERSON_EVENT = {}