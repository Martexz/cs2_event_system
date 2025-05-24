from db_connector import DatabaseConnector

db = DatabaseConnector()
db.connect()

# 测试数据库连接
# 查询所有表
query = "SHOW TABLES"
result = db.execute_query(query)
print(result)

db.disconnect()
