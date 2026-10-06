from processState import ProcessState
import random

class SimProcess:
    def __init__(self, pid:int, procName:str, totalInstructions:int) -> None:
        self.pid = pid
        self.procName = procName
        self.totalInstructions = totalInstructions


    def execute(self, i:int):
        #if there are no more instructions, it's finished
        if i >= self.totalInstructions:
            return ProcessState.FINISHED

        #this will block the process 15 percent of the time
        random_number = random.randint(1, 100)
        if random_number <= 15:
            return ProcessState.BLOCKED
        else:
            return ProcessState.READY