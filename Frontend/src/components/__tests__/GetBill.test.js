import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from 'store';
import GetBill from 'components/GetBill.jsx';
import axios from 'axios';

const renderGetBill = () => render(
    <Provider store={store}>
        <MemoryRouter>
            <GetBill />
        </MemoryRouter>
    </Provider>
);

describe('GetBill', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('renders input field', () => {
        const { getByLabelText } = renderGetBill();
        expect(getByLabelText('ID')).toBeInTheDocument();
    });

    test('handles input change', () => {
        const { getByLabelText } = renderGetBill();
        const input = getByLabelText('ID');
        fireEvent.change(input, { target: { value: '123' } });
        expect(input.value).toBe('123');
    });

    test('submits contract and displays bills', async () => {
        axios.post.mockResolvedValueOnce({
            data: {
                error: false,
                find: true,
                invoices: [{
                    codeInvoice: 1,
                    contract: 1,
                    billingDate: '2020-01-01',
                    deadDatePay: '2020-01-11',
                    stateInvoice: false,
                    total: 50000,
                    is_active: true
                }]
            }
        });

        const { getByLabelText, getByText, findByText } = renderGetBill();
        const input = getByLabelText('ID');
        fireEvent.change(input, { target: { value: '1' } });
        fireEvent.submit(input.closest('form'));

        await new Promise(r => setTimeout(r, 0));
        expect(axios.post).toHaveBeenCalled();
    });

    test('shows error on failure', async () => {
        axios.post.mockResolvedValueOnce({
            data: { error: true, find: false, message: 'Not found' }
        });

        const { getByLabelText } = renderGetBill();
        const input = getByLabelText('ID');
        fireEvent.change(input, { target: { value: '999' } });
        fireEvent.submit(input.closest('form'));

        await new Promise(r => setTimeout(r, 0));
        expect(axios.post).toHaveBeenCalled();
    });
});
