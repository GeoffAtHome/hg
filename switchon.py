''' program to print active zone ID's '''
import config
import utils

# gu = utils.GeniusUtility(config.HG_URL, config.HG_SIG, True)
gu = utils.GeniusUtility(config.HG_URL, config.HG_SIG)

ZONE = 23

# gu.SOCKET_ON(ZONE, 900)
# gu.SOCKET_OFF(ZONE)
gu.CLEAR_TIMER(ZONE)
