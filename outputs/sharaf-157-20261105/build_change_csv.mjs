import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { Workbook } from "@oai/artifact-tool";

const dir = path.dirname(fileURLToPath(import.meta.url));
const input = JSON.parse(await fs.readFile(path.join(dir, "SharafDG_v3외부판매자9_작성입력.json"), "utf8"));
const extraColumns = [
  "변경요청_모수 포함 여부",
  "변경요청_사유",
  "현재_본상품_Sold_by_원문",
  "현재_본상품_판매자",
  "현재_확인시각_KST",
  "현재_확인방법",
  "현재_HTML_첫seller_name",
  "현재_HTML_첫seller_type",
  "현재_판매영역과HTML첫값_일치",
  "10월_상품상세_HTML_보존여부",
];
const columns = [...input.v3_columns, ...extraColumns];
const records = input.selected.map(({v3, observation}) => [
  ...input.v3_columns.map((key) => v3[key] ?? ""),
  "제외",
  `현재 본 상품 Sold by ${observation["상품판매영역_판매자"]}; Sharaf DG 외부 판매자`,
  observation["상품판매영역_표시"],
  observation["상품판매영역_판매자"],
  observation["재확인기록시각_KST"],
  "Codex 내부 브라우저에서 정확한 ?promo= 상품 URL 직접 확인",
  observation["현재HTML_첫seller_name"],
  observation["현재HTML_첫seller_type"],
  observation["판매영역과HTML첫값_일치"],
  "미보존",
]);
const matrix = [columns, ...records];
const workbook = Workbook.create();
const sheet = workbook.worksheets.add("변경 대상");
const dataRange = sheet.getRangeByIndexes(0, 0, matrix.length, columns.length);
dataRange.setNumberFormat("@");
dataRange.values = matrix;
workbook.recalculate();
const readback = sheet.getRangeByIndexes(0, 0, matrix.length, columns.length).values;
for (let r = 0; r < matrix.length; r++) {
  for (let c = 0; c < columns.length; c++) {
    if (String(readback[r]?.[c] ?? "") !== String(matrix[r]?.[c] ?? "")) {
      throw new Error(`artifact_tool readback differs at row ${r + 1}, column ${c + 1}: ${JSON.stringify(readback[r]?.[c])} != ${JSON.stringify(matrix[r]?.[c])}`);
    }
  }
}
const seen = new Set();
for (const row of readback.slice(1)) {
  const id = row[columns.indexOf("행번호")];
  if (seen.has(id) || row[columns.indexOf("모수 포함 여부")] !== "포함" || row[columns.indexOf("변경요청_모수 포함 여부")] !== "제외") {
    throw new Error(`invalid selected row ${id}`);
  }
  seen.add(id);
}
if (seen.size !== 9) throw new Error(`expected 9 unique rows; got ${seen.size}`);
const csvCell = (value) => {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
const csv = "\uFEFF" + readback.map((row) => row.map(csvCell).join(",")).join("\r\n") + "\r\n";
const name = "SharafDG_v3포함_외부판매자9건_포함에서제외_변경대상_20261105.csv";
const localPath = path.join(dir, name);
const downloadPath = path.join(process.env.HOME, "Downloads", name);
await fs.writeFile(localPath, csv, "utf8");
await fs.copyFile(localPath, downloadPath);
console.log(JSON.stringify({rows: records.length, columns: columns.length, localPath, downloadPath}));
