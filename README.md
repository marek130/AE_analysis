# Praktická časť k diplomovej práci: Aplikácia techník umelej inteligencie pri analýze akustických emisií mechanicky namáhaných materiálov
 
 Repozitár obsahuje 7 súborov:
 * init.py
 * clustering.py
 * constants.py
 * matrix\_shape_mscpyr
 * README.md
 * MATRICA_MSCpyr
 * VLAKNA_KV13
 
# Všetky skripty boli testované na stroji s:
* Debian 10
* python 3.7
* NVIDIA GPU
* minimálne 32 GB RAM

# **Požiadavky**: 
- knižnica numpy
- knižnica cupy
- knižnica matplotlib
- knižnica pytubes (https://github.com/stestagg/pytubes)
- knižnica joblib

# Popisy jednotlivých súborov
 ---
## Skripty na transformáciu pravidiel do grafovych modelov
### `INIT.PY`
- skript na analyzu mechanických testov
- skript berie ako argument cestu k súboru so signálom
- výsledkom je kumulatívny graf
- názov súboru reprezentujúci frekvenčný tvar matrice sa dá upraviť prepísaním konštanty **matrix_shape** v súbore constants.py

### `CLUSTERING.PY`
- skript na získanie frekvenčnej stopy zo signálu
- skript berie 1 argument a to cestu k súboru so signálom
- výsledkom sú súbory reprezentujúce frekvečné stopy a obrázky na zobrazenie frekvečnej stopy
- počet klastrových skupín sa dá upraviť prepísaním konštanty **number_of_clusters** v súbore constants.py



### `CONSTANTS.PY`
- súbor predstavujúci definovanie konštánt pre analýzu a klastrovanie

### `matrix_shape_mscpyr`
- zovšeobecnený frekvečný tvar pre MSCpyr matricu
 
