#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { InfraStack } from '../lib/infra-stack';

const app = new cdk.App();
new InfraStack(app, 'WorkshopAppStack', {
  description: 'Workshop application infrastructure; budget managed separately by Terraform.',
  analyticsReporting: false,
  env: { account: '331001679034', region: 'eu-north-1' },
});
