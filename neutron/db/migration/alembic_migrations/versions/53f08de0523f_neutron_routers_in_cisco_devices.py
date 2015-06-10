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

"""Neutron routers in Cisco devices

Revision ID: 53f08de0523f
Revises: 2921fe565328
Create Date: 2014-12-18 14:10:46.191557

"""

# revision identifiers, used by Alembic.
revision = '53f08de0523f'
down_revision = '2921fe565328'

from alembic import op
import sqlalchemy as sa

from neutron.db import migration


def upgrade():
    op.create_table('cisco_router_types',
        sa.Column('tenant_id', sa.String(length=255), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('template_id', sa.String(length=36), nullable=True),
        sa.Column('shared', sa.Boolean(), nullable=False,
                  server_default=sa.sql.true()),
        sa.Column('slot_need', sa.Integer(), autoincrement=False,
                  nullable=True),
        sa.Column('scheduler', sa.String(length=255), nullable=False),
        sa.Column('driver', sa.String(length=255), nullable=False),
        sa.Column('cfg_agent_service_helper', sa.String(length=255),
                  nullable=False),
        sa.Column('cfg_agent_driver', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['template_id'],
                                ['cisco_hosting_device_templates.id'],
                                ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    if migration.schema_has_table('cisco_router_mappings'):
        op.add_column('cisco_router_mappings',
                      sa.Column('role', sa.String(255), nullable=True))
        op.add_column('cisco_router_mappings',
                      sa.Column('router_type_id', sa.String(length=36),
                                nullable=False))
        op.create_foreign_key('cisco_router_mappings_ibfk_3',
                              source='cisco_router_mappings',
                              referent='cisco_router_types',
                              local_cols=['router_type_id'],
                              remote_cols=['id'])
        op.drop_constraint('cisco_router_mappings_ibfk_2',
                           'cisco_router_mappings', type_='foreignkey')
        op.drop_constraint('cisco_router_mappings_ibfk_2',
                           'cisco_router_mappings', type_='primary')
        op.create_foreign_key('cisco_router_mappings_ibfk_2',
                              source='cisco_router_mappings',
                              referent='routers',
                              local_cols=['router_id'],
                              remote_cols=['id'],
                              ondelete='CASCADE')
        op.create_primary_key(
            name='pk_cisco_router_mappings',
            table_name='cisco_router_mappings',
            cols=['router_id', 'router_type_id'])
        op.add_column('cisco_router_mappings',
                      sa.Column('inflated_slot_need', sa.Integer(),
                                autoincrement=False, nullable=True,
                                server_default='0'))
        op.add_column('cisco_router_mappings',
                      sa.Column('share_hosting_device', sa.Boolean(),
                                nullable=False, server_default=sa.sql.true()))
        op.create_index(op.f('ix_cisco_router_types_tenant_id'),
                        'cisco_router_types', ['tenant_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_cisco_router_types_tenant_id'),
                  table_name='cisco_router_types')
    op.drop_column('cisco_router_mappings', 'share_hosting_device')
    op.drop_column('cisco_router_mappings', 'inflated_slot_need')
    op.drop_constraint('cisco_router_mappings_ibfk_2',
                       'cisco_router_mappings', type_='foreignkey')
    op.drop_constraint('cisco_router_mappings_ibfk_3',
                       'cisco_router_mappings', type_='foreign')
    op.drop_constraint('pk_cisco_router_mappings', 'cisco_router_mappings',
                       type_='primary')
    op.drop_column('cisco_router_mappings', 'router_type_id')
    op.create_foreign_key('cisco_router_mappings_ibfk_2',
                          source='cisco_router_mappings',
                          referent='routers',
                          local_cols=['router_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    op.create_primary_key(name='cisco_router_mappings_ibfk_2',
                          table_name='cisco_router_mappings',
                          cols=['router_id'])
    op.drop_column('cisco_router_mappings', 'role')
    op.drop_table('cisco_router_types')
