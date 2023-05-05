# ITT2

## Jak reaguje zvuk na změny?
Na začátku je ticho.
S přidáváním přírodních věcí se zesilují přírodní zvuky. Každý předmět má vlastní stopu, jejíž intenzita zvuku se zvýší když se objeví na scéně.

S přibýváním civilizace (zakrytí IoT senzoru) 
se kromě zvýšení stopy daného předmětu se sníží intenzita zvuku mixu přírodních stop, aby byla civilizace ještě více slyšet.


## Jak přichystat na výstavu
### Programové vybavení potřebné pro spuštění (varianta Windows)
Windows 10
Ableton Live 11 s Max for Live
python 3.10, závislosti řešené přes poetry
ovladač LoopBe1

### Spuštění (Windows)
Je nutné nainstalovat ovladač LoopBe1, který nám umožní posílat MIDI z pythonu na nové MIDI virtuální zařízení.
Lze jej stáhnout zde, pro nekomerční použití je zdarma:
https://www.nerds.de/en/download.html
Po instalaci ovladač rovnou funguje, není zapotřebí nic zapínat.

## Popis realizace

### Princip propojení
**Poznámka pro Kubu: příklad práce s rtmidi je v souboru matej/hello_rtmidi.py**

Zpracování obrazových dat je řešené v pythonu. 
Pro přenos dat z obrazové části (python) do zvukové části (Ableton) je využíváno pro jednoduchost MIDI.
Je k tomu využita knihovna `rtmidi` v pythonu. Ta ale posílá MIDI na output Microsoft GS Wavetable Synth.
My ale potřebujeme do Abletonu input, proto je zapotřebí udělat smyčku, která nám zmíněný výstup pošle na nový vstup a tváří se jako běžné MIDI zařízení. 
To řeší ovladač *LoopBe1*, který vytvoří MIDI output a input, které jsou propojené. 

### Pravidla komunikace obraz-zvuk (protokol nad MIDI)
V této sekci bude popsán význam MIDI hodnot posílaných z obrazové do zvukové části.
Využit je zatím pouze command `0xB0`, tj. *Continuous controller* (to jsou například potenciometry na midi controllerech). Tam je určeno číslo controlleru a hodnota 0-255.

*Pozn.: prozatím jsou čísla controllerů nahodilá a mohou být brzy změněna pro praxi.*
V následující tabulce *n* značí počet kamerových objektů 
se kterými pracujeme (v kódu `CAMERA_OBJECT_COUNT`), 
*m* počet sensorových objektů (Liza, v kódu `SENSOR_OBJECT_COUNT`)


V tuto chvíli n = 11 a m = 6
1 (city vs. nature) zatím pouze rezervováno pro jistotu, ale není řízeno MIDI, nyní je to dané kumulativní vzdáleností od senzorů.

| controller #           | hodnota | význam                                         | reakce zvuku                                                                     |
| ---------------------- | ------- | ---------------------------------------------- | -------------------------------------------------------------------------------- |
| 1                      | 0-127   | poměr města v přírodě (255 je nejvíc)          | zkreslení, zošklivení přírodní stopy                                             |
| 2 až (*n*+1)           | 0-127   | intenzita kamerového objektu (vzd. od středu?) | zesílení zvuku daného objektu, 0 znamená nejtišší                                |
| (*n*+2) až (*n*+*m*+1) | 0-100   | vzdálenost ruky od senzorového objektu         | zesílení zvuku daného objektu (0 nejhlasitější) a ztišení celkové přírodní stopy |

### Mapování MIDI hodnot v Abletonu
Bohužel, Ableton neumožňuje uložit "MIDI mapování" a přenášet jej mezi projekty, proto je zapotřebí v novém projektu provést mapování znova.
K tomu slouží skript `matej/controller_mapping.py`.
Pozor na správné nastavení konstant v něm, je možné je předat jako parametry (`--help` u skriptu).

Postup:
1. Nastartovat Ableton Live, otevřít projekt který chceme namapovat.
2. Zmáčknout Ctrl+M a přepnout se do režimu mapování 
3. Spustit skript `matej/controller_mapping.py` (případně `--help` u skriptu).
4. Skript bude uživatele instruovat, který objekt / funkcionalita / parametr... bude mapován jako následující.
5. Uživatel jej zaklikne v Abletonu, vrátí se do skriptu a zmáčkne Enter
6. Pokud si to program přeje, vrátit se na bod 4.
7. Na konci nezapomenout vypnout mapovací mód před **POSLEDNÍM ENTEREM** (program instruuje)
