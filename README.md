<div align="center">
    <img src="data/icons/hicolor/scalable/apps/org.vanillaos.Sideload.svg" height="64">
    <h1>Vanilla Sideload Utility</h1>
    <a href="https://hosted.weblate.org/engage/vanilla-os/">
        <img src="https://hosted.weblate.org/widget/vanilla-os/sideload-utility/svg-badge.svg" alt="Translation status" />
    </a>
    <p>A frontend in GTK 4 and Libadwaita to sideload apps in VSO.</p>
    <br />
    <img src="data/screenshot.png">
</div>

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
meson setup build
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
