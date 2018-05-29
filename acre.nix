with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "acre";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    python34Full
    python34Packages.pip
    python34Packages.virtualenv
    postgresql95
  ];
}
