# To-Do List: Úpravy konferenčního článku (Camera Ready)

## 1. Gramatika, terminologie a celní úpravy textu
- [x] **Linear amplifiers vs. Voltage amplifiers:** V  sekci o zpětné vazbě a stabilitě explicitně zmínit, že problémy se týkají primárně "Voltage amplifiers" s napěťovou zpětnou vazbou. Zvážit úpravu "Stability Issues with Capacitive Loads" aby nevyznívala tak, že *každý* lineární zesilovač (např. generátor proudu) má tento problém. 
- [ ] **Srovnání Class AB a Class D:** Učinit srovnání férovějším. Zdůraznit, že Class D design obětuje typické vlastnosti "univerzálního zesilovače" se zpětnou vazbou (jako PSRR, nazávislost na výstupní zátěži) za extrémní účinnost, a že pro specifické (prediktivní, periodické) úlohy je to výhodný trade-off. Práce je primárně "Proof of concept", že to jde budit efektivně.
- [x] **Zmínit PSRR (Power Supply Rejection Ratio):** Jasně uvést, že u navrženého Class D bez zpětné vazby je PSRR v podstatě 0 dB a řízení plně spoléhá na stabilní napájení a filtrační kapacitu.
- [x] **"Microscopic gap" u popisu dead-time:** Anglicky se pro mrtvý čas spíše nehodí spojení s prostorovým "microscopic". Přepsat spíše na "extremely short", "nanosecond-scale", apod.
- [ ] **Úvaha o náboji vs. napětí:** (Volitelně pro diskusi / závěr) Lze zmínit, že výchylka (displacement) pieza je z fyzikálního hlediska úměrná spíše dodanému *náboji* než napětí, a že napřímo PWMkovaný charge-source by k řízení polohy byl teoreticky lineárnější (jak poznamenal Michal), i když k dynamickému aktuátoru je napěťové buzení (Class D) praktičtější z hlediska účinnosti řízení výkonu.

## 2. LaTeX Formátování a oprava kompilace
- [x] **Opravit `references.bib`:** Ručně zkrátit a vyčistit URLs u citací `navitas_nv6247c` a `LC_filter_design` (odstranit dlouhé zakódované znaky typu `%20`), protože to shazuje LaTeX kompilátor (`! File ended while scanning use of \url`).
- [ ] **Odkomentovat zbývající obrázky a tabulky:** 
   - [ ] Odkomentovat `schematic_linear.png`.
   - [ ] Odkomentovat `schematic_gan.pdf` a přidat odkazy do textu (pro objasnění obou topologií - Michal chtěl vidět schéma topologie).
   - [ ] Odkomentovat srovnávací tabulku (Table 2 - "Comparative Parameters").
   - [ ] Přidat nebo zkontrolovat tagy v textu (`Fig. \ref{...}`, `Table \ref{...}`).
- [ ] **Odkomentovat kód / rovnice:** Odkomentovat rovnici pro výpočet timeru `CMP(n) = ...`.
- [ ] **Smazat pracovní poznámky / TODO z LaTeX kódu:** (např. `% Placeholder pro vlozeny graf z Pythonu`).
