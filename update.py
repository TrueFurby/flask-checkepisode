from tvchecker.models import *
from updater import *
import os, sys
import urllib

def getSeriesXml(serID):
    if serID:
        filehandle = urllib.urlopen('%sapi/%s/series/%s/en.xml' % (MIRROR, API_KEY, serID))
        tvxml = et.fromstring(filehandle.read())
        return tvxml.find('Series')
    return None

def getEpisodeXml(epID):
    if epID:
        filehandle = urllib.urlopen('%sapi/%s/episodes/%s/en.xml' % (MIRROR, API_KEY, epID))
        tvxml = et.fromstring(filehandle.read())
        return tvxml.find('Episode')
    return None

updFile = open('lastupdate', 'r')
last_update = int(updFile.readline())
updFile.close()

print "Retrieving update, last update = %s" % last_update
print "---------------------------------------"
filehandle = urllib.urlopen('%sapi/Updates.php?type=all&time=%s' % (MIRROR, last_update))
tvxml = et.fromstring(filehandle.read())

new_update = tvxml.findtext("Time")
series_updates = tvxml.findall('Series')
episode_updates = tvxml.findall('Episode')

print "%d series updates\n%d episode updates" % (len(series_updates), len(episode_updates))

for s in series_updates:
    print "---------------------------------------"
    print "Checking series, id = %s" % s.text
    series = Series.query.filter_by(tvdb_id=s.text).first()
    if series:
        updateSeries(series, getSeriesXml(s.text))
    else:
        print "Series not in database"
        
for e in episode_updates:
    print "---------------------------------------"
    #print "Checking episode, id = %s" % e.text
    updateEpisode(getEpisodeXml(e.text))

print "---------------------------------------"
print "Saving update time = %s" % new_update
updFile = open('lastupdate', 'w+')
updFile.write(new_update)
updFile.close()