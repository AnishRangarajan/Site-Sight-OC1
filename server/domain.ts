import type { Site } from '../src/types';
export const cities=['Aliso Viejo','Anaheim','Brea','Buena Park','Costa Mesa','Cypress','Dana Point','Fountain Valley','Fullerton','Garden Grove','Huntington Beach','Irvine','La Habra','La Palma','Laguna Beach','Laguna Hills','Laguna Niguel','Laguna Woods','Lake Forest','Los Alamitos','Mission Viejo','Newport Beach','Orange','Placentia','Rancho Santa Margarita','San Clemente','San Juan Capistrano','Santa Ana','Seal Beach','Stanton','Tustin','Villa Park','Westminster','Yorba Linda'];
export function area(raw:string):number|null { const clean=raw.trim().replaceAll(',',''); const match=clean.match(/^(\d+(?:\.\d+)?)\s*(SF|SQ\.?\s*FT\.?|ACRES?|AC)?$/i); if(!match)return null; const n=Number(match[1]); return n>0?n/(match[2]&&/SF|SQ/i.test(match[2])?43560:1):null; }
export function date(raw:string):string|null { const m=raw.trim().match(/^(\d{2})-(\d{2})-(\d{4})$/); if(!m)return null;const d=`${m[3]}-${m[1]}-${m[2]}`;return Number.isNaN(Date.parse(d))?null:d; }
export function availability(raw:string,due:string|null,today:string):Site['noticeStatus']{if(/archive/i.test(raw))return 'archived';if(/^(active|open)$/i.test(raw.trim())&&due&&due>=today)return 'active';return 'unclear';}
export function csvCell(v:unknown){let s=String(v??'Unknown');if(/^[\s]*[=+@\-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}
export function exportCSV(sites:Site[]){const head=['ID','Address','City','Notice status','Notice date','Response due','Acres','Original area','Zoning (self-reported)','Contact','Coordinate quality','Source','Source updated','Tract units per acre (2020)','Jobs 1 mi (2023)','Jobs 3 mi (2023)','Jobs 5 mi (2023)','Flood screening','Fire screening','Evidence'];return [head,...sites.map(s=>[s.id,s.name,s.city,s.noticeStatus,s.noticeDate,s.dueDate,s.areaAcres,s.rawArea,s.zoning,s.contact,s.coordinateStatus,s.sourceUrl,s.sourceUpdatedAt,s.screening?.housingUnitsPerAcre,s.screening?.jobsByRadius?.['1'],s.screening?.jobsByRadius?.['3'],s.screening?.jobsByRadius?.['5'],s.screening?.flood,s.screening?.fire,s.evidence.map(e=>`${e.label}: ${e.value??'Unknown'} (${e.status}); ${e.sourceUrl}; as of ${e.asOf??'unknown'}`).join(' | ')])].map(r=>r.map(csvCell).join(',')).join('\r\n');}
export function score(s:Site,weights:{contact:number;geometry:number;evidence:number}) {const total=weights.contact+weights.geometry+weights.evidence;if(!total)return 0;return Math.round(100*(weights.contact*Number(!!s.contact)+weights.geometry*Number(!!s.coordinates)+weights.evidence*s.evidence.filter(e=>e.value!==null).length/s.evidence.length)/total);}

export type ScreeningFilters={minDensity:string;minJobs:string;jobRadius:string;risk:string};
export function matchesScreening(s:Site,f:ScreeningFilters){
 const d=s.screening?.housingUnitsPerAcre;const j=s.screening?.jobsByRadius?.[f.jobRadius];
 if(f.minDensity!==''&&(d==null||!Number.isFinite(Number(f.minDensity))||d<Number(f.minDensity)))return false;
 if(f.minJobs!==''&&(j==null||!Number.isFinite(Number(f.minJobs))||j<Number(f.minJobs)))return false;
 if(f.risk==='flag'&&s.screening?.risk!=='flag')return false;
 if(f.risk==='unknown'&&s.screening?.risk==='flag')return false;
 if(f.risk==='flood'&&s.screening?.flood!=='flag')return false;
 if(f.risk==='fire'&&s.screening?.fire!=='flag')return false;
 return true;
}
