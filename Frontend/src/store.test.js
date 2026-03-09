import store from './store';

describe('Redux store', () => {
    test('initial state has language es', () => {
        const state = store.getState();
        expect(state.language).toBe('es');
    });

    test('CHANGE_LAN action updates language', () => {
        store.dispatch({ type: 'CHANGE_LAN', language: 'en' });
        expect(store.getState().language).toBe('en');
        // Reset
        store.dispatch({ type: 'CHANGE_LAN', language: 'es' });
    });

    test('unknown action returns current state', () => {
        const before = store.getState();
        store.dispatch({ type: 'UNKNOWN_ACTION' });
        expect(store.getState()).toEqual(before);
    });
});
