from sqlalchemy import MetaData
from sqlalchemy import (Table,
                        Column,
                        BigInteger,
                        Integer,
                        VARCHAR,
                        JSON,
                        Text,
                        TIMESTAMP,
                        Index,
                        Numeric,
                        Float,
                        DateTime,
                        UniqueConstraint,
                        Boolean,
                        VARCHAR,
                        String,
                        func,
                        text,
                        desc
                        )
from datetime import datetime

metadata_obj = MetaData()

areas =  Table(
    'areas',
    metadata_obj,
	Column ('id',BigInteger,primary_key=True ),
	Column ("name", Text ),
	Column ('created_at', TIMESTAMP, index = True ),
	Column ('updated_at', TIMESTAMP, index = True ),
)



depots = Table(
    'depots',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('name', Text),
    Column('code', Text),
    Column('is_hub', Boolean, default=False, nullable=True),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
)

locations = Table(
    'locations',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('name', Text),
    Column('created_at', TIMESTAMP,index=True),
    Column('updated_at', TIMESTAMP,index=True),
)

property_categories = Table(
    'property_categories',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', Text),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
)

property_types = Table(
    'property_types',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', Text),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
)

reports = Table(
    'reports',
    metadata_obj,
    Column('id', BigInteger, primary_key=True),
    Column('doc_no', Text),
    Column('report_type', Text),
    Column('property_category', Text),
    Column('property_name', Text),
    Column('depot_id', Integer),
    Column('depot_id_report', Integer),
    Column('area', Text),
    Column('completion_status', Boolean),
    Column('completion_at', TIMESTAMP),
    Column('completion_url', Text),
    Column('completion_staff_name', Text),
    Column('evidence_url', Text),
    Column('remarks', Text),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
    Column('created_by', Text),
    Column('created_name', Text),
    Column('pickup_sender_name', Text),
    Column('courier_name', Text),
    Column('pickup_by', Text),
    Column('pickup_at', TIMESTAMP),
    Column('pickup_status', Boolean),
    Column('notes', Text),
    Column('clerance_option', Text),
    Column('clerance_at', TIMESTAMP),
)



responsible_people = Table(
    'responsible_people',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', Text),
    Column('id_card', Text),
    Column('phone', Text),
    Column('email', Text),
    Column('report_id', Integer),
    Column('depot_id', Integer),
    Column('role', Text),
    Column('is_claim_agree', Boolean),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
)

users = Table(
    'users',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('username', Text),
    Column('password', Text),
    Column('role', Text),
    Column('depot_id', Integer),
    Column('created_at', TIMESTAMP, index=True),
    Column('updated_at', TIMESTAMP, index=True),
    Column('login_at', TIMESTAMP),
)

MigrationLog = Table(
    'MigrationLog',
    metadata_obj,
    Column('id', BigInteger,primary_key = True),
    Column('createdAt', TIMESTAMP),
    Column('table', VARCHAR(100)),
    Column('flag', VARCHAR(100)),
    Column('process', VARCHAR(100)),
    Column('description', Text),
    Index('idx_migrationlog_createdAt_table', 'createdAt', 'table')
    # Add any additional columns or constraints here
    # ...
)