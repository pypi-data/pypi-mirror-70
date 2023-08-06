<div align="center">
	<a href="https://machin.readthedocs.io">
		<img width="auto" height="200px" src="https://machin.readthedocs.io/en/latest/_static/icon.svg">
	</a>
</div>
---
[![Read the Docs](https://img.shields.io/readthedocs/machin)](https://machin.readthedocs.io/en/latest/)

**Machin** is a reinforcement library purely based on pytorch. It is designed to be **readable**, **reusable** and **extendable**.


### Supported algorithms? 
---
Currently Machin has implemented the following algorithms, the list is still growing:

#### Single agent algorithms:
* [Deep Q-Network (DQN)](https://storage.googleapis.com/deepmind-media/dqn/DQNNaturePaper.pdf)
* [Double DQN](https://arxiv.org/pdf/1509.06461.pdf)
* [Dueling DQN](https://arxiv.org/abs/1511.06581)
* [RAINBOW](https://arxiv.org/abs/1710.02298)
* [Deep Deterministic policy Gradient (DDPG)](https://arxiv.org/pdf/1509.02971.pdf), 
* [Twin Delayed DDPG (TD3)](https://arxiv.org/pdf/1802.09477.pdf)
* [Hystereric DDPG (Modified from Hys-DQN)](https://hal.archives-ouvertes.fr/hal-00187279/document)
* [Advantage Actor-Critic (A2C)](https://openai.com/blog/baselines-acktr-a2c/)
* [Proximal Policy Optimization (PPO)](https://arxiv.org/pdf/1707.06347.pdf)
* [Soft Actor Critic (SAC)](https://arxiv.org/pdf/1812.05905.pdf)

#### Multi-agent algorithms:
* [Multi-agent DDPG (MADDPG)](https://arxiv.org/pdf/1706.02275.pdf)

#### Massively parallel algorithms:
* [Asynchronous A2C (A3C)](https://arxiv.org/abs/1602.01783)
* [APEX-DQN, APEX-DDPG](https://arxiv.org/pdf/1803.00933)
* [IMPALA](https://arxiv.org/pdf/1802.01561)

#### Enhancements:
* [Prioritized Experience Replay (PER)](https://arxiv.org/pdf/1511.05952.pdf)
* [Generalized Advantage Estimation (GAE)](https://arxiv.org/pdf/1506.02438.pdf)
* [Recurrent networks in DQN, etc.](https://arxiv.org/pdf/1507.06527.pdf)
#### Algorithms to be supported:
* [Distributed DDPG (D4PG)](https://arxiv.org/abs/1804.08617)
* [Generative Adversarial Imitation Learning (GAIL)](https://arxiv.org/abs/1606.03476)
* Evolution Strategies
* QMIX (multi agent)
* Model-based methods

### 
TODO: write examples, test and debug
TODO: add clip grad norm for DDPG, DQN etc.
TODO: add update interval for IMPALA, APEX, A3C
TODO: integrate with NNI
TODO: add more network structure implementations
