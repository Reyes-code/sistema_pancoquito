{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        pkgs.mysql80  # Sin .dev
        pkgs.gcc
        pkgs.zlib
        pkgs.libffi
    ];
}