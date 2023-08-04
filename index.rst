:tocdepth: 1

.. sectnum::

.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

Abstract
========

This technote describes the analysis and results derived from individual hardpoint breakaway tests conducted with the M1M3 surrogate.
The notebook is located within `notebooks_vandv <https://github.com/lsst-sitcom/notebooks_vandv/blob/tickets/SITCOM-838/notebooks/tel_and_site/subsys_req_ver/m1m3/SITCOM-838_Anaysis.ipynb>`_ GitHub repository.
With all the steps guarded with reasonable timeouts, so problems are detected if hardpoint cannot travel to hit low/high limit switches etc.
**If this test shows that the hardpoints do not work properly at the limits, this could be one of the blockers for the installation of M1M3 until it is solved.** 


Hardpoint Breakaway Test
========================

The active support system of the M1M3 includes six axial hard point actutators in the hexapod configuration. :cite:`2018SPIE10700E..3GD`
These hard point actuators should minimize forces during slews at any TMA position and be kept under the breakaway limit. 
The breakaway limits for each hard points should happen in the range of -4420 to -3456 N for retraction and 2981 to 3959 N for extension.
The followings steps are performed during the individual hardpoint breakaway test.

1. Move hardpoint in negative (increasing tension) direction until either a low limit switch is actuated

2. Move hardpoint in positive (increasing compression) direction till the high limit switch is triggered

3. Move hardpoint downwards (increasing tension) until the low limit switch is hit

4. Move hardpoint back to reference position

5. Wait for the hardpoint to reach the reference position


For tests, only full travel (from low limit to high limit and back) performed in steps 2 and 3 shall be considered. Other hardpoint movements does not guarantee a full hardpoint motion range will be examined.


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



Hard Point Breakaway Test at el=90
==================================

These are results from hardpoint breakaway tests when the TMA is positioned at el=90 deg and az=-29.69 deg.  
Figure 1 shows that measured forces on the hardpoint 1 - 6 during the hardpoint axial break test. 
 
.. figure:: /_static/m1m3004_hp_timeline_El_90.png
   
   Figure 1. Transition of the measured forces on each hardpoint when the TMA is at el=90deg. 


In Figure 2, there are the change of the measured force for each phase/status in the hardpoint breakaway test, Moving Negative, Testing Positive, and Testing Negative, respectively. 
The stiffness of each curves are fitted from :math:`\Delta`\displacement = 0 :math:`{\mu}m`. 
The slopes of the all stiffness are shallower than the values expected for specification (100N/:math:`{\mu}m`). 
 
.. figure:: /_static/Force_displacement_salidx_100061_El_90.png
   :scale: 45 %

   Figure 2. :math:`\Delta`\Displacement versus Measured Forces for each phase during the hardpoint breakaway test 


In order to check residual bumps during the movements of hardpoints, we adopted the error function :eq:`error_function` to fit the measured forces with respect to :math:`\Delta`\displacement for active phases (when hardpoints are moving toward negative and positive directions).  
As hardpoints breakway limits for each direction are different, the functions at the positive and negative in x-axes were fitted separately.    
The maxima of the bumps are about < 250\N, which correspond < 10\% of applied forces. 
 

.. math:: erf(x) = {\frac{2}{\sqrt{\pi}} \int_{0}^{x} e^{-t^2}\,dt}
   :label: error_function 



.. figure:: /_static/Force_displacement_fitting_residual_salidx_100061_El_90.png
   
   Figure 3. (Left) Same as Figure2, but fit with error function. (Right) Residual, the difference between data and fit, with respect to :math:`\Delta`\displacement 





Hard Point Breakaway Test at el=0
===================================

These are results from hardpoint breakaway test when the TMA was positioned at el=0 deg and az=-29.69 deg. 
In Figure 4, hardpoint 2 and hardpoint 5 were not contracted and the duration time of negative forces applied on HPs were shorter for hardpoint 3 and hardpoint 4 
 

.. figure:: /_static/m1m3004_hp_timeline_El_0.png
   
   Figure 4.  Same as Figure 1 but the TMA at el=0 deg. 

The stiffness of each curves are fitted from :math:`\Delta`\displacement = 0 :math:`{\mu}m` (Figure 5). 

.. figure:: /_static/Force_displacement_salidx_100056_El_0.png
   :scale: 45 %

   Figure 5. Same as Figure 2 but the TMA at el=0 deg. 


.. figure:: /_static/Force_displacement_fitting_residual_salidx_100056_El_0.png
   
   Figure 6.  Same as Figure 3 but the TMA at el=0 deg.   


Hard Point Breakaway Test at el=40
===================================

.. figure:: /_static/m1m3004_hp_timeline_El_40.png
   
   Figure 7.  Same as Figure 1 but the TMA at el=40 deg. 

.. figure:: /_static/Force_displacement_salidx_100034_El_40.png
   :scale: 45 %

   Figure 8. Same as Figure 2 but the TMA at el=40 deg. 

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100034_El_40.png
   
   Figure 9.  Same as Figure 3 but the TMA at el=40 deg.   


Hard Point Breakaway Test at el=20
===================================

.. figure:: /_static/m1m3004_hp_timeline_El_20.png
   
   Figure 10.  Same as Figure 1 but the TMA at el=20 deg. 

.. figure:: /_static/Force_displacement_salidx_100036_El_20.png
   :scale: 45 %

   Figure 11. Same as Figure 2 but the TMA at el=20 deg. 

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100036_El_20.png
   
   Figure 12.  Same as Figure 3 but the TMA at el=20 deg.   

Hard Point Breakaway Test at el=10
===================================

.. figure:: /_static/m1m3004_hp_timeline_El_10.png
   
   Figure 13. Same as Figure 1 but the TMA at el=10 deg. 

.. figure:: /_static/Force_displacement_salidx_100059_El_10.png
   :scale: 45 %

   Figure 14. Same as Figure 2 but the TMA at el=10 deg. 

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100059_El_10.png
   
   Figure 15. Same as Figure 3 but the TMA at el=10 deg.   

Hard Point Breakaway Test at el=5
===================================

.. figure:: /_static/m1m3004_hp_timeline_El_5.png
   
   Figure 16. Same as Figure 1 but the TMA at el=5 deg. 

.. figure:: /_static/Force_displacement_salidx_100058_El_5.png
   :scale: 45 %

   Figure 17. Same as Figure 2 but the TMA at el=5 deg. 

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100058_El_5.png
   
   Figure 18. Same as Figure 3 but the TMA at el=5 deg.   


Hard Point Breakaway Test at el=1
===================================

.. figure:: /_static/m1m3004_hp_timeline_El_1.png
   
   Figure 13. Same as Figure 1 but the TMA at el=1 deg. 

.. figure:: /_static/Force_displacement_salidx_100057_El_1.png
   :scale: 45 %

   Figure 14. Same as Figure 2 but the TMA at el=10 deg. 

.. figure:: /_static/Force_displacement_fitting_residual_salidx_100057_El_1.png
   
   Figure 15. Same as Figure 3 but the TMA at el=1 deg.   


.. rubric:: References

.. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
   :style: lsst_aa
