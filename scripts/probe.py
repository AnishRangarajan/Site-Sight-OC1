import json,urllib.request,concurrent.futures
urls={
'parcels':'https://www.ocgis.com/arcpub/rest/services/Map_Layers/Parcels/FeatureServer/0?f=pjson',
'flood':'https://www.ocgis.com/arcpub/rest/services/Map_Layers/Floodplains/MapServer/0?f=pjson',
'fire':'https://www.ocgis.com/arcpub/rest/services/Map_Layers/Fire_Hazard_Severity_Zones_LRA/MapServer/0?f=pjson',
'zoning':'https://maps.scag.ca.gov/scaggis/rest/services/LDX/Zoning_poly_OR/MapServer?f=pjson',
'census':'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer?f=pjson'}
def probe(kv):
 k,u=kv
 try:
  d=json.load(urllib.request.urlopen(u,timeout=40));return k,{x:d.get(x) for x in ['name','fields','layers','description','extent','error']}
 except Exception as e:return k,str(e)
for k,v in concurrent.futures.ThreadPoolExecutor(4).map(probe,urls.items()):print(k,json.dumps(v))
