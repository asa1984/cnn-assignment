import "https://deno.land/std@0.202.0/dotenv/load.ts"; // .envファイルから環境変数を読み込む
import { parse } from "https://deno.land/std@0.202.0/flags/mod.ts";

import {
  getWebFontFamily,
  FONT_CATEGORIES,
  type google,
} from "./fetch_font.ts";
import { genImgData, createImgFile } from "./gen_img.tsx";

const { trainFontCount, validateFontCount, outDir } = parse(Deno.args, {
  default: {
    trainFontCount: 10,
    validateFontCount: 3,
    outDir: "dataset",
  },
});

const TRAIN_FONT_COUNT: number = trainFontCount;
const VALIDATE_FONT_COUNT: number = validateFontCount;
const OUT_DIR: string = outDir;
const TRAIN_DATA_DIR = `${OUT_DIR}/train`;
const VALIDATE_DATA_DIR = `${OUT_DIR}/validate`;

// すでにデータセットが存在する場合は削除する
try {
  await Deno.remove(OUT_DIR, { recursive: true });
  console.log("===> 既存のデータセットを削除");
} catch (_) {
  // ディレクトリが存在しない場合は何もしない
}

const allFonts = await getWebFontFamily();

// 訓練用データセット
const trainFonts = FONT_CATEGORIES.flatMap((category) => {
  const categoryFonts = allFonts.filter((font) => font.category === category);
  return getRandomUniqueElements(categoryFonts, TRAIN_FONT_COUNT);
});

// 検証用データセット
const validateFonts = FONT_CATEGORIES.flatMap((category) => {
  // 訓練用データセットに含まれていないフォントを抽出
  const unusedFonts = allFonts.filter((font) => !trainFonts.includes(font));
  const categoryFonts = unusedFonts.filter(
    (font) => font.category === category,
  );
  return getRandomUniqueElements(categoryFonts, VALIDATE_FONT_COUNT);
});

console.log("===> データセットを生成中...");
await createDataset(TRAIN_DATA_DIR, trainFonts);
await createDataset(VALIDATE_DATA_DIR, validateFonts);
console.log("===> データセットの生成完了");

async function createDataset(
  dataDir: string,
  fonts: google.fonts.WebfontFamily[],
) {
  const ALPHABET = "abcdefghijklmnopqrstuvwxyz";
  for (const char of ALPHABET) {
    await Deno.mkdir(`${dataDir}/${char}`, { recursive: true });

    for (const font of fonts) {
      try {
        const fontFile = font.files.regular;
        const imgData = await genImgData(char, fontFile);
        const fontFamily = font.family.replace(/\s/g, "_"); // 空白をアンダースコアに置換
        const fileName = `${dataDir}/${char}/${fontFamily}.png`;
        await createImgFile(fileName, imgData);
      } catch (e) {
        // opentype.jsがサポートしていないフォントファミリーの場合はスキップする
        console.error(`フォントファミリー: ${font.family}で画像の生成に失敗`);
        console.error(e);
      }
    }
  }
}

function getRandomUniqueElements<T>(array: T[], count: number): T[] {
  if (count <= 0 || count > array.length) {
    throw new Error("Invalid count value");
  }

  // Fisher-Yates shuffle
  const shuffledArray = [...array];
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  const result = shuffledArray.slice(0, count);

  return result;
}
