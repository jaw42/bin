#!/bin/sh
# Print a list of packages that no other package depends on

PackageCount=0
PackageIter=0

# Populate package array
declare -A Packages
PackageList=$(cygcheck.exe -c | cut -d' ' -f1 | tail -n +3)
for P in $PackageList; do
    Packages[${P,,}]=0
    PackageCount=$PackageCount+1
done

# Determine the last mirror used
LastMirror=$(sed -n '/last-mirror/{n;p}' /etc/setup/setup.rc | tr -d '\t')
echo "[DEBUG] LastMirror = $LastMirror"

# Download the setup.ini file from the mirror server
echo "[DEBUG] Downloading setup.ini from mirror"
#wget --quiet "${LastMirror}setup.ini" -O setup.ini
curl -s "${LastMirror}/x86_64/setup.ini" > setup.ini

for P in $PackageList; do
    PackageIter=$PackageIter+1
    echo -ne "[DEBUG] Processing packages $((((PackageIter * 100) / PackageCount)))%\r"

    deps=$(sed -n "/^@ $P$/,/^requires/p" setup.ini | grep -i '^requires' | cut -d' ' -f2-)

    for dep in $deps; do
        if [[ ${Packages[${dep,,}]} ]]; then
            Packages[${dep,,}]=${Packages[${dep,,}]}+1
        fi
    done
done

echo -e "\n== Packages =="

for P in $PackageList; do
    if [[ ${Packages[${P,,}]} == 0 ]]; then
        echo $P
    fi
done

rm setup.ini
