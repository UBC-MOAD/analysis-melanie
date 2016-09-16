import numpy as np
import pandas as pd
import Data

def AllData_variables():
    data = pd.read_csv('/home/mgrenier/Documents/GEOTRACES_ARCTIC/GEOTRACES2015-Legs2b3b_ODV_forPaTh.txt',sep='\t')
    #data
    #data.head() # Displays the head of the table
    #data.tail() # Displays the tail of the table
    data.rename(columns={'yyyy-mm-ddThh:mm:ss.ss':'date',
                     'Longitude [degrees_east]':'lon','Latitude [degrees_north]':'lat',
                     'Bot. Depth [m]':'z_bottom','PRES_01 [decibars]':'P','Depth [metres]':'d',
                     'TE90_01 [degrees C]':'temp','PSAL_01 [psu]':'sal','SIGT_01 [kg/m**3]':'dens',
                     '231-Pa (fg/kg)':'Pa','230-Th (fg/kg)':'Th','231-Pa/230-Th':'PaTh'}, inplace= True)

    # Define the number of columns and rows to display
    pd.options.display.max_columns = 64
    pd.options.display.max_columns = 94

    #data.head(n=2) # Displays the 2 first rows of the head of the table
    #data.tail(n=2) # Displays the 2 first rows of the tail of the table

    # Redefine the variables with a handy name
    sta = data.Station
    date = data.date
    lon = data.lon
    lat = data.lat
    P = data.P
    d = data.d
    t = data.temp
    s = data.sal

    #print(t.values,s.values,d.values,'\n') # Returns Series as ndarray or ndarray-like depending on the dtype 
                           # Quotes around the numbers indicate that the type is an object, not a float

        
    t = pd.to_numeric(t, errors='coerce')
    s = pd.to_numeric(s, errors='coerce')
    
    from salishsea_tools import  psu_tools
    
    rho = psu_tools.calculate_density(t,s)
    rho = rho - 1000
    rhomin=rho.min()
    rhomax=rho.max()
    #print(rhomin,rhomax,rho.shape,rho.values,'\n')
    
    idx = 25 # Number of the column where you want to insert your new column, starting from 0 
    col_name = 'rho'
    value = rho
    data.insert(idx, col_name, value)

    import DerivVar
    from importlib import reload

    reload(DerivVar)
    isop,si,ti = DerivVar.isopycnal_forTSplot(s,t)
   
    import numpy as np

    isopmin=isop.min()
    isopmax=isop.max()
    levels = np.arange(isopmin,isopmax,0.2) 
    #isopmin,isopmax,isop.shape
    #levels    
    
    return data,sta,date,lon,lat,P,d,t,s,rho,isop,si,ti

#####################################################################################################################
#####################################################################################################################
def PaTh_variables():

    data,sta,date,lon,lat,P,d,t,s,rho,isop,si,ti = Data.AllData_variables()
    
    PaData=data[data.Pa.notnull()] # PaData: select only rows where Pa is not NaN -> n=92
    ThLost=PaData[PaData.Th.isnull()] # Among PaData, select only rows where Th is NaN 
                                  # (refer to Th sample lost)-> n=2
    PaThData=pd.concat([data[data.Th > 0],PaData[PaData.Th.isnull()]]) # Concatenate the rows where Th is not NaN
                                                                   # and where Th is NaN but Pa is not NaN -> n=94
    #print(len(PaData),len(PaThData),'\n')
    #print(PaThData[PaThData.Station == 'BB3']) # Displays the rows of the table corresponding to the Pa and Th data 
                                           # of the station BB3
    PaTh_sta = PaThData.Station
    PaTh_lon = PaThData.lon
    PaTh_lat = PaThData.lat
    PaTh_t = PaThData.temp
    PaTh_s = PaThData.sal
    PaTh_rho = PaThData.rho
    PaTh_d = PaThData.d
    
    
    return PaThData,PaTh_sta,PaTh_lon,PaTh_lat,PaTh_t,PaTh_s,PaTh_rho,PaTh_d

#####################################################################################################################
#####################################################################################################################

def PaTh_varSorted():
    
    data,sta,date,lon,lat,P,d,t,s,rho,isop,si,ti = Data.AllData_variables()
    PaThData,PaTh_sta,PaTh_lon,PaTh_lat,PaTh_t,PaTh_s,PaTh_rho,PaTh_d = Data.PaTh_variables()
    
    listAllSta = []
    listPaThSta = []

    for i in range(0,len(lon-1),1):
        if sta[i] not in listAllSta:
            listAllSta.append(sta[i])
        if data.Th.notnull()[i]:
            if sta[i] not in listPaThSta:
                listPaThSta.append(sta[i])
                

    from collections import OrderedDict

    d_sort = OrderedDict()
    for stn in listPaThSta:
        d_sort[stn] = PaThData[PaThData.Station == stn].sort_values(by='d', ascending=[True])
    PaThDataSorted = pd.concat(d_sort.values())
    #d_sort[listPaThSta[0]] ## This line and the line below are equivalent
    #d_sort['K1']
    #PaThDataSorted
    
    return listAllSta,listPaThSta,PaThDataSorted
