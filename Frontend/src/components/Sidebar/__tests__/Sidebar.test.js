import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

jest.mock('perfect-scrollbar', () => {
    return jest.fn().mockImplementation(() => ({
        destroy: jest.fn()
    }));
});

import Sidebar from 'components/Sidebar/Sidebar.jsx';

const mockRoutes = [
    { path: '/test1', name: 'Test1', icon: 'nc-icon nc-diamond', layout: '/admin' },
    { path: '/test2', name: 'Test2', icon: 'nc-icon nc-pin-3', layout: '/admin' },
];

describe('Sidebar', () => {
    test('renders with routes', () => {
        const { getByText } = render(
            <MemoryRouter>
                <Sidebar routes={mockRoutes} location={{ pathname: '/admin/test1' }} />
            </MemoryRouter>
        );
        expect(getByText('Test1')).toBeInTheDocument();
        expect(getByText('Test2')).toBeInTheDocument();
    });

    test('renders logo brand', () => {
        const { getByText } = render(
            <MemoryRouter>
                <Sidebar routes={mockRoutes} location={{ pathname: '/admin' }} />
            </MemoryRouter>
        );
        expect(getByText('energyCorp')).toBeInTheDocument();
    });

    test('active route gets active class', () => {
        const { container } = render(
            <MemoryRouter initialEntries={['/admin/test1']}>
                <Sidebar routes={mockRoutes} location={{ pathname: '/admin/test1' }} />
            </MemoryRouter>
        );
        const items = container.querySelectorAll('li');
        expect(items[0].className).toContain('active');
    });
});
