describe('Auth class', () => {
    let auth;

    beforeEach(() => {
        localStorage.clear();
        jest.resetModules();
        auth = require('components/auth/auth.js').default;
        // Reset the singleton state
        auth.authenticated = null;
    });

    test('isAuthenticated returns false initially', () => {
        expect(auth.isAuthenticated()).toBe(false);
    });

    test('login stores session and calls callback', () => {
        const obj = { user_type_name: 'admin', token: 'abc', user_id: '123' };
        const cb = jest.fn();
        auth.login(obj, cb);
        expect(auth.isAuthenticated()).toBe(true);
        expect(cb).toHaveBeenCalledWith('admin');
    });

    test('logout clears session and calls callback', () => {
        const obj = { user_type_name: 'operator', token: 'x' };
        auth.login(obj, jest.fn());
        const cb = jest.fn();
        auth.logout(cb);
        expect(auth.isAuthenticated()).toBe(false);
        expect(cb).toHaveBeenCalled();
    });

    test('getType returns user_type_name', () => {
        const obj = { user_type_name: 'manager', token: 'x' };
        auth.login(obj, jest.fn());
        expect(auth.getType()).toBe('manager');
    });

    test('getSession returns parsed session', () => {
        const obj = { user_type_name: 'admin', token: 'abc', user_id: '1' };
        auth.login(obj, jest.fn());
        const session = auth.getSession();
        expect(session.token).toBe('abc');
    });

    test('getObj returns parsed object', () => {
        const obj = { user_type_name: 'admin', id: 5 };
        auth.login(obj, jest.fn());
        expect(auth.getObj().id).toBe(5);
    });

    test('login sets localStorage', () => {
        const obj = { user_type_name: 'admin', token: 'tok' };
        auth.login(obj, jest.fn());
        expect(localStorage.getItem('session')).toBeTruthy();
    });

    test('logout clears localStorage', () => {
        const obj = { user_type_name: 'admin' };
        auth.login(obj, jest.fn());
        auth.logout(jest.fn());
        expect(localStorage.getItem('session')).toBeNull();
    });
});
