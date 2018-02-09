''' program to print active zone ID's '''
import config
import utils


gu = utils.GeniusUtility(config.HG_URL, config.HG_SIG, True)

# Get the data
whole_house = gu.GETJSON(0)
zone_list = gu.getzonelist(whole_house)

for zone in sorted(zone_list):
    key = zone_list[zone]['key']
    print(str(key).zfill(2), zone)
