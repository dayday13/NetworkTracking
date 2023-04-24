import dpkt
import socket
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat') #a database that is used to translate an IP address into a Geo location(longitude & latitude)

def retKML(dstip, srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('10.0.0.10') #change to your computer ip
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = ( #creats the record with all the details
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n' #that's the style that tells google maps that we want a line instead of dots for example
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

def plotIPs(pcap):
    kmlPts ='' #start with empty variable
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src) #translates the ip adderess into geo location
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts

def main():
    
    file = open('wiresharkCapture.pcap', 'rb') # rb - opens in binary format
    pcap = dpkt.pcap.Reader(file)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n <kmlxmlns="http://www.opengis.net/kml/2.2:>\n<Document>\n'\
        '<Style id-"transBluePoly">'\
            '<LineStyle>'\
            '<width>2.0</width>'\
                '<color>501400E6</color>'\
                    '</ineStyle>'\
                        '</Style>' #kml file is something that we can put to google maps and it will know how to read it, search for kml files styling to change the style if you like
    kmlfooter = '<Document>\n</kml>\n' #closing text that we opend
    kmldoc = kmlheader + plotIPs(pcap) + kmlfooter #plotIPs def is the content of the file we opened
    print(kmldoc)
    
if __name__ == '__main__':
    main()