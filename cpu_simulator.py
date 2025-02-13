# CPU Simulation: Implements a simple CPU with MIPS-like instruction handling

class CPU:
    def __init__(self, cache, memory_bus):
        self.registers = {f'R{i}': 0 for i in range(32)}  # Simulating 32 general-purpose registers
        self.cache = cache
        self.memory_bus = memory_bus

    def execute_instruction(self, instruction):
        print(f"[CPU] Executing: {instruction}")
        parts = instruction.split()

        if parts[0] == "ADD":
            _, dest, src1, src2 = parts
            dest, src1, src2 = dest.strip(','), src1.strip(','), src2.strip(',')
            self.registers[dest] = self.registers[src1] + self.registers[src2]

        elif parts[0] == "SUB":
            _, dest, src1, src2 = parts
            dest, src1, src2 = dest.strip(','), src1.strip(','), src2.strip(',')
            self.registers[dest] = self.registers[src1] - self.registers[src2]

        elif parts[0] == "LW":  # Load Word
            _, reg, mem_addr = parts
            reg = reg.strip(',')
            address = int(mem_addr.split('(')[0])
            self.registers[reg] = self.cache.read(address)

        elif parts[0] == "SW":  # Store Word
            _, reg, mem_addr = parts
            reg = reg.strip(',')
            address = int(mem_addr.split('(')[0])
            self.cache.write(address, self.registers[reg])

        elif parts[0] == "BEQ":  # Branch if Equal
            _, reg1, reg2, label = parts
            reg1, reg2 = reg1.strip(','), reg2.strip(',')
            if self.registers[reg1] == self.registers[reg2]:
                print(f"[CPU] Branching to {label}")

        print(f"[CPU] Registers: {self.registers}")


class Cache:
    def __init__(self, memory_bus):
        self.memory_bus = memory_bus
        self.cache_storage = {}

    def read(self, address):
        if address in self.cache_storage:
            print(f"[Cache] Cache Hit! Address {address} -> {self.cache_storage[address]}")
            return self.cache_storage[address]
        else:
            print(f"[Cache] Cache Miss! Fetching from MemoryBus.")
            value = self.memory_bus.read(address)
            self.cache_storage[address] = value  # Store in cache
            return value

    def write(self, address, value):
        print(f"[Cache] Writing to cache & MemoryBus: {address} -> {value}")
        self.cache_storage[address] = value
        self.memory_bus.write(address, value)

class MemoryBus:
    def __init__(self):
        self.memory = {}

    def load_memory(self, filename):
        print("[MemoryBus] Loading memory from file...")
        with open(filename, 'r') as file:
            for line in file:
                addr, value = line.strip().split()
                self.memory[int(addr, 16)] = int(value)

    def read(self, address):
        return self.memory.get(address, 0)

    def write(self, address, value):
        self.memory[address] = value

class InstructionParser:
    def __init__(self, filename):
        self.filename = filename

    def load_instructions(self):
        print("[InstructionParser] Loading instructions from file...")
        with open(self.filename, 'r') as file:
            return [line.strip() for line in file]

class Simulator:
    def __init__(self, instruction_file, memory_file):
        self.memory_bus = MemoryBus()
        self.memory_bus.load_memory(memory_file)
        self.cache = Cache(self.memory_bus)
        self.cpu = CPU(self.cache, self.memory_bus)
        self.instructions = InstructionParser(instruction_file).load_instructions()

    def run(self):
        print("[Simulator] Starting execution...")
        for instr in self.instructions:
            self.cpu.execute_instruction(instr)
        print("[Simulator] Execution completed.")

# --- Main Execution ---
if __name__ == "__main__":
    simulator = Simulator("instructions.txt", "memory_init.txt")
    simulator.run()
