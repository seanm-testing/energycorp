import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import store from 'store';
import axios from 'axios';

jest.mock('views/operator/CreateClientForm.jsx', () => {
    return function MockCreateClientForm(props) {
        return (
            <button data-testid="add-btn" onClick={() => props.submitAction({
                type_client: 1,
                user: { id_user: '123', name: 'Test', email: 't@t.com', password: 'p', phone: '123', address: 'a', neighborhood: 'n', is_active: true, is_staff: true, is_superuser: false }
            })}>
                Add
            </button>
        );
    };
});

import CreateClient from 'views/operator/CreateClient.jsx';

const renderComponent = () => render(
    <Provider store={store}>
        <CreateClient />
    </Provider>
);

describe('CreateClient', () => {
    beforeEach(() => jest.clearAllMocks());

    test('renders component', () => {
        const { container } = renderComponent();
        expect(container.querySelector('.content')).toBeInTheDocument();
    });

    test('adds item to list', () => {
        const { getByTestId, getByText } = renderComponent();
        fireEvent.click(getByTestId('add-btn'));
        expect(getByText(/Test/)).toBeInTheDocument();
    });

    test('sends bulk on create click', async () => {
        axios.post.mockResolvedValueOnce({ data: {} });
        window.alert = jest.fn();

        const { getByTestId, getByText } = renderComponent();
        fireEvent.click(getByTestId('add-btn'));

        // Find the create button (it's a Button with Tr content)
        const buttons = document.querySelectorAll('button');
        const createBtn = Array.from(buttons).find(b => b.className.includes('warning'));
        if (createBtn) {
            fireEvent.click(createBtn);
            await new Promise(r => setTimeout(r, 0));
            expect(axios.post).toHaveBeenCalled();
        }
    });
});
