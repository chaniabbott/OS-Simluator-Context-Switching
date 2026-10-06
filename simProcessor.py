import random

class SimProcessor:
    def __init__(self) -> None:
        self.currentProcess = None
        self.register1 = 0
        self.register2 = 0
        self.register3 = 0
        self.register4 = 0
        self.current_instruction = 0

    def execute_next_instruction(self):
        result = self.currentProcess.execute(self.current_instruction)
        self.current_instruction += 1
        self.register1 = random.randint(-2147483648, 2147483647)
        self.register2 = random.randint(-2147483648, 2147483647)
        self.register3 = random.randint(-2147483648, 2147483647)
        self.register4 = random.randint(-2147483648, 2147483647)
        return result