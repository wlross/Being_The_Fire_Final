import datetime
import planet 
from planet import api
from planet.api import filters
import processing

#TODO --- need to strip a shape file only for the fires you're using out!!!
#pick the shape file you're looping through
fileName = "C:/Users/wlross/Desktop/Capstone/Spur_0.shp"

#note -- this also adds the layer to the interface... 
spur = iface.addVectorLayer(fileName, '', 'ogr')

#loop through field names for attribute table
for field in spur.fields():
    print(field.name())
 
#get the relevant bounding box and save as AOI ('area of interest')
featureCount = spur.featureCount() #feature count is rows
for i in range(0,featureCount):
    feat = spur.getFeature(i)
    fireName = feat['incidentna']
    fireDate = feat['perimeterd']
    bBox=feat.geometry().boundingBox().toString()
    bBox=bBox.replace(':',',')
    bBox=bBox.split(',')
    bBox[2]=bBox[2].lstrip(' ')
    finBox = [[float(bBox[0]),float(bBox[1])],[float(bBox[2]),float(bBox[1])],[float(bBox[2]),float(bBox[3])],[float(bBox[0]),float(bBox[3])]]
    geom_AOI = { "type": "Polygon", "coordinates": [finBox]} #OKAY


#convert to date time and get 30 days to 2 day prior (ASSUMES FROM 0)
fireDate=datetime.datetime.strptime(fireDate,'%Y-%m-%d')
startDate = fireDate - datetime.timedelta(30)
endDate = fireDate - datetime.timedelta(2)   #TODO -- NEED TO FIND TIME RANGE THAT WORKS FOR ALL 2017 FIRES... works if -360 (ie, one year forward)
#bring in Planet API Key
client = api.ClientV1(api_key="e262ca6835e64fa7b6975c558237e509")

#Build up Planet filter... 
date_filter = filters.date_range('acquired', gte= startDate, lte= endDate)
cloud_filter = filters.range_filter('cloud_cover', lte=0.03)
geom_filter = filters.geom_filter(geom_AOI)
and_filter = filters.and_filter(date_filter, cloud_filter, geom_filter)
item_types = ["REOrthoTile"] #could be PSOrthoTile

request = filters.build_search_request(and_filter, item_types)
print(request)

results = client.quick_search(request)

print("it should print something :")  #TODO: DON'T KNOW WHY IT IS NOT PRINTING... COME BACK TO W. WILLIAM
print(type(results))
print(results.items_iter)
for item in results.items_iter(1):
    print(item['id'], item['properties']['item_type'])

#create grid
paramBox = bBox[0]+','+bBox[2]+','+bBox[1]+','+bBox[3]+' [EPSG:4269]'
gridFile = 'C:/Users/wlross/Desktop/Capstone/' + fireName + '_Grid_Test.shp'
print(gridFile)
myParams = { 'CRS' : QgsCoordinateReferenceSystem('EPSG:4269'), 'EXTENT' : paramBox, 'HOVERLAY' : 0, 'HSPACING' : 0.0005, 'OUTPUT' : gridFile, 'TYPE' : 2, 'VOVERLAY' : 0, 'VSPACING' : 0.0005 }
processing.run('native:creategrid', myParams)
testGrid = iface.addVectorLayer(gridFile, '', 'ogr')

#geojoin fire bound day 0   #TODO -- need to replace filename to make it scale
joinFile = fileName + '|layername=Spur_0'
joinZero = 'C:/Users/wlross/Desktop/Capstone/' + fireName + '_join_Zero.shp'
myParams = { 'DISCARD_NONMATCHING' : False, 'INPUT' : gridFile, 'JOIN' : joinFile, 'JOIN_FIELDS' : ['incidentna'], 'METHOD' : 1, 'OUTPUT' : joinZero, 'PREDICATE' : [0], 'PREFIX' : '' }
processing.run('qgis:joinattributesbylocation', myParams)
zeroGrid = iface.addVectorLayer(joinZero, '', 'ogr')

#geojoin fire bound day 1
#TODO -- repeat code above




#NOTE TODO -- what to do about null values?
#take average pixel value for each band and store in table
inputRaster = 'C:/Users/wlross/Desktop/Capstone/Spur_1_Image_REOrthoTile_Explorer/files/1254723_2016-04-27_RE5_3A_Analytic_clip.tif'
joinFile = joinZero + '|layername=Spur_join_Zero'
#band 1 - Red
myParams = {'COLUMN_PREFIX' : 'Red_', 'INPUT_RASTER': inputRaster, 'INPUT_VECTOR': joinFile, 'RASTER_BAND': 1, 'STATS': [2] }
processing.run('qgis:zonalstatistics', myParams)
redGrid = iface.addVectorLayer(joinZero, '', 'ogr')
#band 2 - Green
myParams = {'COLUMN_PREFIX' : 'Green_', 'INPUT_RASTER': inputRaster, 'INPUT_VECTOR': joinFile, 'RASTER_BAND': 2, 'STATS': [2] }
processing.run('qgis:zonalstatistics', myParams)
redGrid = iface.addVectorLayer(joinZero, '', 'ogr')
#band 3 - Blue
myParams = {'COLUMN_PREFIX' : 'Blue_', 'INPUT_RASTER': inputRaster, 'INPUT_VECTOR': joinFile, 'RASTER_BAND': 3, 'STATS': [2] }
processing.run('qgis:zonalstatistics', myParams)
redGrid = iface.addVectorLayer(joinZero, '', 'ogr')
#band 4 - RedEdge
myParams = {'COLUMN_PREFIX' : 'REdge_', 'INPUT_RASTER': inputRaster, 'INPUT_VECTOR': joinFile, 'RASTER_BAND': 4, 'STATS': [2] }
processing.run('qgis:zonalstatistics', myParams)
redGrid = iface.addVectorLayer(joinZero, '', 'ogr')
#band 5 - NearInfrared
myParams = {'COLUMN_PREFIX' : 'NIR_', 'INPUT_RASTER': inputRaster, 'INPUT_VECTOR': joinFile, 'RASTER_BAND': 5, 'STATS': [2] }
processing.run('qgis:zonalstatistics', myParams)
redGrid = iface.addVectorLayer(joinZero, '', 'ogr')