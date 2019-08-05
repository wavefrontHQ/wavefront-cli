The Wavefront Integration Command Line Interface (CLI) is a utility for installing and configuring the Wavefront proxy, Telegraf
collector agent, and integrations. The CLI uses native package managers to install packages (i.e. yum, apt-get) and therefore should be run as sudo.

## Requirements

The Wavefront Integration CLI is currently supported on Linux environments only and has been tested on the following Linux versions:

-   Amazon Linux AMI 2016.09.0
-   CentOS 6.7, 7.2
-   Debian Jesse, Wheezy
-   RedHat 6.6, 7.3
-   Ubuntu 14.04, 16.04

The lowest version of Python the CLI has been tested with is 2.6.6.

## Installing Wavefront Integration CLI

The Wavefront Integration CLI is available on PyPI as a pip package. To install the CLI, run:

```shell
$ sudo pip install wavefront-cli
```

## Installing and Running Wavefront Integration CLI

You can install and run the Wavefront Integration CLI directly via `curl`. This is useful when you want to install the CLI, Wavefront proxy, and/or agent in a single command. Arguments added to the following command are passed to the CLI.

```shell
$ sudo bash -c "$(curl -sL https://raw.githubusercontent.com/wavefronthq/wavefront-cli/master/sh/install.sh)" --
```

## Usage

To invoke the Wavefront Integration CLI, run

```shell
$ sudo wave <command>
```

where `<command>` is `install`, `integration`, or `configure`. To see a full list of all options, run `wave -h`.

### The Install Command

The most common use for the Wavefront Integration CLI is installing the Wavefront proxy and/or Telegraf. The `install` command
accepts multiple options each of which accepts arguments. If a required argument is not passed to an option, the CLI
prompts you for missing input. If all required arguments are passed, the CLI does not prompt for input.

The `install` command accepts one or more options:

-   `--proxy` - Install and configure the Wavefront proxy on the current host.
-   `--agent` - Install and configure Telegraf on the current host.
-   `--aws` - Add [AWS EC2 metadata](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html) to the Telegraf
configuration as tags. Metrics from an EC2 instance are tagged with the EC2 tags, AWS region, the VPC ID, and Image ID of the EC2 instance.
-   `--statsd` - Enable the Telegraf StatsD service plugin. You must also install Telegraf with the `--agent` option.

### Install: Example Usage

Each option has one or more arguments. If you do not provide a required argument, the CLI prompts for input.

Install a Wavefront proxy and Telegraf (the CLI prompts for required options):

```shell
$ sudo wave install --proxy --agent
```

Install a Wavefront proxy and Telegraf agent with no prompts:

```shell
$ sudo wave install \
    --proxy \
        --wavefront-url=https://YOUR_INSTANCE.wavefront.com \
        --api-token=YOUR_API_TOKEN \
    --agent \
        --proxy-address=localhost \
        --proxy-port=2878
```

Install the Wavefront proxy and Telegraf agent and configure AWS metadata and StatsD in Telegraf:

```shell
$ sudo wave install \
    --proxy \
        --wavefront-url=https://YOUR_INSTANCE.wavefront.com \
        --api-token=YOUR_API_TOKEN \
    --agent \
        --proxy-address=localhost \
        --proxy-port=2878 \
        --agent-tags="env=dev,app=myapp"
    --statsd \
        --statsd-port=8125 \
    --aws \
        --aws-region=us-west-2 \
        --aws-secret-key-id=YOUR_KEY_ID \
        --aws-secret-key=YOUR_SECRET_KEY
```

## The Integration Command

The `integration` command installs or removes a Wavefront integration. In most cases, this means generating a Telegraf
config file in `/etc/telegraf/telegraf.d`.

```shell
$ sudo wave integration <name> (install|remove) [<option>...]
```

### Integration: Example Usage

Install StatsD service plugin on port 8215 (default) in Telegraf:

```shell
$ sudo wave integration StatsD install statsd_port=8125
```

Install Wavefront output plugin in Telegraf to emit to a Wavefront proxy installed on localhost:2878:

```shell
$ sudo wave integration Wavefront install proxy_address=localhost proxy_port=2878
```

### Contributing Integrations

The `<name>` argument of the `integration` command creates an instance of a `wavefront_cli.integrations.Base` subclass
matching the `<name>` argument. When installing an integration, any arguments passed in the `[<option>...]` part of the
command are passed to the subclass as a dictionary. This makes it possible to drop in new integrations. At a minimum,
an integration subclass must implement the following methods:

```python
class Example(Base):

    def install(self):
        return True

    def remove(self):
        return True

    def validate_options(self):
        return True
```

See [`wavefront_cli/integrations/statsd.py`](https://raw.githubusercontent.com/wavefrontHQ/wavefront-cli/master/wavefront_cli/integrations/statsd.py) for a very simple example of an integration implementation.

## The Configure Command

The `configure` command updates the Wavefront URL and API token.

```shell
$ sudo wave configure \
    --wavefront-url=https://YOUR_INSTANCE.wavefront.com \
    --api-token=YOUR_API_TOKEN \
```

## Release Process

`release.sh` packages and ships this module to PyPI. To create your own version and upload to your own PyPI project, edit `setup.py`.

```shell
$ ./release.sh
```
