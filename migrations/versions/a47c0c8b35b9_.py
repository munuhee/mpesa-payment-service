"""empty message

Revision ID: a47c0c8b35b9
Revises: 
Create Date: 2024-05-21 13:19:00.001926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a47c0c8b35b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mpesa_transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=13), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('checkout_request_id', sa.String(length=100), nullable=False),
    sa.Column('mpesa_receipt_number', sa.String(length=100), nullable=True),
    sa.Column('transaction_date', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('result_desc', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('checkout_request_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mpesa_transaction')
    # ### end Alembic commands ###