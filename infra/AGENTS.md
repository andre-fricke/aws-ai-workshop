# AGENTS.md

The repository-root `AGENTS.md` applies here. Follow
[AWS-KI-Workshop.md](../AWS-KI-Workshop.md) as the authoritative project plan;
this file adds CDK-specific instructions.

This is an AWS CDK app written in TypeScript. The app entry point is the file in
`bin/` that creates the `App`; the stack is defined in `lib/` (the `*-stack.ts`
file). `cdk.json` tells the CDK Toolkit how to run the app.

## Read the construct library docs before writing code

AWS CDK service documentation ships inside the aws-cdk-lib package. After you
install dependencies with `npm install` (so `node_modules/aws-cdk-lib` exists)
and before you write your CDK constructs, find the service READMEs once:

```
find node_modules/aws-cdk-lib -name README.md
```

For each AWS service you use in this app, read that service's module README (for
example, `node_modules/aws-cdk-lib/aws-s3/README.md`) first and follow its
documented construct usage and patterns. Not every service has a README; a
missing one is not an error. Read the relevant READMEs before writing the
constructs for each service.

Before reading a service README, list its section headings with
`grep -n '^#' node_modules/aws-cdk-lib/<module>/README.md`, then read only the
sections for the constructs you use, for example with
`sed -n '<start>,<end>p' node_modules/aws-cdk-lib/<module>/README.md`. Do not
read a whole README into context or re-read a section you have already read.

## Check your work

Run applicable local routine checks independently within the current assignment,
from `infra/`:

- `npm run build` — type-check the project.
- `npm run test` — run the jest unit tests.
- `npx cdk synth` — synthesize the CloudFormation template. This is local only
  when all required context is available and the app performs no cloud calls;
  missing context lookups can access AWS. Inspect the app and context first.

Checks with cloud access are separate from local checks:

- `npx cdk diff` compares against AWS and can create a CloudFormation change set
  in its default mode. Explain the mode, cloud access and possible side effects
  first. Any cloud change requires the concrete approval described below.
- Other AWS reads or lookups must be identified as cloud checks, including any
  possible costs. Existing credentials do not imply approval for cloud changes.

## Cloud changes and approval

Manage AWS infrastructure exclusively through IaC. Before cloud changes,
including `cdk deploy`, `cdk bootstrap` and `cdk destroy`, explain the concrete
resources, permissions and expected costs and obtain approval for that scope.
Do not ask again for already approved substeps; obtain further approval if the
scope changes. Do not use manual Console changes as a substitute.

Later, automatic demo deployments may run within explicitly approved limits;
this is not approval for automatic CDK/CloudFormation changes. Do not commit,
push or publish without an explicit assignment.

## More resources

- [AWS CDK Reference](https://docs.aws.amazon.com/cdk/api/)
