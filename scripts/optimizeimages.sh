#!/bin/bash
echo "Optimize Images"
find ./static/ -type f -name "*.png" -printf '%p\n' -exec convert {} -strip {} \;
find ./static/ -type f -name "*.gif" -printf '%p\n' -exec convert {} -strip {} \;
find ./static/ -type f -name "*.jpg" -printf '%p\n' -exec convert {} -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -colorspace sRGB {} \;