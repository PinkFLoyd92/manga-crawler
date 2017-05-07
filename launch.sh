#/bin/sh
#pip install -r requirements.txt; 
DIRNAME = ""
function mangafox() {
    	(cd $DIRPROJECT && python main.py "$1" "$2" "$3" "$4");
}
