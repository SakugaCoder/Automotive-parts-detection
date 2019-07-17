formato=$1
inicio=$2
label=$3
directorio=$4
contador=0

echo "Formato: $formato"
echo "Inicio: $inicio"
echo "label: $label"
echo "directorio: $directorio"
cd Images/Training/$directorio


if [ $2 -ge 0 ]; then
	contador=$2
	echo "Inicio de contador puesto en: $contador"
fi



for f in *.$formato; do
	echo "Cambiando nombre de $f a: $label""_$contador.$formato"
	mv -- "$f" "$label""_$contador.$formato"
	contador=$((contador+1))
done


