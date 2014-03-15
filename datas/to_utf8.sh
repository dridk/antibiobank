rm -R utf8
mkdir utf8

for f in *.csv
do 
 iconv --from-code=ISO-8859-1 --to-code=UTF-8 $f > utf8/$f

done
