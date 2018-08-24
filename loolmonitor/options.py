import os.path
import argparse

DEFAULT = {
    'user' : 'admin',
    'password' : 'admin',
    'webscript' : 'http://localhost:8080/alfresco/s/'
}

configs = {}

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-w", "--webscript_uri", help="Alfresco webscript base url (default: {})".format(DEFAULT["webscript"]))
parser.add_argument("-u", "--user", help="Alfresco user account (default: {})".format(DEFAULT["user"]))
parser.add_argument("-p", "--password", help="Alfresco password account (default: {})".format(DEFAULT["password"]))
args = parser.parse_args()

configs["webscript"] = args.webscript_uri or DEFAULT["webscript"]
configs["user"] = args.user or DEFAULT["user"]
configs["password"] = args.password or DEFAULT["password"]
