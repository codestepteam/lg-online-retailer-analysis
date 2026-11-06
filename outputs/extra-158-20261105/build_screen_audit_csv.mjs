import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Workbook } from "@oai/artifact-tool";

const dir = path.dirname(fileURLToPath(import.meta.url));
const input = JSON.parse(await fs.readFile(path.join(dir, "eXtra_v3상품화면전수확인272_작성입력.json"), "utf8"));
const day = "2026-11-05";
const method = "Codex 내부 브라우저 5개 탭에서 정확한 URL의 상품 화면 직접 확인";
const screenColumns = [
  "상품화면_확인일_KST",
  "상품화면_두_아랍어_문구_함께표시",
  "상품화면_장바구니버튼",
  "상품화면_분류",
  "상품화면_확인문구",
  "상품화면_확인방법",
];
const auditColumns = [...input.audit_columns, ...screenColumns];
const auditMatrix = [auditColumns, ...input.rows.map(({audit, screen_class, screen_phrase, screen_cart}) => [
  ...input.audit_columns.map((key) => audit[key] ?? ""),
  day,
  screen_class === "본상품_두문구표시_장바구니없음" ? "Y" : "N",
  screen_cart,
  screen_class,
  screen_phrase,
  method,
])];
const changeColumns = [...input.v3_columns,
  "변경요청_모수 포함 여부",
  "변경요청_사유",
  "상품화면_확인일_KST",
  "상품화면_확인문구",
  "상품화면_장바구니버튼",
  "상품화면_확인방법",
  "OSM_20261026_AVLBL_STAT_참고",
  "20261105_상품JSON_재고코드_참고",
  "20261105_HTML_SHA256_참고",
];
const confirmed = input.rows.filter((row) => row.screen_class === "본상품_두문구표시_장바구니없음");
const changeMatrix = [changeColumns, ...confirmed.map(({v3, audit, screen_phrase, screen_cart}) => [
  ...input.v3_columns.map((key) => v3[key] ?? ""),
  "제외",
  "2026-11-05 본 상품 화면에 هذا المنتج حاليًا 및 غير متوفر حاليًا 표시, 장바구니 버튼 없음",
  day,
  screen_phrase,
  screen_cart,
  method,
  audit["OSM_AVLBL_STAT"],
  audit["현재_재고코드"],
  audit["HTML_SHA256"],
])];
if (auditMatrix.length !== 273 || changeMatrix.length !== 130) throw new Error("incorrect output row count");

const workbook = Workbook.create();
function addMatrix(name, matrix) {
  const sheet = workbook.worksheets.add(name);
  const range = sheet.getRangeByIndexes(0, 0, matrix.length, matrix[0].length);
  range.setNumberFormat("@");
  range.values = matrix;
  return range;
}
const allRange = addMatrix("272 화면 감사", auditMatrix);
const changeRange = addMatrix("129 변경 대상", changeMatrix);
workbook.recalculate();
function check(readback, expected) {
  for (let r = 0; r < expected.length; r++) {
    for (let c = 0; c < expected[r].length; c++) {
      if (String(readback[r]?.[c] ?? "") !== String(expected[r][c] ?? "")) {
        throw new Error(`artifact_tool readback mismatch at row ${r + 1}, col ${c + 1}`);
      }
    }
  }
}
const allValues = allRange.values;
const changeValues = changeRange.values;
check(allValues, auditMatrix);
check(changeValues, changeMatrix);
const csvCell = (value) => {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
const toCsv = (rows) => "\uFEFF" + rows.map((row) => row.map(csvCell).join(",")).join("\r\n") + "\r\n";
const files = [
  ["eXtra_v3포함272_상품화면_품절문구_전수확인_20261105.csv", allValues],
  ["eXtra_v3포함_화면품절문구129건_포함에서제외_변경대상_20261105.csv", changeValues],
];
for (const [name, rows] of files) {
  const local = path.join(dir, name);
  const download = path.join(process.env.HOME, "Downloads", name);
  await fs.writeFile(local, toCsv(rows), "utf8");
  await fs.copyFile(local, download);
}
console.log(JSON.stringify({all: auditMatrix.length - 1, selected: changeMatrix.length - 1, files: files.map(([name]) => name)}));
