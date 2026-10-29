import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';

const folder = path.dirname(fileURLToPath(import.meta.url));
const input = JSON.parse(await fs.readFile(path.join(folder, 'inputs.json'), 'utf8'));
if (!Array.isArray(input.files) || input.files.length !== 4) throw new Error('Expected four source CSV files');
const mode = process.argv[2];
if (!['preview', 'author'].includes(mode)) throw new Error('Use preview or author');

if (mode === 'preview') {
  const source = input.files[0];
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add('Before');
  const columns = ['행번호', '상품명', '판정', '판매자', '페이지상태'];
  sheet.getRange('A1:E6').values = [columns, ...source.rows.map(row => columns.map(key => row[key]))];
  sheet.getRange('A1:E6').format.columnWidthPx = 110;
  sheet.getRange('B1:B6').format.columnWidthPx = 240;
  sheet.getRange('A1:E1').format.font.bold = true;
  sheet.getRange('A1:E6').format.rowHeightPx = 30;
  workbook.recalculate();
  const preview = await workbook.render({sheetName: 'Before', autoCrop: 'all', scale: 1, format: 'png'});
  await fs.writeFile(path.join(folder, 'before.png'), new Uint8Array(await preview.arrayBuffer()));
  console.log((await workbook.inspect({kind: 'table', range: 'Before!A1:E6', maxChars: 1500, tableMaxRows: 6})).ndjson);
} else {
  const files = [];
  for (const source of input.files) {
    if (!Array.isArray(source.headers) || source.rows.length !== 5) throw new Error(`Invalid source: ${source.name}`);
    const workbook = Workbook.create();
    const sheet = workbook.worksheets.add('Correction');
    const width = source.headers.length;
    sheet.getRangeByIndexes(0, 0, 6, width).values = [source.headers, ...source.rows.map(row => source.headers.map(key => row[key]))];
    const statusKey = source.headers.includes('모수 포함 여부') ? '모수 포함 여부' : '판정';
    const pageKey = source.headers.includes('페이지 접속 확인 결과') ? '페이지 접속 확인 결과' : '페이지상태';
    const arrivedKey = source.headers.includes('접속 후 URL') ? '접속 후 URL' : '실제URL';
    for (const [index, old] of source.rows.entries()) {
      const observation = input.observations[old['행번호']];
      if (!observation || old['리테일러'] !== 'DARTY') throw new Error(`Missing observation: ${old['행번호']}`);
      const external = observation['실시간_화면_상태'] === '외부 판매자';
      if (!external && observation['실시간_화면_상태'] !== '판매 종료') throw new Error('Unexpected correction kind');
      const evidence = external
        ? '2026-10-29 프랑스 VPN·Codex 내부 브라우저에서 원본 ofmp 주소의 본 상품 판매자 "Vendu et expédié par Electro Store" 확인'
        : '2026-10-29 원본 ofmp 주소에 "Produit hors catalogue / Ce produit n\'est plus commercialisé sur Darty.com" 표시. 저장 HTML에도 같은 판매 종료 문구 확인';
      const note = external
        ? '2026-10-29 원본 ofmp 주소 재확인: Electro Store 외부 판매자. 기존 수집은 ofmp 없는 주소로 이동해 DARTY로 잘못 기록함.'
        : '2026-10-29 원본 ofmp 주소 재확인: 판매 종료. 기존 수집의 가격 0·OutOfStock·DARTY 메타를 직판 포함 근거로 사용하지 않음.';
      const updates = {
        [pageKey]: external ? '정상' : '영구품절',
        [arrivedKey]: observation['원본_URL'],
        '판매자': external ? 'Electro Store' : '',
        '판매자구분': external ? '외부판매자' : '확인불가',
        '판매자근거': evidence,
        '메모': source.a_version ? `${note} A판은 기존 #58 목록 범위에 따른 제외 판정을 유지함.` : note,
      };
      if (!source.a_version) {
        updates[statusKey] = '제외';
        updates['제외단계'] = external ? '③리리부' : '④영구품절';
        updates['제외사유'] = external ? '외부 판매자 (Electro Store)' : '영구 품절(단종) 표시';
      } else if (old[statusKey] !== '제외') {
        throw new Error('A-version scope exclusion must already exist');
      }
      for (const [key, value] of Object.entries(updates)) {
        const column = source.headers.indexOf(key);
        if (column < 0) throw new Error(`Missing column: ${key}`);
        sheet.getCell(index + 1, column).values = [[value]];
      }
    }
    workbook.recalculate();
    const values = sheet.getRangeByIndexes(1, 0, 5, width).values;
    const rows = values.map(cells => Object.fromEntries(source.headers.map((key, column) => [key, cells[column] ?? ''])));
    if (rows.some(row => row[statusKey] !== '제외')) throw new Error('Correction status verification failed');
    files.push({path: source.path, rows});
    console.log(JSON.stringify({file: source.name, rows: rows.length, statuses: rows.map(row => row[statusKey])}));
  }
  await fs.writeFile(path.join(folder, 'authored_rows.json'), JSON.stringify({files}, null, 2) + '\n');
}
