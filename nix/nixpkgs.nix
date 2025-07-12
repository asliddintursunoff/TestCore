with import <nixpkgs> {};

let
  myTexLive = texlive.combine {
    inherit (texlive)
      scheme-medium
      enumitem
      tikz
      fancyhdr
      graphics
      multicol;
  };
in
[
  python311
  myTexLive
]
