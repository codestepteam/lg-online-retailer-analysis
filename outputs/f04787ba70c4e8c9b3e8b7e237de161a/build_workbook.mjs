import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const out = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(await fs.readFile(path.join(out, 'workbook_data.json'), 'utf8'));
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('전체판정');
sheet.showGridLines = false;

const endRow = data.rows.length + 1;
sheet.getRange('A1:Z1').values = [data.columns];
const batchSize = 200;
for (let start = 0; start < data.rows.length; start += batchSize) {
  const part = data.rows.slice(start, start + batchSize).map((row) => {
    const values = [...row];
    values[11] = new Date(Date.UTC(2026, 10, 3));
    return values;
  });
  sheet.getRangeByIndexes(start + 1, 0, part.length, data.columns.length).values = part;
}

const table = sheet.tables.add(`A1:Z${endRow}`, true, 'MomoshopFullPopulation');
table.style = 'TableStyleMedium2';
table.showFilterButton = true;

const header = sheet.getRange('A1:Z1');
header.format.fill = '#203864';
header.format.font = { name: 'Arial', size: 10, bold: true, color: '#FFFFFF' };
header.format.rowHeight = 30;
header.format.verticalAlignment = 'center';
header.format.horizontalAlignment = 'center';
header.format.wrapText = true;
sheet.getRange(`L2:L${endRow}`).setNumberFormat('yyyy-mm-dd');
for (const column of ['A', 'N']) {
  sheet.getRange(`${column}2:${column}${endRow}`).setNumberFormat('#,##0');
}
sheet.getRange(`G2:H${endRow}`).setNumberFormat('@');
sheet.getRange(`Q2:Q${endRow}`).conditionalFormats.add('containsText', {
  text: '포함',
  format: { fill: '#DCFCE7', font: { bold: true, color: '#166534' } },
});

const widths = {
  A: 9, B: 8, C: 12, D: 16, E: 10, F: 14, G: 13, H: 13,
  I: 58, J: 57, K: 57, L: 14, M: 19, N: 13, O: 13, P: 42,
  Q: 14, R: 14, S: 45, T: 24, U: 18, V: 19, W: 55, X: 50,
  Y: 15, Z: 52,
};
for (const [column, width] of Object.entries(widths)) {
  sheet.getRange(`${column}1`).format.columnWidth = width;
}
sheet.freezePanes.freezeRows(1);
sheet.freezePanes.freezeColumns(4);

workbook.recalculate();
for (const range of ['A1:I6', 'M1:S6', 'W1:Z6']) {
  const result = await workbook.inspect({ kind: 'region', sheetId: '전체판정', range, maxChars: 1200, tableMaxRows: 6, tableMaxCols: 9 });
  console.log(`INSPECT ${range} ${result.ndjson}`);
}
const errors = await workbook.inspect({
  kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',
  options: { useRegex: true, maxResults: 10 }, maxChars: 600,
});
console.log(`ERROR_SCAN ${errors.ndjson}`);
for (const [range, name] of [['A1:I9', 'preview_left.png'], ['P1:Z9', 'preview_right.png']]) {
  const preview = await workbook.render({ sheetName: '전체판정', range, scale: 1, format: 'png' });
  await fs.writeFile(path.join(out, name), new Uint8Array(await preview.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(workbook);
const target = path.join(out, 'Momoshop_검색어기반_PDP모수_전체판정_6407행_20261103.xlsx');
await output.save(target);
console.log(`EXPORTED ${target}`);
