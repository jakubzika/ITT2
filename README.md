# ITT2

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
V následující tabulce *n* značí počet objektů se kterými pracujeme.

| controller # | hodnota | význam | reakce zvuku |
| ------------ | ------- | ------ | ------------ |
| 1            | 0-255   | poměr města v přírodě (255 je nejvíc)  | zkreslení, zošklivení přírodní stopy
| 2 až (2+*n*) | 0 / 255 | prezence objektu | coming soon, možné konkretizovat na jednotlivé objekty |