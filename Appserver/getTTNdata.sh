#gets all data from specified time in $2
if [ $1 == 'query' ]
     then
	curl -X GET --header 'Accept: application/json' --header 'Authorization: key ttn-account-v2.d7Q2pGiB97SPJFjr_WphmoaZKctmJRE93MhC6T9rP-g' 'https://htwg-konstanz-testapp.data.thethingsnetwork.org/api/v2/query?last='$2
fi

#lists all deviced of app
if [ $1 == 'devices' ]
     then
	curl -X GET --header 'Accept: application/json' --header 'Authorization: key ttn-account-v2.d7Q2pGiB97SPJFjr_WphmoaZKctmJRE93MhC6T9rP-g' 'https://htwg-konstanz-testapp.data.thethingsnetwork.org/api/v2/devices'
fi

#gets all data from specified time in $3 from device $2
if [ $1 == 'device-id' ]
     then
	curl -X GET --header 'Accept: application/json' --header 'Authorization: key ttn-account-v2.d7Q2pGiB97SPJFjr_WphmoaZKctmJRE93MhC6T9rP-g' 'https://htwg-konstanz-testapp.data.thethingsnetwork.org/api/v2/query/'$2'?last='$3
fi
