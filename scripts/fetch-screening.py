import json,urllib.request,urllib.parse,pathlib,concurrent.futures
root=pathlib.Path('data/screening');root.mkdir(exist_ok=True)
def fetch(name,url):
 p=root/name
 if p.exists():return name,p.stat().st_size
 try:
  with urllib.request.urlopen(url,timeout=60) as r:p.write_bytes(r.read())
  return name,p.stat().st_size
 except Exception as e:return name,str(e)
urls={
'parcel-sample.json':'https://www.ocgis.com/arcpub/rest/services/Map_Layers/Parcels/FeatureServer/0/query?'+urllib.parse.urlencode({'f':'json','where':"ASSESSMENT_NO IN ('405-262-25','40526225')",'outFields':'*','outSR':4326,'returnGeometry':'true'}),
'zoning-fields.json':'https://maps.scag.ca.gov/scaggis/rest/services/LDX/Zoning_poly_OR/MapServer/0?f=pjson',
'census-fields.json':'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Tracts_Blocks/MapServer/10?f=pjson',
'ca_wac_S000_JT00_2023.csv.gz':'https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_S000_JT00_2023.csv.gz',
'ca_xwalk.csv.gz':'https://lehd.ces.census.gov/data/lodes/LODES8/ca/ca_xwalk.csv.gz'}
for k,result in concurrent.futures.ThreadPoolExecutor(4).map(lambda kv:fetch(*kv),urls.items()):print(k,result,flush=True)
