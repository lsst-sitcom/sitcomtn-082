:tocdepth: 1

.. sectnum::

.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

Abstract
========

This technote describes the analysis and results derived from individual hard point breakaway tests conducted with the M1M3 surrogate.
The notebook is located within `notebooks_vandv <https://github.com/lsst-sitcom/notebooks_vandv/blob/tickets/SITCOM-838/notebooks/tel_and_site/subsys_req_ver/m1m3/SITCOM-838_Anaysis.ipynb>`_ GitHub repository.
With all the steps guarded with reasonable timeouts, so problems are detected if hard point cannot travel to reach low or high limit switches, etc.
**If this test shows that the hard points do not work properly at the limits, this could be one of the blockers for the installation of M1M3 until it is solved.** 



Hardpoint Breakaway Test
========================

The active support system of the M1M3 includes six axial hard point actutators in a hexapod configuration. :cite:`2018SPIE10700E..3GD`
These hard point actuators should minimize forces during slews at any TMA position and be kept under the breakaway limit. 
The breakaway limits for each hard points should happen in the range of -4420 to -3456 N for retraction and 2981 to 3959 N for extension.
The followings steps are performed during the individual hard point breakaway test.

1. Move hard point in negative (increasing tension) direction until a low limit switch is actuated

2. Move hard point in positive (increasing compression) direction till the high limit switch is triggered

3. Move hard point downwards (increasing tension) until the low limit switch is hit

4. Move hard point back to reference position

5. Wait for the hard point to reach the reference position

.. todo::

    Check if there are limit switches for this. 
    Confirm sentences in the first section. 

Requirements and Tickets
========================

Associated JIRA tickets and requirements with this test. 

    - `SITCOM-838 <https://jira.lsstcorp.org/browse/SITCOM-838>`_
    - `LTS-88 <https://docushare.lsst.org/docushare/dsweb/Get/LTS-88>`_ LTS-88-REQ-0017-V-01: 3.7.5.1 Load Limiting Axial Breakaway Mechanism Displacement
    - `LVV-11200 <https://jira.lsstcorp.org/browse/LVV-11200>`_ LTS-88-REQ-0015-V-01: 3.7.1.3 Hardpoint Displacement Repeatability and Resolution_1
    - `LVV-11184 <https://jira.lsstcorp.org/browse/LVV-11184>`_ LTS-88-REQ-0024-V-01: 3.7.1.7 Hardpoint Axial Breakaway Repeatability_1
    - `LVV-11208 <https://jira.lsstcorp.org/browse/LVV-11208>`_ LTS-88-REQ-0025-V-01: 3.7.1.8 Hardpoint Stiffness Limits_1



List of Hardpoint Breakwaway Test
=================================

.. _table-label:

.. table:: Table 1. List of the Hardpoint Breakaway Test


    +----------+--------+----------------------+----------+ 
    | elevation| azimuth| Start Time           | SALIndex |
    +----------+--------+----------------------+----------+ 
    | (deg)    | (deg)  | (YYYY-MM-DDTHH:MM:SS)|          |
    +==========+========+======================+==========+ 
    | 0        | -29.69	| 2023-05-30T21:26:51  | 100056   |
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



Hard Point Test Result 
======================


A general results of HP Test
----------------------------
.. todo:: 
   - General results from HP test
   - More detailed description for results from HP tests. 


HP Test at el 90 deg
--------------------

These are results from hard point breakaway tests when the TMA is positioned at el=90 deg, az=-29.69 deg.  
Figure 1 shows that measured forces on the hard point 1 - 6 during the hard point axial break test.
Measured forces on all hard points look working properly because breakaway happened in the range of the requirement (tension: -4420 - -3456N, compression: 2981 - 3959N). 

.. Todo::

   More detailed descriptions and explanations might be further needed. 
 
.. figure:: /_static/m1m3004_hp_timeline_El_90.png
   
   Transition of the measured forces on each hard point when the TMA is at el=90deg. 


In Figure 2, there are the change of the measured force for each phase/status in the hard point breakaway test, moving Negative, testing positive, and testing negative, respectively. 
The stiffness of each curves are fitted with +-10 points from :math:`\Delta`\displacement = 0 :math:`{\mu}m`. 
All stiffness slopes are shallower than specification (100N/:math:`{\mu}m`). 
 
.. figure:: /_static/Force_displacement_salidx_100061_El_90.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=90deg. 

In order to check residual bumps during the movements of hard points, we adopted the error function :eq:`error_function` to fit the measured forces with respect to :math:`\Delta`\displacement for active phases when the hard points are moving toward negative and positive directions.  
As hard points breakaway limits for each direction are different, the functions at the positive and negative in x axes were fitted separately.    
The maxima of the bumps are about < 250\N, which correspond < 10\% of the measured forces.  
 

.. math:: erf(x) = {\frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2}\,dt}
   :label: error_function 



.. figure:: /_static/Force_displacement_fitting_residual_salidx_100061_El_90.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=90deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 




HP Test at el 0 deg
--------------------


These are results from hard point breakaway test when the TMA was positioned at el=0 deg, az=-29.69 deg. 
In Figure 4, hard point 2 and hard point 5 were not moving to the positive direction. 
Hardpoint 1 and hard point 6 were both staying on the position for testing positive for a shorter period of time whereas hard point 3 and hard point 4 were staying on testing negative position for a shorter period time.  
This is because depending on the position of each hard point.  

.. todo:: 
    - Reference cross check



.. figure:: /_static/m1m3004_hp_timeline_El_0.png
   
    Figure 4. Transition of the measured forces on each hard point when the TMA is at el=0deg. 

The stiffness of each curves are fitted from :math:`\Delta`\displacement = 0 :math:`{\mu}m` (Figure 5). 

.. figure:: /_static/Force_displacement_salidx_100056_El_0.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=0 deg.  


.. figure:: /_static/Force_displacement_fitting_residual_salidx_100056_El_0.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=0deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


HP Test at el 40 deg
--------------------

.. figure:: /_static/m1m3004_hp_timeline_El_40.png
   
   Transition of the measured forces on each hard point when the TMA is at el=40deg. 

.. figure:: /_static/Force_displacement_salidx_100034_El_40.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=40 deg.  

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100034_El_40.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=40deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


HP Test at el 20 deg
--------------------

.. figure:: /_static/m1m3004_hp_timeline_El_20.png
   
   Transition of the measured forces on each hard point when the TMA is at el=20deg. 

.. figure:: /_static/Force_displacement_salidx_100036_El_20.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=20 deg.  

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100036_El_20.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=20deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


HP Test at el 10 deg
--------------------

.. figure:: /_static/m1m3004_hp_timeline_El_10.png
   
   Transition of the measured forces on each hard point when the TMA is at el=10deg. 

.. figure:: /_static/Force_displacement_salidx_100059_El_10.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=10 deg.  

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100059_El_10.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=10deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


HP Test at el 5 deg
--------------------

.. figure:: /_static/m1m3004_hp_timeline_El_5.png
   
   Transition of the measured forces on each hard point when the TMA is at el=5deg. 

.. figure:: /_static/Force_displacement_salidx_100058_El_5.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=5 deg.  

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100058_El_5.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=5deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


HP Test at el 1 deg
--------------------

.. figure:: /_static/m1m3004_hp_timeline_El_1.png
   
   Transition of the measured forces on each hard point when the TMA is at el=1deg. 

.. figure:: /_static/Force_displacement_salidx_100057_El_1.png
   :scale: 45 %

   :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test when the TMA is at el=1 deg.  

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100057_El_1.png
   
   (Left) :math:`\Delta`\Displacement versus measured forces for each phase during the hard point breakaway test fit with error function (the TMA at el=1deg). (Right) The residual, a difference between data and error function, with respect to :math:`\Delta`\displacement 


.. rubric:: References

.. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
   :style: lsst_aa
