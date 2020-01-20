# Ansible Homebrew Services
Ansible module to start/stop macOS services that are managed with
[Homebrew Services](https://github.com/Homebrew/homebrew-services).

## Options
|parameter      |required |default |choices                     |comments|
|---            |---      |---     |---                         |---|
|name           |yes      |        |                            |Name of service that will be started/stopped.|
|state          |no       |auto    |started, stopped, restarted |Whether to start or stop the service.|

## Installing
Just clone the `ansible-homebrew-services` repository into your user custom-module directory:

```
git clone https://github.com/luizribeiro/homebrew-services ~/.ansible/plugins/modules/homebrew-services
```

## Usage
Use it in a task, as in the following examples:
```
- name: Start collectd daemon as root and enable it on boot
  homebrew_services:
    name: collectd
    state: started
  become: yes

- name: Stop nginx daemon and disable it on boot
  homebrew_services:
    name: nginx
    state: stopped
```

## TODOs

* Add support for enabling/disabling services to run on boot, separately from `started`/`stopped` `state`
