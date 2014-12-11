# Copyright 2014 OpenStack Foundation
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
#

"""Cisco N1kv ML2 driver tables

Revision ID: 589f9237ca0e
Revises: 796c68dffbb
Create Date: 2014-08-13 13:31:43.537460

"""

# revision identifiers, used by Alembic.
revision = '589f9237ca0e'
down_revision = '796c68dffbb'


from alembic import op
import sqlalchemy as sa

network_profile_type = sa.Enum('vlan', 'vxlan', 'trunk',
                               name='network_profile_type')
profile_type = sa.Enum('network', 'policy', name='profile_type')

def upgrade(active_plugins=None, options=None):

    op.create_table(
        'cisco_ml2_n1kv_policy_profiles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'cisco_ml2_n1kv_network_profiles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('segment_type', network_profile_type, nullable=False),
        sa.Column('segment_range', sa.String(length=255), nullable=True),
        sa.Column('multicast_ip_index', sa.Integer(), nullable=True),
        sa.Column('multicast_ip_range', sa.String(length=255), nullable=True),
        sa.Column('sub_type', sa.String(length=255), nullable=True),
        sa.Column('physical_network', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'cisco_ml2_n1kv_port_bindings',
        sa.Column('port_id', sa.String(length=36), nullable=False),
        sa.Column('profile_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['port_id'], ['ports.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profile_id'],
                                ['cisco_ml2_n1kv_policy_profiles.id']),
        sa.PrimaryKeyConstraint('port_id'),
    )

    op.create_table(
        'cisco_ml2_n1kv_network_bindings',
        sa.Column('network_id', sa.String(length=36), nullable=False),
        sa.Column('network_type', sa.String(length=32), nullable=False),
        sa.Column('segmentation_id', sa.Integer(), autoincrement=False),
        sa.Column('profile_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['network_id'], ['networks.id'],
                                ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['profile_id'],
                                ['cisco_ml2_n1kv_network_profiles.id']),
        sa.PrimaryKeyConstraint('network_id')
    )

    op.create_table(
        'cisco_ml2_n1kv_vxlan_allocations',
        sa.Column('vxlan_id', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('allocated', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('vxlan_id')
    )

    op.create_table(
        'cisco_ml2_n1kv_vlan_allocations',
        sa.Column('physical_network', sa.String(length=64), nullable=False),
        sa.Column('vlan_id', sa.Integer(), autoincrement=False,
                  nullable=False),
        sa.Column('allocated', sa.Boolean(), autoincrement=False,
                  nullable=False),
        sa.PrimaryKeyConstraint('physical_network', 'vlan_id')
     )

    op.create_table(
        'cisco_ml2_n1kv_profile_bindings',
        sa.Column('profile_type', profile_type, nullable=True),
        sa.Column('tenant_id', sa.String(length=36), nullable=False),
        sa.Column('profile_id', sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint('tenant_id', 'profile_id')
    )


def downgrade(active_plugins=None, options=None):

    op.drop_table('cisco_ml2_n1kv_profile_bindings')
    profile_type.drop(op.get_bind(), checkfirst=False)
    op.drop_table('cisco_ml2_n1kv_vlan_allocations')
    op.drop_table('cisco_ml2_n1kv_vxlan_allocations')
    op.drop_table('cisco_ml2_n1kv_network_bindings')
    op.drop_table('cisco_ml2_n1kv_port_bindings')
    op.drop_table('cisco_ml2_n1kv_network_profiles')
    network_profile_type.drop(op.get_bind(), checkfirst=False)
    op.drop_table('cisco_ml2_n1kv_policy_profiles')
