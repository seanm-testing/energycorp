import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import store from 'store';
import axios from 'axios';

jest.mock('components/auth/auth.js', () => ({
    __esModule: true,
    default: {
        isAuthenticated: jest.fn(() => true),
        getType: jest.fn(() => 'operator'),
        getObj: jest.fn(() => ({ id: 1 })),
        getSession: jest.fn(() => ({ id: 1 })),
    },
}));

import Payment from 'views/operator/Payment.jsx';

const renderPayment = () => render(
    <Provider store={store}>
        <Payment />
    </Provider>
);

describe('Payment', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        global.fetch = jest.fn(() => Promise.resolve({
            json: () => Promise.resolve([])
        }));
    });

    test('renders contract input', () => {
        const { container } = renderPayment();
        const input = container.querySelector('input[name="contract"]');
        expect(input).toBeInTheDocument();
    });

    test('handles contract input change', () => {
        const { container } = renderPayment();
        const input = container.querySelector('input[name="contract"]');
        fireEvent.change(input, { target: { name: 'contract', value: '42' } });
        expect(input.value).toBe('42');
    });

    test('submits contract query', async () => {
        axios.post.mockResolvedValueOnce({
            data: { error: false, find: true, invoices: [] }
        });

        const { container } = renderPayment();
        const input = container.querySelector('input[name="contract"]');
        fireEvent.change(input, { target: { name: 'contract', value: '1' } });
        fireEvent.submit(input.closest('form'));

        await new Promise(r => setTimeout(r, 0));
        expect(axios.post).toHaveBeenCalled();
    });
});
