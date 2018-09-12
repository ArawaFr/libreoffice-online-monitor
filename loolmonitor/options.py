import argparse

DEFAULT = {
    'user': 'admin',
    'password': 'admin',
    'webscript': 'http://localhost:8080/alfresco/s/',
    'host': None,
    'port': 8765,
    'ssl': False
}

configs = {}

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-w", "--webscript_uri",
                    help="Alfresco webscript base url (default: {})"
                    .format(DEFAULT["webscript"]))
parser.add_argument("-u", "--user",
                    help="Alfresco user account (default: {})"
                    .format(DEFAULT["user"]))
parser.add_argument("-p", "--password",
                    help="Alfresco password account (default: {})"
                    .format(DEFAULT["password"]))
parser.add_argument("-H", "--host",
                    help="Monitor host (default: {})"
                    .format(DEFAULT["host"]))
parser.add_argument("-P", "--port",
                    help="Monitor port (default: {})"
                    .format(DEFAULT["port"]))
parser.add_argument("-S", "--ssl",
                    help="ssl (true|false) (default: {})"
                    .format(DEFAULT["ssl"]))
args = parser.parse_args()

configs["webscript"] = args.webscript_uri or DEFAULT["webscript"]
configs["user"] = args.user or DEFAULT["user"]
configs["password"] = args.password or DEFAULT["password"]
configs["host"] = args.host or DEFAULT["host"]
configs["port"] = args.port or DEFAULT["port"]
configs["ssl"] = args.ssl or DEFAULT["ssl"]
