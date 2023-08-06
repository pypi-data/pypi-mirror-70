##############################################################
### Radiko                                                 ###
### Copyright © 2020 kokarare1212 All rights reserved.     ###
###                                                        ###
### This software is released under the Apache License 2.0 ###
### see http://www.apache.org/licenses/LICENSE-2.0         ###
##############################################################
from .Exception import *
from .Config import *
import xml.etree.ElementTree as ET
import base64, datetime, hashlib, math, os, random, subprocess, time, re, requests

class Radiko():

   authToken = None
   region = None
   version = "1.1.3"

   def __init__(self, regionId=None):

      if regionId is None:
         auth1_headers = {
            "X-Radiko-App": "pc_html5",
            "X-Radiko-App-Version": "0.0.1",
            "X-Radiko-User": "dummy_user",
            "X-Radiko-Device": "pc"
         }
      else:
         info = self._getRandomInfo()
         auth1_headers = {
            "User-Agent": info["userAgent"],
            "X-Radiko-App": "aSmartPhone7a",
            "X-Radiko-App-Version": info["appVersion"],
            "X-Radiko-User": info["userId"],
            "X-Radiko-Device": info["device"]
         }
      auth1_response = requests.get(AUTH1_URL, headers=auth1_headers)
      if auth1_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to authenticate auth1")
      auth1_response.encoding = "UTF-8"
      authToken = auth1_response.headers["X-Radiko-AuthToken"]
      keyLenght = int(auth1_response.headers["X-Radiko-KeyLength"])
      keyOffset = int(auth1_response.headers["X-Radiko-KeyOffset"])
      if regionId is None:
         partialKey = base64.b64encode(AUTHKEY[ keyOffset : keyOffset + keyLenght ].encode()).decode()
         auth2_headers = {
            "X-Radiko-AuthToken": authToken,
            "X-Radiko-PartialKey": partialKey,
            "X-Radiko-User": "dummy_user",
            "X-Radiko-Device": "pc"
         }
      else:
         partialKey = base64.b64encode(base64.b64decode(FULLKEY)[ keyOffset : keyOffset + keyLenght ])
         auth2_headers = {
            "User-Agent": info["userAgent"],
            "X-Radiko-App": "aSmartPhone7a",
            "X-Radiko-App-Version": info["appVersion"],
            "X-Radiko-User": info["userId"],
            "X-Radiko-Device": info["device"],
            "X-Radiko-AuthToken": authToken,
            "X-Radiko-PartialKey": partialKey,
            "X-Radiko-Connection": "wifi",
            "X-Radiko-Location": self._getLocation(regionId)
         }
      auth2_response = requests.get(AUTH2_URL, headers=auth2_headers)
      if auth2_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to authenticate auth2")
      auth2_response.encoding = "UTF-8"
      self.authToken = authToken
      self.region = auth2_response.text.split(",")[0]

   def _getLocation(self, regionId):
      lat = latlonList[regionId][0]
      lon = latlonList[regionId][1]
      lat = lat + random.random() / 40.0 * ( 1 if random.random() > 0.5 else -1)
      lon = lon + random.random() / 40.0 * ( 1 if random.random() > 0.5 else -1)
      return str(round(lat, 6)) + "," + str(round(lon, 6)) + ",gps"

   def _getRandomInfo(self):
      appVersion = random.choice(appVersionList)
      userId = ""
      for i in range(32):
         userId = userId + random.choice(userIdBase)
      ver = random.choice(list(versionMap.keys()))
      sdk = versionMap[ver]["sdk"]
      build = random.choice(versionMap[ver]["builds"])
      model = random.choice(modelList)
      device = sdk + "." + model
      userAgent = "Dalvik/2.1.0 (Linux; U; Android " + ver + "; " + model + "/" + build + ")"
      return {
         "appVersion": appVersion,
         "userId": userId,
         "userAgent": userAgent,
         "device": device
      }

   def changeRegion(self, regionId):
      info = self._getRandomInfo()
      auth1_headers = {
         "User-Agent": info["userAgent"],
         "X-Radiko-App": "aSmartPhone7a",
         "X-Radiko-App-Version": info["appVersion"],
         "X-Radiko-User": info["userId"],
         "X-Radiko-Device": info["device"]
      }
      auth1_response = requests.get(AUTH1_URL, headers=auth1_headers)
      if auth1_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to authenticate auth1")
      auth1_response.encoding = "UTF-8"
      authToken = auth1_response.headers["X-Radiko-AuthToken"]
      keyLenght = int(auth1_response.headers["X-Radiko-KeyLength"])
      keyOffset = int(auth1_response.headers["X-Radiko-KeyOffset"])
      partialKey = base64.b64encode(base64.b64decode(FULLKEY)[ keyOffset : keyOffset + keyLenght ])
      auth2_headers = {
         "User-Agent": info["userAgent"],
         "X-Radiko-App": "aSmartPhone7a",
         "X-Radiko-App-Version": info["appVersion"],
         "X-Radiko-User": info["userId"],
         "X-Radiko-Device": info["device"],
         "X-Radiko-AuthToken": authToken,
         "X-Radiko-PartialKey": partialKey,
         "X-Radiko-Connection": "wifi",
         "X-Radiko-Location": self._getLocation(regionId)
      }
      auth2_response = requests.get(AUTH2_URL, headers=auth2_headers)
      if auth2_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to authenticate auth2")
      auth2_response.encoding = "UTF-8"
      self.authToken = authToken
      self.region = auth2_response.text.split(",")[0]

   def getStationList(self):
      station_response = requests.get(STATION_BASE + self.region + ".xml")
      station_response.encoding = "UTF-8"
      stationList = ET.fromstring(station_response.text)
      stations = []
      for s in stationList:
         stations.append(s[0].text)
      return stations

   def getStationDetail(self, stationId):
      station_response = requests.get(STATION_BASE + self.region + ".xml")
      station_response.encoding = "UTF-8"
      if station_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to get station detail")
      stationList = ET.fromstring(station_response.text)
      station = {}
      station["id"] = None
      station["name"] = None
      station["ascii"] = None
      station["ruby"] = None
      station["areafree"] = None
      station["timefree"] = None
      station["logo"] = {}
      station["logo"]["224x100"] = None
      station["logo"]["258x60"] = None
      station["logo"]["448x200"] = None
      station["logo"]["688x160"] = None
      station["logo"]["224x100"] = None
      station["logo"]["258x60"] = None
      station["logo"]["448x200"] = None
      station["logo"]["688x160"] = None
      station["logo"]["banner"] = None
      station["web"] = None
      station["tf"] = None
      for s in stationList:
         if s[0].text == stationId:
            station["id"] = s[0].text
            station["name"] = s[1].text
            station["ascii"] = s[2].text
            station["ruby"] = s[3].text
            station["areafree"] = s[4].text
            station["timefree"] = s[5].text
            station["logo"]["224x100"] = s[6].text
            station["logo"]["258x60"] = s[7].text
            station["logo"]["448x200"] = s[8].text
            station["logo"]["688x160"] = s[9].text
            station["logo"]["224x100"] = s[10].text
            station["logo"]["258x60"] = s[11].text
            station["logo"]["448x200"] = s[12].text
            station["logo"]["688x160"] = s[13].text
            station["logo"]["banner"] = s[14].text
            station["web"] = s[15].text
            station["tf"] = s[16].text
            return station
      return station

   def getPrograms(self, station=None, d=datetime.datetime.now().strftime('%Y%m%d'), query=None):
      if re.search(r"\d{8}", d) is None:
         raise RadikoException("Invalied aragments")
      program_response = requests.get(PROGRAM_BASE + d + "/" + self.region + ".xml")
      program_response.encoding = "UTF-8"
      list1 = ET.fromstring(program_response.text)[2]
      
      if query is None:
         list2 = {}
         for li1 in list1:
            if not station is None and li1.attrib["id"] != station:
               continue
            list2[li1.attrib["id"]] = []
            for li2 in li1:
               i = True
               for li3 in li2:
                  if i:
                     i = False
                     continue
                  list2[li1.attrib["id"]].append({"start": li3.attrib["ft"], "end": li3.attrib["to"], "title": li3[0].text, "url": li3[1].text, "info": li3[6].text, "pfm": li3[7].text, "img": li3[8].text, li3[9][0].attrib["name"]: li3[9][0].attrib["value"]})
      else:
         list2 = {}
         for li1 in list1:
            if not station is None and li1.attrib["id"] != station:
               continue
            for li2 in li1:
               i = True
               for li3 in li2:
                  if i:
                     i = False
                     continue
                  if not re.search(query, li3[0].text) is None:
                     list2[li1.attrib["id"]] = []
                     list2[li1.attrib["id"]].append({"start": li3.attrib["ft"], "end": li3.attrib["to"], "title": li3[0].text, "url": li3[1].text, "info": li3[6].text, "pfm": li3[7].text, "img": li3[8].text, li3[9][0].attrib["name"]: li3[9][0].attrib["value"]})
      return list2

   def downloadProgram(self, station, start, end, path):
      if re.search(r"\d{14}", start) is None or re.search(r"\d{14}", end) is None:
         raise RadikoException("Invalied aragments")
      playlistm3u8_headers = {
         "X-Radiko-AuthToken": self.authToken
      }
      playlistm3u8_response = requests.get(M3U8_BASE + "?station_id=" + station + "&l=15&ft=" + start + "&to=" + end, headers=playlistm3u8_headers)
      playlistm3u8_response.encoding = "UTF-8"
      if playlistm3u8_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to get playlist")
      for text in playlistm3u8_response.text.split("\n"):
         if text.startswith("https://"):
            chunklistm3u8_url = text
            break
      chunklistm3u8_response = requests.get(chunklistm3u8_url)
      chunklistm3u8_response.encoding = "UTF-8"
      if chunklistm3u8_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to get chunklist")
      audio = b""
      for text in chunklistm3u8_response.text.split("\n"):
         if text.startswith("https://"):
            while True:
               try:
                  audio_response = requests.get(text)
                  break
               except:
                  continue
            audio_response.encoding = "UTF-8"
            audio = audio + audio_response.content
      with open(path, "wb") as f:
         f.write(audio)

   def getLiveStationStreamUrls(self, station):
      streambase_response = requests.get(STREAM_BASE + station + ".xml")
      streambase_list = ET.fromstring(streambase_response.text)
      streamUrl = streambase_list[0][0].text
      a_exp = hashlib.md5(str(math.floor(random.random() * 1000000000) + math.floor(time.time())).encode()).hexdigest()
      stream_headers = {
         "X-Radiko-AuthToken": self.authToken
      }
      stream_response = requests.get(streamUrl + "?station_id=" + station + "&l=15&lsid=" + a_exp + "&type=b", headers=stream_headers)
      stream_response.encoding = "UTF-8"
      if stream_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to get playlist")
      m3u8_url = None
      for text in stream_response.text.split("\n"):
         if text.startswith("https://") or text.startswith("http://"):
            m3u8_url = text
            break
      if m3u8_url is None:
         raise RadikoException("Failed to get m3u8 url")
      m3u8_response = requests.get(m3u8_url)
      if m3u8_response.status_code != requests.codes.ok:
         raise RadikoException("Failed to get m3u8")
      streamUrls = []
      for text in m3u8_response.text.split("\n"):
         if text.startswith("https://") or text.startswith("http://"):
            streamUrls.append(text)
      return streamUrls

   def getAuthToken(self):
      return self.authToken

   def getRegion(self):
      return self.region

   def getVersion(self):
      return self.version