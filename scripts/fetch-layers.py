import json,urllib.request,urllib.parse,pathlib,concurrent.futures,time
root=pathlib.Path('data/screening');root.mkdir(exist_ok=True)
def fetch(name,base,params):
 p=root/(name+'.json')
 if p.exists():return name,'cached'
 for attempt in range(2):
  try:
   with urllib.request.urlopen(base+'/query?'+urllib.parse.urlencode(params),timeout=45) as r:d=json.load(r)
   if d.get('error'):return name,d['error']
   p.write_text(json.dumps(d));return name,{'features':len(d.get('features',[])),'truncated':d.get('exceededTransferLimit') or d.get('properties',{}).get('exceededTransferLimit')}
  except Exception as e:
   if attempt:return name,str(e)
common={'f':'geojson','outFields':'*','outSR':4326,'returnGeometry':'true','resultRecordCount':2000}
params=dict(common,where="STATE='06' AND COUNTY='059'")
jobs=[('tracts','https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/10',params)]
sites=json.loads(pathlib.Path('data/sites.json').read_text());apns=set()
for s in sites:
 a=s['apn'].replace('-','').strip()
 if len(a)==8 and a.isdigit():apns.add(a)
for i in range(0,len(apns),30):
 batch=sorted(apns)[i:i+30];where='APN24 IN ('+','.join("'"+a+"'" for a in batch)+')';jobs.append(('zoning-'+str(i),'https://maps.scag.ca.gov/scaggis/rest/services/LDX/Zoning_poly_OR/MapServer/0',dict(common,where=where)))
for name,layer in [('flood','Floodplains'),('fire','Fire_Hazard_Severity_Zones_LRA'),('liquefaction','Liquefaction')]:jobs.append((name,'https://www.ocgis.com/arcpub/rest/services/Map_Layers/'+layer+'/MapServer/0',dict(common,where='1=1')))
with concurrent.futures.ThreadPoolExecutor(3) as pool:
 futures=[pool.submit(fetch,*j) for j in jobs]
 for f in concurrent.futures.as_completed(futures):print(f.result(),flush=True)
