import { lstatSync } from 'node:fs';
import { resolve, join } from 'node:path';

const artifactPath = process.argv[2];
if (!artifactPath) {
  console.error('Usage: node scripts/verify-artifacts.mjs <artifact-directory>');
  process.exit(1);
}

const directory = resolve(artifactPath);
try {
  if (!lstatSync(directory).isDirectory()) {
    throw new Error('Artifact path must be a directory.');
  }
  for (const file of ['routing.js', 'parcels.js', 'demo.js']) {
    const info = lstatSync(join(directory, file));
    if (!info.isFile() || info.size === 0) {
      throw new Error(`Required artifact must be a nonempty regular file: ${file}`);
    }
  }
  console.log(`Build artifacts verified: ${artifactPath} (routing.js, parcels.js, demo.js)`);
} catch (error) {
  console.error(`Build artifact check failed for ${artifactPath}: ${error.message}`);
  process.exitCode = 1;
}
