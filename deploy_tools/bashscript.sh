#! /usr/bin/bash


# for line in $(ps -A|grep python);
# 	do echo "$line";
# done

# es_numero='^-?[0-9]+([.][0-9]+)?$'

# for line in $(ps -A|grep python);
# 	if [[$line != $es_numero]] ;
# 		then
# 		do echo "ERROR: No es un Numero" > &amp;2; exit 1
# 	else
# 		do echo "$line";
# 	fi
# done
	
es_entero() {
    printf "%d" $1 > /dev/null 2>&1
    return $?
}

for line in $(ps -A|grep $1);
do
	if es_entero "$line"; then
	   echo "$line"
	   kill $line
	else
	   echo ""
	fi

done

 