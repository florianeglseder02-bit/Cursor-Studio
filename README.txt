CURSOR STUDIO – WINDOWS
=======================

Was enthalten ist
- 40 Cursor-Designs aus den zwei bereitgestellten Bildsammlungen
- Vorschau und Größenregler (32 bis 128 Pixel)
- Übernimmt das ausgewählte Design als Windows-Standardpfeil
- Schaltfläche zum Wiederherstellen der Windows-Standardcursor

SOFORT STARTEN (mit Python)
1. Python 3.10 oder neuer installieren.
2. Im Ordner eine Eingabeaufforderung öffnen.
3. Ausführen: py -m pip install -r requirements.txt
4. Ausführen: py cursor_studio.py

EIGENE EXE ERSTELLEN
1. Python 3.10 oder neuer auf Windows installieren.
2. build_windows.bat doppelklicken.
3. Die fertige Anwendung liegt in dist\CursorStudio\CursorStudio.exe.
   Den ganzen Ordner dist\CursorStudio weitergeben, nicht nur die EXE.

HINWEISE
- Das Ändern des System-Cursors funktioniert nur unter Windows.
- Die Anwendung verändert den Windows-Standardpfeil systemweit.
- Mit „Windows-Standard wiederherstellen“ kann der Originalzustand geladen werden.
- Windows kann beim Anwenden je nach Systemeinstellung eine Sicherheitsabfrage anzeigen.
- Die App wird hier als Quellpaket geliefert; eine fertige Windows-EXE kann in dieser
  Linux-Buildumgebung nicht zuverlässig erstellt werden. Die BAT-Datei baut sie auf Windows.
