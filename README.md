# Praktická časť k diplomovej práci: Aplikácia techník umelej inteligencie pri analýze akustických emisií mechanicky namáhaných materiálov
 
 Repozitár obsahuje 6 súborov:
 * init.py
 * clustering.py
 * constants.py
 * matrix\_shape_mscpyr
 * README.md
 * frekvecne_udalosti_MATRICA_MSCpyr_a_VLAKNA_KV13
 
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
- knižnica sklearn

# Popisy jednotlivých súborov
 ---
### `INIT.PY`
- skript na analýzu mechanických testov
- skript berie ako argument cestu k súboru s dátami
- výsledkom je kumulatívny graf
- názov súboru reprezentujúci frekvenčný tvar matrice sa dá upraviť prepísaním konštanty **matrix_shape** v súbore constants.py
- príklad spustenia: ```python3.7 init.py data_mscpyr.dat```

### `CLUSTERING.PY`
- skript na získanie frekvenčnej stopy zo signálu
- skript berie 1 argument a to cestu k súboru s dátami
- výsledkom sú súbory reprezentujúce frekvečné stopy a obrázky na zobrazenie frekvečnej stopy
- počet klastrových skupín sa dá upraviť prepísaním konštanty **number_of_clusters** v súbore constants.py
- príklad spustenia: ```python3.7 clustering.py data_mscpyr.dat```

### `CONSTANTS.PY`
- súbor predstavujúci definovanie konštánt pre analýzu a klastrovanie

### `matrix_shape_mscpyr`
- zovšeobecnený frekvečný tvar pre MSCpyr matricu

### frekvecne_udalosti_MATRICA_MSCpyr_a_VLAKNA_KV13
- složka obsahujúca obrázky udalostí, ktoré skript označil ako udalosť prasknutia matrice alebo prasknutie vlákna
- udalostí sú zobrazené vo frekvečnej doméne
- jedná sa o ukážku udalostí z ťahového testu pre materiál MSCpyr s vláknami KV13
 
