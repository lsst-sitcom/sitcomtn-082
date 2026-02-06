# Hard Point Breakaway Analysis

```{eval-rst}

   This is a technote for the description of results from Individual Hardpoint Breakaway Test.



```


## Abstract

This technote describes the analysis and results derived from individual hardpoint breakaway tests conducted with the M1M3 surrogate.
The notebook is located within [notebooks_vandv](https://github.com/lsst-sitcom/notebooks_vandv/blob/tickets/SITCOM-838/notebooks/tel_and_site/subsys_req_ver/m1m3/SITCOM-838_Anaysis.ipynb) GitHub repository.
With all the steps guarded with reasonable timeouts, so problems are detected if hardpoint cannot travel to reach low or high limit switches, etc.
**If this test shows that the hardpoints do not work properly at the limits, this could be one of the blockers for the installation of M1M3 until it is solved.**

## Hardpoint Breakaway Test

The active support system of the M1M3 includes six axial hardpoint actuators in a hexapod configuration. {cite}`2018SPIE10700E..3GD`

These hardpoint actuators should minimize forces during slews at any TMA position and be kept under the breakaway limit.
The breakaway limit for each hardpoint is in the range of -4420N to -3456N for retraction and 2981N to 3959N for extension.
The following steps are performed during an individual hardpoint breakaway test are shown in test case [LVV-T231](https://jira.lsstcorp.org/secure/Tests.jspa#/testCase/LVV-T231).

As a summary:

1. Move hardpoint in negative (increasing tension) direction until the breakaway mechanism activates.
2. Move hardpoint in positive (increasing compression) direction until the breakaway mechanism activates.
3. Move hardpoint downwards (increasing tension) until the breakaway mechanism activates.
4. Move hardpoint back to its reference position.
5. Wait for the hardpoint to reach its reference position.

## Requirements and Tickets

Associated JIRA tickets and requirements with this test:

> - [SITCOM-838](https://jira.lsstcorp.org/browse/SITCOM-838)
> - [LTS-88](https://docushare.lsst.org/docushare/dsweb/Get/LTS-88) LTS-88-REQ-0017-V-01: 3.7.5.1 Load Limiting Axial Breakaway Mechanism Displacement
> - [LVV-11200](https://jira.lsstcorp.org/browse/LVV-11200) LTS-88-REQ-0015-V-01: 3.7.1.3 Hardpoint Displacement Repeatability and Resolution_1
> - [LVV-11184](https://jira.lsstcorp.org/browse/LVV-11184) LTS-88-REQ-0024-V-01: 3.7.1.7 Hardpoint Axial Breakaway Repeatability_1
> - [LVV-11208](https://jira.lsstcorp.org/browse/LVV-11208) LTS-88-REQ-0025-V-01: 3.7.1.8 Hardpoint Stiffness Limits_1

## List of Hardpoint Breakaway Test

(table-label)=

```{eval-rst}
.. table:: Table 1. List of the Hardpoint Breakaway Tests executions

    +----------+--------+----------------------+----------+
    | elevation| azimuth| Start Time           | SALIndex |
    +----------+--------+----------------------+----------+
    | (deg)    | (deg)  | (YYYY-MM-DDTHH:MM:SS)|          |
    +==========+========+======================+==========+
    | 0        | -29.69 | 2023-05-30T21:26:51  | 100056   |
    +----------+--------+----------------------+----------+
    | 1        | -29.69 | 2023-05-30T22:40:34  | 100057   |
    +----------+--------+----------------------+----------+
    | 5        | -29.69 | 2023-05-31T00:00:10  | 100058   |
    +----------+--------+----------------------+----------+
    | 10       | -29.69 | 2023-05-31T01:03:26  | 100059   |
    +----------+--------+----------------------+----------+
    | 20       | 153    | 2023-05-27T02:49:55  | 100036   |
    +----------+--------+----------------------+----------+
    | 20       | 153    | 2023-05-30T08:26:34  | 100047   |
    +----------+--------+----------------------+----------+
    | 40       | 153    | 2023-05-26T02:23:28  | 100034   |
    +----------+--------+----------------------+----------+
    | 89.95    | 153    | 2023-06-20T03:11:00  | 100038   |
    +----------+--------+----------------------+----------+
    | 90       | -29.69 | 2023-05-31T05:44:14  | 100061   |
    +----------+--------+----------------------+----------+


```

## Hardpoint Test Result

### A general results of HP Test

:::{note}
   - General results from HP test
   - More detailed description for results from HP tests.
:::

### HP Test at EL = 90deg

These are results from hardpoint breakaway tests when the TMA is positioned at EL=90 deg, AZ=-29.69 deg.
Figure 1 shows that measured forces on the hardpoint 1 - 6 during the hardpoint axial breakaway test.
Measured forces on all hardpoints look working properly because breakaway happened in the range of the requirement (tension: -4420 - -3456N, compression: 2981 - 3959N).



::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_90_30/m1m3004_hp1_timeline_El_90.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_90_30/m1m3004_hp2_timeline_El_90.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_90_30/m1m3004_hp3_timeline_El_90.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_90_30/m1m3004_hp4_timeline_El_90.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_90_30/m1m3004_hp5_timeline_El_90.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_90_30/m1m3004_hp6_timeline_El_90.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=90deg.
::::

In Figure 2, there are the change of the measured force for each phase/status in the hardpoint breakaway test, moving Negative, testing positive, and testing negative, respectively.
The stiffness of each curves are fitted with +-10 points from $\Delta$displacement = 0 ${\mu}m$.
All stiffness slopes are shallower than specification (100N/${\mu}m$).

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_90_30/Force_displacement_El_90.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_90_30/Force_displacement_El_90.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_90_30/Force_displacement_El_90.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_90_30/Force_displacement_El_90.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_90_30/Force_displacement_El_90.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_90_30/Force_displacement_El_90.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=90deg.
::::


In order to check residual bumps during the movements of hardpoints, we adopted the error function {eq}`error_function` to fit the measured forces with respect to $\Delta$displacement for active phases when the hardpoints are moving toward negative and positive directions.
As hardpoints breakaway limits for each direction are different, the functions at the positive and negative in x axes were fitted separately.
The maxima of the bumps are about < 250N, which correspond < 10% of the measured forces.

$$
erf(x) = {\frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2}\,dt}
$$ (error_function)

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_90_30/Force_displacement_fitting_residual_El_90.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=90deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 0 deg

These are results from hardpoint breakaway test when the TMA was positioned at el=0 deg, az=-29.69 deg.
In F(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=90deg). (Rig>igure 4, hardpoint 2 and hardpoint 5 were not moving to the positive direction.
Hardpoint 1 and hardpoint 6 were both staying on the position for testing positive for a shorter period of time whereas hardpoint 3 and hardpoint 4 were staying on testing negative position for a shorter period time.
This is because depending on the position of each hardpoint.

:::{note}
    - Reference cross check
:::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_0_30/m1m3004_hp1_timeline_El_0.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_0_30/m1m3004_hp2_timeline_El_0.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_0_30/m1m3004_hp3_timeline_El_0.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_0_30/m1m3004_hp4_timeline_El_0.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_0_30/m1m3004_hp5_timeline_El_0.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_0_30/m1m3004_hp6_timeline_El_0.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=0deg.
::::

The stiffness of each curves are fitted from $\Delta$displacement = 0 ${\mu}m$ (Figure 5).

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_0_30/Force_displacement_El_0.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_0_30/Force_displacement_El_0.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_0_30/Force_displacement_El_0.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_0_30/Force_displacement_El_0.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_0_30/Force_displacement_El_0.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_0_30/Force_displacement_El_0.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=0deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_0_30/Force_displacement_fitting_residual_El_0.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=0deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 40 deg

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-26/HP1/m1m3004_hp1_timeline_El_40.png
:alt: HP1
:::

:::{image} /_static/2023-05-26/HP2/m1m3004_hp2_timeline_El_40.png
:alt: HP2
:::

:::{image} /_static/2023-05-26/HP3/m1m3004_hp3_timeline_El_40.png
:alt: HP3
:::

:::{image} /_static/2023-05-26/HP4/m1m3004_hp4_timeline_El_40.png
:alt: HP4
:::

:::{image} /_static/2023-05-26/HP5/m1m3004_hp5_timeline_El_40.png
:alt: HP5
:::

:::{image} /_static/2023-05-26/HP6/m1m3004_hp6_timeline_El_40.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=40deg.
::::


::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-26/HP1/Force_displacement_El_40.png
:alt: HP1
:::

:::{image} /_static/2023-05-26/HP2/Force_displacement_El_40.png
:alt: HP2
:::

:::{image} /_static/2023-05-26/HP3/Force_displacement_El_40.png
:alt: HP3
:::

:::{image} /_static/2023-05-26/HP4/Force_displacement_El_40.png
:alt: HP4
:::

:::{image} /_static/2023-05-26/HP5/Force_displacement_El_40.png
:alt: HP5
:::

:::{image} /_static/2023-05-26/HP6/Force_displacement_El_40.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=40deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-26/HP1/Force_displacement_fitting_residual_El_40.png
:alt: HP1
:::

:::{image} /_static/2023-05-26/HP2/Force_displacement_fitting_residual_El_40.png
:alt: HP2
:::

:::{image} /_static/2023-05-26/HP3/Force_displacement_fitting_residual_El_40.png
:alt: HP3
:::

:::{image} /_static/2023-05-26/HP4/Force_displacement_fitting_residual_El_40.png
:alt: HP4
:::

:::{image} /_static/2023-05-26/HP5/Force_displacement_fitting_residual_El_40.png
:alt: HP5
:::

:::{image} /_static/2023-05-26/HP6/Force_displacement_fitting_residual_El_40.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=40deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 20 deg

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-27/HP1/m1m3004_hp1_timeline_El_20.png
:alt: HP1
:::

:::{image} /_static/2023-05-27/HP2/m1m3004_hp2_timeline_El_20.png
:alt: HP2
:::

:::{image} /_static/2023-05-27/HP3/m1m3004_hp3_timeline_El_20.png
:alt: HP3
:::

:::{image} /_static/2023-05-27/HP4/m1m3004_hp4_timeline_El_20.png
:alt: HP4
:::

:::{image} /_static/2023-05-27/HP5/m1m3004_hp5_timeline_El_20.png
:alt: HP5
:::

:::{image} /_static/2023-05-27/HP6/m1m3004_hp6_timeline_El_20.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=20deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-27/HP1/Force_displacement_El_20.png
:alt: HP1
:::

:::{image} /_static/2023-05-27/HP2/Force_displacement_El_20.png
:alt: HP2
:::

:::{image} /_static/2023-05-27/HP3/Force_displacement_El_20.png
:alt: HP3
:::

:::{image} /_static/2023-05-27/HP4/Force_displacement_El_20.png
:alt: HP4
:::

:::{image} /_static/2023-05-27/HP5/Force_displacement_El_20.png
:alt: HP5
:::

:::{image} /_static/2023-05-27/HP6/Force_displacement_El_20.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=20 deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-27/HP1/Force_displacement_fitting_residual_El_20.png
:alt: HP1
:::

:::{image} /_static/2023-05-27/HP2/Force_displacement_fitting_residual_El_20.png
:alt: HP2
:::

:::{image} /_static/2023-05-27/HP3/Force_displacement_fitting_residual_El_20.png
:alt: HP3
:::

:::{image} /_static/2023-05-27/HP4/Force_displacement_fitting_residual_El_20.png
:alt: HP4
:::

:::{image} /_static/2023-05-27/HP5/Force_displacement_fitting_residual_El_20.png
:alt: HP5
:::

:::{image} /_static/2023-05-27/HP6/Force_displacement_fitting_residual_El_20.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=20deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 10 deg

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_10_30/m1m3004_hp1_timeline_El_10.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_10_30/m1m3004_hp2_timeline_El_10.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_10_30/m1m3004_hp3_timeline_El_10.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_10_30/m1m3004_hp4_timeline_El_10.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_10_30/m1m3004_hp5_timeline_El_10.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_10_30/m1m3004_hp6_timeline_El_10.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=10deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_10_30/Force_displacement_El_10.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_10_30/Force_displacement_El_10.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_10_30/Force_displacement_El_10.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_10_30/Force_displacement_El_10.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_10_30/Force_displacement_El_10.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_10_30/Force_displacement_El_10.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=10 deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_10_30/Force_displacement_fitting_residual_El_10.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=10deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 5 deg

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_5_30/m1m3004_hp1_timeline_El_5.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_5_30/m1m3004_hp2_timeline_El_5.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_5_30/m1m3004_hp3_timeline_El_5.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_5_30/m1m3004_hp4_timeline_El_5.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_5_30/m1m3004_hp5_timeline_El_5.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_5_30/m1m3004_hp6_timeline_El_5.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=5deg.
::::

:::{image} /_static/2023-05-31/HP1_5_30/Force_displacement_El_5.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_5_30/Force_displacement_El_5.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_5_30/Force_displacement_El_5.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_5_30/Force_displacement_El_5.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_5_30/Force_displacement_El_5.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_5_30/Force_displacement_El_5.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=5 deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-31/HP1_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP1
:::

:::{image} /_static/2023-05-31/HP2_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP2
:::

:::{image} /_static/2023-05-31/HP3_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP3
:::

:::{image} /_static/2023-05-31/HP4_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP4
:::

:::{image} /_static/2023-05-31/HP5_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP5
:::

:::{image} /_static/2023-05-31/HP6_5_30/Force_displacement_fitting_residual_El_5.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=5deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### HP Test at el 1 deg

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_1_30/m1m3004_hp1_timeline_El_1.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_1_30/m1m3004_hp2_timeline_El_1.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_1_30/m1m3004_hp3_timeline_El_1.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_1_30/m1m3004_hp4_timeline_El_1.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_1_30/m1m3004_hp5_timeline_El_1.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_1_30/m1m3004_hp6_timeline_El_1.png
:alt: HP6
:::

Transition of the measured forces on each hardpoint when the TMA is at el=1deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP6
:::

$\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test when the TMA is at el=1 deg.
::::

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/2023-05-30/HP1_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP1
:::

:::{image} /_static/2023-05-30/HP2_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP2
:::

:::{image} /_static/2023-05-30/HP3_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP3
:::

:::{image} /_static/2023-05-30/HP4_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP4
:::

:::{image} /_static/2023-05-30/HP5_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP5
:::

:::{image} /_static/2023-05-30/HP6_1_30/Force_displacement_fitting_residual_El_1.png
:alt: HP6
:::

(Left) $\Delta$Displacement versus measured forces for each phase during the hardpoint breakaway test fit with error function (the TMA at el=1deg). (Right) The residual, a difference between data and error function, with respect to $\Delta$displacement
::::

### Requirment discussion

## References

```{eval-rst}
.. bibliography::
```
