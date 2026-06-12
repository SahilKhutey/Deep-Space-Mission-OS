# Deep Space Propulsion Simulator

This repository contains high-fidelity mathematical models and simulation tools for chemical, electric, and nuclear spacecraft propulsion subsystems.

## Engines and Models Supported

1.  **Chemical Bipropellant Systems**
    *   Cryogenic systems (LOX/LH2, LOX/LCH4)
    *   Storable hypergolic systems (NTO/MMH)
    *   Pre-configured engines: RL-10, Raptor, Merlin, Vulcain, Aerojet-R4D

2.  **Electric Propulsion Systems**
    *   Electrostatic Grid Ion Thrusters (NSTAR, NEXT)
    *   Electromagnetic Hall Effect Thrusters (BHT-600, PPS-1350)
    *   Exhaust jet power, beam efficiency, and electrical specific power sizing

3.  **Nuclear Propulsion Systems**
    *   Nuclear Thermal Propulsion (NTP) (NERVA, Pewee) - heats molecular hydrogen
    *   Nuclear Electric Propulsion (NEP) - reactor coupled with high-impulse ion thrusters
    *   Thermal sizing, specific mass power constraints

## Getting Started

```python
from propulsion.chemical import BipropellantEngine
from propulsion.electric import IonThruster
from propulsion.nuclear import NuclearEngine
```

## Sizing Equations

*   Propellant sizing matches Tsiolkovsky: $m_p = m_0 \left(1 - e^{-\frac{\Delta V}{I_{sp} g_0}}\right)$
*   Mass flow rate: $\dot{m} = \frac{T}{I_{sp} g_0}$
*   Electrical efficiency: $\eta = \frac{P_{jet}}{P_{electric}} = \frac{T I_{sp} g_0}{2 P_{electric}}$
