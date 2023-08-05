#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.devices.flows.snmp_action_flows import AutoloadFlow
from cloudshell.firewall.paloalto.panos.autoload.panos_snmp_autoload import PanOSSNMPAutoload


class PanOSSnmpAutoloadFlow(AutoloadFlow):
    def execute_flow(self, supported_os, shell_name, shell_type, resource_name):
        with self._snmp_handler.get_snmp_service() as snpm_service:
            snmp_autoload = PanOSSNMPAutoload(
                snpm_service, shell_name, shell_type, resource_name, self._logger)
        return snmp_autoload.discover(supported_os)
