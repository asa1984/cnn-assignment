{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.simpleFlake {
      inherit self nixpkgs;
      name = "rye-dev-env";
      shell = {pkgs}: let
        noto-serif-jp = pkgs.fetchzip {
          url = "https://github.com/notofonts/noto-cjk/releases/download/Serif2.002/07_NotoSerifCJKjp.zip";
          stripRoot = false;
          hash = "sha256-GbE1VKJ+eLprWfkI3GOmaOUavnmNocF7+L2H36BKN3E=";
        };
        noto-sans-jp = pkgs.fetchzip {
          url = "https://github.com/notofonts/noto-cjk/releases/download/Sans2.004/06_NotoSansCJKjp.zip";
          stripRoot = false;
          hash = "sha256-QoAXVSotR8fOLtGe87O2XHuz8nNQrTBlydo5QY/LMRo=";
        };
        typst-fonts = pkgs.stdenv.mkDerivation {
          name = "typst-fonts";
          phases = ["installPhase"];
          installPhase = ''
            mkdir -p $out
            mkdir fonts
            cp -r ${noto-serif-jp} fonts
            cp -r ${noto-sans-jp} fonts
            find fonts -type f -name "*.otf" -exec mv {} $out \;
          '';
        };
        typst-tools = with pkgs; [
          typst
          typst-lsp
          typst-fmt
        ];
        scripts = with pkgs; [
          # Compile typst files
          (writeScriptBin "compile" ''
            ${pkgs.typst}/bin/typst compile "$@" --font-path ${typst-fonts} --root=./
          '')
        ];
      in
        pkgs.mkShell {
          packages = with pkgs;
            [
              deno
              rye
            ]
            ++ typst-tools
            ++ scripts;
        };
    };
}
