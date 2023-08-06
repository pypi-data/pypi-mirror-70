=============================
OSD Neo2
=============================

------------------------------------------------------------
On screen display for learning the keyboard layout Neo2
------------------------------------------------------------

This file is written in German, since the audience of the program are
users of a German keymapping. The code and commit-massages are written
in English, though. Please have a llok there, the URL is at the bottom
of this file.

------------------------------------------------------------
On-Screen-Display zum Lernen des Neo2-Tastaturlayouts
------------------------------------------------------------

Das Programm `OSD Neo2` für Linux zeigt die Zeichen der gerade
verwendeten Ebene des Neo2-Tastaturlayouts auf dem Bildschirm an.


:Homepage:       https://htgoebel.gitlab.io/OSD-Neo2/
:Source-Code:    https://gitlab.com/htgoebel/OSD-Neo2
:Copyright (C): 2009–2010 Martin Zuther, 2015-2020 Hartmut Goebel
:Licence: GNU General Public License, Version 3 (GPLv3)

  This program comes with ABSOLUTELY NO WARRANTY. This is free software,
  and you are welcome to redistribute it under certain conditions.
  Please read the file "LICENSE" for details.


Abhängigkeiten
===============

Die folgenden Programme und Bibliotheken werden für `OSD Neo2`
benötigt (frühere oder spätere Versionen können allerdings genauso gut
funktionieren):

* Python 3.7 oder höher
* GTK+ 3
* PyGObject 3

Die meisten GNU/Linux-Benutzer können vermutlich gleich
loslegen, ohne etwas anderes als `OSD Neo2` installieren zu müssen,
denn die benötigten Programme und Bibliotheken sind oft schon
über andere Weg installiert.

Falls nicht:
Hier die Paketnamen der benötigten Abhängigkeiten
für einige GNU/Linux Distributionen:

:Debian, Ubuntu, etc: python3-gi gir1.2-gtk-3.0
:openSuse:  python3-gobject python3-gobject-Gdk
:Fedora:    python3-gobject gtk3
:ArchLinux: python-gobject  gtk3
:Mageia:    python3-gobject3

Hinweise für andere GNU/Linux-Distributionen,
Windows und MacOS finden sich im
`Handbuch von PyGObject
<https://pygobject.readthedocs.io/en/latest/getting_started.html>`_



Installation & Start
====================

Nach dem Installieren der Abhängigkeiten (s. oben) muss lediglich
der Inhalt des Archivs "OSDneo2_x.xx.tar.gz" in ein Verzeichnis
entpackt werden, dann kann es losgehen: Einfach im Dateimanager in das
Verzeichnis des Programms wechseln und die Datei ``ODSneo2``
doppelklicken.

Falls das nicht geht: Die Konsole öffnen, in das Verzeichnis des
Programms wechseln und ./OSDneo2 eingeben.


Update
---------------

Soll das Programm im gleichen Ordner wie vorher installiert werden,
sollte dessen Inhalt vorher gelöscht werden.  Die Einstellungen
werden im Homeverzeichnis jedes Benutzers gespeichert (siehe
unten) und bleiben daher erhalten.


Bedienung
=============

Das Fenster lässt sich verschieben, auch wenn es keinen Rand hat.

Über die rechte Maustaste gelangt man zu einem Menü, mit dem sich die
das Programm beenden lässt oder Einstellungen getätigt werden können.

Durch Doppel-Klick verwandelt sich das Fenster in ein Icon im
Benachrichtigungsfeld (`tray`) und kann dort per Klick wieder heraus
geholt werden. Das Icon hat auch ein kleines Menü (rechte Maustaste),
um das Fenster wieder zu öffnen oder die Anwendung zu beenden.

Die ausführliche Anleitung finden Sie auf der `Homepage
<https://htgoebel.gitlab.io/OSD-Neo2/>`_.


Mitwirken
=================

Ich höre gerne von Anwendern meiner Programme.  Wenn Sie also Zeit und
Lust haben, schreiben Sie mir eine E-mail (die Adresse gibt's unter
http://www.crazy-compilers.com/), gerne auch mit Vorschlägen, Verbesserungen
oder Bugfixes! Oder öffne einen Vorgang auf der Entwicklungs-Homepage
der Programms https://gitlab.com/htgoebel/OSD-Neo2.

* Source-Code: https://gitlab.com/htgoebel/OSD-Neo2

* Bug-Reports: https://gitlab.com/htgoebel/OSD-Neo2/issues

Mehr Infos, wie Sie mithelfen können, finden Sie auf der `Homepage
<https://htgoebel.gitlab.io/OSD-Neo2/>`_.


.. Emacs config:
 Local Variables:
 mode: rst
 ispell-local-dictionary: "german"
 End:
