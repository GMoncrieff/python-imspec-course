#!/bin/bash

while IFS=, read -r col1 col2
do
  python unmix_image.py --f_url $col1 --f_mask_url $col2 --log INFO
done < data/infiles.csv
