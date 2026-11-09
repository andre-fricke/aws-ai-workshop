import * as cdk from 'aws-cdk-lib/core';
import { Construct } from 'constructs';

/** Application placeholder. Global budget belongs exclusively to Terraform. */
export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
  }
}
