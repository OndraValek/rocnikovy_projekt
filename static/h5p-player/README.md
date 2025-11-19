# H5P Player - Instalace

Tato složka je určena pro soubory z h5p-standalone projektu.

## Instalace

1. Jdi na https://github.com/tunapanda/h5p-standalone/releases
2. Stáhni nejnovější release (např. `h5p-standalone-x.x.x.zip`)
3. Rozbal archiv
4. Zkopíruj následující soubory do této složky:

```
static/h5p-player/
  ├── main.bundle.js
  ├── frame.bundle.js
  └── styles/
      └── h5p.css
```

## Struktura

Po instalaci by měla být struktura:

```
static/
  h5p-player/
    ├── main.bundle.js      (z h5p-standalone/dist/)
    ├── frame.bundle.js      (z h5p-standalone/dist/)
    └── styles/
        └── h5p.css          (z h5p-standalone/dist/styles/)
```

## Ověření

Po zkopírování souborů spusť:

```bash
python manage.py collectstatic
```

