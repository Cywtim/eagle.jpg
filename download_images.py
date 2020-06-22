import eagleSqlTools as sql
import numpy as np
import urllib
import BeautifulSoup
from sys import argv

# Array of chosen simulations. Entries refer to the simulation name and comoving box length.
mySims = np.array([('RefL0100N1504', 100.)])

# This uses the eagleSqlTools module to connect to the database with your username and password.
con = sql.connect('user', password='passw')

for sim_name, sim_size in mySims:
        print( sim_name)
	# Construct and execute query for each simulation. This query returns the number of galaxies
	# for a given 30 pkpc aperture stellar mass bin (centered with 0.2 dex width).

	# This query specifically select galaxies with a stellar mass within a range of ~4^10 and 10^11 solar 		# masses. In order to discern their morphological trais, two more conditions related to dark matter and
	# star particles are imposed. (In this case, at least 20000 star particles and 100000 Dark matter 	  # particles)
        myQuery = "SELECT \
                        Image_face,\
                        Image_box as myurl\
                   FROM \
			%s_SubHalo as SH, \
			%s_FOF as FOF, \
		  	%s_Aperture as AP, \
                        %s_ParticleCounts as PC \
                   WHERE \
			AP.ApertureSize = 30 and \
                        PC.Count_Star > 20000 and \
			AP.Mass_Star > 3.99e10 and \
			SH.MassType_DM/9.70e6 > 100000 and \
			AP.Mass_Star < 1e11 and \
			SubGroupNumber = 0 and \
			SH.SnapNum = 28 and \
                        AP.GalaxyID = SH.GalaxyID and \
			PC.GalaxyID = SH.GalaxyID and \
			FOF.GroupID = SH.GroupID \
		   ORDER BY \
			mass"%(sim_name, sim_name, sim_name, sim_name)

#Execute query.
myData 	= sql.execute_query(con, myQuery)
print('Selected %i galaxies.'%len(myData['myurl']))

for i in range(len(myData['myurl'])):
    soup = BeautifulSoup.BeautifulSoup(myData['myurl'][i])
    img = "img/image_%06d.jpg"%i
    url = soup.find('img')['src']
    print("Downloading EAGLE galaxy %i..."%i)
    urllib.urlretrieve(url, img)

# np.save("mass.npy", myData['mass'])
# np.save("virial.npy", myData['virial'])
