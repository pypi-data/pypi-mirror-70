# InOut Scan

Draft for the command deamon that reads bar codes from the serial port and
forwards them to an API.
```
Usage: inout_scan [OPTIONS] COMMAND [ARGS]...

  Gather bar codes from a scanner connected to the serial port and pass them
  to the InOut API. A local cache is maintained to be able to handle
  communication problems. Use the flush command to communicate unsubmitted
  bar codes.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  flush  Flush unsubmitted data to the api
  scan   Listen for strings from a barcode scanner connected to the...
```
## Scan
```
Usage: inout_scan scan [OPTIONS]

  Listen for strings from a barcode scanner connected to the (virtual)
  serial port and make an API call to InOut for each scanned code.

Options:
  --serial_port TEXT   Serial port device that the barcode scanner is
                       connected to.  [default: /dev/ttyACM0]
  --baud_rate INTEGER  Serial baud rate of the bar code scanner.  [default:
                       9600]
  --api_url TEXT       InOut API url.  [required]
  --api_key TEXT       InOut API key.
  --scanner TEXT       Unique scanner name, ie: "reception1".  [required]
  --help               Show this message and exit.
```

## Flush
```
Usage: inout_scan flush [OPTIONS]

  Flush unsubmitted data to the api

Options:
  --api_url TEXT  InOut API url.  [required]
  --api_key TEXT  InOut API key.
  --help          Show this message and exit.
```

# Testing without a bar code scanner
To test the software without a bar code connected, use a virtual
bar code scanner. This can be done by using `socat`:

``` console
$ socat  -d -d  PTY PTY
2020/05/15 10:44:48 socat[47219] N PTY is /dev/pts/3
2020/05/15 10:44:48 socat[47219] N PTY is /dev/pts/4
2020/05/15 10:44:48 socat[47219] N starting data transfer loop with FDs [5,5] and [7,7]
```
It will output the pseudoterminal names. Leave it running.

In another terminal, run `inout_scan`:
``` console
$ inout_scan scan --serial_port /dev/pts/4  --api_url 'https://inout.example.com' --scanner fake_scanner
```

Now, send strings to the other end of the tunnel `/dev/pts/3`, ie:

``` console
$ seq 1 1000 | while read nr; do echo "mybadge$nr" > /dev/pts/3; sleep 1 ;done
```
