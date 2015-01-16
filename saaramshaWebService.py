import logging
logging.basicConfig(level=logging.DEBUG)
from spyne.application import Application
from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode
from spyne.model.complex import Iterable
from spyne.protocol.http import HttpRpc
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from spyne.util.simple import wsgi_soap_application
from spyne.model.primitive import UnsignedInteger
from spyne.model.primitive import String
from spyne.util.xml import get_object_as_xml
from spyne.protocol.xml import XmlDocument
#import MySQLdb
import requests
import json
import yaml
import subprocess
import logging
import re
import ftplib
from xml.dom.minidom import parseString

from petl import look, fromdb, tojson


class HelloWorldService(ServiceBase):

    @srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(name, times):

        logging.basicConfig(filename='C:\\Users\\Tejas\\Desktop\\example.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.warning('And this, too')

        # ResourcePath = "D:\\Work\\Projects\\Python\\Saaramsha_webService\\XMLText.xml"
        # ConfigFilePath = "D::\\Work\\Projects\\Python\\Saaramsha_webService\\ConfigFiles\\XMLConfig2.yml"
        # GenerateConfigCommand = "metl-generate --resource %s --headerRow 0 --skipRows 1 xml %s" % (ResourcePath, ConfigFilePath)
        # WriteToDbCommand = "metl %s" % ConfigFilePath

        logging.basicConfig(filename='C:\\Users\\Tejas\\Desktop\\example.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')

        # try:
        #    subprocess.call(GenerateConfigCommand, shell=True)
        #    with open(ConfigFilePath) as f:
        #        newDict = yaml.load(f)
        #        newDict['target']['type'] = 'Database'
        #        newDict['target']['url'] = 'mysql://root:q1w2e3r4@localhost:3306/metlDb'
        #        newDict['target']['table'] = 'authors'
        #        newDict['target']['createTable'] = True
        #    with open(ConfigFilePath, "w") as f:
        #        yaml.dump(newDict, f)
        #    subprocess.call(WriteToDbCommand, shell=True)
        #
        # except Exception as ex:
        #    return ex.Message



    @srpc(String, String, _returns=String)
    def ShowDisplay(name, times):
        
        ftp = ftplib.FTP('achumen.com', 'achumen', 'Ftp@2809')
        print "File List: "
        files = ftp.nlst('AchFileShare')
        yield files
#         ftp.cwd("/pub/unix") #changing to /pub/unix
#         headers = {'content-type': 'application/xml'}
#         r = requests.get('http://192.168.1.6:8080/jasperserver-pro/rest/resources/RelianceDatasource', auth=('reliance|reliance', 'reliance'), headers=headers)
#         regex = re.compile(r'[\n\r\t]')
#         newstr = regex.sub('', r.text)
#         anostr = newstr.replace('<![CDATA[', '')
#         anostr = anostr.replace(']]', '')
#         xmldoc = parseString(anostr)
#         for s in xmldoc.getElementsByTagName('resourceProperty'):
#             if s.getAttribute('name') == 'PROP_DATASOURCE_CONNECTION_URL':
#                 xyz = s.childNodes[0]
#         yield xmldoc

        

application = Application([HelloWorldService], tns='spyne.examples.hello', in_protocol=HttpRpc(validator='soft'), out_protocol=JsonDocument())

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.

    #wsgi_app = wsgi_soap_application([HelloWorldService], 'spyne.examples.hello.soap')
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
