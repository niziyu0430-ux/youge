// Web delivery derivatives only: resize and encode, preserving the original artwork files.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(import.meta.url);
const modulePaths=[root,...(process.argv[2]?[process.argv[2]]:[])];
const sharp=require(require.resolve('sharp',{paths:modulePaths}));
const manifest=JSON.parse(await fs.readFile(path.join(root,'web/assets/personas-v2/preview.json'),'utf8'));
const output=path.join(root,'web/assets/personas-ribbon');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const records=[];
sharp.concurrency(2);

for(const edition of ['v1','v2']) {
  await fs.mkdir(path.join(output,edition),{recursive:true});
  for(let start=0;start<manifest.assets.length;start+=4) {
    await Promise.all(manifest.assets.slice(start,start+4).map(async persona=>{
      const source=path.join(root,'web',persona[edition].replace(/^\//,''));
      const sourceBytes=await fs.readFile(source);
      const destination=path.join(output,edition,`${persona.id}.webp`);
      const info=await sharp(sourceBytes).resize({width:320,height:480,fit:'inside',withoutEnlargement:true}).webp({quality:88,alphaQuality:100,effort:4}).toFile(destination);
      const result=await fs.readFile(destination);
      const currentOriginal=await fs.readFile(source);
      if(hash(currentOriginal)!==hash(sourceBytes))throw Error(`Original changed: ${source}`);
      records.push({id:persona.id,edition,source:persona[edition],path:`/assets/personas-ribbon/${edition}/${persona.id}.webp`,width:info.width,height:info.height,bytes:result.length,source_bytes:sourceBytes.length,original_sha256:hash(sourceBytes),sha256:hash(result)});
    }));
  }
}
records.sort((a,b)=>(a.edition+a.id).localeCompare(b.edition+b.id));
await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify({version:'ribbon-0.4.3',mode:'deterministic_resize_and_webp_encoding',width:320,height:480,originals_unchanged:true,assets:records},null,2)+'\n');
for(const edition of ['v1','v2']) {
  const list=records.filter(p=>p.edition===edition);
  console.log(`${edition}: ${list.length} thumbnails, ${list.reduce((n,p)=>n+p.bytes,0)} bytes total`);
}
