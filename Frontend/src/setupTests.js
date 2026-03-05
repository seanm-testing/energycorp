import '@testing-library/jest-dom/extend-expect';

// Mock react-translate-component.
// In production, webpack's CommonJS interop makes `import * as Tr` callable.
// In Jest, we need __esModule on the function so _interopRequireWildcard returns it directly.
jest.mock('react-translate-component', () => {
    const React = require('react');
    const Tr = (props) => React.createElement(props.component || 'span', null, props.content || '');
    Tr.__esModule = true;
    Tr.default = Tr;
    return Tr;
});

// Mock counterpart (i18n library)
jest.mock('counterpart', () => {
    const translate = (key) => key;
    translate.registerTranslations = jest.fn();
    translate.setLocale = jest.fn();
    translate.translate = translate;
    translate.__esModule = true;
    translate.default = translate;
    return translate;
});
