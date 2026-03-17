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
.. table:: List of the Hardpoint Breakaway Tests executions

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

# Historical Trending 

The previous figures for each hardpoint at different test days show, for example, that lower elevation angles tend to be associated with higher stiffness values. The relationship between stiffness and other parameters may help identify patterns that could reduce the risk of operational issues, which gives us clues about the importance to study the behavior of each hardpoint over time. 

Therefore, in this section, we analyze the historical trends of the hardpoint breakaway tests using data from completed tests between 2023 and the present day.


:::{note}
- Each month has a different number of testing days.
- Some days have no tests, while others have more than one test.
:::

In order to view graphically the above we plot a dashboard to compare the data obtain for each day with completed test. 

<div class="figure" id="dashboard-hardpoints" style="margin-bottom: 25px;">
  <iframe 
    src="_static/dashboard_hardpoints.html" 
    width="100%" height="750px" 
    frameborder="0" 
    style="border:1px solid #E0E0E0; border-radius:6px;">
  </iframe>
  <p style="text-align: center; font-style: italic; margin-top: 10px;">
    (Top) Interactive dashboard of test days. (Bottom) Interactive dashboard of hardpoint stiffness trends since 2023.
  </p>
</div>

In the dashboard, the top plot shows the days with completed tests up to the present day. The y-axis represents the number of tests performed on each day. From this, we observe that in may 2023 had the highest number of tests conducted in a single day.

On the other hand, the bottom plot shows how the daily mean stiffness evolves over time, modeled by Hardpoint (HP) and state. In general, we observe that stiffness values tend to become more linear over time.

The following dashboard clearly illustrates the dependence of stiffness on the elevation angle for each HP. For this analysis, we considered only physical stiffness values. To apply the normal fit, only angle ranges that met the minimum sample size requirement (n≥10) were considered. Consequently, angles such as 45°–50° for HP2 (testing positive state), which has only 3 data points (n=3), were excluded as they do not provide enough information to obtain statistically significant results.

<div class="figure" id="dashboard-elevation" style="margin-bottom: 25px;">
  <iframe 
    src="_static/dashboard_elevation.html" 
    width="100%" height="750px" 
    frameborder="0" 
    style="border:1px solid #E0E0E0; border-radius:6px;">
  </iframe>
  <p style="text-align: center; font-style: italic; margin-top: 10px;">
    Interactive dashboard illustrating how stiffness distribution varies in relation to angle range, categorized by state and hardpoint (HP).
  </p>
</div>

Furthermore, for elevation angles up to 70 degrees, there are insufficient data points for each HP to calculate the median or standar deviation via normal fit, given our minimum requirement of n≥10.

In contrast, for angles above 70°, we observe that HP1 reaches a minimum mean stiffness of 15.02 N/µm in the 80°–85° range ($\sigma$=2.38), while HP6 reaches a maximum of 31.03 N/µm in the 85°–90° range ($\sigma$=1.78). Overall, a general trend is observed: for each hardpoint, an increase in elevation angle correlates with a decrease in stiffness values.

Regarding the breakaway analysis, we obtained the breakaway force (N) and displacement (µm) for each HP and state. The following figure illustrates the distribution of these values: points in the positive testing state are located within the tension band, while points in the negative testing state are situated within the compression band.

The crosses represent data points that, for various reasons, fell outside these bands and were classified as outliers. The plots indicate that the positive testing state (tension) exhibits a higher frequency of outliers compared to the negative testing state (compression).

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/Breakaway_by_HP_state/HP1_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP1
:::

:::{image} /_static/Breakaway_by_HP_state/HP2_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP2
:::

:::{image} /_static/Breakaway_by_HP_state/HP3_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP3
:::

:::{image} /_static/Breakaway_by_HP_state/HP4_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP4
:::

:::{image} /_static/Breakaway_by_HP_state/HP5_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP5
:::

:::{image} /_static/Breakaway_by_HP_state/HP6_breakaway_TESTINGPOSITIVE_TESTINGNEGATIVE.png
:alt: HP6
:::

Plots breakaway force vs breakaway displacement for each hardpoint. The blue circles represent the points on state testing positive that are located in the tension band and the blue crosses are the points that we called outliers because are located between the compression and tension bands. The orange circles, instead, are the points on state testing negative located in the compression band, and the same way, the orange crosses are outliers in this state.  
::::

## Hardpoint Timeline

Analyzing each hardpoint individually provides insights into their mechanical condition and therefore the safety of the M1M3 mirror. Hence another element to consider is the behavior of the hardpoints over time.

The dashboard reveals that the trend for each HP differs. We can observe that the period from 2023 to late 2024 was the most unstable, whereas the period from 2025 to the present shows a more linear behavior. Additionally, the heatmap indicates that HP2 exhibited lower stiffness at the end of 2023.

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/heatmap_stiffness_mean_TESTINGNEGATIVE.png
:alt: Stiffness mean testingnegative
:::

:::{image} /_static/heatmap_stiffness_mean_TESTINGPOSITIVE.png
:alt: Stiffness mean testingpositive
:::

(Top) Heatmap of monthly stiffness mean (negative/compression state). (Bottom) Heatmap of monthly stiffness mean (positive/tension state).
Both plots show high stiffness values during 2023 and 2024.
::::

Based on these observations, a more robust analysis should prioritize data from 2025 onwards. In addition, three different filters were applied to exclude zeros, non-physical values, and days with incomplete states (i.e., days containing only 'testing positive' or 'testing negative' states).
Consequently, 154 valid days have been retained since 2025.

The following plots illustrate how each HP changes depending on the testing state. Asymmetry between compression and tension is expected, as the piston sizes differ while the internal pressure remains equal. 

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP1.png
:alt: HP1
:::

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP2.png
:alt: HP2
:::

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP3.png
:alt: HP3
:::

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP4.png
:alt: HP4
:::

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP5.png
:alt: HP5
:::

:::{image} /_static/breakaway_by_hp_2025/breakaway_time_HP6.png
:alt: HP6
:::

Breakaway Force vs. Time: Green circles represent positive state points (tension band), and green crosses indicate outliers located between the compression and tension bands. Blue circles represent negative state points (compression band), with blue crosses as outliers. 
::::

When comparing the figures, the breakaway time plots show significantly fewer outliers. HP4 is the exception, showing six outliers, the highest among all units, primarily in the positive testing state.

Regarding stiffness, the overall trend for both states has become more linear for most HPs. However, HP3 and HP4 exhibit the most irregular trends in both tension and compression, while HP1 consistently shows the lowest stiffness trend.

::::{subfigure}
:layout-sm: 1
:gap: 8px

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP1.png
:alt: HP1
:::

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP2.png
:alt: HP2
:::

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP3.png
:alt: HP3
:::

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP4.png
:alt: HP4
:::

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP5.png
:alt: HP5
:::

:::{image} /_static/stiffness_daily_by_hp_2025/daily_stiffness_HP6.png
:alt: HP6
:::

Stiffness vs. Time: Green and blue points represent the daily mean stiffness values for the positive (tension) and negative (compression) states, respectively. These figures clearly demonstrate the unusual behavior of HP3 and HP4, which exhibit significantly higher fluctuations compared to the other hardpoints.
::::

Finally, if standar deviation is calculated, we can see, that HP3 and HP4 have the highest values. 

:::{figure} _static/std_by_hp_2025.png
:alt: STD

Standar deviation for each hp since 2025.
:::



```markdown
(table-std-hp)=
### Table 2: Standard deviation for each HP for state.
 
| HP | $\sigma$ Testing Negative | $\sigma$ Testing Positive |
|:--:|:-------------------------:|:-------------------------:|
|  1 |           2.032           |           1.677           |
|  2 |           1.646           |           2.445           |
|  3 |           4.012           |           4.093           |
|  4 |           3.764           |           3.673           |
|  5 |           0.573           |           1.321           |
|  6 |           2.288           |           2.024           |

```

## Summary

The historical analysis of the M1M3 breakaway hardpoint tests leads to the following findings:

1. Data Representativeness: Data collected prior to 2025 is considered non-representative. From 2025 onwards, the data is reliable and should be used for behavioral modeling.
2. Angular Sensitivity (HP2 & HP5): HP2 and HP5 exhibit higher instability at elevation angles below 60°. While this behavior was clearly visible in pre-2025 datasets, there is currently insufficient data in the recent logs to confirm if this trend persists.
3. Anomalous Fluctuations (HP3 & HP4): Unexpectedly, HP3 and HP4 show significantly higher dispersion and fluctuations compared to the other hardpoints. It is necessary to analyze this behavior in detail and incorporate additional parameters that may be affecting the system's performance.

## References

```{eval-rst}
.. bibliography::
```
