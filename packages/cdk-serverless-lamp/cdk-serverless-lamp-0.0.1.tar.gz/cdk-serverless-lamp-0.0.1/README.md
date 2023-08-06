# Welcome to `cdk-serverless-lamp`

A JSII construct library for AWS CDK to build the [New Serverless LAMP Stack](https://aws.amazon.com/tw/blogs/compute/introducing-the-new-serverless-lamp-stack/)

## Prepare the vendor directory with `gizzlehttp` and `bref`

```bash
$ git clone https://github.com/pahud/cdk-serverless-lamp.git
$ cd cdk-serverless-lamp
$ mkdir composer && cd composer
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer require guzzlehttp/guzzle
$ docker run --rm -ti \
  --volume $PWD:/app \
  composer require bref/bref
```

(`./composer/vendor` will be created)

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_serverless_lamp import ServerlessApi

ServerlessApi(self, "API")
```
