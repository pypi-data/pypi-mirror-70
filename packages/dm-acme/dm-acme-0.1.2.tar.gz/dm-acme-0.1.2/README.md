<img src="docs/logos/acme.png" width="50%">

# Acme: A research framework for reinforcement learning

**[Overview](#overview)** | **[Installation](#installation)** |
**[Documentation]** | **[Agents]** | **[Examples]** | **[Paper]**

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dm-acme)
![pytest](https://github.com/deepmind/acme/workflows/pytest/badge.svg)

Acme is a library of reinforcement learning (RL) agents and agent building
blocks. Acme strives to expose simple, efficient, and readable agents, that
serve both as reference implementations of popular algorithms and as strong
baselines, while still providing enough flexibility to do novel research. The
design of Acme also attempts to provide multiple points of entry to the RL
problem at differing levels of complexity.

<div align="center" style="display: grid; grid-template-columns: auto auto;">
  <div>
    <video width="25%" autoplay loop muted>
      <source src="https://storage.googleapis.com/dm-acme/videos/d4pg_humanoid_run_features_short.webm" type="video/webm">
    </video>
    <video width="25%" autoplay loop muted>
      <source src="https://storage.googleapis.com/dm-acme/videos/d4pg_acrobot_swingup_features_short.webm" type="video/webm">
    </video>
  </div>
  <div>
    <video width="25%" autoplay loop muted>
      <source src="https://storage.googleapis.com/dm-acme/videos/r2d2_breakout.webm" type="video/webm">
    </video>
    <video width="25%" autoplay loop muted>
      <source src="https://storage.googleapis.com/dm-acme/videos/r2d2_ms_pacman.webm" type="video/webm">
    </video>
  </div>
</div>


## Overview

At the highest level Acme exposes a number of agents which can be used simply as
follows:

```python
import acme

# Create an environment and an actor.
environment = ...
actor = ...

# Run the environment loop.
loop = acme.EnvironmentLoop(environment, actor)
loop.run()
```

Acme also tries to maintain this level of simplicity while either diving deeper
into the agent algorithms or by using them in more complicated settings. An
overview of Acme along with more detailed descriptions of its underlying
components can be found by referring to the [documentation][Documentation].

For a quick start, take a look at the more detailed working code examples found
in the [examples][Examples] subdirectory, which also includes a tutorial
notebook to get you started. And finally, for more information on the various
agent implementations available take a look at the [agents][Agents] subdirectory
along with the `README.md` associated with each agent.

## Installation

We have tested `acme` on Python 3.6 & 3.7.

1.  **Optional**: We recommend using a
    [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)
    to manage your dependencies, so as to avoid version conflicts:

    ```bash
    python3 -m venv acme
    source acme/bin/activate
    pip install --upgrade pip setuptools
    ```

1.  To install `acme` core:

    ```bash
    # Install Acme core dependencies.
    pip install dm-acme

    # Install Reverb, our replay backend.
    pip install dm-acme[reverb]
    ```

1.  To install dependencies for our JAX/TensorFlow-based agents:

    ```bash
    pip install dm-acme[tf]
    # and/or
    pip install dm-acme[jax]
    ```

1.  Finally, to install environments ([gym], [dm_control], [bsuite]):

    ```bash
    pip install dm-acme[envs]
    ```

## Citing Acme

If you use Acme in your work, please cite the accompanying
[technical report][Paper]:

```bibtex
@article{hoffman2020acme,
    title={Acme: A Research Framework for Distributed Reinforcement Learning},
    author={Matt Hoffman and
            Bobak Shahriari and
            John Aslanides and
            Gabriel Barth-Maron and
            Feryal Behbahani and
            Tamara Norman and
            Abbas Abdolmaleki and
            Albin Cassirer and
            Fan Yang and
            Kate Baumli and
            Sarah Henderson and
            Alex Novikov and
            Sergio Gómez Colmenarejo and
            Serkan Cabi and
            Caglar Gulcehre and
            Tom Le Paine and
            Andrew Cowie and
            Ziyu Wang and
            Bilal Piot and
            Nando de Freitas},
    year={2020},
    journal={arXiv preprint arXiv:2006.00979},
    url={https://arxiv.org/abs/2006.00979},
}
```

[Documentation]: docs/index.md
[Examples]: examples/
[Agents]: acme/agents/
[Reverb]: https://github.com/deepmind/reverb
[Paper]: https://arxiv.org/abs/2006.00979
[gym]: https://github.com/openai/gym
[dm_control]: https://github.com/deepmind/dm_control
[bsuite]: https://github.com/deepmind/bsuite
