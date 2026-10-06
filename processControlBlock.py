from simProcess import SimProcess

class ProcessControlBlock:
    def __init__(self, process:SimProcess):
        self.process = process
        self.current_instruction = 0
        self.register1 = 0
        self.register2 = 0
        self.register3 = 0
        self.register4 = 0