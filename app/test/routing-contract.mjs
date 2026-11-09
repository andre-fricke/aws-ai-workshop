import assert from 'node:assert/strict';
import { test } from 'node:test';

// Explicit business expectations, independent of implementation and demo data.
// Two different IDs per destination detect routing tied to a single sample ID.
const cases = [
  { id: 'CHECK-B1', destination: 'Berlin', expected: 'berlin' },
  { id: 'OTHER-B2', destination: 'Berlin', expected: 'berlin' },
  { id: 'CHECK-H1', destination: 'Hamburg', expected: 'hamburg' },
  { id: 'OTHER-H2', destination: 'Hamburg', expected: 'hamburg' },
  { id: 'CHECK-M1', destination: 'München', expected: 'munich' },
  { id: 'OTHER-M2', destination: 'München', expected: 'munich' },
];

export function verifyRouting(routeParcel) {
  for (const { id, destination, expected } of cases) {
    test(`${id}: ${destination} → ${expected}`, () => {
      const parcel = Object.freeze({ id, destination });
      assert.equal(routeParcel(parcel), expected);
    });
  }
}
