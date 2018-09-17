''' program to turn a socket on and off '''
''' change device_id as necessary '''
import config
import utils

gu = utils.GeniusUtility(config.HG_SIG)

device_id = 23

# Turn socket on
gu.putjson('/zones/' + str(device_id) + '/mode', 'override')


# Turn socket off
gu.putjson('/zones/' + str(device_id) + '/mode', 'off')
