import urllib.request,urllib.parse,json,pathlib
base='https://maps.scag.ca.gov/scaggis/rest/services/OpenData/ENV_Flood_Zones_PL_SCAG/MapServer/0'
features=[]
for offset in range(0,10000,500):
 q={'f':'geojson','where':'1=1','geometry':'-118.13,33.38,-117.4,33.96','geometryType':'esriGeometryEnvelope','inSR':4326,'outSR':4326,'spatialRel':'esriSpatialRelIntersects','outFields':'*','resultOffset':offset,'resultRecordCount':500,'orderByFields':'OBJECTID'}
 d=json.load(urllib.request.urlopen(base+'/query?'+urllib.parse.urlencode(q),timeout=45))
 if d.get('error'):raise RuntimeError(str(d['error']))
 features+=d['features'];print('Flood features',len(features),flush=True)
 if not (d.get('exceededTransferLimit') or d.get('properties',{}).get('exceededTransferLimit')):
  pathlib.Path('data/screening/flood-scag.json').write_text(json.dumps({'type':'FeatureCollection','features':features,'sourceUrl':base,'vintage':'2020 RTP/SCS input; historical screening only'}));break
else:raise RuntimeError('Incomplete paging')
