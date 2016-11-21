

# Wavefront CLI

The Wavefront Command Line Interface (CLI) is a utility for automating the installation and configuration of Wavefront Proxies, 
Collector Agents (Telegraf), and Integrations. Future versions will provide an interface for common API tasks such as adding source tags to 
a host, deploying dashboards, and sending events into Wavefront.

## Installation

The Wavefront CLI is available on PyPI as a pip package.

```
$ sudo pip install wavefront-cli
$ wave --version
```

## Running Remotely

The Wavefront CLI can also be run directly via curl. This is useful when you want to install the proxy and/or agent in a single command.
Any command line arguments added to the example below will be passed to the Wavefront CLI.
 
 ```
 $ sudo bash -c "$(curl -sL https://raw.githubusercontent.com/wavefronthq/wavefront-cli/master/sh/install.sh)" --
 ```
 
## Usage

The Wavefront CLI currently three top level commands: `install`, `integration`, and `configure`. 
To see a full list of all options run `wave -h`

### The Install Command

The most common use for the Wavefront CLI, is the installation of the Wavefront Proxy and/or Collector Agent (Telegraf).
The `install` command accepts multiple options. If a required option is not passed as an argument, the CLI will prompt the user for missing input. 
If all required options are passed, the CLI will not prompt for input.

The `install` command accepts 1-4 top level options: `--proxy`, `--agent`, `--statsd`, `--aws`.

- `--proxy` - When passed, the Wavefront Proxy will be installed and configured.
- `--agent` - When passed, Telegraf will be installed and configured.
- `--aws` - *AWS only - When passed, the CLI will add AWS EC2 metadata to the Telegraf configuration as tags. This means metrics from the current host will be tagged with the EC2 tags, AWS region, the VPC ID, and Image ID of the EC2 instance.
- `--statsd` - When passed, the Telegraf StatsD service plugin will be enabled. *Note: This requires installing Telegraf via the `--agent` option. 

#### Install: Example Usage

Each top-level option has 1 to several sub-options. If any required sub-option is not provided, the CLI will prompt for input. 
Below is a complete example of the install command. This example would install the Wavefront Proxy, Telegraf, configure AWS tags, and StatsD 
without prompting the user for input.

```
$ sudo bash -c "$(curl -sL https://raw.githubusercontent.com/wavefronthq/wavefront-cli/master/sh/install.sh)" -- \
    --proxy \
        --wavefront-url=https://try.wavefront.com \
        --api-token=YOUR_API_TOKEN \
    --agent \
        --proxy-address=localhost \
        --proxy-port=2878 \
    --statsd \
        --statsd-port=8125 \
    --aws \
        --aws-region=us-west-2 \
        --aws-secret-key-id=YOUR_KEY_ID \
        --aws-secret-key=YOUR_SECRET_KEY
```
 
### The Integration Command

The `integration` will install a Wavefront integration. In most cases, this means generating a Telegraf config file in `/etc/telegraf/telegraf.d`
and deploying a template Dashboard.

```
wave integration <name> (install|remove) [<option>...]
```

