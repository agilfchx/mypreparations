#!/bin/bash

read -p "How many folders? " num_folders

for ((i = 1; i <= num_folders; i++)); do
    read -p "Enter name for folder $i: " folder_name
    
    mkdir -p "$folder_name"
    touch "$folder_name/users.txt"
    touch "$folder_name/passwords.txt"
    mkdir -p "$folder_name/interestings"
    mkdir -p "$folder_name/nmap"
    mkdir -p "$folder_name/fuzzing"

    echo "Folder $folder_name has been created with its files."
done

echo "Next step: Run these Nmap commands for each folder:"
echo "---"
echo "nmap -p- --max-retries 1 --max-scan-delay 20 -T4 -v --open -oN <folder_name>/nmap/Full_192.168.x.x.nmap --system-dns --stats-every 3s 192.168.x.x"
echo "nmap -sCV -p x --open -oN <folder_name>/nmap/Full_Extra_192.168.x.x.nmap --system-dns --stats-every 2s 192.168.x.x"

echo "---"
echo "After running the Nmap commands, you can perform directory fuzzing using the following commands:"
echo ""
echo "1. dirsearch:"
echo "   dirsearch -u http://192.168.x.x -e * -t 10 -o <folder_name>/fuzzing/dirsearch_results.txt --format=plain"
echo ""
echo "2. ffuf:"
echo "   ffuf -u http://192.168.x.x/FUZZ -w /path/to/wordlist.txt -c -v -ic -o <folder_name>/fuzzing/ffuf_results.txt"
echo ""
echo "3. gobuster:"
echo "   gobuster dir -u http://192.168.x.x -w /path/to/wordlist.txt -o <folder_name>/fuzzing/gobuster_results.txt"

echo ""
echo "Replace 'http://192.168.x.x' with the target IP or URL and specify the correct wordlist for fuzzing/scanning."
