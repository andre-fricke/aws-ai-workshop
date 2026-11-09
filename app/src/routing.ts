export type Destination = 'Berlin' | 'Hamburg' | 'München';
export type Station = 'berlin' | 'hamburg' | 'munich';

export interface Parcel {
  readonly id: string;
  readonly destination: Destination;
}

/** Route a parcel using its destination, independently of its ID. */
export function routeParcel(parcel: Parcel): Station {
  switch (parcel.destination) {
    case 'Berlin':
      return 'berlin';
    case 'Hamburg':
      return 'hamburg';
    case 'München':
      return 'munich';
  }
}
