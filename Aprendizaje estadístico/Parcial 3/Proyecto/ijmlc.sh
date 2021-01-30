#!/bin/bash

function CreateDir {
	if [[ -d $directory ]]; then
		rm -rf $directory
		mkdir -p "$directory/PDF"
		mkdir -p "$directory/TXT"
	else
		mkdir -p "$directory/PDF"
		mkdir -p "$directory/TXT"
	fi
}

function Resquest {
		rl=$( echo "$url list-6-1.html" | tr -d ' ' )
		curl $rl > /tmp/resquest 2>/tmp/err
		cat /tmp/resquest | sed 's/> />/g' | grep -o "href=\"http://www.ijmlc.org/list-[0-9]*-[0-9]*.html\">Volume.*" > /tmp/listvol
}

function Download {
	cd $directory
		touch metadata
		i=1
		while read -r lsv
		do
			rl=$( echo $lsv | cut -d '"' -f2 )
			dire=$( echo $lsv | cut -d '>' -f2 | cut -d '<' -f1 )
			mkdir ./PDF/"$dire"
			mkdir ./TXT/"$dire"
			curl $rl > /tmp/resquest 2>/tmp/err
			cat /tmp/resquest | grep -o "<a .*" | sed '1,20 d' | sed '$d' | sed '$d' > /tmp/listart

			while read -r lsa
			do 
				r=$( echo $lsa | cut -d '"' -f2 )
				art=$( echo $lsa | cut -d '>' -f2 | cut -d '<' -f1 )

				curl $r > /tmp/pdf 2>/tmp/err
				namepdf=$( echo "$art.pdf" )
				nametxt=$( echo "$art.txt" )
				pdf=$( cat /tmp/pdf | grep "PDF" | cut -d '"' -f2 )
				urlpdf=$( echo "$url $pdf" | tr -d ' ' )

				wget -O ./PDF/"$dire"/"$namepdf" "$urlpdf"
				pdf2txt -o ./TXT/"$dire"/"$nametxt" ./PDF/"$dire"/"$namepdf" 2>/tmp/err
				path=$( echo "TXT/$dire/$nametxt" )
				echo "$i: $path" >> metadata
				let i=i+1
			done < /tmp/listart
		done < /tmp/listvol
}

function Split_Set {
	cd $directory
	lim=$( wc metadata | tr -s ' ' | cut -d ' ' -f2 )
	i=1
	mkdir "Set"
	#touch meta
	while [[ $i -lt 215 ]]
	do
		sample=$(($RANDOM%$lim+1))
		File=$( cat metadata | grep "^$sample:" | sed 's/: /:/g' )
		id=$( echo "$File" | cut -d ':' -f1 )
		ope=$( cat meta | grep "^$id:" | wc | tr -s ' ' | cut -d ' ' -f2 )
		if [[ $ope -eq 0 ]]
		then 
			name=$( echo "$File" | cut -d ':' -f2- )
			len=$( wc "$name" | tr -s ' ' | cut -d ' ' -f2 )
			if [[ $len -ne 0 ]]
			then
				cp ./"$name" ./Set/
				echo "$File" >> meta
				let i=i+1
			fi
		fi
	done

}

function SS {
	ls ./IJMLC/Set1 > /tmp/ll
	while read -r l
	do
		len=$( wc "./IJMLC/Set1/$l" | tr -s ' ' | cut -d ' ' -f2 )
		if [[ len -ne 0 ]]
		then
			echo "$len"
		fi
	done < /tmp/ll
}
# Main
directory="IJMLC"
url="http://www.ijmlc.org/"
#CreateDir
#Resquest
#Download
Split_Set
#SS

exit 0



