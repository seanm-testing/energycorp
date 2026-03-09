# Frontend Local Development

## Node Version Requirement

This project requires **Node 12** (tested with v12.22.12). It will NOT work with newer Node versions due to:

- `node-sass@4.12.0` — uses native bindings that only compile against Node 12 and below
- `react-scripts@3.0.1` — incompatible with Node 14+

### Using nvm

```bash
nvm use 12          # Switch to Node 12 (interactive shells only)
# or install it first:
nvm install 12
```

When running any npm command (install, start, build, test), always ensure Node 12 is active first.

### Non-interactive shells (Claude Code, scripts, CI)

`nvm use` and `nvm.sh` are unreliable in non-interactive shells — `nvm.sh` exits with code 3 and `bash -l` does not reliably fix it. **The most reliable approach is to prepend the Node 12 binary directory to PATH directly:**

```bash
PATH="$HOME/.nvm/versions/node/v12.22.12/bin:$PATH" npm test -- --watchAll=false --coverage
```

This works for any npm command (install, start, build, test). Always use this pattern instead of `nvm use` when running from non-interactive shells.

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
python3 manage.py runserver 8000
```

## Known Warnings (Safe to Ignore)

- `Browserslist: caniuse-lite is outdated` — cosmetic warning, does not affect functionality
- `found N vulnerabilities` after install — expected for dependencies from 2020; do not run `npm audit fix` as it may break compatibility

## Testing

52 tests across 14 suites using Jest (bundled with react-scripts 3.0.1) and `@testing-library/react@9.5.0`.

```bash
nvm use 12
npm test                                  # Interactive watch mode
npm test -- --watchAll=false              # Run once
npm test -- --watchAll=false --coverage   # Run once with coverage report
```

Coverage is scoped to tested files via `collectCoverageFrom` in `package.json` (~74%).

### Test Infrastructure

- `src/setupTests.js` — Global mocks for `react-translate-component` and `counterpart`. Uses `__esModule = true` on mock functions to handle the `import * as Tr` CommonJS/ESM interop difference between webpack and babel-jest.
- `src/__mocks__/axios.js` — Mock axios with `jest.fn()` for get/post/put/delete/create.
- `src/__mocks__/fileMock.js` — Returns `'test-file-stub'` for image imports.
- `src/__mocks__/styleMock.js` — Returns `{}` for CSS imports.

### Adding New Tests

When testing components that use `react-translate-component` (`import * as Tr from "react-translate-component"`), the global mock in `setupTests.js` handles it automatically. Components that need Redux state should be wrapped with `<Provider store={store}>`. Auth-dependent components should mock `components/auth/auth.js`.
