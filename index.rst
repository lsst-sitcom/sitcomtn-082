:tocdepth: 1

.. sectnum::

.. Metadata such as the title, authors, and description are set in metadata.yaml

.. TODO: Delete the note below before merging new content to the main branch.

Abstract
========


This technote is to describe analysis and results from individual hardpoint breakaway tests with M1M3 surrogate.
 
The notebook can be found on `notebooks_vandv <https://github.com/lsst-sitcom/notebooks_vandv/blob/tickets/SITCOM-838/notebooks/tel_and_site/subsys_req_ver/m1m3/SITCOM-838_Anaysis.ipynb>`_ github repo.   


Hardpoint Breakaway Test
========================
The active support system of the M1M3 mirror includes six axial hard point actutators in a hexapod configuration.
These hard point actuators should minimize forces during slews at any TMA position and be kept under the breakaway limit. 
The breakaway limits for each hard points should happen in the range of -4420 to -3456 N for retraction and 2981 to 3959 N for extension.
The followings are procedures (achieved/proceeded/done/executed) in the script of the individual hardpoint breakaway test. 
 
1. Perform the following steps for full extension for a hardpoint actuator

2. Issue/command hardpoint step command

3. Moving the hardpoint to be extended (Moving Negative)

4. Waiting for hardpoint motion to complete or to operate a limit switch 

5. When hardpoint is stopped, query hardpoint monitor and actuator data 

6. The hardpoint is compressed until its completion or the activation of the limit switch and collect data 

7. Re-extend the hardpoint until its breakaway range and collect data. 

8. Moving the hardpoint to extend it and repeat the steps for the other hardpoints. 

9. Reverting status of M1M3 from parked engineering to standby state.


List of Hardpoint Breakwaway Test
=================================

.. _table-label:

.. table:: Table 1. List of the Hardpoint Breakaway Test


    +----------+--------+----------------------+----------+ 
    | elevation| Azimuth| Start Time           | SALIndex |
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

These are results from hardpoint breakaway tests when the TMA is positioned at el=90 deg and Az=-29.69 deg.  
Figure 1 shows that measured forces on the hardpoint 1 - 6 during the hardpoint axial break test. 
 


.. figure:: /_static/m1m3004_hp_timeline_El_90.png
   :name: hp_timeline_EL_90
   
   Figure 1. Transition of the measured forces on each hardpoint when the TMA is at el=90deg. 


In Figure 2, there are the change of the measured force for each phase/status in the hardpoint breakaway test, Moving Negative, Testing Positive, and Testing Negative, respectively. 
The stiffness of each curves are fitted from :math:`\Delta`\displacement = 0 :math:`{\mu}m`. 
The slopes of the all stiffness are shallower than the values expected for specification (100N/:math:`{\mu}m`). 
 

.. figure:: /_static/Force_displacement_salidx_100061_El_90.png
   :name: force_displacement_EL_90

   Figure 2. :math:`\Delta` Displacement versus Measured Forces for each phase during the hardpoint breakaway test 



Hard Point Breakaway Test at el=0
===================================

These are results from hardpoint breakaway test when the TMA was positioned at el=0 deg and Az=-29.69 deg. 
In Figure 3,    

.. figure:: /_static/m1m3004_hp_timeline_El_0.png
   :name: hp_timeline_EL_0
   
   Figure 3. Same as Figure 1 but the TMA at el=0deg. 

In Figure 4,  
The stiffness of each curves are fitted from :math:`\Delta`\displacement = 0 :math:`{\mu}m`

.. figure:: /_static/Force_displacement_salidx_100056_El_0.png
   :name: force_displacement_EL_0

   Figure 4. Same as Figure 2 but the TMA at el=0 deg. 


.. rubric:: References

.. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
   :style: lsst_aa
