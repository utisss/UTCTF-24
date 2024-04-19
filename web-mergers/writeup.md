# Easy Mergers v0.1

### Background

[Prototype Pollution](https://learn.snyk.io/lesson/prototype-pollution/) is a type of vuln where through modification of a JS Object's prototype, you can arbitrarily add properties to objects descendant from the same prototype. This applies to the Object() class, which can lead to adding a property throughout the entire application

### Solution

Examining merger.js, we see that we we can get an arbitrary argument to the exec call if we modify secret somehow. Looking at the code, we need to modify secret.cmd. We can do this by abusing a prototype pollution vulnerability

We are able to pass in objects as an attribute by sending requests to the endpoint ourselves on /api/absorbCompany

Modifying a request to the following will get you the flag. {"attributes":["\_\_proto\_\_"],"values":[{"cmd": "cat flag.txt"  }]}
