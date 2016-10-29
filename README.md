# xStream für Kodi - README & FAQ

[![Join the chat at https://gitter.im/xStream-Kodi/plugin.video.xstream](https://badges.gitter.im/xStream-Kodi/plugin.video.xstream.svg)](https://gitter.im/xStream-Kodi/plugin.video.xstream?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

![xStream logo](https://github.com/StoneOffStones/plugin.video.xstream/blob/wiki/graphics/website/logo/logo_512.png?raw=true)


[![Join the chat at https://gitter.im/StoneOffStones/plugin.video.xstream](https://badges.gitter.im/StoneOffStones/plugin.video.xstream.svg)](https://gitter.im/StoneOffStones/plugin.video.xstream?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)



## Inhaltsverzeichnis
- [1. Allgemeines zum Addon](#1-allgemeines-zum-addon)
    - [1.1 Verfügbare Webseiten](#11-verfügbare-webseiten)
    - [1.2 Rechtliche Konsequenzen bei Nutzung](#12-rechtliche-konsequenzen-bei-nutzung)
   
   
- [2. Installation und Konfiguration](#2-installation-und-konfiguration)
    - [2.1 Bezugsquellen zur Installation](#21-bezugsquellen-zur-installation)
    - [2.2 Allgemeine Einstellungen](#22-allgemeine-einstellungen)
    - [2.3 Webseiten Aktivieren und Deaktivieren](#23-webseiten-aktivieren-und-deaktivieren)
    - [2.4 Manuelle und automatische Hosterwahl](#24-manuelle-und-automatische-hosterwahl)
    - [2.5 Funktion des Metahandlers](#25-funktion-des-metahandlers)
 
 
- [3. Bekannte Probleme](#3-bekannte-probleme)
    - [3.1 Fehler bei der Installation](#31-fehler-bei-der-installation)
    - [3.2 Fehler bei Verwendung der Globalen Suche](#32-fehler-bei-verwendung-der-globalen-suche)
    - [3.3 Fehler bei Verwendung einzelner Webseiten](#33-fehler-bei-verwendung-einzelner-webseiten)
    - [3.4 Fehler bei Verwendung einiger Hoster](#34-fehler-bei-verwendung-einiger-hoster)
  
  
- [4. Fehlerbericht über Log-Datei](#4-fehlerbericht-über-log-datei)
    - [4.1 Allgemeines zur Log-Datei](#41-allgemeines-zur-log-datei)
    - [4.2 Erstellen, bearbeiten und hochladen der Log-Datei](#43-erstellen-bearbeiten-und-hochladen-der-log-datei)
    - [4.3 Speicherort der Log Datei](#42-speicherort-der-log-datei)

    
- [5. Phyton Dateien](#5-phyton-dateien)
    - [5.1 Allgemeines zur .py-Datei](#51-allgemeines-zur-py-datei)
    - [5.2 Bearbeiten einer .py-Datei](#52-bearbeiten-einer-py-datei)
    - [5.3 Speicherort der einzelnen Webseiten](#53-speicherort-der-einzelnen-webseiten)



## 1. Allgemeines zum Addon

xStream ist ein Video Addon für die Media-Center-Software Kodi.
Mit xStream ist es möglich Serien und Filme unterschiedlichster Streaming-Plattformen über eine simple und optisch ansprechende Benutzeroberfläche zu sehen.


### 1.1 Verfügbare Webseiten

| Name           | Domain            | Status                 | Stand      |
|:-------------- |:----------------- | :--------------------- | :--------- |
| AnimeLoads     | anime-loads.org   | funktioniert           | 09.04.2016 |
| BurningSeries  | bs.to             | funktioniert           | 09.04.2016 |
| Cine           | cine.to           | funktioniert           | 25.05.2016 |
| CineDream      | cine-dream.net    | funktioniert           | 21.06.2016 |
| Cineplex       | cineplex.tv       | funktioniert           | 29.07.2016 |
| Die Filme      | diefilme.net      | funktioniert           | 25.05.2016 |
| DirectDownLoad | ddl.me            | funktioniert           | 09.04.2016 |
| FilmPalast     | filmpalast.to     | funktioniert           | 09.04.2016 |
| FilmeStreamz   | filme-streamz.com | funktioniert           | 29.07.2016 |
| Goldstream     | goldstream.org    | funktioniert           | 23.06.2016 |
| Gute Filme     | gute-filme.to     | funktioniert           | 09.04.2016 |
| HDfilme        | hdfilme.tv        | funktioniert           | 09.04.2016 |
| KinoX          | kinox.to          | funktioniert           | 09.04.2016 |
| KinoKiste      | kkiste.to         | funktioniert teilweise | 09.04.2016 |
| Movie4k        | movie4k.to        | funktioniert           | 09.04.2016 |
| MoviesEver     | moviesever.com    | funktioniert teilweise | 09.04.2016 |
| SeriesEver     | seriesever.net    | funktioniert           | 09.04.2016 |
| StreamTausch   | streamtausch.tv   | funktioniert           | 29.07.2016 |
| SzeneStreams   | szene-streams.com | funktioniert           | 09.04.2016 |


Empfehlungen und Vorschläge für neue Seiten können über das [Forum](http://xstream-addon.square7.ch) unter dem Bereich [Wünsche und Anregungen](http://xstream-addon.square7.ch/forumdisplay.php?fid=9) angefragt bzw. eingestellt werden. Die Intergration der gewünschten Seiten ist nicht selbsverständlich und erfolgt nicht automatisch!
Alle Vorschläge werden in der [Site-Plugin Wunschliste](https://docs.google.com/spreadsheets/d/1b_9C6BONlpWcugMgocFbKxe7nFp99HfvVUJznxTzT4I/edit?usp=sharing) ([Forumbeitrag](http://xstream-addon.square7.ch/showthread.php?tid=663)) gesammelt und auf ihren tatsächlichen Mehrwert untersucht. Daraufhin folgt bei den interessanten Content-Anbieter eine Priorisierung bzw. Entwicklung eines neuen Site-Plugins für xStream.
Grundsätzlich ist jedoch zu betonen, dass stätig an der Weiterentwicklung von xStream und deren Site-Plugins gearbeitet wird.


### 1.2 Rechtliche Konsequenzen bei Nutzung

Es ist festzuhalten, dass das Addon xStream lediglich die Nutzung eines bereits verfügbaren Angebotes an Streaminginhalten bestehender Webseiten  ermöglicht. Das bloße streamen von Medien kann in Deutschland aktuell weder als eindeutig legale oder illegale Handlung eingestuft werden und befindet sich somit in einer rechtlichen Grauzone. Vor Verwendung des Addons und dem damit verbundenen Inhalten ist die aktuelle rechtliche Situaltion im jeweiligen Land zu prüfen! 

Weiterhin ist zu erwähnen, dass ein großteil der Streaming-Plattfromen weder Nutzerverhalten noch Zugriffsdaten speichern. Jedoch ist dies im Einzelfall zu prüfen. 

Aufklärendes Video zum Thema Streaming von Rechtsanwalt Christian Solmecke:
[![Nutzerfragen: Legalität von Streaming, Arbeitszeiten und Bild.de | Rechtsanwalt Christian Solmecke](http://img.youtube.com/vi/cDmvhJrLkmM/0.jpg)](http://www.youtube.com/watch?v=cDmvhJrLkmM)



## 2. Installation und Konfiguration


### 2.1 Bezugsquellen zur Installation

Das Addon kann direkt über das xStream-Repository bezogen werden. Empfohlen wird die Installation dieser sogenanten Repo über das xStream-Forum.

Alternativ könnte die xStream-Repository ebenfalls über das _SuperRepo_ geladen werden. Bei _SuperRepo_ handelt es sich um eine Ansammlung verschiedenster Addons, Skripte, Repos und Weiteres rund um Kodi.

***WICHTIG:***
*Jedoch muss an dieser Stelle klar darauf hingewiesen werden, dass unter der alternativen Bezugsquelle nicht für den aktuellsten Stand der Software garantiert werden kann!*


xStream-Repository aus Forum:

- [xStream-Forum] (http://xstream-addon.square7.ch/showthread.php?tid=1)


xStream-Repository aus SuperRepo:

- [SuperRepo](https://superrepo.org/kodi/addon/repository.xstream/)


GitHub:

- [Master-Branch bei GitHub](https://github.com/Lynx187/xStreamRepo/archive/master.zip)
- [Beta-Branch bei GitHub](https://github.com/StoneOffStones/plugin.video.xstream/tree/beta)
- [Nightly-Branch bei GitHub](https://github.com/StoneOffStones/plugin.video.xstream/tree/nightly)


***ACHTUNG:*** 
*Die Beta und Nightly Versionen gelten als Experimentell und werden nicht offiziell unterstützt!*

Außerdem ist beim Download der Addon-Daten von Github gilt es folgendes zu Beachten: 

Um eine korrekte Installation zu gewährleisten ist es notwendig den jeweiligen Ordner in der heruntergeladenen Zip-Datei anzupassen. Dabei muss darauf geachtet werden, dass der enthaltene Ordner um Begriffe wie z.B. _Master, Beta, Nightly_ gekürzt werden.

Um den aktuellsten Beta- und Nightly-Versionen kann es durchaus erfordelich sein das neue noch nicht im System vorhandene fehlende Abhängigkeiten des Addons händisch nachinstallieren werden müssen.


### 2.2 Allgemeine Einstellungen

Das Addon kann prinzipiell mit den Grundeinstellungen, welche nach der Erstinstallation vorgefunden werden, ohne Bedenken verwendet werden.

Unter der Auswahl der jeweiligen Sprache kann die jeweilig bevorzugte Sprache ausgewählt werden. Dabei kann unter den Optionen Deutsch, Englisch und Alle gewählt werden, wobei Alle beide Sprachen einbezieht. Zu berücksichtigen ist jedoch, dass die einzelnen Site-Plugins diese Option unterstützen müssen.
Wird also die aufgezählte Option nicht unterstützt werden auch Inhalte anderer Sprache angezeigt.

Ab xStream 2.2.0 gibt es in den Settings eine Auto-Update Funktion. Diese installiert automatisch Änderungen an Seiten usw., welche auf der Entwicklerplattform (Github) durchgeführt werden. Dadurch werden Fehler/Bugs/Error, schnell & einfach behoben. Als Standard ist die Master zu verstehen, welche auch als Stable bezeichnet wird. Natürlich können auch die zuständigen Branches für die Entwicklung Beta bzw. Nightly ausgewählt werden. Jedoch ist für jegliche Entwicklerversion der Support bei auftretenden Fehlern bzw. Problemen ausgeschlossen und vom Entwicklungsteam nicht zu erwarten!


### 2.3 Webseiten aktivieren und deaktivieren

In den Einstellungen, unter dem Menüpunkt *Site-Plugins*, besteht die Möglichkeit bestimmte Seiten an- bzw. auszuschalten. Dies kann von Nutzen sein, wenn kein Interesse an bestimmten Webseiten besteht. Diese werden dann auch nicht mehr in der globalen Suche angezeigt.


### 2.4 Manuelle und automatische Hosterwahl

Die Hosterwahl als solches ist sehr schlicht und einfach gehalten.
Es erinnert stark an die eigentlichen Benuteroberflächen der jeweiligen Streaming-Seiten

Wenn keine besonderen Wünsche bzw. keine entprechende Kenntisse im Bezug auf die Hosterauswahl vorhanden sind, kann die Automatische Hosterwahl verwednet werden. In dieser Einstellung werden darüber hinaus nicht funktionierende Hoster rausgefiltert. 

- **Hosterliste prüfen und sortieren**

Bei Aktivierung werden aus der Hosterliste alle nicht unterstützten Hoster entfernt und nach ihrer Priorität über die "Resolver Settings" sortiert.
Die Deaktivierung diese Features kann auf leistungsschwachen System wie z.B. RespberryPi oder ähnliches kann einen spürbaren schnelleren Ablauf bewirken.


### 2.5 Funktion des Metahandlers

Bei Aktivierung wird das externe Modul "Metahandler" genutzt um ausführliche Informationen in form von Metadaten, wie Fanarts, Covers oder Episodenbilder, zu den Streams bereitzustellen.
Darüber hinaus ermöglicht es eine relativ konsistente Verwendung der "gesehen" Markierung.

Bei erstmaliger Verwendung dauern die Ladevorgänge deutlich länger. Dies liegt daran, dass  zunächst alle neuen Informationen zusätzlich über das Internet abgerufen werden müssen.
Für schwache Systeme ist dieses Feature nur bedingt zu empfehlen und muss vom jeweiligen Site-Plugin unterstützt werden, ansonsten zeigt diese Option keine Funktion an.

- **Metahandler ersetzt Infos von Site**

- Bei Aktivierung werden Metainformationen vom  "Metahandler" bevorzugt. D.h. Metainformationen die von einem Site-Plugin geliefert wurden werden nicht nur ergänzt sondern auch ersetzt.

- ***ACHTUNG:*** Da viele Seiten nicht sofort genug Informationen bereitstellen um jeden Film eindeutig zu identifizieren kann es vorkommen, dass alle angezeigten Informationen nicht zum tatsächlich verlinkten Film passen.



## 3. Bekannte Probleme

In diesem Kapitel wird auf mögliche Fehlermeldungen sowohl beim Installationsvorgang als auch im eigentlichen Betireb eingegangen. Darüber hinaus wird auch im Forum im Bereich [Support - Skriptfehler, Bugs, etc.](http://xstream-addon.square7.ch/forumdisplay.php?fid=8) auf aktuelle Probelme eingegangen. Hervorzugheben sind die sogenannten wichtigen Themen, welche im Forum zuerst dargestellt werden und auf häufig gestellte Fragen (FAQs: Frequently Asked Questions) bzw. auf bereits bekannte Problematiken eingehen und den aktuellen Arbeitsstand dazu aufzeigen.

- [[Bugs] Bekannte Probleme](http://xstream-addon.square7.ch/showthread.php?tid=619)

- [[FAQs] - Bugs, Scriptfehler, usw.](http://xstream-addon.square7.ch/showthread.php?tid=3)

- [[FAQs] - Einstellungen](http://xstream-addon.square7.ch/showthread.php?tid=2)


### 3.1 Fehler bei der Installation

Fehler können verschiedene Ursachen haben. Bei Hilfe bitte immer folgendes bekannt geben:
Log, Kodi Version, Betriebssystem, xStream Version, genaue Fehlerbeschreibung!
Wird die aktuelle 2.1.16 Beta installiert, ist es vorher notwendig das script.modul "Cryptopy" zu installieren und vor dem Entpacken den Zusatz _-master_ aus der .zip entfernen::

- [https://github.com/StoneOffStones/script.module.cryptopy/archive/master.zip](https://github.com/StoneOffStones/script.module.cryptopy/archive/master.zip)

**WICHTIG:** Erst lesen, dann fragen! Bitte kontrollieren, ob der Fehler in einem früheren Post schon beantwortet wurde!
Es kann auch eine fehlerhafte Datei vorliegen, oder die .zip ist falsch aufbereitet.


### 3.2 Fehler bei Verwendung der Globalen Suche

Falls bei der Globalen Suche eine Fehlermeldung aufkommt, dass eine Seite nicht erreichbar ist bzw. die Suche durch eine Meldung unterbrochen wurde, liegt dies meist an der eigentlichen Ereichbarkeit der Webseite. Dagegen meist nicht viel mehr getan werden als abzuwarten bis die Probleme der Seite behoben sind und diese wieder online verfügbar ist.

Wenn von der Globalen Suche keine Treffer angezeigt werden, dann bitte die Suche in der gewünschten Seite nutzen. Um schnelle Abhilfe zu leisten lohnt es sich in diesem Fall durchaus die Entwicklergemeinde darauf aufmerksam zu machen.


### 3.3 Fehler bei Verwendung einzelner Webseiten

Dieser Fehler kann verschiedene Ursachen haben. Meistens liegt es jedoch an der eigentlichen Webseite.
Denn wenn dort Anpassungen vorgenommen werden kann unter Umständen bereits die Funktion des Site-Plugin in xStream gestört sein.
Im Regelfall sind die Entwickler informiert und arbeiten an einer Lösung. Bitte fortbestand bitte sachlich bleiben und Ruhe bewahren!
Falls noch nicht bekannt dann bitte die Seite im Browser aufrufen, auf Funktion überprüfen und im Anschluss das Problem über das Forum oder direkt bei GitHub schildern.

*Für die Streaming-Seiten kinox.to und movie4k.to können in den Einstellungen alternative Domäne bestimmt werden. Nutzen sie diese falls die Seiten nicht zu erreichen sind!*


### 3.4 Fehler bei Verwendung einiger Hoster

Sollte dies der Fall sein, bitte ggf. eine aktuellere Version des "URLResolver" über eine der folgenden Bezugsquellen beziehen:

- TVA Repo, kann über das offizielle xStream-Repo installiert werden

- https://offshoregit.com/tvaresolvers/tva-common-repository/raw/master/zips/script.module.urlresolver/

Bitte den gewünschten Film auf der Homepage erneut auf Funktion prüfen.
 


## 4. Fehlerbericht über Log-Datei


### 4.1 Allgemeines zur Log-Datei

In der sogenannten Log-Datei werden alle Aktivitäten bzw. Programmabläufe von Kodi protokolliert und gespeichert. Wenn nun ein Problem bei der Verwendung von Kodi oder dessen Addons auftritt ist es notwednig, dass diese Log-Dati bei entsprechender Meldung übermittelt wird. Dabei ist egal ob die Kommunikation im xStream-Forum oder auf anderen Kanälen wie z.B. GitHub, stattfindet. Nur so kann eine schnelle und Zielgerichtete Lösung erfolgen, ist dieses Protokoll kann ebenfalls die unterschtützung untersagt werden!


### 4.2 Erstellen, bearbeiten und hochladen der Log-Datei

**Erstellen / Hochladen:**

Kodi hat standardmäßig die Addons zur Erstellung und Bereitstellung der Log-Dateien integriert. Damit ist das Erstellen und Posten der Log-Datei und im Forum sehr viel einfacher.

In Kodi wie folgt vorgehen:

1. Desktop-Optionen
2. Einstellungen
3. Addons
4. Suche

Den Begriff "log" in das Suchfeld eingeben, bestätigen und anschließend folgende Addons auswählen und installieren:

- Log-Viewer für Kodi (nur zum Lesen der Log-Datei)
- Kodi-Log-Uploader (zum Auslesen & Uploaden der Log-Datei)

Mit dem "Log-Viewer" kann man die Log-Datei ansehen, mit dem "Kodi-Log-Uploadeder" die Log-Datei auf http://xbmclogs.com hochladen.
Bei der Installation eine E-Mail Adresse angeben. An diese wird dir dann nach dem "Kodi-Log-Uploadeder" ein Link zur Log Datei geschickt.
Diesen Link im Forum Posten oder alles in einen Texteditor koperien, die Datei speicherun und im Forum hochladen.


**Bearbeiten:**

Die Log-Datei kann unter Windows z.B. mit der Software "Notepad++" oder "gedit" unter Linux betrachtet werden.
Auch der normale Texteditor unter Windows funktioniert, auch wenn nicht ganz so übersichtlich.
Auf Android einen beliebigen Texteditor verwenden zum Betrachten.
Das Notepad++ weist zum Texteditor einige Vorteile auf. Es werden so z.B. die Zeilen nummärisch angezeigt, somit ist die ganze Darstellung übersichtlicher gestalltet. Außerdem können mit dem Notepad++ .py Datei sofort geöffnet und wieder gespeichert werden.


**Debug-Logging:**

Eventuell ist es sinnvoll das "Debug-Logging" in Kodi zu aktivieren um noch mehr Informationen zu erhalten.

Folgendes Ausführen:
 
1. Einstellungen
2. System
3. Debugging
4. "Debug-Logging aktivieren" anklicken

Nun wird am oberen Rand eine Statuszeile eingeblendet mit Infos. **Hier ist auch der Speicherort der Log-Datei zu sehen!**

Starte Kodi neu und öffne das Addon welches einen Fehler verursacht. Erstelle anschließend umgehend eine Log-Datei um den Fehler leichter ausfindich machen zu können.

Falls nicht mehr benötigt kann das "Debug-Logging" im Anschluss wieder in den Einstellungen deaktiviert werden.

Unter dem Punkt Komponentenspezifische Protokollierung kann man bei der Kategorie "Konfiguration der Komponentenspezifischen Protokollierung" noch Einstellen was alles im Debug-Log Protokolliert werden soll.


### 4.3 Speicherort der Log Datei

Den Speicherpfad von Kodi anzeigen lassen – runter scrollen zum Punkt "Debug_Loggin" und folgenden Beschreibungen.

Pfad ist vom verwedneten Betriebssystem abhängig.
Im Folgenden werden Ordnerstrukturen der jeweiligen Betriebssysteme aufgelistet. Anstelle von "xbmc" kann in den Ordnern auch "kodi" stehen hinzu kommt, dass die Ordnerstruktur auch leicht den aufgeführten abweichen kann:

- Windows XP
    - `Documents and Settings\<your_user_name>\Application Data\Kodi`
- Vista/Windows 7
    - `C:\Users\<your_user_name>/%APPDATA%/Roaming/Kodi/Kodi.log`
- Mac OS X
    - `/Users/<username>/Library/Logs/ oder`
    - `/Users/<your_user_name>/Library/Application Support/Kodi/userdata`
- iOS
    - `/private/var/mobile/Library/Preferences`
- Linux, OpenElec, Raspberry Pi 1-3
    - `$HOME/.kodi/temp/`
    - `$HOME/.kodi/userdata/temp/xbmc.log`
    - `$HOME/.kodi/userdata`
- Android
    - `/android/data/org.xbmc.Kodi/files/.kodi/temp`
    - `data/data/org.xbmc.Kodi/cache/temp`

**WICHTIG:** Die Ordner sind meist versteckt und müssen erst sichtbar gemacht werden. Bei Windows kann dies über den Explorer und auf Android Systemen mit dem ESDateiexplorer eingestellt werden.

Die in Kodi als „log.old“ bezeichnete Datei ist die Log-Datei vom letzten Neustart bzw. Absturz. Wenn somit kein aktuelleres Protokoll vorhanden ist sollte diese zur Problemfindung benutzt werden.



## 5. Phyton Dateien


### 5.1 Allgemeines zur .py-Datei

Eine .py Datei ist im eigentlichen Sinne eine Textdatei. Dabei verweist die Dateiendung .py auf die eigentliche Programmiersprache namens Python, welche in Kodi bzw. dessen Addons häufig zur Anwendung kommt.
 
 
### 5.2 Bearbeiten einer .py-Datei

Wenn der User aufgefordert wird die .py Datei zu wechseln, diese in einem explizieten Ordner zu verschieben bzw. zu kopieren eine bestimmte Zeile innerhalb der Datei zu ändern ist damit ein händisches Anpassen der Position bzw. des Inhaltes gemeint. Bearbeitet werden können diese Dateien mit Programmen wie z.B. Notepad++ oder dem standatdmäßg installierten Texteditor, wie bereits in Kapitel 4.3 aufgezeigt.

Bei Verwendung des Texteditors muss die Endung zuvor von .py auf .txt geändert werden. Anschließend kann die Datei geöffnet und Änderungen vorgenommen werden. Beim Beendigung der Anpassung die Datei über „Speichern unter“ absichern, unter „Dateityp“ alle auswählen und wieder als .py Datei abspeichern.


### 5.3 Speicherort der einzelnen Webseiten

In folgenden Ordnern sind die Kodi-Addons abgelegt:

- Android 
	- `/Android/data/org.xbmc.kodi/files/.kodi/addons/`
	- `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/`  (.kodi ist ein versteckter Ordner)
- iOS
	- `/private/var/mobile/Library/Preferences/Kodi/addons/`
- Linux 
	- `~/.kodi/addons/`
- Mac 
	- `/Users/<your_user_name>/Library/Application Support/Kodi/addons/`
- OpenELEC 
	- `/storage/.kodi/addons/`
- Windows
	- `C:\Users\BENUTZERNAME\AppData\Roaming\Kodi\addons`    (AppData ist ein versteckter Ordner)

Das Addon xStream wird in aller Regel unter plugin.video.xstream istalliert.
Im Verzeichnis `sites/` sind die .py Daten und im Ordner `resources/art/sites/` die jeweiligen Artworks bzw. Site-Icons der einzelnen Webseiten abgelegt.
