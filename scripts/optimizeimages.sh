#!/bin/bash
echo "Optimize Images"
find ./static/ -type f -name "*.png" -print -exec convert {} -strip {} \;
find ./static/ -type f -name "*.gif" -print -exec convert {} -strip {} \;
find ./static/ -type f -name "*.jpg" -print -exec convert {} -sampling-factor 4:2:0 -strip -quality 85 -interlace JPEG -colorspace sRGB {} \;