if [ "$1" == "" ]; then
    >&2 echo "You must provide a version number (i.e. v0.3.2) or tag (i.e. latest)"
    exit 1
fi

python3 configure.py version $1
docker-compose pull dash
docker-compose up -d
