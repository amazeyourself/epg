import urllib3
import json
from datetime import datetime, time, timedelta
import xml.etree.ElementTree as ET
import gzip

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself')

filters = [3, 10, 1, 7, 5, 4, 19, 20, 18]
channels = []
for fi in filters:
    resp = urllib3.request(
        "GET",
        f"https://prod-epg-sec.runn.tv/runtv/v4/schedule/getEpgByFilters/{fi}",
        headers={
            "Partner_code": "ALL",
            "Referer": "https://runn.tv/",
            "X-Tenant-Id": "runn",
            "Userid": "8C-EB-8C-42-E7-E2",
            "Runn-Api-Key": "pXh1VC0Asx9Wy+D7AaicqJruRZFJYulegB4SMSrvGM9G4veO0VZfpgFhR6sJkXaPAkkbIhg59Pq8vA7li0YZ"
        }
    )
    channeldata = resp.json()
    print("filter: " + str(fi))
    for i in channeldata:
        epgid = i['id']
        chnlname = i['title']
        imglocation = i['baseSourceLocation']
        img = imglocation + i['images']['logo']['tv']
        if chnlname not in channels:
            print(chnlname)
            chnl = ET.SubElement(root, 'channel')
            chnl.set('id', str(epgid))
            dspl = ET.SubElement(chnl, 'display-name')
            icon = ET.SubElement(chnl, 'icon')
            dspl.text = chnlname
            icon.set('src', img)
            schedule = i['schedules']
            for prg in schedule:
                startepoch = prg['startTime'] / 1000
                start = datetime.fromtimestamp(startepoch)
                duration = prg['durationSeconds']
                stop = start + timedelta(seconds=duration)
                prog = ET.SubElement(root, 'programme')
                prog.set('channel', str(epgid))
                prog.set('start', start.strftime('%Y%m%d%H%M%S +0530'))
                prog.set('stop', stop.strftime('%Y%m%d%H%M%S +0530'))
                prog.set('catchup-id', prg['id'])
                title = prg['programName']
                if 'description' in prg:
                    desc = prg['description']
                else:
                    desc = ""
                if 'tv' in prg['infoImages']:
                    thumb = imglocation + prg['infoImages']['tv']
                elif 'web' in prg['infoImages']:
                    thumb = imglocation + prg['infoImages']['web']
                elif 'mobile' in prg['infoImages']:
                    thumb = imglocation + prg['infoImages']['mobile']
                prgtitle = ET.SubElement(prog, 'title')
                prgtitle.text = title
                prgdesc = ET.SubElement(prog, 'desc')
                prgdesc.text = desc
                if prg['genres'] != []:
                    category = ET.SubElement(prog, 'category')
                    category.text = prg['genres'][0]['name']

                if prg['audioLanguages'] != []:
                    language = ET.SubElement(prog, 'language')
                    language.text = prg['audioLanguages'][0]['name']
                    
                prgico = ET.SubElement(prog, 'icon')
                prgico.set("src", thumb)
                rating = ET.SubElement(prog, 'rating')
                ratvalue = ET.SubElement(rating, 'value')
                ratvalue.text = prg['ageRating']
            channels.append(chnlname)

xml_data = ET.tostring(root)

with open('./epg/runntv.xml', 'wb') as f:
    f.write(xml_data)
f.close()

with gzip.open('./epg/runntv.xml.gz', 'wb') as f:
    f.write(xml_data)
f.close()
