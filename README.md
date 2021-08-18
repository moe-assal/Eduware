# Eduware
a collection of exploits, web-scrapers, and bots that are targeted on Eduware-powered web portals

This repository contains two exploits for now.

## Login Xss 

(general)

defs:

attacker.com: (attackers website, use 000webhosting, cz it's free)
portal.com/login: (example: https://portalobkc.almakassed.edu.lb/AccountAdministration/Login)

the login page imports AngularJS v1.6.10 which is vulnerable to reflected xss. Just type `{{constructor.constructor('alert(1)')()}}` under 
the username, anything under Password, then press Login. Weird write?

Well the pecularity happended because AngularJS dynamically loads content that is between double brackets, but in a sandbox. The vulnerability 
allows us to escape the sandbox. [1]

Now the exploit. If we can run JS in the victim's browser, then the sky is the limit. And we can basically sniff the credentials with ease.

Technical details:
A specialy crafted link (attacker.com) is sent to the victim. Once pressed, the html file `index.html` is sent as a response. The file conatains 
a JS payload which is sent to `portal.com/login` via a POST request. The payload is contained in the 'Username' arg. The payload executes doing
this stuff chronologically:
 1. Check if a meta tag is in the document. If true, don't run. else append meta tag to signify that the payload already ran. (important, since 
 the payload will run approx 5 times)
 2. inject form identical to the login form. Autocomplete turned on ( effective in firefox ).
 3. Wait (200ms) and retry recursively to sniff the credentials
 4. Once sniffed, send an XMLHttp GET (I forgot why it needs to be GET) request to attacker.com/api.php with the creds supllied

YOU NEED TO EDIT api.php AND index.html TO ADJUST FOR YOUR SPECIFIC USE CASE.

## Weak-Credentials BruteForce 

(portal.omec.leb specific, can be generalized)

As the title suggests.. More info in the well-documented bruteforce.py

[1]: https://portswigger.net/research/dom-based-angularjs-sandbox-escapes
