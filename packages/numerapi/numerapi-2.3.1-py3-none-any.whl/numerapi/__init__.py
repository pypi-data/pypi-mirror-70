import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'


from numerapi.numerapi import NumerAPI
from numerapi.signalsapi import SignalsAPI
