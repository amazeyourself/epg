import urllib3
import xml.etree.ElementTree as ET
import json
import gzip

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself/m3u')
for i in [1,2,3,4,7]:
    resp = urllib3.request("GET", f"https://www.kableone.com/LiveTV/GetLiveTvChannelsForCategory?categoryId={i}")
    epgdata = resp.json()
    for channel in epgdata['data']:
        chnl = ET.SubElement(root, 'channel')
        chnl.set('id', str(channel['tvId']))
        dspl = ET.SubElement(chnl, 'display-name')
        icon = ET.SubElement(chnl, 'icon')
        dspl.text = channel['tvName']
        ico = channel['url']
        icon.set('src', ico)
        programlist = channel['programmes']
        epgid = str(channel['tvId'])
        for prg in programlist:
            start = prg['fromDate'].replace('-', '').replace(':', '') + ' +0530'
            stop = prg['toDate'].replace('-', '').replace(':', '') + ' +0530'
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start)
            prog.set('stop', stop)
            title = prg['programmeName']
            prgtitle = ET.SubElement(prog, 'title')
            prgtitle.text = title


xml_data = ET.tostring(root)

with open('./epg/kableone.xml', 'wb') as f:
    f.write(xml_data)
    print("Exported!")
f.close()

with gzip.open('./epg/kableone.xml.gz', 'wb') as f:
    f.write(xml_data)
f.close()
