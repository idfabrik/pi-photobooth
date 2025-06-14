#!/bin/bash

TMP_DIR="/var/www/html/tmp_id"
mkdir -p "$TMP_DIR"

mkdir -p /var/www/html/tmp_id
chmod 775 /var/www/html/tmp_id
chown pi:www-data /var/www/html/tmp_id

sleep 3

# Nettoyer anciens fichiers
rm -f "$TMP_DIR/temp"*.jpg
rm -f /var/www/html/image.jpg

for i in 1 2 3 4; do
  echo "▶ Photo $i"

  # LED verte (prêt)
  gpioset --mode=exit gpiochip0 17=1
  sleep 0.8
  gpioset --mode=exit gpiochip0 17=0

  # LED rouge (prise)
  gpioset --mode=exit gpiochip0 27=1

  # Capture
  libcamera-still -n -t 300 \
    --roi 0.15,0.15,0.5,0.5 \
    --awb indoor --contrast 1 --saturation 0.0 \
    --sharpness 1.0 \
    -o "$TMP_DIR/temp$i.jpg"

  # Éteint LED rouge
  gpioset --mode=exit gpiochip0 27=0

  # Traitement simple : redim + rotation + contraste + bordure
  convert "$TMP_DIR/temp$i.jpg" \
    -resize 800x600\! \
    -rotate 90 \
    -contrast -contrast -contrast \
    -bordercolor white -border 10x10 \
    "$TMP_DIR/temp$i.jpg"
done

# Montage final 2x2 propre
OUTPUT_NAME="/var/www/html/image_$(date +%Y%m%d_%H%M%S).jpg"
montage "$TMP_DIR/temp1.jpg" "$TMP_DIR/temp2.jpg" \
        "$TMP_DIR/temp3.jpg" "$TMP_DIR/temp4.jpg" \
        -tile 2x2 -geometry +0+0 -background white \
        "$OUTPUT_NAME"

convert "$OUTPUT_NAME" -rotate 180 "$OUTPUT_NAME"

# LED verte allumée à la fin
gpioset --mode=exit gpiochip0 27=1
sleep 0.2
gpioset --mode=exit gpiochip0 27=0
sleep 0.2
gpioset --mode=exit gpiochip0 27=1
sleep 0.2
gpioset --mode=exit gpiochip0 27=0
sleep 0.2
gpioset --mode=exit gpiochip0 27=1
sleep 0.2
gpioset --mode=exit gpiochip0 27=0
sleep 0.2
gpioset --mode=exit gpiochip0 27=1
sleep 0.2
gpioset --mode=exit gpiochip0 27=0
sleep 0.2
gpioset --mode=exit gpiochip0 27=1
sleep 0.2
gpioset --mode=exit gpiochip0 27=0
sleep 0.2
#gpioset --mode=exit gpiochip0 27=1
#sleep 0.2
#gpioset --mode=exit gpiochip0 17=0
#sleep 0.2
#gpioset --mode=exit gpiochip0 17=1
#sleep 0.2
#gpioset --mode=exit gpiochip0 17=0

echo "!! terminé !!"
echo $TMP_DIR/temp$i.jpg
