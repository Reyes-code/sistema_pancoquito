{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
    buildInputs = [
        pkgs.python311
        pkgs.python311Packages.pip  # Añade pip explícitamente
        pkgs.mysql80
        pkgs.gcc
        pkgs.zlib
        pkgs.libffi
        pkgs.pkg-config  # Necesario para algunas compilaciones
        pkgs.libmysqlclient  # Librerías de MySQL
    ];
    
    # Variables de entorno críticas
    shellHook = ''
        export LD_LIBRARY_PATH="${pkgs.libmysqlclient}/lib:$LD_LIBRARY_PATH"
        export MYSQLCLIENT_CFLAGS="-I${pkgs.libmysqlclient.dev}/include/mysql"
        export MYSQLCLIENT_LDFLAGS="-L${pkgs.libmysqlclient}/lib"
    '';
}