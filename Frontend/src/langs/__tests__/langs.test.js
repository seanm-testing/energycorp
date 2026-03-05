import spanish from 'langs/spanish.js';
import english from 'langs/english.js';
import portuguese from 'langs/portuguese.js';

describe('Language files', () => {
    test('all three have matching top-level keys', () => {
        const esKeys = Object.keys(spanish).sort();
        const enKeys = Object.keys(english).sort();
        const poKeys = Object.keys(portuguese).sort();
        expect(esKeys).toEqual(enKeys);
        expect(esKeys).toEqual(poKeys);
    });

    test('all have home section with required keys', () => {
        const requiredKeys = ['title', 'download', 'pay', 'consult'];
        for (const lang of [spanish, english, portuguese]) {
            for (const key of requiredKeys) {
                expect(lang.home).toHaveProperty(key);
            }
        }
    });

    test('all have getBill section with required keys', () => {
        const requiredKeys = ['insert', 'download', 'home', 'contract', 'total'];
        for (const lang of [spanish, english, portuguese]) {
            for (const key of requiredKeys) {
                expect(lang.getBill).toHaveProperty(key);
            }
        }
    });
});
