if [ `whoami` != root ]; then
    echo Please run this script as root or using sudo
    exit
fi

cp code/* /bin
