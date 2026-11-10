import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import { Workbook } from '@oai/artifact-tool';

const outputDir = new URL('.', import.meta.url);
/** @type {(string | number)[][]} */
const matrix = JSON.parse(await fs.readFile(new URL('result-matrix.json', outputDir), 'utf8'));
assert.equal(matrix.length, 1240);
assert.equal(new Set(matrix[0]).size, matrix[0].length);
assert(matrix.every(row => row.length === matrix[0].length));

const workbook = Workbook.create();
const sheet = workbook.worksheets.add('판정결과');
sheet.getRangeByIndexes(0, 0, matrix.length, matrix[0].length).values = matrix;
workbook.recalculate();
const savedMatrix = sheet.getRangeByIndexes(0, 0, matrix.length, matrix[0].length).values
  .map(row => row.map(value => value instanceof Date ? value.toISOString() : value));
assert(JSON.stringify(savedMatrix) === JSON.stringify(matrix), 'Artifact cell values differ from the prepared source matrix');
console.log((await workbook.inspect({kind:'table',range:'판정결과!O1:V5',include:'values',tableMaxRows:5,tableMaxCols:8,maxChars:1700})).ndjson);

// CSV has no formatting or formulas. Serialize the verified artifact cell values.
const quote = value => '"' + String(value ?? '').replaceAll('"', '""') + '"';
const csv = '\uFEFF' + savedMatrix.map(row => row.map(quote).join(',')).join('\r\n') + '\r\n';
const name = 'Sharaf DG 두레이 157 적용_필터결과.csv';
for (const target of [new URL(name, outputDir), '/Users/codestepseunghee/Downloads/' + name]) {
  try {
    await fs.writeFile(target, csv, {encoding:'utf8',flag:'wx'});
  } catch (error) {
    if (error.code !== 'EEXIST') throw error;
    assert.equal(await fs.readFile(target,'utf8'), csv, 'Existing file differs; overwrite not performed');
  }
}
console.log(JSON.stringify({rows:matrix.length-1,columns:matrix[0].length,path:'/Users/codestepseunghee/Downloads/'+name}));
