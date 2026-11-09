import { exampleParcels } from '../../src/parcels.ts';
import { routeParcel } from './routing.ts';

console.log(JSON.stringify(exampleParcels.map((parcel) => ({
  ...parcel,
  station: routeParcel(parcel),
})), null, 2));
