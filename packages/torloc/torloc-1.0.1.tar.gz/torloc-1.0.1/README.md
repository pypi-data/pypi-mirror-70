# Torloc
Torloc runs Tor services on local ports. So you can use many different ip addresses without having to start
each service manually.

For Linux, Windows and MacOS.

# Installation

    pip install torloc

Or download the tarball / `git clone` and...

    python setup.py install

# Usage
```python
import torloc

# Several ports
processes = torloc.CreateMany(16)  # threads is 8 by default
ports = processes.ports            # {port: TorProcess}
while not processes.ready:         # Waiting for all ports to be ready
    pass
processes.stop(list(ports.keys())[0])
processes.stop_all()

# One port
process = torloc.TorProcess(49152)
stdout = process.stdout            # file object
stderr = process.stderr            # file object
while not process.ip:              # Waiting for the port to be ready
    pass
process.stop()
```
