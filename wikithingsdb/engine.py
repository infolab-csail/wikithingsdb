from sqlalchemy import create_engine


engine = Create_engine(
    'mysql://root:@localhost/py_wikipedia', pool_recycle=3600)
