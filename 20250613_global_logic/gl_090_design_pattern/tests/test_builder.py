import unittest
from src.design_patterns.builder import (
    Computer, GamingComputerBuilder, OfficeComputerBuilder, ComputerDirector
)


class TestBuilder(unittest.TestCase):
    
    def test_gaming_computer_builder(self):
        """Test building a gaming computer"""
        builder = GamingComputerBuilder()
        director = ComputerDirector(builder)
        
        computer = director.build_computer()
        
        self.assertEqual(computer.cpu, "Intel i9-12900K")
        self.assertEqual(computer.ram, "32GB DDR4")
        self.assertEqual(computer.storage, "1TB NVMe SSD")
        self.assertEqual(computer.gpu, "RTX 4080")
        self.assertEqual(computer.os, "Windows 11")
    
    def test_office_computer_builder(self):
        """Test building an office computer"""
        builder = OfficeComputerBuilder()
        director = ComputerDirector(builder)
        
        computer = director.build_computer()
        
        self.assertEqual(computer.cpu, "Intel i5-12400")
        self.assertEqual(computer.ram, "16GB DDR4")
        self.assertEqual(computer.storage, "512GB SSD")
        self.assertEqual(computer.gpu, "Integrated Graphics")
        self.assertEqual(computer.os, "Windows 11 Pro")
    
    def test_builder_method_chaining(self):
        """Test that builder methods return self for chaining"""
        builder = GamingComputerBuilder()
        
        result = builder.set_cpu()
        self.assertIs(result, builder)
        
        # Test full chain
        computer = (builder.set_cpu()
                   .set_ram()
                   .set_storage()
                   .set_gpu()
                   .set_os()
                   .get_computer())
        
        self.assertIsInstance(computer, Computer)
    
    def test_manual_building_without_director(self):
        """Test building computer manually without director"""
        builder = GamingComputerBuilder()
        
        computer = (builder.set_cpu()
                   .set_ram()
                   .set_storage()
                   .get_computer())
        
        self.assertEqual(computer.cpu, "Intel i9-12900K")
        self.assertEqual(computer.ram, "32GB DDR4")
        self.assertEqual(computer.storage, "1TB NVMe SSD")
        self.assertIsNone(computer.gpu)  # Not set
        self.assertIsNone(computer.os)   # Not set
    
    def test_different_builders_produce_different_computers(self):
        """Test that different builders produce different specifications"""
        gaming_builder = GamingComputerBuilder()
        office_builder = OfficeComputerBuilder()
        
        director1 = ComputerDirector(gaming_builder)
        director2 = ComputerDirector(office_builder)
        
        gaming_computer = director1.build_computer()
        office_computer = director2.build_computer()
        
        self.assertNotEqual(gaming_computer.cpu, office_computer.cpu)
        self.assertNotEqual(gaming_computer.ram, office_computer.ram)
        self.assertNotEqual(gaming_computer.gpu, office_computer.gpu)
    
    def test_computer_string_representation(self):
        """Test computer string representation"""
        builder = OfficeComputerBuilder()
        director = ComputerDirector(builder)
        computer = director.build_computer()
        
        str_repr = str(computer)
        self.assertIn("Intel i5-12400", str_repr)
        self.assertIn("16GB DDR4", str_repr)
        self.assertIn("512GB SSD", str_repr)
        self.assertIn("Integrated Graphics", str_repr)
        self.assertIn("Windows 11 Pro", str_repr)
    
    def test_builder_reuse(self):
        """Test that builder can be reused for multiple computers"""
        builder = GamingComputerBuilder()
        director = ComputerDirector(builder)
        
        computer1 = director.build_computer()
        computer2 = director.build_computer()
        
        # Should be different instances but same specifications
        self.assertIsNot(computer1, computer2)
        self.assertEqual(computer1.cpu, computer2.cpu)
        self.assertEqual(computer1.ram, computer2.ram)
    
    def test_empty_computer_initialization(self):
        """Test that computer starts with None values"""
        computer = Computer()
        self.assertIsNone(computer.cpu)
        self.assertIsNone(computer.ram)
        self.assertIsNone(computer.storage)
        self.assertIsNone(computer.gpu)
        self.assertIsNone(computer.os)


if __name__ == '__main__':
    unittest.main()