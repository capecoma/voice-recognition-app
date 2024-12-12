{ pkgs }: {
    deps = [
        pkgs.python310Full
        pkgs.replitPackages.prybar-python310
        pkgs.replitPackages.stderred
        pkgs.portaudio
        pkgs.ffmpeg
    ];
}