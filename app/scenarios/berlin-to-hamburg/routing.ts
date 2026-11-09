import type { Parcel, Station } from '../../src/routing.ts';

// Deliberately broken scenario. The functional baseline stays in src/routing.ts.
export function routeParcel(parcel: Parcel): Station {
  switch (parcel.destination) {
    case 'Berlin':
      return 'hamburg';
    case 'Hamburg':
      return 'hamburg';
    case 'München':
      return 'munich';
  }
}
