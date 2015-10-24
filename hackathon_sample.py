#!/usr/bin/python

import json
import urllib2
import base64
import zlib

# Overall WS Access Variables
dbsAlias = 'xTD150'
wsHost = 'dragon.teradata.ws'
wsPort =  '1080'
path = '/tdrest/systems/' + dbsAlias + '/queries'



def rest_request ( query ,wsUser,wsPass):
    url = 'http://' + wsHost + ':' + wsPort + path
   
    headers={}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.com.teradata.rest-v1.0+json'
    headers['Authorization'] = "Basic %s" % base64.encodestring('%s:%s' % (wsUser, wsPass)).replace('\n', '');

    # Set query bands
    queryBands = {}
    queryBands['applicationName'] = 'MyApp'
    queryBands['version'] = '1.0'

    # Set request fields. including SQL
    data = {}
    data['query'] = query
    data['queryBands'] = queryBands
    data['format'] = 'array'

    # Build request.
    request = urllib2.Request(url, json.dumps(data), headers)

    #Submit request
    try:
        response = urllib2.urlopen(request);
        # Check if result have been compressed.
        if response.info().get('Content-Encoding') == 'gzip':
            response = zlib.decompress(response.read(), 16+zlib.MAX_WBITS)
        else:
            response = response.read();
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        response = e.read();
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
        response = e.read();

    # Parse response to confirm value JSON.
    results = json.loads(response);

    list = results.get(u'results')[0].get(u'data')
    sum = 0
    for x in range (0,len(list)-1):
            sum += list[x][0]

#    print json.dumps(results, indent=4, sort_keys=True) 

    return sum

def perform_query( query, wsUser, wsPass ):
    i = rest_request(query, wsUser, wsPass)
    
    return i;

wsUser = 'hack_user02'
wsPass = 'tdhackathon'

weapon = ''
typeOfWeapon = ["All firearms", "Handguns", "Rifles", "Shotguns", "Other guns", "Other Firearms", "Knives", "Blunt objects", "Personal weapons", "Poison", "Exposives", "Fire", "Narcotics", "Drowning", "Strangualtion", "Asphyxiation", "Other"]
while weapon not in typeOfWeapon:
        weapon = raw_input('Choose a weapon: '+', '.join(typeOfWeapon) + '\n')

if weapon == 'Other Firearms':
        weaponSum = perform_query ( 'select "Firearms, type not stated" from crime_data.murders_by_weapon_type', wsUser, wsPass)
elif weapon == 'All firearms':
        weaponSum = perform_query ( 'select "Total by Firearms" from crime_data.murders_by_weapon_type', wsUser, wsPass)
elif weapon == 'Other guns':
        weaponSum = perform_query ( 'select "Other guns" from crime_data.murders_by_weapon_type', wsUser, wsPass)
elif weapon == 'Blunt objects':
        weaponSum = perform_query ( 'select "Blunt objects" from crime_data.murders_by_weapon_type', wsUser, wsPass)
elif weapon == 'Personal weapons':
        weaponSum = perform_query ( 'select "Personal weapons" from crime_data.murders_by_weapon_type', wsUser, wsPass)
else:
        weaponSum = perform_query ( 'select ' + weapon + ' from crime_data.murders_by_weapon_type', wsUser, wsPass)
        

murderSum = perform_query ( 'select "Total Murders" from crime_data.murders_by_weapon_type', wsUser, wsPass)

proportion = weaponSum*1.0/murderSum
percentage = round(proportion * 100,4)

print('If you die, there is a ' + str(percentage) + '% chance that ' + str(weapon) + ' is what killed you. D:')
