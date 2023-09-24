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
      shell = {pkgs}:
        pkgs.mkShell {
          packages = with pkgs; [
            deno
            rye
          ];
        };
    };
}
