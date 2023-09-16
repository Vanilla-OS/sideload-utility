# Sideload Utility
A frontend in GTK 4 and Libadwaita to sideload apps in VSO.

## Build
### Dependencies
- build-essential
- meson
- libadwaita-1-dev
- gettext
- desktop-file-utils
- vanilla-system-operator

### Build
```bash
meson build
ninja -C build
```

### Install
```bash
sudo ninja -C build install
```

## Run
```bash
vanilla-sideload
```