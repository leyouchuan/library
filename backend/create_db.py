from connect import engine
from tables import Base
import tables  # 让模型类被加载进来

Base.metadata.create_all(bind=engine)
print("建表完成")