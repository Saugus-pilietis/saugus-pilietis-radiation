import requests
import json
from influxdb import InfluxDBClient
import pprint

host = os.getenv("INFLUXDB_HOST")
port = os.getenv("INFLUXDB_PORT")
username = os.getenv("INFLUXDB_USER")
password = os.getenv("INFLUXDB_PASS")
client = InfluxDBClient(host, port, username, password)

client.switch_database('sauguspilietis')

stations = '{"LT21072": "Kybartai", "BY26825": "Grodno", "LT21064": "Kedainiai", "LT21065": "Mazeikiai", "LT20461": "Rusne", "LT20460": "Raipole", "LT20466": "Smalininkai", "LT20465": "Buivydziai", "LT21063": "Ukmerge", "LT20408": "Rimse", "LV0012": "Daugavpils(Rainastreet)", "LV0010": "Liepaja", "LV0017": "Jelgava", "LV0015": "Daugavpils(Udensvadastreet)", "LV0019": "Medumi", "LV0018": "Silene", "BY26748": "Volojin", "LT21054": "Dubininkas", "LT20394": "Turmantas", "BY26649": "Napoc\'", "LT21051": "Medininkai", "LT21050": "Svencionys", "BY26832": "Lida", "LT21075": "Pagegiai", "BY26745": "Vileika", "LT21052": "Adutiskis", "LT21078": "Raseiniai", "LT21077": "Kaltinenai", "LT21076": "Plateliai", "LT20414": "Rugsteliskis", "LT21074": "Panevezys", "LT20412": "Utena", "LT20413": "Paluse", "LT21071": "Joniskis", "LT21070": "Birzai", "LT21053": "Dieveniskes", "RU26711": "Chernyakhovsk", "LV0001": "Demene", "BY26643": "Sarkovqina", "RU26614": "Sovetsk", "LT20364": "Klaip\\u0117da", "LT20365": "Vilnius", "LT20366": "Alytus", "LT20367": "Visaginas", "LV0013": "Baldone(1Radons)", "LT21073": "Lazdijai", "LV0022": "Baldone(2Parupes)", "LT21046": "Elektrenai", "LT21047": "Turgeliai", "LT21044": "Sirvintos", "LT21043": "Salcininkai", "LT21041": "Moletai", "LT0248": "Siauliai", "LT0249": "Kaunas", "PL0015": "Suwalki", "LT21055": "Pavovere", "LT21048": "Kalveliai", "LT21049": "Valkininkai"}'
station_id = (json.loads(stations))

data_for_database = []

stationInfo = {}

for station in station_id:
    res = requests.get('https://rewidget.jrc.ec.europa.eu/v3/objects/point?id='+str(station)+'')
    stationJSON = res.json()
    pprint.pprint(stationJSON)
    stationInfo[station] = {'avg' : json.dumps(stationJSON['avg']['val']), 'max' : json.dumps(stationJSON['max']['val'])}
    print "First"
    print stationJSON.keys()
    values = {}

    for key in stationJSON.keys():
        if key == 'footer':
            continue
        else:
            values[key] = str(stationJSON[key]['val'])

    data_for_database.append({
        "measurement": "radiationLevel",
        "tags": {
            "id": station,
            "name": station_id[station]
        },
        "fields": values
    })

stationDetails = json.dumps(stationInfo)

client.write_points(data_for_database)


