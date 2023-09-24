declare namespace google.fonts {
  type WebfontList = {
    kind: string;
    items: WebfontFamily[];
  };

  type WebfontFamily = {
    category?: string | undefined;
    kind: string;
    family: string;
    subsets: string[];
    variants: string[];
    version: string;
    lastModified: string;
    files: { [variant: string]: string };
  };
}

const GOOGLE_FONTS_API_KEY = Deno.env.get("GOOGLE_FONTS_API_KEY");
if (!GOOGLE_FONTS_API_KEY) {
  throw new Error("GOOGLE_FONTS_API_KEY is not defined");
}

export async function getWebFontFamily(): Promise<
  google.fonts.WebfontFamily[]
> {
  const resp = await fetch(
    `https://www.googleapis.com/webfonts/v1/webfonts?key=${GOOGLE_FONTS_API_KEY}`,
  ).then((response) => response.json());
  return resp.items;
}

export const FONT_CATEGORIES = [
  "sans-serif",
  "serif",
  "display",
  "handwriting",
  "monospace",
];
