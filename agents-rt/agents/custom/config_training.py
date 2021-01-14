from agents import TrainingOffline
import agents.custom.config as cfg
from agents.envs import UntouchedGymEnv
from agents.sac import Agent as SAC_Agent
from agents.drtac import Agent as DCAC_Agent
from agents.custom.custom_dcac_interfaces import Tm20rtgymDcacInterface
from agents.util import partial

# ALGORITHM: ===================================================

if cfg.PRAGMA_DCAC:
    AGENT = partial(DCAC_Agent,
                    Interface=Tm20rtgymDcacInterface,
                    OutputNorm=partial(beta=0., zero_debias=False),
                    Memory=cfg.MEMORY,
                    device='cuda' if cfg.PRAGMA_CUDA_TRAINING else 'cpu',
                    Model=partial(cfg.TRAIN_MODEL, act_buf_len=cfg.ACT_BUF_LEN),
                    memory_size=1000000,
                    batchsize=128 if cfg.PRAGMA_LIDAR else 64,  # 512,  # default: 256
                    lr=0.0003,  # default 0.0003
                    discount=0.995,  # default and best tmnf so far: 0.99
                    target_update=0.005,
                    reward_scale=2.0,  # 2.0,  # default: 5.0, best tmnf so far: 0.1, best tm20 so far: 2.0
                    entropy_scale=1.0)  # default: 1.0),  # default: 1.0
else:
    AGENT = partial(SAC_Agent,
                    OutputNorm=partial(beta=0., zero_debias=False),
                    Memory=cfg.MEMORY,
                    device='cuda' if cfg.PRAGMA_CUDA_TRAINING else 'cpu',
                    Model=partial(cfg.TRAIN_MODEL, act_buf_len=cfg.ACT_BUF_LEN),
                    memory_size=1000000,
                    batchsize=128 if cfg.PRAGMA_LIDAR else 64,  # 512,  # default: 256 128
                    lr=0.00005,  # default 0.0003
                    discount=0.995,  # default and best tmnf so far: 0.99
                    target_update=0.005,
                    reward_scale=2.0,  # 2.0,  # default: 5.0, best tmnf so far: 0.1, best tm20 so far: 2.0
                    entropy_scale=1.0)  # default: 1.0),  # default: 1.0

if cfg.PRAGMA_LIDAR:
    TRAINER = partial(TrainingOffline,
                      Env=partial(UntouchedGymEnv, id="rtgym:real-time-gym-v0", gym_kwargs={"config": cfg.CONFIG_DICT}),
                      epochs=400,  # 400
                      rounds=10,  # 10
                      steps=1000,  # 1000
                      update_model_interval=1000,
                      update_buffer_interval=1000,
                      max_training_steps_per_env_step=1.0,
                      Agent=AGENT)
else:
    TRAINER = partial(TrainingOffline,
                      Env=partial(UntouchedGymEnv, id="rtgym:real-time-gym-v0", gym_kwargs={"config": cfg.CONFIG_DICT}),
                      epochs=100000,  # 10
                      rounds=10,  # 50
                      steps=10,  # 2000
                      update_model_interval=10,
                      update_buffer_interval=1000,
                      max_training_steps_per_env_step=1.0,
                      Agent=AGENT)