This file is written in German, since the audience of the program are
users of a German keymapping. The code and commit-massages are written
in English, though.

0.15 (2020-06-05)
-----------------

Author: Hartmut Goebel <h.goebel@crazy-compilers.com>

- Portiert zu Python 3.
- Portiert zu GObject.


0.14.1 (2017-09-04)
-------------------

Author: Hartmut Goebel <h.goebel@crazy-compilers.com>

- Behebt den Absturz, wenn `OSD Neo2` gestartet wird, wenn es ein
  Icon im Benachrichtigungsfeld (`tray`) ist.


0.14 (2017-08-30)
=================

Author: Hartmut Goebel <h.goebel@crazy-compilers.com>

Sichtbare Änderungen
-----------------------

- Durch Doppel-Klick verwandelt sich das Fenster in ein Icon im
  Benachrichtigungsfeld (`tray`)
- Es gibt jetzt ein Kontext-Menü (erreichbar über die rechte Maustaste)
- Es gibt jetzt einen Einstellungs-Dialog
- Das Fenster lässt sich verschieben, auch wenn es keinen Rand hat.
- Das Fenster kann auf allen Arbeitsflächen angezeigt werden.
- Die Tastatur "Ergodox" kann angezeigt werden
- Einstellungen werden nun in ``$XDG_CONFIG_HOME/OSDneo2`` gespeichert
- Der ``xkbdmap`` Treiber verwendet einen `event handler` anstelle des
  bisherigen `pollings`.


Interne Änderungen
-----------------------

- Modernized the code.
- Reorganized the code into a Python package structure.


0.13 (2010-10-15)
=================

Author: Martin Zuther  <code@mzuther.de>

* SimpleXkbWrapper.py: the "X Keyboard Extension" functions have been
  moved from "libXxf86misc" to "libX11", so the code now checks which
  library to link to


0.12 (2009-09-07)
=================

Author: Martin Zuther  <code@mzuther.de>

* osd_neo2.py: renamed to "OSDneo2.py"

* settings.py: renamed to "Settings.py"

* settings.py: settings are now stored in "~/.OSDneo2"

* osd_neo2.py (OSDneo2): added new INI file option
  'selected_keyboard_driver' and corresponding matrices for
  switching between the two Neo2 keyboard drivers ("xkbdmap" and
  "xmodmap")

* osd_neo2.py (OSDneo2): layer switching is now controlled via
  matrices

* caught exceptions for files that cannot be accessed or are missing

* osd_neo2.py (OSDneo2): changed X11 keyboard defines to official
  Neo2 values

* SimpleXkbWrapper.py (SimpleXkbWrapper.__init__): changed
  "c_bool" return value of function "XkbGetState" to
  "c_int" (compatibility to Python v2.5)


0.11 (2009-08-31)
=================

Author: Martin Zuther  <code@mzuther.de>

* removed start scripts and "evdev" library
* SimpleXkbWrapper.py (SimpleXkbWrapper): new class that uses X
  Keyboard Extension v1.0 to poll keyboard modifier states
* removed support for Win32 (there are better alternatives)


0.10 (2009-08-27)
=================

Author: Martin Zuther  <code@mzuther.de>

* first public release


.. Emacs config:
 Local Variables:
 mode: rst
 ispell-local-dictionary: "german"
 End:
