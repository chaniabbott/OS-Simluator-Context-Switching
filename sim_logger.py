"""
sim_logger.py

Provided boilerplate for the Context Switching Simulation assignment.

DO NOT MODIFY THIS FILE.

This module only formats and prints output in the exact format required
for automated grading. It has NO knowledge of processes, queues,
quantum, or scheduling -- that logic is entirely your responsibility.

You are responsible for:
  - Tracking your own step counter and incrementing it correctly
  - Calling the correct method at the correct point in your main loop
  - Passing in correct, consistent data (pid, instruction number,
    register values, etc.)

Marker types (pass one of these string constants to marker()):
  BLOCKED, QUANTUM_EXPIRED, COMPLETED
"""

BLOCKED = "BLOCKED"
QUANTUM_EXPIRED = "QUANTUM_EXPIRED"
COMPLETED = "COMPLETED"

_MARKER_TEXT = {
    BLOCKED: "*** Process blocked ***",
    QUANTUM_EXPIRED: "*** Quantum expired ***",
    COMPLETED: "*** Process completed ***",
}


class SimLogger:

    def exec(self, step, pid, name, instr):
        """
        Log execution of one instruction.

        step:  int, the current step number (you track/increment this)
        pid:   int, the process id currently on the processor
        name:  str, the process's name
        instr: int, the instruction number being executed
        """
        print(f"Step {step} Proc {name}, PID: {pid} executing instruction: {instr}")

    def context_switch(self, step, saved_pid, saved_instr, saved_regs,
                        restored_pid, restored_instr, restored_regs):
        """
        Log a full context switch (save outgoing process, restore incoming
        process) as a single step.

        step:           int, the step number for this context switch
        saved_pid:      int, pid of the process being saved (taken off processor)
        saved_instr:    int, next instruction the saved process will execute
                        when it resumes
        saved_regs:     sequence of 4 ints, R1-R4 for the saved process
        restored_pid:   int, pid of the process being restored (put on processor)
        restored_instr: int, next instruction the restored process will execute
        restored_regs:  sequence of 4 ints, R1-R4 for the restored process
        """
        r = saved_regs
        print(f"Step {step} Context Switch: Saving process: {saved_pid}")
        print(f"Instruction: {saved_instr} - R1: {r[0]}, R2: {r[1]}, R3: {r[2]}, R4: {r[3]}")
        r = restored_regs
        print(f"Restoring process: {restored_pid}")
        print(f"Instruction: {restored_instr} - R1: {r[0]}, R2: {r[1]}, R3: {r[2]}, R4: {r[3]}")

    def idle(self, step):
        """
        Log that the processor idled this step because no ready process
        was available to restore.

        step: int, the step number for this idle step
        """
        print(f"Step {step} Context Switch: Processor idling, no ready process available")

    def marker(self, marker_type):
        """
        Log an event marker immediately after the EXEC line that triggered it.

        marker_type: one of BLOCKED, QUANTUM_EXPIRED, COMPLETED
        """
        if marker_type not in _MARKER_TEXT:
            raise ValueError(f"Unknown marker type: {marker_type}")
        print(_MARKER_TEXT[marker_type])
