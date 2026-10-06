from simProcess import SimProcess
from simProcessor import SimProcessor
from processControlBlock import ProcessControlBlock
from processState import ProcessState
from sim_logger import SimLogger
import random

processor = SimProcessor()
process1 = SimProcess(1001, "Word", 395)
process2 = SimProcess(1002, "Chrome", 228)
process3 = SimProcess(1003, "Spotify", 100)
process4 = SimProcess(1004, "Candy Crush", 333)
process5 = SimProcess(1005, "Photos", 257)
process6 = SimProcess(1006, "Kindle", 400)
process7 = SimProcess(1007, "Powerpoint", 184)
process8 = SimProcess(1008, "Notepad", 325)
process9 = SimProcess(1009, "Zoom", 314)
process10 = SimProcess(1010, "Netflix", 299)

pcb1 = ProcessControlBlock(process1)
pcb2 = ProcessControlBlock(process2)
pcb3 = ProcessControlBlock(process3)
pcb4 = ProcessControlBlock(process4)
pcb5 = ProcessControlBlock(process5)
pcb6 = ProcessControlBlock(process6)
pcb7 = ProcessControlBlock(process7)
pcb8 = ProcessControlBlock(process8)
pcb9 = ProcessControlBlock(process9)
pcb10 = ProcessControlBlock(process10)

QUANTUM = 5
ready = [pcb1, pcb2, pcb3, pcb4, pcb5, pcb6, pcb7, pcb8, pcb9, pcb10]
blocked = []
#this saves the last execution result so that the program knows where to put the process when it is moved off the processor
last_execution_result = None
#this is the quantum that the process is up to and when it hits five the process is moved off the processor
current_q = 1
current_pcb = None
logger = SimLogger()

def context_switch(current_pcb, ready, blocked, logger):
    #if you need to save the state of the process (it could be that the processor was idle the previous cycle
    if current_pcb:
        #saving the information from the processor to the pcb of the process that was running
        current_pcb.current_instruction = processor.current_instruction
        current_pcb.register1 = processor.register1
        current_pcb.register2 = processor.register2
        current_pcb.register3 = processor.register3
        current_pcb.register4 = processor.register4
        #where the process goes after being removed from the processor
        if last_execution_result == ProcessState.BLOCKED:
            blocked.append(current_pcb)
        else:
            if last_execution_result != ProcessState.FINISHED:
                ready.append(current_pcb)
    #save the information from the processor so that it can be accessed by the logger before switching the current_pcb
    old_current_pcb = current_pcb
    #if there are processes in the ready state then the first one goes onto the processor and its pcb is updated, otherwise the processor is idle
    if ready != []:
        current_pcb = ready.pop(0)
        processor.currentProcess = current_pcb.process
        processor.current_instruction = current_pcb.current_instruction
        processor.register1 = current_pcb.register1
        processor.register2 = current_pcb.register2
        processor.register3 = current_pcb.register3
        processor.register4 = current_pcb.register4
    else:
        current_pcb = None
        processor.currentProcess = None
    #if there was an old process, log it using the logger
    if old_current_pcb:
        logger.context_switch(i, old_current_pcb.process.pid, old_current_pcb.current_instruction,
                         [old_current_pcb.register1, old_current_pcb.register2, old_current_pcb.register3, old_current_pcb.register4,],
                          current_pcb.process.pid, current_pcb.current_instruction, [current_pcb.register1, current_pcb.register2, current_pcb.register3, current_pcb.register4])
    #return the current pcb so that it isn't just switched locally
    return current_pcb


#this is the main loop
for i in range(3000):
    #if there is a current process, either do a context switch or run the next instruction.
    if processor.currentProcess:
        #if a context switch is needed, do the context switch, reset the current quantum to 0, and reset the last_execution_result, because it hasn't been executed yet
        if last_execution_result == ProcessState.FINISHED or last_execution_result == ProcessState.BLOCKED or current_q > 5:
            current_pcb = context_switch(current_pcb, ready, blocked, logger)
            current_q = 1
            last_execution_result = None
        #if there is no context switch, run the next instruction, and mark using the logger
        else:
            logger.exec(i, processor.currentProcess.pid, processor.currentProcess.procName, processor.current_instruction)
            last_execution_result = processor.execute_next_instruction()
            current_q += 1
            if last_execution_result == ProcessState.FINISHED:
                logger.marker("COMPLETED")
            if last_execution_result == ProcessState.BLOCKED:
                logger.marker("BLOCKED")
            if current_q > 5 and last_execution_result != ProcessState.BLOCKED and last_execution_result != ProcessState.FINISHED:
                logger.marker("QUANTUM_EXPIRED")
    #if there isn't a current process, check if there are any processes in the ready state.
    else:
        # if yes, put it on the processor
        if ready != []:
            current_pcb = ready.pop(0)
            processor.currentProcess = current_pcb.process
        #if not, the processor is idle for the current cycle
        else:
            logger.idle(i)
    #loop through all the processes that are blocked and move them to ready 30 percent of the time
    copy_blocked = blocked.copy()
    for value in copy_blocked:
        r = random.randint(1, 10)
        if r <= 3:
            blocked.remove(value)
            ready.append(value)
