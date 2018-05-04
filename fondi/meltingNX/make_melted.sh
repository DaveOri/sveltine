#! /bin/bash

folder='/data/optimice/scattering_databases/DavideOri_2014'
files=`ls $folder/davide_shapefiles/*`

if [ ! -d "$folder/melted" ]; then
echo "Making melted"
  mkdir $folder/melted
fi

melts=`seq 0.01 0.01 1.00`
#echo $melts

for f in $files; do
  filename=$(basename -- "$f")
  extension="${filename##*.}"
  dmax="${filename%.*}"
  echo $filename $extension $dmax
  curfld=$folder/melted/$dmax
  if [ ! -d "$curfld" ]; then
    mkdir $curfld
  fi
  dip=20
  if (( $(echo "$dmax > 14000" | bc -l) )); then
    dip=40
  fi
  echo $dmax $dip $filename

  fin=$f
  if [ $(ls *temp 2> /dev/null) ]; then
    echo "another process is working here"
  else
    for m in $melts; do
      fout=$curfld/${dmax}_${m}.$extension
      if [ ! -f "$fout" ]; then
        touch $fout.temp
        ./melting --dmax $dmax --dipole $dip --melt $m --input $fin --output $fout
        rm $fout.temp
      fi
      fin=$fout
    done
  fi
done
