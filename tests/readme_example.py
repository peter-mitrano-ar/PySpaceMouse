import pyspacemouse
import time

def readme_example_code():
    success = pyspacemouse.open(dof_callback=pyspacemouse.print_state, button_callback=pyspacemouse.print_buttons)
    if success:
        while 1:
            state = pyspacemouse.read()
            time.sleep(0.01)

if __name__ == "__main__":
    readme_example_code()
