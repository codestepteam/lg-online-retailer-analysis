import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const files=await fs.readdir('/Users/codestepseunghee/Downloads');
const file=files.find(x=>x.normalize('NFC')==='25개국 분석_261113_v0.1_수정.xlsx');
const path='/Users/codestepseunghee/Downloads/'+file;
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
console.log((await wb.inspect({kind:'workbook,sheet',maxChars:2500})).ndjson);
const names=['※ 25개국 Summary','8월_국가','8월_국가x리테일러','8월_국가x리테일러x카테고리','10월_국가','10월_국가x리테일러','10월_국가x리테일러x카테고리','11월_국가x리테일러x카테고리'];
const data={path,sheets:{}};
for(const n of names){ const s=wb.worksheets.getItem(n);data.sheets[n]={values:s.getRange('A1:CI60').values,formulas:s.getRange('A1:CI60').formulas}; }
await fs.writeFile('/tmp/lg-audit-39d0ac5e/workbook.json',JSON.stringify(data));
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!',options:{useRegex:true,maxResults:30},maxChars:1500})).ndjson);
