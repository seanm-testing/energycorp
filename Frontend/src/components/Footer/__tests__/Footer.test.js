import React from 'react';
import { render } from '@testing-library/react';
import Footer from 'components/Footer/Footer.jsx';

describe('Footer', () => {
    test('renders without crashing', () => {
        const { container } = render(<Footer />);
        expect(container.querySelector('footer')).toBeInTheDocument();
    });

    test('shows copyright text', () => {
        const { getAllByText } = render(<Footer />);
        expect(getAllByText(/Creative Tim/).length).toBeGreaterThan(0);
    });

    test('applies footer-default class when default prop is true', () => {
        const { container } = render(<Footer default={true} />);
        expect(container.querySelector('footer')).toHaveClass('footer-default');
    });
});
