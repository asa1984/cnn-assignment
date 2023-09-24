/** @jsxImportSource https://esm.sh/react */

import { ImageResponse } from "https://deno.land/x/og_edge@0.0.6/mod.ts";

export async function genImgData(
  text: string,
  fontUrl: string,
): Promise<ImageResponse> {
  const fontData = await fetch(fontUrl).then((res) => res.arrayBuffer());

  return new ImageResponse(
    (
      <div
        style={{
          backgroundColor: "white",
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 100,
          fontFamily: "Custom",
        }}
      >
        {text}
      </div>
    ),
    {
      width: 150,
      height: 150,
      fonts: [
        {
          name: "Custom",
          style: "normal",
          data: fontData,
        },
      ],
    },
  );
}

export async function createImgFile(path: string, imgData: ImageResponse) {
  const blob = await imgData.blob();
  await Deno.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}
