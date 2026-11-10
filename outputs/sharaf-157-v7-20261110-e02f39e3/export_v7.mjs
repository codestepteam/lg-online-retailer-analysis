import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import { Workbook } from '@oai/artifact-tool';

const directory = new URL('.',import.meta.url);
/** @type {{columns:string[],preserved:string[][],changed:string[][],output_paths:string[]}} */
const input = JSON.parse(await fs.readFile(new URL('prepared.json',directory),'utf8'));
assert.equal(input.columns.length,26);
assert.equal(input.preserved.length,53204);
assert.equal(input.changed.length,1239);
const matrix = [input.columns,...input.changed];
assert(matrix.every(row=>row.length===26));

// Only the replaced rows are authored; other retailers are retained verbatim.
const book = Workbook.create();
const sheet = book.worksheets.add('Sharaf DG재조사');
sheet.getRangeByIndexes(0,0,matrix.length,26).values = matrix;
book.recalculate();
const authored = sheet.getRangeByIndexes(0,0,matrix.length,26).values.map((row,i)=>row.map((value,j)=>{
  if (value instanceof Date) {
    assert.equal(value.toISOString(),new Date(matrix[i][j]).toISOString());
    return matrix[i][j]; // Preserve the original CSV date spelling.
  }
  return value;
}));
assert(JSON.stringify(authored)===JSON.stringify(matrix),'Replacement values changed during authoring');
console.log((await book.inspect({kind:'table',range:'Sharaf DG재조사!Q1:T4',include:'values',tableMaxRows:4,tableMaxCols:4,maxChars:900})).ndjson);
const quote = value=>'"'+String(value??'').replaceAll('"','""')+'"';
const all = [input.columns,...input.preserved,...authored.slice(1)];
const csv = '\uFEFF'+all.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n';
for(const target of input.output_paths){
  try { await fs.writeFile(target,csv,{encoding:'utf8',flag:'wx'}); }
  catch(error){
    if(error.code!=='EEXIST')throw error;
    assert.equal(await fs.readFile(target,'utf8'),csv,'Existing output differs; overwrite not performed');
  }
}
console.log(JSON.stringify({rows:all.length-1,columns:26,outputs:input.output_paths}));
