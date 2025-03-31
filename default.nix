{
  lib,
  stdenvNoCC,
  makeWrapper,
  python3
}:
  let
   fs = lib.fileset;
   relevantFiles = fs.gitTracked ./.;
   
   python = (python3.withPackages (ps: [ps.pygame]));
  in
  stdenvNoCC.mkDerivation (self: {
    strict = true;
    pname = "sq42";
    version = "1.0";

    src = fs.toSource {
      root = ./.;
      fileset = relevantFiles;
    };

    nativeBuildInputs = [
      makeWrapper
    ];

    installPhase = ''
        mkdir -p $out/lib $out/bin
        mv ./* $out/lib/

        makeWrapper ${lib.getExe python} $out/bin/sq42 --add-flags "$out/lib/project_main.py"
      '';

    meta.mainProgram = "sq42";
  })
