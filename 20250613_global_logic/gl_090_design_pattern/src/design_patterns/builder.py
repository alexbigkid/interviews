"""
Builder Pattern - Constructs complex objects step by step
Common interview question: House builder, Computer builder, SQL query builder
"""

from abc import ABC, abstractmethod


class Computer:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
        self.os = None
    
    def __str__(self):
        return f"Computer(CPU: {self.cpu}, RAM: {self.ram}, Storage: {self.storage}, GPU: {self.gpu}, OS: {self.os})"


class ComputerBuilder(ABC):
    def __init__(self):
        self.computer = Computer()
    
    @abstractmethod
    def set_cpu(self):
        pass
    
    @abstractmethod
    def set_ram(self):
        pass
    
    @abstractmethod
    def set_storage(self):
        pass
    
    @abstractmethod
    def set_gpu(self):
        pass
    
    @abstractmethod
    def set_os(self):
        pass
    
    def get_computer(self):
        result = self.computer
        self.computer = Computer()  # Reset for next build
        return result


class GamingComputerBuilder(ComputerBuilder):
    def set_cpu(self):
        self.computer.cpu = "Intel i9-12900K"
        return self
    
    def set_ram(self):
        self.computer.ram = "32GB DDR4"
        return self
    
    def set_storage(self):
        self.computer.storage = "1TB NVMe SSD"
        return self
    
    def set_gpu(self):
        self.computer.gpu = "RTX 4080"
        return self
    
    def set_os(self):
        self.computer.os = "Windows 11"
        return self


class OfficeComputerBuilder(ComputerBuilder):
    def set_cpu(self):
        self.computer.cpu = "Intel i5-12400"
        return self
    
    def set_ram(self):
        self.computer.ram = "16GB DDR4"
        return self
    
    def set_storage(self):
        self.computer.storage = "512GB SSD"
        return self
    
    def set_gpu(self):
        self.computer.gpu = "Integrated Graphics"
        return self
    
    def set_os(self):
        self.computer.os = "Windows 11 Pro"
        return self


class ComputerDirector:
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_computer(self):
        return (self.builder
                .set_cpu()
                .set_ram()
                .set_storage()
                .set_gpu()
                .set_os()
                .get_computer())


# Usage example
if __name__ == "__main__":
    # Build gaming computer
    gaming_builder = GamingComputerBuilder()
    director = ComputerDirector(gaming_builder)
    gaming_pc = director.build_computer()
    print(gaming_pc)
    
    # Build office computer
    office_builder = OfficeComputerBuilder()
    director = ComputerDirector(office_builder)
    office_pc = director.build_computer()
    print(office_pc)