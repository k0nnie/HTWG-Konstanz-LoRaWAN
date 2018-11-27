function start_rec() {
	screen -dmSL test python3 receiver.py
	}

function end_rec() {
	screen -S test -X quit
}


if [ $1 == "startrec" ]
     then
	start_rec
fi

if [ $1 == "stoprec" ]
     then
	end_rec
fi
