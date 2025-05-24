# db_connector.py
import pymysql
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量(如果存在)
load_dotenv()

class DatabaseConnector:
    """数据库连接器类，负责管理与MySQL数据库的连接"""
    
    def __init__(self):
        """初始化数据库连接器"""
        # 从环境变量获取数据库配置，如果没有则使用默认值
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '123456'),
            'database': os.getenv('DB_NAME', 'cs2_events'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor  # 返回字典格式的结果
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接到MySQL数据库"""
        try:
            self.connection = pymysql.connect(**self.config)
            if self.connection:
                print(f"已成功连接到MySQL数据库 {self.config['database']}")
                self.cursor = self.connection.cursor()
                return True
        except pymysql.Error as e:
            print(f"连接数据库时出错: {e}")
            return False
    
    def disconnect(self):
        """断开与数据库的连接"""
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("数据库连接已关闭")
    
    def execute_query(self, query, params=()):
        """执行SELECT查询并返回结果"""
        result = None
        try:
            if not self.connection:
                self.connect()
            
            if not self.cursor:
                print("游标对象为空")
                return []
                
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except pymysql.Error as e:
            print(f"执行查询时出错: {e}")
            return []
    
    def execute_update(self, query, params=()):
        """执行INSERT, UPDATE, DELETE等修改操作"""
        try:
            if not self.connection:
                self.connect()
                
            if not self.cursor:
                print("游标对象为空")
                return 0
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount  # 返回受影响的行数
        except pymysql.Error as e:
            print(f"执行更新操作时出错: {e}")
            return 0
    
    def execute_insert(self, query, params=()):
        """执行INSERT操作并返回最后插入的ID"""
        try:
            if not self.connection:
                self.connect()
                
            if not self.cursor:
                print("游标对象为空")
                return None
            
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.connection.insert_id()  # 返回最后插入的ID
        except pymysql.Error as e:
            print(f"执行插入操作时出错: {e}")
            return None
    
    def execute_many(self, query, params_list):
        """批量执行SQL操作"""
        try:
            if not self.connection:
                self.connect()
                
            if not self.cursor:
                print("游标对象为空")
                return 0
            
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return self.cursor.rowcount
        except pymysql.Error as e:
            print(f"批量执行操作时出错: {e}")
            return 0
    
    def begin_transaction(self):
        """开始事务"""
        try:
            if not self.connection:
                self.connect()
                
            if not self.cursor:
                print("游标对象为空")
                return False
            
            self.connection.begin()
            return True
        except pymysql.Error as e:
            print(f"开始事务时出错: {e}")
            return False
    
    def commit(self):
        """提交事务"""
        try:
            if not self.connection:
                print("数据库连接不存在")
                return False
            
            self.connection.commit()
            return True
        except pymysql.Error as e:
            print(f"提交事务时出错: {e}")
            return False
    
    def rollback(self):
        """回滚事务"""
        try:
            if not self.connection:
                print("数据库连接不存在")
                return False
            
            self.connection.rollback()
            return True
        except pymysql.Error as e:
            print(f"回滚事务时出错: {e}")
            return False