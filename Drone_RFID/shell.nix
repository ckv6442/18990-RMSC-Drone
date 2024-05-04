let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.pyserial
      python-pkgs.pysimplegui
      python-pkgs.screeninfo
      (python-pkgs.opencv4.override {enableGtk2 = true; })
    ]))
  ];
}