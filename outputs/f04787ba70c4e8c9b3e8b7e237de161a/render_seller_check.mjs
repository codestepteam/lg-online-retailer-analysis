import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const out = path.dirname(fileURLToPath(import.meta.url));
const file = path.join(out, 'Momoshop_검색어기반_PDP모수_전체판정_6407행_20261103.xlsx');
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(file));
const preview = await workbook.render({ sheetName: '전체판정', range: 'W20:Z26', scale: 2, format: 'png' });
await fs.writeFile(path.join(out, 'preview_seller_check.png'), new Uint8Array(await preview.arrayBuffer()));
console.log('Rendered saved workbook seller cells W20:Z26');
