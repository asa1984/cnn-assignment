import "https://deno.land/std@0.202.0/dotenv/load.ts"; // .envファイルから環境変数を読み込む

import { getWebFontFamily, FONT_CATEGORIES } from "./fetch_font.ts";
import { genImgData, createImgFile } from "./gen_img.tsx";

async function main() {
  const DATASET_DIR = "./dataset";

  // すでにデータセットが存在する場合は削除する
  try {
    await Deno.remove(DATASET_DIR, { recursive: true });
  } catch (_) {
    // ディレクトリが存在しない場合は何もしない
  }

  const fonts = await getWebFontFamily();
  const randomFonts = FONT_CATEGORIES.flatMap((category) => {
    const categoryFonts = fonts.filter((font) => font.category === category);
    return getRandomUniqueElements(categoryFonts, 5);
  });

  const ALPHABET = "abcdefghijklmnopqrstuvwxyz";

  // データセットを作成
  for (const char of ALPHABET) {
    await Deno.mkdir(`${DATASET_DIR}/${char}`, { recursive: true });

    for (const font of randomFonts) {
      try {
        const fontFile = font.files.regular;
        const imgData = await genImgData(char, fontFile);
        const fontFamily = font.family.replace(/\s/g, "_"); // 空白をアンダースコアに置換
        const fileName = `${DATASET_DIR}/${char}/${fontFamily}.png`;
        await createImgFile(fileName, imgData);
      } catch (e) {
        // opentype.jsがサポートしていないフォントファミリーの場合はスキップする
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
