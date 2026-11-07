import 'dotenv/config';
import Anthropic from '@anthropic-ai/sdk';
const token=process.env.VITE_MAPBOX_ACCESS_TOKEN?.trim();
try{const r=await fetch('https://api.mapbox.com/styles/v1/mapbox/light-v11?access_token='+encodeURIComponent(token||''),{signal:AbortSignal.timeout(20000)});console.log('Mapbox style authentication:',r.status);}catch{console.log('Mapbox connection failed (network).');}
try{const client=new Anthropic({timeout:20000,maxRetries:0});const model=await client.models.retrieve(process.env.CLAUDE_MODEL||'claude-sonnet-4-5');console.log('Claude model authentication: OK; model',model.id);}catch(e){console.log('Claude authentication/model check:',e.status||'network failure');}
