PROFILES_MODEL = '''from sqlalchemy import Column, String

from app.database.models.base import Base

"""
DO NOT INCLUDE THIS TABLE IN ALEMBIN MIGRATIONS! 

You need to manually create this table in the Supabase UI.

We cannot use alembic to link this to the private 
auth.users table managed by supabase. 

See the instructions below.

Use this model class to query the profiles table if you like,
but do not include it in alembic migrations.
"""


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True)
    # link to supabase auth manually in UI
    user_id = Column(String, unique=True)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)


"""
Create the table manually in Supabase Dashboard:

- Go to your project > Database > Table Editor > New Table.
- Schema: public.
- Table Name: profiles.
- Enable Row Level Security (RLS)
- Columns (add these one by one):
    - id (Type: uuid, Primary Key: Yes, Default Value: gen_random_uuid()).
    - user_id (Type: uuid, Nullable: No).
        - Add foreign key relation 
            > Select auth.users schema 
            > Select reference column user_id -> auth.users(id)
            > Hit save
    - email (Type: text, Nullable: No).
    - first_name (Type: text, Nullable: Yes).
    - last_name (Type: text, Nullable: Yes).
- Save the table.
"""

'''
