import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import CreateReports from 'views/manager/CreateReports.jsx';

describe('CreateReports', () => {
    beforeEach(() => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                json: () => Promise.resolve({
                    numclientsmora: 5,
                    numclientsuspended: 3,
                    mora: [],
                    suspended: [],
                    topfiveplus: [
                        { codeCounter: 1, value: 500 },
                        { codeCounter: 2, value: 400 },
                        { codeCounter: 3, value: 300 },
                        { codeCounter: 4, value: 200 },
                        { codeCounter: 5, value: 100 },
                    ],
                    topfiveminus: [
                        { codeCounter: 6, value: 10 },
                        { codeCounter: 7, value: 20 },
                        { codeCounter: 8, value: 30 },
                        { codeCounter: 9, value: 40 },
                        { codeCounter: 10, value: 50 },
                    ],
                })
            })
        );
    });

    test('renders report buttons', () => {
        const { getByText } = render(<CreateReports />);
        expect(getByText('Slow Payers and Suspended Users')).toBeInTheDocument();
        expect(getByText('Highest Consuming Transformers')).toBeInTheDocument();
        expect(getByText('Lowest Consuming Transformers')).toBeInTheDocument();
    });

    test('initial state shows choose message', () => {
        const { getByText } = render(<CreateReports />);
        expect(getByText(/Choose a report from the options/)).toBeInTheDocument();
    });

    test('clicking button shows report', async () => {
        const { getByText, findByText } = render(<CreateReports />);

        // Wait for componentDidMount fetch
        await new Promise(r => setTimeout(r, 100));

        fireEvent.click(getByText('Slow Payers and Suspended Users'));
        expect(getByText(/Number of Slow Payers/)).toBeInTheDocument();
    });
});
