import fs from 'node:fs/promises';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const outputDir = '/Users/codestepseunghee/codestep/lg-online-retailer-analysis/outputs/riribu-keyword-effect-20261103-d0bfd680';
const data = JSON.parse(await fs.readFile('/tmp/riribu-keyword-effect-d0bfd680.json', 'utf8'));
const workbook = Workbook.create();
const summary = workbook.worksheets.add('Summary');
const detail = workbook.worksheets.add('제외 URL');
summary.showGridLines = false;
detail.showGridLines = false;
summary.tabColor = '#1E3A5F';
const font = { name: 'Arial', size: 10, color: '#17243A' };

summary.getRange('A2').values = [['리/리/부 키워드 매칭으로 제외된 URL']];
summary.getRange('A2').format.font = { ...font, size: 15, bold: true };
summary.getRange('A4').values = [['국가·리테일러·URL이 같은 중복 행을 한 번만 센 고유 URL 수']];
summary.getRange('A4').format.font = { ...font, italic: true, color: '#516273' };
summary.getRange('A6:B6').values = [['국가', '제외된 URL 수']];
summary.getRange('A6:B6').format = {
  fill: '#1E3A5F', font: { ...font, color: '#FFFFFF', bold: true },
  rowHeight: 25,
};

const countryStart = 7;
const countryEnd = countryStart + data.countries.length - 1;
const detailStart = 7;
const detailEnd = detailStart + data.details.length - 1;
summary.getRange(`A${countryStart}:A${countryEnd}`).values = data.countries.map(country => [country]);
summary.getRange(`B${countryStart}:B${countryEnd}`).formulas = data.countries.map((_, i) => [
  `=COUNTIFS('제외 URL'!$A$${detailStart}:$A$${detailEnd},A${countryStart + i})`,
]);
summary.getRange(`A${countryStart}:B${countryEnd}`).format.font = font;
summary.getRange(`A${countryStart}:B${countryEnd}`).format.rowHeight = 21;
summary.getRange(`B${countryStart}:B${countryEnd}`).format.numberFormat = '#,##0';
summary.getRange(`A${countryEnd + 1}:B${countryEnd + 1}`).values = [['합계', null]];
summary.getRange(`B${countryEnd + 1}`).formulas = [[`=SUM(B${countryStart}:B${countryEnd})`]];
summary.getRange(`A${countryEnd + 1}:B${countryEnd + 1}`).format = {
  fill: '#E7EEF7', font: { ...font, bold: true }, rowHeight: 24,
};
summary.getRange(`B${countryEnd + 1}`).format.numberFormat = '#,##0';
summary.getRange('A35').values = [['집계 기준']];
summary.getRange('A35').format.font = { ...font, bold: true };
summary.getRange('A36').values = [['공식 제외키워드가 상품명에 처음 매칭되어 ③리리부 단계에서 제외된 행만 포함']];
summary.getRange('A37').values = [[`원본 ${data.matched_rows.toLocaleString()}행에서 중복 URL ${data.duplicate_rows}행 제거`]];
summary.getRange('A36:A37').format.font = { ...font, color: '#516273' };
summary.getRange('A1:A37').format.columnWidth = 68;
summary.getRange('B1:B37').format.columnWidth = 18;

detail.getRange('A2').values = [['공식 키워드 매칭으로 제외된 URL 목록']];
detail.getRange('A2').format.font = { ...font, size: 15, bold: true };
detail.getRange('A3').values = [[`판정 출처: ${data.source}`]];
detail.getRange('A4').values = [['키워드 출처: EY 진단 항목 v2.2(2026-10-23 송부본), 제외키워드(리리부) 탭의 25개국 표']];
detail.getRange('A3:A4').format.font = { ...font, color: '#516273', italic: true };
detail.getRange('A6:D6').values = [['국가', '리테일러', '제외된 URL', '매칭된 리/리/부 키워드']];
detail.getRange(`A${detailStart}:D${detailEnd}`).values = data.details;
detail.getRange(`A${detailStart}:D${detailEnd}`).format.font = font;
detail.getRange(`A${detailStart}:D${detailEnd}`).format.rowHeight = 20;
detail.getRange(`A${detailStart}:D${detailEnd}`).format.wrapText = false;
const table = detail.tables.add(`A6:D${detailEnd}`, true, 'KeywordExcludedUrls');
table.showFilterButton = true;
detail.getRange('A1:A6').format.columnWidth = 22;
detail.getRange('B1:B6').format.columnWidth = 25;
detail.getRange('C1:C6').format.columnWidth = 100;
detail.getRange('D1:D6').format.columnWidth = 30;
detail.freezePanes.freezeRows(6);

workbook.recalculate();
const check = await workbook.inspect({kind:'region', sheetId:'Summary', range:`A6:B${countryEnd + 1}`, maxChars:8000, tableMaxRows:30, tableMaxCols:2});
console.log(check.ndjson);
const errorCheck = await workbook.inspect({kind:'match', searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options:{useRegex:true,maxResults:20}, maxChars:2000});
console.log(errorCheck.ndjson);
const preview = await workbook.render({sheetName:'Summary', range:'A1:B37', scale:1.5, format:'png'});
await fs.writeFile(`${outputDir}/summary-preview.png`, new Uint8Array(await preview.arrayBuffer()));
const detailPreview = await workbook.render({sheetName:'제외 URL', range:'A1:D12', scale:1, format:'png'});
await fs.writeFile(`${outputDir}/detail-preview.png`, new Uint8Array(await detailPreview.arrayBuffer()));
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/리리부_키워드_제외URL_국가별Summary_20261103.xlsx`);
