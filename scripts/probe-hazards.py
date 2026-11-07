import urllib.request,urllib.parse,json,concurrent.futures
urls={
'county-json':'https://www.ocgis.com/arcpub/rest/services/Map_Layers/Floodplains/MapServer/0/query?'+urllib.parse.urlencode({'f':'json','where':'1=1','outFields':'*','returnGeometry':'false','resultRecordCount':1}),
'county-no-www':'https://ocgis.com/arcpub/rest/services/Map_Layers/Fire_Hazard_Severity_Zones_LRA/MapServer/0/query?'+urllib.parse.urlencode({'f':'geojson','where':'1=1','outFields':'*','outSR':'4326','resultRecordCount':1000}),
'scag-flood':'https://maps.scag.ca.gov/scaggis/rest/services/OpenData/ENV_Flood_Zones_PL_SCAG/MapServer?f=json',
'fire-current':'https://services.arcgis.com/jIL9msH9OI208GCb/arcgis/rest/services?f=json',
'landslide':'https://services2.arcgis.com/zr3KAIbsRSUyARHG/arcgis/rest/services/CGS_Landslide_Zones/FeatureServer/0?f=json'}
def run(kv):
 k,u=kv
 try:
  with urllib.request.urlopen(u,timeout=20) as r:d=json.load(r)
  if k=='county-no-www':open('data/screening/fire.json','w').write(json.dumps(d));return k,str(d)[:300]
  return k,str(d)[:2500]
 except Exception as e:return k,str(e)
with concurrent.futures.ThreadPoolExecutor(4) as p:
 for f in concurrent.futures.as_completed([p.submit(run,i) for i in urls.items()]):print(f.result(),flush=True)
