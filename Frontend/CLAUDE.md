# Frontend Local Development

## Node Version Requirement

This project requires **Node 12** (tested with v12.22.12). It will NOT work with newer Node versions due to:

- `node-sass@4.12.0` — uses native bindings that only compile against Node 12 and below
- `react-scripts@3.0.1` — incompatible with Node 14+

### Using nvm

```bash
nvm use 12          # Switch to Node 12
# or install it first:
nvm install 12
```

When running any npm command (install, start, build, test), always ensure Node 12 is active first.

In non-interactive shells (scripts, CI, background tasks), nvm must be sourced explicitly via a login shell:

```bash
bash -l -c 'export NVM_DIR="$HOME/.nvm"; source "$NVM_DIR/nvm.sh"; nvm use 12 && npm start'
```

`nvm.sh` exits with code 3 in non-login shells even when it works — use `bash -l` to avoid this.

## Installing Dependencies

```bash
nvm use 12
npm install --no-optional
```

- The `--no-optional` flag skips optional dependencies (`@types/*`, `jquery`, `typescript`) that aren't needed at runtime and avoids potential install issues.
- If `npm install` fails with **"Maximum call stack size exceeded"**, delete `package-lock.json` and `node_modules/`, then reinstall:

```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --no-optional
```

## Starting the Dev Server

```bash
nvm use 12
npm start          # Starts on http://localhost:3000
```

The backend Django API must also be running (default: http://localhost:8000) for the app to function. Start it from `Backend/src/`:

```bash
python manage.py runserver 8000
```

## Known Warnings (Safe to Ignore)

- `Browserslist: caniuse-lite is outdated` — cosmetic warning, does not affect functionality
- `found N vulnerabilities` after install — expected for dependencies from 2020; do not run `npm audit fix` as it may break compatibility
