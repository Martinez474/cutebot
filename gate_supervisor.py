from controller import Supervisor

TIME_STEP = 30

supervisor = Supervisor()

# Find objects using their DEF names.
epuck_node = supervisor.getFromDef("EPUCK")

maze_gate_node0 = supervisor.getFromDef("MAZE_GATE0")
maze_gate_node1 = supervisor.getFromDef("MAZE_GATE1")
maze_gate_node2 = supervisor.getFromDef("MAZE_GATE2")


# Check that every node was found.
if epuck_node is None:
    raise RuntimeError("Could not find DEF EPUCK")

if maze_gate_node0 is None:
    raise RuntimeError("Could not find DEF MAZE_GATE0")

if maze_gate_node1 is None:
    raise RuntimeError("Could not find DEF MAZE_GATE1")

if maze_gate_node2 is None:
    raise RuntimeError("Could not find DEF MAZE_GATE2")


# Get translation fields once before the main loop.
epuck_translation = epuck_node.getField("translation")

maze_gate_translation0 = maze_gate_node0.getField("translation")
maze_gate_translation1 = maze_gate_node1.getField("translation")
maze_gate_translation2 = maze_gate_node2.getField("translation")


# Closed positions for each gate.
MAZE_GATE_CLOSED_POSITION0 = [
    -0.065757,
    0.3087,
    0.190004
]

MAZE_GATE_CLOSED_POSITION1 = [
    -0.065757,
    1.1887,
    0.390004
]

MAZE_GATE_CLOSED_POSITION2 = [
    -0.065757,
    3.2087,
    0.180004
]



# Prevent each gate from being closed repeatedly.
maze_gate_closed0 = False
maze_gate_closed1 = False
maze_gate_closed2 = False

step_count = 0
start_previous_section_step = 0

start_previous_section_time = 0.0

while supervisor.step(TIME_STEP) != -1:
    current_time = supervisor.getTime()
    position = epuck_translation.getSFVec3f()

    x = position[0]
    y = position[1]
    z = position[2]
    
    
    #edit
    on_gray_box = (
        1.2 <= x <= 1.5 and
        -0.3 <= z <= 0.0
    )
    

    # print("E-puck position:", x, y, z)

    # Close the first gate.
    if not maze_gate_closed0 and y > 0.4:
        maze_gate_translation0.setSFVec3f(
            MAZE_GATE_CLOSED_POSITION0
        )

        maze_gate_closed0 = True
        print(
            f"Gate 1 closed | "
            f"Split: {step_count - start_previous_section_step} steps | "
            f"Total: {step_count} steps"
        )
        
        print(
            f"Gate 1 closed | "
            f"Split: {current_time - start_previous_section_time:.2f} s | "
            f"Total: {current_time:.2f} s"
        )
        
        # Reset for the next section
        start_previous_section_step = step_count
        start_previous_section_time = current_time

    # Close the second gate.
    if not maze_gate_closed1 and y > 1.33:
        maze_gate_translation1.setSFVec3f(
            MAZE_GATE_CLOSED_POSITION1
        )

        maze_gate_closed1 = True
        print(
            f"Gate 2 closed | "
            f"Split: {step_count - start_previous_section_step} steps | "
            f"Total: {step_count} steps"
        )
        
        print(
            f"Gate 2 closed | "
            f"Split: {current_time - start_previous_section_time:.2f} s | "
            f"Total: {current_time:.2f} s"
        )
        
        start_previous_section_step = step_count
        start_previous_section_time = current_time

    # Close the third gate.
    if not maze_gate_closed2 and y > 3.35:
        maze_gate_translation2.setSFVec3f(
            MAZE_GATE_CLOSED_POSITION2
        )

        maze_gate_closed2 = True
        print(
            f"Gate 3 closed | "
            f"Split: {step_count - start_previous_section_step} steps | "
            f"Total: {step_count} steps"
        )
        
        print(
            f"Gate 3 closed | "
            f"Split: {current_time - start_previous_section_time:.2f} s | "
            f"Total: {current_time:.2f} s"
        )
        
        # Reset for the next section (if there is one)
        start_previous_section_step = step_count
        start_previous_section_time = current_time
        
    if on_gray_box:
        print("Reached the gray box!")
        
    step_count += 1