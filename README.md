# Barcode_Reader

USB-laitteena viivakoodilukija, jonka kautta luetaan tilausnumero ja tehdään erinäisiä toimintoja. Tilausnumeron perusteella päivitettään tilauksien hallintaan käytettävään exceliin saapumispäivämäärä, lähetetään sähköpostilla ilmoitus ja avataan selaimeen tilausta vastaava ticketti ServiceNowsta. Vaatii toimiakseen seuraavan udev-säännön:



SUBSYSTEMS=="usb", KERNEL=="event14", ACTION=="add", ATTRS{idVendor}=="24ea", ATTRS{idProduct}=="0197", RUN+="/bin/sh -c 'logger -p user.info muipmuip'", RUN+="/bin/sh -c 'echo remove > /sys$env{$
ACTION=="add", ATTRS{idVendor}=="24ea", ATTRS{idProduct}=="0197", SYMLINK+="barcode"
KERNEL=="hidraw", SUBSYSTEM=="hidraw", MODE="0664", GROUP="users"

Sääntö estää viivakoodilukijan normaalin inputin, mutta symlink mahdollistaa koodissa hidraw syötön lukemisen.
