import unittest
import threading
import time
from src.design_patterns.singleton import Singleton, DatabaseConnection


class TestSingleton(unittest.TestCase):
    
    def test_singleton_same_instance(self):
        """Test that multiple instantiations return the same instance"""
        instance1 = Singleton()
        instance2 = Singleton()
        self.assertIs(instance1, instance2)
    
    def test_database_connection_singleton(self):
        """Test DatabaseConnection singleton behavior"""
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        self.assertIs(db1, db2)
    
    def test_database_connection_methods(self):
        """Test DatabaseConnection methods work correctly"""
        db = DatabaseConnection()
        self.assertEqual(db.connect(), "Connected to database")
        self.assertEqual(db.query("SELECT * FROM users"), "Executing: SELECT * FROM users")
    
    def test_singleton_thread_safety(self):
        """Test singleton is thread-safe"""
        instances = []
        
        def create_instance():
            instances.append(Singleton())
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All instances should be the same
        first_instance = instances[0]
        for instance in instances:
            self.assertIs(instance, first_instance)


if __name__ == '__main__':
    unittest.main()