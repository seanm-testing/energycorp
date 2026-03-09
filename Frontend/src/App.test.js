import React from 'react';
import { render } from '@testing-library/react';

jest.mock('views/Start.jsx', () => () => <div data-testid="start">Start</div>);
jest.mock('components/login/Login.jsx', () => () => <div>Login</div>);
jest.mock('components/GetBill.jsx', () => () => <div>GetBill</div>);
jest.mock('layouts/DashLayout.jsx', () => () => <div>DashLayout</div>);
jest.mock('components/auth/auth.js', () => ({
    __esModule: true,
    default: {
        isAuthenticated: jest.fn(() => false),
        getType: jest.fn(() => 'admin'),
    },
}));

import App from './App';

describe('App', () => {
    test('renders without crashing', () => {
        const { container } = render(<App />);
        expect(container).toBeTruthy();
    });

    test('renders start at root path', () => {
        const { getByTestId } = render(<App />);
        expect(getByTestId('start')).toBeInTheDocument();
    });
});
