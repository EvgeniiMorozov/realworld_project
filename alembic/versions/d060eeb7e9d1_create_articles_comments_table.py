"""Create articles, comments table

Revision ID: d060eeb7e9d1
Revises: f7cbee279cef
Create Date: 2020-09-21 20:44:23.765050

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "d060eeb7e9d1"
down_revision = "f7cbee279cef"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("body", sa.String(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_articles_id"), "articles", ["id"], unique=False)
    op.create_table(
        "tag_assoc",
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("tag", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag"],
            ["tags.tag"],
        ),
        sa.PrimaryKeyConstraint("article_id", "tag"),
    )
    op.create_index(
        op.f("ix_tag_assoc_article_id"), "tag_assoc", ["article_id"], unique=False
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", sa.String(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("article_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
    op.create_table(
        "favoriter_assoc",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["articles.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "article_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("favoriter_assoc")
    op.drop_index(op.f("ix_comments_id"), table_name="comments")
    op.drop_table("comments")
    op.drop_index(op.f("ix_tag_assoc_article_id"), table_name="tag_assoc")
    op.drop_table("tag_assoc")
    op.drop_index(op.f("ix_articles_id"), table_name="articles")
    op.drop_table("articles")
    # ### end Alembic commands ###
