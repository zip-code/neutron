# Copyright 2014 OpenStack Foundation
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo.config import cfg


n1kv_opts = [
    cfg.ListOpt('n1kv_vsm_ips',
               help=_("Comma Seperated IP Addresses of the Cisco Nexus1000V "
                      "VSMs")),
    cfg.StrOpt('username',
               help=_("Username for the Cisco Nexus1000V VSM")),
    cfg.StrOpt('password',
               help=_("Password for the Cisco Nexus1000V VSM"), secret=True),
    cfg.StrOpt('default_vlan_network_profile', default='default-vlan-np',
               help=_("Cisco Nexus1000V default network profile for VLAN "
                      "networks")),
    cfg.StrOpt('default_vxlan_network_profile', default='default-vxlan-np',
               help=_("Cisco Nexus1000V default network profile for VXLAN "
                      "networks")),
    cfg.StrOpt('default_policy_profile', default='default-pp',
               help=_("Cisco Nexus1000V default policy profile")),
    cfg.BoolOpt('restrict_policy_profiles', default=False,
               help=_("Restrict the visibility of policy profiles to the "
                      "tenants")),
    cfg.BoolOpt('enable_vif_type_n1kv', default=False,
               help=_("Set the portbinding VIF type to N1KV. "
                      "If it is set to False, VIF type will be set to OVS.")),
    cfg.IntOpt('poll_duration', default=60,
               help=_("Cisco Nexus1000V policy profile polling duration in "
                      "seconds")),
    cfg.IntOpt('http_pool_size', default=4,
               help=_("Number of threads to use to make HTTP requests")),
    cfg.IntOpt('http_timeout', default=15,
               help=_("HTTP timeout, in seconds, for connections to the "
                      "Nexus1000V VSM")),
    cfg.IntOpt('sync_interval', default=300,
               help=_("Time interval between consecutive neutron-VSM syncs ")),

]


cfg.CONF.register_opts(n1kv_opts, "ml2_cisco_n1kv")