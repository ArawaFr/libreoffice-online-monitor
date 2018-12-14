import argparse

DEFAULT = {
    'directory': '/opt/loolmonitor',
    'user': 'admin',
    'password': 'admin',
    'server' : 'localhost',
#    'webscript': 'http://localhost:8080/alfresco/s/',
    'host': None,
    'port': 8765,
    'use_ssl': False,
    'fullchain' : 'fullchain.pem',
    'privatekey' : 'privatekey',
    'logconf': 'logging.conf'
}

configs = {}

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
# config file as parameter
parser.add_argument("-c", "--config", help="config file")
args = parser.parse_args()


# config file parser
import configparser
config = configparser.ConfigParser()

# read config file
config.read(args.config)

configs["directory"] = config.get('LOOLMONITOR','directory') or DEFAULT["directory"]
configs["server"] = config.get('LOOLMONITOR','server') or DEFAULT["server"]
configs["webscript"] = 'https://'+configs["server"]+'/alfresco/s/'
configs["user"] = config.get('LOOLMONITOR','username') or DEFAULT["user"]
configs["password"] = config.get('LOOLMONITOR','password') or DEFAULT["password"]
configs["host"] = config.get('LOOLMONITOR','host') or DEFAULT["host"]
configs["port"] = config.get('LOOLMONITOR','port') or DEFAULT["port"]
configs["use_ssl"] = config.get('SSL','ssl') or DEFAULT["use_ssl"]
configs["privatekey"] = configs["directory"]+'/'+config.get('SSL','privatekey') or configs["directory"]+'/'+DEFAULT["privatekey"]
configs["fullchain"] = configs["directory"]+'/'+config.get('SSL','fullchain') or configs["directory"]+'/'+DEFAULT["fullchain"]
configs["logging"] = configs["directory"]+'/'+config.get('LOOLMONITOR','logconf') or configs["directory"]+'/'+DEFAULT["logconf"]

