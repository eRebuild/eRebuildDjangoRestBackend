# Server Setup

If creating new server pick a new subdirectory to replace django/ and an IP in the address range not taken.

## IIS URL Rewrite Inbound Rule

Pattern = django/(.*)
ActionType = Rewrite
RewriteURL = http://192.168.0.2:8000/{R:1}

## IIS Configuration Editor

preserveHostHeader needs to be set to True

## VM Setup

1. Create new VM in Hyper-V Manager.
2. Turn off SecureBoot
3. Load ISO of OS
    * Currently using Ubuntu Server 22.04.1 LTS
4. Move DVD to first boot device.
5. Install OS
    * Netmask = 192.168.0.0/24
    * Address = 192.168.0.2
    * Gateway = 192.168.0.1
    * DNS     = 8.8.8.8

## Code Update
1. Ensure FORWARDED_TO_VM is set in settings.py.
2. Update Unity artifacts in static/unity/Build
3. Push code changes to GitHub.
4. (For now) Pull latest on server. 
    * Note: Ideally, this is done as a merge request. After the request is accepted, a trigger will happen on the server.