import { rmSync } from 'node:fs';

// Remove only generated output so stale files cannot conceal a broken build.
rmSync(new URL('../dist/', import.meta.url), { recursive: true, force: true });
