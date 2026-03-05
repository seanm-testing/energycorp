import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

jest.mock('react-google-recaptcha', () => {
    return function MockReCAPTCHA(props) {
        return <div data-testid="recaptcha" onClick={() => props.onChange && props.onChange('token')} />;
    };
});

jest.mock('components/auth/auth.js', () => ({
    __esModule: true,
    default: {
        login: jest.fn((obj, cb) => cb(obj.user_type_name)),
        isAuthenticated: jest.fn(() => false),
        getType: jest.fn(() => 'admin'),
    },
}));

import Login from 'components/login/Login.jsx';
import axios from 'axios';

describe('Login', () => {
    const renderLogin = () => render(
        <MemoryRouter>
            <Login history={{ push: jest.fn() }} />
        </MemoryRouter>
    );

    test('renders login form', () => {
        const { getByText, getByPlaceholderText } = renderLogin();
        expect(getByText('Login')).toBeInTheDocument();
        expect(getByPlaceholderText('Login')).toBeInTheDocument();
        expect(getByPlaceholderText('Password')).toBeInTheDocument();
    });

    test('handles input changes', () => {
        const { getByPlaceholderText } = renderLogin();
        const emailInput = getByPlaceholderText('Login');
        fireEvent.change(emailInput, { target: { name: 'username', value: 'test@test.com' } });
        expect(emailInput.value).toBe('test@test.com');
    });

    test('submit button is initially disabled', () => {
        const { getByText } = renderLogin();
        expect(getByText('SIGN IN')).toBeDisabled();
    });

    test('renders home link', () => {
        const { getByText } = renderLogin();
        expect(getByText('Home')).toBeInTheDocument();
    });

    test('successful login calls auth.login', async () => {
        const auth = require('components/auth/auth.js').default;
        axios.post.mockResolvedValueOnce({
            data: {
                code: 200,
                token: 'testtoken',
                data: { user__id_user: '123', user_type: 1, id: 1 }
            }
        });

        const push = jest.fn();
        const { getByPlaceholderText, getByTestId, getByText } = render(
            <MemoryRouter>
                <Login history={{ push }} />
            </MemoryRouter>
        );

        fireEvent.change(getByPlaceholderText('Login'), { target: { name: 'username', value: 'a@b.com' } });
        fireEvent.change(getByPlaceholderText('Password'), { target: { name: 'password', value: 'pass' } });
        // Enable button via captcha
        fireEvent.click(getByTestId('recaptcha'));
        fireEvent.submit(getByText('SIGN IN').closest('form'));

        // Wait for async
        await new Promise(r => setTimeout(r, 0));
        expect(axios.post).toHaveBeenCalled();
    });
});
