#!/bin/bash

baseurl=http://neo-layout.org/svn/grafik
baseurl_3d=${baseurl}/tastatur3d

# Hauptfeld
for i in $(seq 1 6) ; do
    wget -nv -O neo2-hauptfeld_ebene${i}.png ${baseurl_3d}/hauptfeld/tastatur_neo_Ebene${i}.png
done
for i in 1 2 ; do
    wget -nv -O neo2-hauptfeld_ebene${i}-caps.png ${baseurl_3d}/hauptfeld/tastatur_neo_Ebene${i}Caps.png
done

# Ziffernfeld
for i in $(seq 1 6) ; do
    wget -nv -O neo2-ziffernfeld_ebene${i}.png ${baseurl_3d}/ziffernfeld/tastatur_neo_Ebene${i}.png
done
for i in 1 2 ; do
    wget -nv -O neo2-ziffernfeld_ebene${i}-caps.png ${baseurl_3d}/ziffernfeld/tastatur_neo_Ebene${i}Caps.png
done

# Icon
wget -nv -O neo-icon.svg ${baseurl}/logos/Neo-Icon.svg
