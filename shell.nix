{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        pkgs.mysql80.dev
        pkgs.gcc
        pkgs.zlib.dev
        pkgs.libffi.dev
    ];
}