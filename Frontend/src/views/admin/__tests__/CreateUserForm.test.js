import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import store from 'store';
import CreateUserForm from 'views/admin/CreateUserForm.jsx';

const renderForm = (props = {}) => render(
    <Provider store={store}>
        <CreateUserForm submitAction={jest.fn()} editMode={false} {...props} />
    </Provider>
);

describe('CreateUserForm', () => {
    test('renders all form fields', () => {
        const { getByPlaceholderText } = renderForm();
        expect(getByPlaceholderText('ID')).toBeInTheDocument();
        expect(getByPlaceholderText('Email')).toBeInTheDocument();
    });

    test('handles input changes', () => {
        const { getByPlaceholderText } = renderForm();
        const idInput = getByPlaceholderText('ID');
        fireEvent.change(idInput, { target: { name: 'id_user', value: '12345' } });
        expect(idInput.value).toBe('12345');
    });

    test('submit calls submitAction prop', () => {
        const submitAction = jest.fn();
        const { container } = renderForm({ submitAction });
        const form = container.querySelector('form');
        fireEvent.submit(form);
        expect(submitAction).toHaveBeenCalled();
    });

    test('edit mode shows state selector', () => {
        const { container } = renderForm({ editMode: true });
        const selects = container.querySelectorAll('select');
        // Should have user_type select + is_active select
        expect(selects.length).toBeGreaterThanOrEqual(2);
    });
});
