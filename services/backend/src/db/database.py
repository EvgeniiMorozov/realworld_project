from sqlalchemy import Column
from sqlalchemy import ForeignKey


def reference_column(tablename, nullable=False, pk_name="id", **kwargs):
    return Column(ForeignKey(f"{tablename}.{pk_name}"), nullable=nullable, **kwargs)
