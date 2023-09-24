import "https://deno.land/std@0.202.0/dotenv/load.ts"; // .envファイルから環境変数を読み込む

import { getWebFontFamily, FONT_CATEGORIES } from "./fetch_font.ts";
import { genImgData, createImgFile } from "./gen_img.tsx";

async function main() {
  const TRAIN_DATA_DIR = "./dataset/train";
  const VAL_DATA_DIR = "./dataset/val";

  // すでにデータセットが存在する場合は削除する
  try {
    await Deno.remove(TRAIN_DATA_DIR, { recursive: true });
  } catch (_) {
    // ディレクトリが存在しない場合は何もしない
  }

  const allFonts = await getWebFontFamily();

  const ALPHABET = "abcdefghijklmnopqrstuvwxyz";

  // 訓練用データセット
  const trainFonts = FONT_CATEGORIES.flatMap((category) => {
    const categoryFonts = allFonts.filter((font) => font.category === category);
    return getRandomUniqueElements(categoryFonts, 5);
  });

  // 訓練用データセットの生成
  for (const char of ALPHABET) {
    await Deno.mkdir(`${TRAIN_DATA_DIR}/${char}`, { recursive: true });

    for (const font of trainFonts) {
      try {
        const fontFile = font.files.regular;
        const imgData = await genImgData(char, fontFile);
        const fontFamily = font.family.replace(/\s/g, "_"); // 空白をアンダースコアに置換
        const fileName = `${TRAIN_DATA_DIR}/${char}/${fontFamily}.png`;
        await createImgFile(fileName, imgData);
      } catch (e) {
        // opentype.jsがサポートしていないフォントファミリーの場合はスキップする
        console.error(`フォントファミリー: ${font.family}で画像の生成に失敗`);
        console.error(e);
      }
    }
  }

  // 検証用データセット
  const valFonts = FONT_CATEGORIES.flatMap((category) => {
    // 訓練用データセットに含まれていないフォントを抽出
    const unusedFonts = allFonts.filter((font) => !trainFonts.includes(font));
    const categoryFonts = unusedFonts.filter(
      (font) => font.category === category,
    );
    return getRandomUniqueElements(categoryFonts, 1);
  });

  // 検証用データセットの生成
  for (const char of ALPHABET) {
    await Deno.mkdir(`${VAL_DATA_DIR}/${char}`, { recursive: true });

    for (const font of valFonts) {
      try {
        const fontFile = font.files.regular;
        const imgData = await genImgData(char, fontFile);
        const fontFamily = font.family.replace(/\s/g, "_"); // 空白をアンダースコアに置換
        const fileName = `${VAL_DATA_DIR}/${char}/${fontFamily}.png`;
        await createImgFile(fileName, imgData);
      } catch (e) {
        console.error(`フォントファミリー: ${font.family}で画像の生成に失敗`);
        console.error(e);
      }
    }
  }
}

main();

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
