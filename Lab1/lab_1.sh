#!/bin/bash

echo $#
if [ $# == 0 ];
then
	folder_name="./"
else
	folder_name=$1
fi
echo $folder_name

time_ext=(mp3 mp4 avi m4v mov MPG MPEG)
dlm=','
echo "File name$dlm Extension$dlm Change data$dlm Size$dlm Duration" > data.csv

for file_path in $(find $folder_name -type f -not -name ".*")
do
	# echo $file_path
	file_name="${file_path##*/}"
	extension="${file_name#*.}"
	if [ "$file_name" == "$extension" ];
	then
		extension=-
	fi

	size=$(du -hs $file_path | cut -f1 )

	date=$(date -r $file_path)

	for vid_ext in ${time_ext[@]};
	do
		if [ "$vid_ext" == "$extension" ]; then
			time=$(ffmpeg -i $file_path 2>&1 | grep Duration | awk '{print $2}' | tr -d ,)
			break
		else
			time=-
		fi
	done

	echo "$file_name  $extension  $date  $size  $time"
	echo "$file_name$dlm$extension$dlm$date$dlm$size$dlm$time" >> data.csv
done
	
	ssconvert data.csv example.xls
rm data.csv