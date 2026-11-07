import csv,gzip,json,pathlib
p=pathlib.Path('data/screening');coords={}
with gzip.open(p/'ca_xwalk.csv.gz','rt') as f:
 for r in csv.DictReader(f):
  lat,lon=float(r['blklatdd']),float(r['blklondd'])
  if 33.25<=lat<=34.10 and -118.30<=lon<=-117.25:coords[r['tabblk2020']]=[lon,lat]
blocks=[]
with gzip.open(p/'ca_wac_S000_JT00_2023.csv.gz','rt') as f:
 for r in csv.DictReader(f):
  if r['w_geocode'] in coords:blocks.append({'geoid':r['w_geocode'],'coordinates':coords[r['w_geocode']],'jobs':int(r['C000'])})
(p/'jobs.json').write_text(json.dumps(blocks,separators=(',',':')))
print('Employment blocks:',len(blocks),'includes neighboring counties for complete 5-mile buffers')
