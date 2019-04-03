O zadatku:
    - Cilj zadatka je pravljenje genetskog algoritma koji minimizuje vrednost zadate funkcije.
    - Uslovi:
        - Tip genetskog algoritma: Binarni
        - Uksrtanje: Dvotackasto
        - Mutacija: Tackasta
        - Funckija: Goldstajn-Prajsova
            - Domen promenljivih x i y: [-2, 2]
            - Fmin(x, y) = 3.0, x = 0.0, y = -1.0

O resenju
    - Resenje je implementirano u programskom jeziku Python, verzija 3.7.0, 64-bit
    - Koriscene biblioteke:
        - Ugradjene: json, random, sys
        - Eksterne: numpy, matplotlib
    - Konfigurisanje:
        - Konfiguracija se cuva u JSON fajlu "konf.json"
        - Parametri:
            - min_xy     - donja granica domena
            - max_xy     - gornja granica domena
            - min_x      - vrednost x-a za Fmin
            - min_y      - vrednost y-a za Fmin
            - min_f      - Fmin - minimum funkcije
            - evolucija  - broj evolucija za svaku populaciju
            - populacija - broj jedinki u populaciji
            - iteracija  - broj iteracija genetskog algoritma sa parametrima iznad
                           i novom populacijom u svakoj iteraciji
            - mutacija   - ucestalost mutacija - opseg [0,1)
    - Pokretanje:
        - Instalirati verziju Python-a navedenu iznad
        - Instalirati potrebne biblioteke navedene iznad
        - Smestiti fajlove "bga.py" i "konf.json" u isti direktorijum
        - Otvoriti terminal, doci do foldera u kojem se nalaze ova 2 fajla
        - Pokrenuti program komandom "python bga.py"
