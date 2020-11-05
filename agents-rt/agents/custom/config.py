import numpy as np
import os
from agents.util import partial
from agents.sac_models import Mlp, MlpPolicy
from agents.custom.custom_models import Tm_hybrid_1, TMPolicy
from agents.custom.custom_gym_interfaces import TM2020InterfaceLidar, TMInterfaceLidar, TM2020Interface, TMInterface
from agents.custom.custom_preprocessors import obs_preprocessor_tm_act_in_obs, obs_preprocessor_tm_lidar_act_in_obs, sample_preprocessor_tm_lidar_act_in_obs
from agents.custom.custom_memories import get_local_buffer_sample, MemoryTMNFLidar, MemoryTMNF, MemoryTM2020, get_local_buffer_sample_tm20_imgs

# HIGH-LEVEL PRAGMAS: ==========================================

PRAGMA_EDOUARD_YANN_CC = 0  # 2 if ComputeCanada, 1 if Edouard, 0 if Yann  # TODO: remove for release
PRAGMA_TM2020_TMNF = True  # True if TM2020, False if TMNF
PRAGMA_LIDAR = False  # True if Lidar, False if images
PRAGMA_CUDA = True  # True if CUDA, False if CPU
CRC_DEBUG = True  # Only for checking the consistency of the custom networking methods, set it to False otherwise
CRC_DEBUG_SAMPLES = 5  # Number of samples collected in CRC_DEBUG mode

# FILE SYSTEM: =================================================

if PRAGMA_EDOUARD_YANN_CC == 2:  # Compute Canada
    MODEL_PATH_TRAINER = r"/home/yannbout/scratch/base_tmrl/data/expt.pth"
    CHECKPOINT_PATH = r"/home/yannbout/scratch/base_tmrl/data/exp0"
    DATASET_PATH = r"/home/yannbout/scratch/base_tmrl/data/dataset"
    MODEL_PATH_WORKER = r"/home/yannbout/scratch/base_tmrl/data/exp.pth"
    REWARD_PATH = r"/home/yannbout/scratch/base_tmrl/data/reward.pkl"
elif PRAGMA_EDOUARD_YANN_CC == 1:  # Edouard
    MODEL_PATH_WORKER = r"D:\cp\weights\exp.pth"
    MODEL_PATH_TRAINER = r"D:\cp\weights\expt.pth"
    CHECKPOINT_PATH = r"D:\cp\exp0"
    DATASET_PATH = r"D:\data2020"
    REWARD_PATH = r"D:\data2020reward\reward.pkl"
elif PRAGMA_EDOUARD_YANN_CC == 0:  # Yann
    MODEL_PATH_WORKER = r"C:\Users\Yann\Desktop\git\tmrl\checkpoint\weights\exp.pth"
    MODEL_PATH_TRAINER = r"C:\Users\Yann\Desktop\git\tmrl\checkpoint\weights\expt.pth"
    CHECKPOINT_PATH = r"C:\Users\Yann\Desktop\git\tmrl\checkpoint\chk\exp0"
    DATASET_PATH = r"C:\Users\Yann\Desktop\git\tmrl\data"
    REWARD_PATH = r"C:/Users/Yann/Desktop/git/tmrl/tm20reward/reward.pkl"

# WANDB: =======================================================

WANDB_RUN_ID = "SAC_tm20_test_edi_2"
WANDB_PROJECT = "tmrl"
WANDB_ENTITY = "yannbouteiller"  # TODO: remove for release
WANDB_KEY = "9061c16ece78577b75f1a4af109a427d52b74b2a"  # TODO: remove for release

os.environ['WANDB_API_KEY'] = WANDB_KEY

# MODEL, GYM ENVIRONMENT, REPLAY MEMORY AND TRAINING: ===========

TRAIN_MODEL = Mlp if PRAGMA_LIDAR else Tm_hybrid_1
POLICY = MlpPolicy if PRAGMA_LIDAR else TMPolicy
ACT_IN_OBS = True
BENCHMARK = False

if PRAGMA_LIDAR:
    INT = partial(TM2020InterfaceLidar, img_hist_len=1) if PRAGMA_TM2020_TMNF else partial(TMInterfaceLidar, img_hist_len=1)
else:
    INT = partial(TM2020Interface, img_hist_len=4) if PRAGMA_TM2020_TMNF else partial(TMInterface, img_hist_len=4)
CONFIG_DICT = {
    "interface": INT,
    "time_step_duration": 0.05,
    "start_obs_capture": 0.04,
    "time_step_timeout_factor": 1.0,
    "ep_max_length": np.inf,
    "real_time": True,
    "async_threading": True,
    "act_in_obs": ACT_IN_OBS,
    "benchmark": BENCHMARK,
    "wait_on_done": True
}

# to compress a sample before sending it over the local network/Internet:
SAMPLE_COMPRESSOR = get_local_buffer_sample if PRAGMA_LIDAR else get_local_buffer_sample_tm20_imgs
# to preprocess observations that come out of the gym environment and of the replay buffer:
OBS_PREPROCESSOR = obs_preprocessor_tm_lidar_act_in_obs if PRAGMA_LIDAR else obs_preprocessor_tm_act_in_obs
# to augment data that comes out of the replay buffer (applied after observation preprocessing):
SAMPLE_PREPROCESSOR = sample_preprocessor_tm_lidar_act_in_obs if PRAGMA_LIDAR else None

if PRAGMA_LIDAR:
    MEM = MemoryTMNFLidar
else:
    MEM = MemoryTM2020 if PRAGMA_TM2020_TMNF else MemoryTMNF
MEMORY = partial(MEM,
                 path_loc=DATASET_PATH,
                 imgs_obs=1 if PRAGMA_LIDAR else 4,
                 act_in_obs=ACT_IN_OBS,
                 obs_preprocessor=OBS_PREPROCESSOR,
                 sample_preprocessor=SAMPLE_PREPROCESSOR,
                 crc_debug=CRC_DEBUG
                 )

# NETWORKING: ==================================================

LOCALHOST = False  # set to True to enforce localhost
REDIS_IP = "96.127.215.210" if not LOCALHOST else "127.0.0.1"

PORT_TRAINER = 55555  # Port to listen on (non-privileged ports are > 1023)
PORT_ROLLOUT = 55556  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 268435456  # 1048576  # 8192  # 32768  # socket buffer size (200 000 000 is large enough for 1000 images right now)
HEADER_SIZE = 12  # fixed number of characters used to describe the data length

SOCKET_TIMEOUT_CONNECT_TRAINER = 300.0
SOCKET_TIMEOUT_ACCEPT_TRAINER = 300.0
SOCKET_TIMEOUT_CONNECT_ROLLOUT = 300.0
SOCKET_TIMEOUT_ACCEPT_ROLLOUT = 300.0  # socket waiting for rollout workers closed and restarted at this interval
SOCKET_TIMEOUT_COMMUNICATE = 30.0
SELECT_TIMEOUT_OUTBOUND = 30.0
SELECT_TIMEOUT_PING_PONG = 60.0
ACK_TIMEOUT_WORKER_TO_REDIS = 300.0
ACK_TIMEOUT_TRAINER_TO_REDIS = 300.0
ACK_TIMEOUT_REDIS_TO_WORKER = 300.0
ACK_TIMEOUT_REDIS_TO_TRAINER = 300.0
WAIT_BEFORE_RECONNECTION = 10.0
LOOP_SLEEP_TIME = 1.0
