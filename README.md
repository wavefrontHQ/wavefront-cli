

# Wavefront CLI

The Wavefront Command Line Interface (CLI) is a utility for automating the installation and configuration of the Wavefront proxy, 
Telegraf (metric collector agent), and integrations. The CLI uses native package managers to install packages (i.e. yum, apt-get) and therefore
should be run as sudo.

## Installation

The Wavefront CLI is available on PyPI as a pip package.

```
$ sudo pip install wavefront-cli
```

## Running Remotely

The Wavefront CLI can also be run directly via curl. This is useful when you want to install the proxy and/or agent in a single command.
Any command line arguments added to the example below will be passed to the Wavefront CLI.
 
 ```
 $ sudo bash -c "$(curl -sL https://raw.githubusercontent.com/wavefronthq/wavefront-cli/master/sh/install.sh)" --
 ```
 
## Usage

The Wavefront CLI currently has three top level commands: `install`, `integration`, and `configure`. 
To see a full list of all options run `wave -h`

### The Install Command

The most common use for the Wavefront CLI, is the installation of the Wavefront Proxy and/or Telegraf on a host.
The `install` command accepts multiple options. If a required option is not passed as an argument, the CLI will prompt the user for missing input. 
If all required options are passed, the CLI will not prompt for input.

The `install` command accepts 1-4 top level options: `--proxy`, `--agent`, `--statsd`, `--aws`.

- `--proxy` - When passed, the Wavefront Proxy will be installed and configured on the current host.
- `--agent` - When passed, Telegraf will be installed and configured on the current host.
- `--aws` - *AWS only - When passed, the CLI will add AWS EC2 metadata to the Telegraf configuration as tags. This means metrics from the current host will be tagged with the EC2 tags, AWS region, the VPC ID, and Image ID of the EC2 instance.
- `--statsd` - When passed, the Telegraf StatsD service plugin will be enabled. *Note: This requires installing Telegraf via the `--agent` option. 

#### Install: Example Usage

Each top-level option has 1 to several sub-options. If any required sub-option is not provided, the CLI will prompt for input. 
Below are examples of the install command. This example would install the Wavefront Proxy, Telegraf, configure AWS tags, and StatsD 
without prompting the user for input.


*Install Proxy and Telegraf (the CLI will prompt for required options):*
```
$ sudo wave --proxy --agent 
```

*Install Proxy and Telegraf with no prompt:*
```
$ sudo wave \
    --proxy \
        --wavefront-url=https://YOUR_INSTANCE.wavefront.com \
        --api-token=YOUR_API_TOKEN \
    --agent \
        --proxy-address=localhost \
        --proxy-port=2878
```
 
*Install Proxy and Telegraf and configure AWS Metadata and StatsD in Telegraf:*
```
$ sudo wave \
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
 
 
### The Integration Command

The `integration` command will install or remove a Wavefront integration. In most cases, this means generating a Telegraf config file in `/etc/telegraf/telegraf.d`
and deploying a template Dashboard.

```
$ wave integration <name> (install|remove) [<option>...]
```

#### Integration: Example Usage

Install StatsD service plugin on port 8215 (default) in Telegraf:

```
$ wave integration StatsD install statsd_port=8125
```

Install Wavefront output plugin in Telegraf to emit to a Proxy installed on localhost:2878:

```
$ wave integration Wavefront install proxy_address=localhost proxy_port=2878
```

#### Contributing Integrations

The `<name>` argument of the `integration` command will create an instance of a `wavefront_cli.integrations.Base` subclass matching the `<name>` argument. 
When installing an integration, any arguments passed in the `[<option>...]` part of the command are passed to the subclass as a dictionary. This makes it possible
to drop-in new integrations.

At a minimum, an integration subclass must implement the following methods:
```
class Example(Base):

    def install(self):
        return True
        
    def remove(self):
        return True

    def validate_options(self):
        return True
```

See `wavefront_cli/integrations/statsd.py` for a very simple example of an integration implementation.  


## Release Process

`release.sh` will package and ship this module to PyPI. If you wish to cut your own version and upload to your own PyPI project, edit `setup.py`.

```
$ ./release.sh
```