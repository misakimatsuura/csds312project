{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = {...}@inputs:
  inputs.flake-utils.lib.eachDefaultSystem (system: let
    pkgs = (import inputs.nixpkgs) {
      inherit system;
      config = {
        allowUnfree = true;

      };
    };
    in
    {
      devShells = rec {
        docker-python = pkgs.mkShell {
          packages = with pkgs; [
            docker-compose
            docker
            podman-compose
            podman
            jupyter
            cudaPackages.cudatoolkit
            basedpyright
            (python3.withPackages (pythonPackages: with pythonPackages; [
              ipykernel
              pandas
              scikit-learn
              pip
              numpy
              scipy
              matplotlib
              notebook
              requests
              python-dotenv
              psycopg2
              psycopg
              asyncpg
              opencv-python
              (keras.override { tensorflow = tensorflowWithCuda; })
              tensorflowWithCuda
              sqlalchemy
              zstandard
              textblob
            ]))
          ];
          shellHook = ''
            export CUDA_DIR=${pkgs.cudaPackages.cudatoolkit}
            export XLA_FLAGS=--xla_gpu_cuda_data_dir=${pkgs.cudaPackages.cudatoolkit}
          '';
        };
        default = docker-python;
      };
      apps = rec {
        compose = {
          type = "app";
          program = "${pkgs.writeShellScriptBin "start-compose.sh" ''
            ${pkgs.podman-compose}/bin/podman-compose up --build --force-recreate
          ''}/bin/start-compose.sh";
        };
        default = compose;
      };
    }
  );
}