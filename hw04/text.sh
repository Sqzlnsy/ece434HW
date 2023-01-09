# Here's how to use imagemagick to display text
# Jason Su @ 01/09/2023
SIZE=320x240
TMP_FILE=/tmp/frame.png
BACKGROUND=/home/debian/exercises/displays/demo/boris.png

# From: http://www.imagemagick.org/Usage/text/
convert -fill blue -font Times-Roman -pointsize 24 \
     -size $SIZE \
     label:'ImageMagick\nBoris.png\nby Jason Su' \
     -draw "text 0,200 '01/08/2023'" \
     $TMP_FILE
composite -geometry $SIZE+150 $BACKGROUND $TMP_FILE $TMP_FILE   

convert $TMP_FILE -rotate 90 $TMP_FILE
sudo fbi -noverbose -T 1 $TMP_FILE
