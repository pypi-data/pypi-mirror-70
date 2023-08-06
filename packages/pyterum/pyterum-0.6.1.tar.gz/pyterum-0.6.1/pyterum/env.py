import os
import json

# Location of the shared volume between sidecar and the processing step
DATA_VOLUME_PATH = os.getenv("DATA_VOLUME_PATH", "")

# Location of the shared volume between sidecar and the processing step
CONFIG_PATH = os.path.join(DATA_VOLUME_PATH, os.getenv("ITERUM_CONFIG_PATH", ""))
_CONFIG_DATA = json.loads(os.getenv("ITERUM_CONFIG", "{ }"))

# Socket file paths for both what comes in and goes out
FRAGMENTER_INPUT = os.path.join(DATA_VOLUME_PATH, os.getenv("FRAGMENTER_INPUT", default=""))
FRAGMENTER_OUTPUT = os.path.join(DATA_VOLUME_PATH, os.getenv("FRAGMENTER_OUTPUT", default=""))

# Socket file paths for both what comes in and goes out 
TRANSFORMATION_STEP_INPUT = os.path.join(DATA_VOLUME_PATH, os.getenv("TRANSFORMATION_STEP_INPUT", default=""))
TRANSFORMATION_STEP_OUTPUT = os.path.join(DATA_VOLUME_PATH, os.getenv("TRANSFORMATION_STEP_OUTPUT", default=""))

# Size encoding of message with a default value of 4
ENC_MSG_SIZE_LENGTH = os.getenv("ENC_MSG_SIZE_LENGTH", default=4)

EXAMPLE_SOCKET_INPUT = "./pyterum_example_sockets/example_in.sock"
EXAMPLE_SOCKET_OUTPUT = "./pyterum_example_sockets/example_out.sock"

def verify_shared_envs():
    assert DATA_VOLUME_PATH != ""

def verify_fragmenter_envs():
    verify_shared_envs()
    assert FRAGMENTER_INPUT.endswith(".sock")
    assert FRAGMENTER_OUTPUT.endswith(".sock")

def verify_transformation_step_envs():    
    verify_shared_envs()
    assert TRANSFORMATION_STEP_INPUT.endswith(".sock")
    assert TRANSFORMATION_STEP_OUTPUT.endswith(".sock")
