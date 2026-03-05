import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ProtectedRoute, ProtectedLoginRoute } from 'components/auth/ProtectedRoute.js';

jest.mock('components/auth/auth.js', () => ({
    __esModule: true,
    default: {
        isAuthenticated: jest.fn(),
        getType: jest.fn(),
    },
}));

const auth = require('components/auth/auth.js').default;

const TestComponent = () => <div data-testid="protected">Protected Content</div>;

describe('ProtectedRoute', () => {
    test('redirects to login when unauthenticated', () => {
        auth.isAuthenticated.mockReturnValue(false);
        const { queryByTestId } = render(
            <MemoryRouter initialEntries={['/admin']}>
                <ProtectedRoute path="/admin" userType="admin" render={() => <TestComponent />} />
            </MemoryRouter>
        );
        expect(queryByTestId('protected')).toBeNull();
    });

    test('renders component when correct type', () => {
        auth.isAuthenticated.mockReturnValue(true);
        auth.getType.mockReturnValue('admin');
        const { getByTestId } = render(
            <MemoryRouter initialEntries={['/admin']}>
                <ProtectedRoute path="/admin" userType="admin" render={() => <TestComponent />} />
            </MemoryRouter>
        );
        expect(getByTestId('protected')).toBeInTheDocument();
    });

    test('redirects when wrong type', () => {
        auth.isAuthenticated.mockReturnValue(true);
        auth.getType.mockReturnValue('operator');
        const { queryByTestId } = render(
            <MemoryRouter initialEntries={['/admin']}>
                <ProtectedRoute path="/admin" userType="admin" render={() => <TestComponent />} />
            </MemoryRouter>
        );
        expect(queryByTestId('protected')).toBeNull();
    });
});

describe('ProtectedLoginRoute', () => {
    test('renders login when unauthenticated', () => {
        auth.isAuthenticated.mockReturnValue(false);
        const LoginComponent = () => <div data-testid="login">Login</div>;
        const { getByTestId } = render(
            <MemoryRouter initialEntries={['/login']}>
                <ProtectedLoginRoute path="/login" component={LoginComponent} />
            </MemoryRouter>
        );
        expect(getByTestId('login')).toBeInTheDocument();
    });

    test('redirects away from login when authenticated', () => {
        auth.isAuthenticated.mockReturnValue(true);
        auth.getType.mockReturnValue('admin');
        const LoginComponent = () => <div data-testid="login">Login</div>;
        const { queryByTestId } = render(
            <MemoryRouter initialEntries={['/login']}>
                <ProtectedLoginRoute path="/login" component={LoginComponent} />
            </MemoryRouter>
        );
        expect(queryByTestId('login')).toBeNull();
    });
});
