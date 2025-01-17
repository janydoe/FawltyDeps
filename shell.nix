{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "nixos-22.11";
    rev = "96e18717904dfedcd884541e5a92bf9ff632cf39";
  }) {}
}:
let
  python310WithPoetry = (
    pkgs.python310.withPackages (pypkgs: with pypkgs; [
      poetry
    ])
  );
in
pkgs.mkShell {
  name = "fawltydeps-env";
  buildInputs = with pkgs; [
    python37
    python38
    python39
    python310WithPoetry
    python311
  ];
  shellHook = ''
    # This is needed to keep python3.7 working while in the same nix-shell
    # as a later python (see https://github.com/NixOS/nixpkgs/issues/88711
    # for more details):
    unset _PYTHON_HOST_PLATFORM
    unset _PYTHON_SYSCONFIGDATA_NAME

    poetry env use "${python310WithPoetry}/bin/python"
    poetry install --sync --with=dev
    source "$(poetry env info --path)/bin/activate"
  '';
}
