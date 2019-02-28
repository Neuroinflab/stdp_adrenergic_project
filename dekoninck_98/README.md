### De Koninck Paul, Schulman Howard, Sensitivity of CaM Kinase II to the Frequency of Ca 2 Oscillations, 1998

* Fig.1 experiment (Ca2+ oscilations) can't be directly replicated:
  * there were no information about what does it mean High/Low Ca2+ level
  
* This folder contains replication of Fig.2 experiment - CaMKII autophosphorylation due to CaM concentration:
  * tube experiment with immobilized CaMKII
  * Ca2+ 500 uM (constant)
  * CaMKII 100% phosphorilation at 5uM
  * CaM: 0.5nM - 1000 nM injection
  
### Description

* There are 1 injection files (select one and insert it to model_start.xml):
  * CaM_50ms.xml
  
### Usage

* Change simulation to 1ms in model_start.xml
* run neurord 
* run analiza.py [h5 file created by NeuroRD]
  * read volume size in microns
* run ../molar_to_particles.py --mol [molar value] --unit [of molarity: nano or micro] --volume [volume in microns]
  * read particle number
* in selected injection file change <rate></rate> number to one you obtained from the previous step 
  * optionally divide this number by time in ms if your injection is longer than 1ms 
* change simulation for 6000ms (or any other you require) in model_start.xml
* run NeuroRD for desired simulation
* run analiza.py to create csv file with your results

