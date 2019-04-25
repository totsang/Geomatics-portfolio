##################################################
#Link to the resultant Esri Story Map: https://arcg.is/0XeHf9
##################################################
path = r"C:\Users\totsang\Desktop\test"
path_name = r"\lab_3_test_3.gdb"
path_to_data = r"C:\Users\totsang\Desktop\data"
##################################################
gdb_path = path + path_name
arcpy.CreateFileGDB_management(path, path_name)
hospitals_shp = r"\HOSPITALS_point.shp"
path_hospital = path_to_data + hospitals_shp
cities_shp = r"\POP_PL_1M_point.shp"
path_cities = path_to_data + cities_shp
arcpy.env.workspace = gdb_path
#import datasets
#Hospitals
in_feature = path_hospital
out_name = "hospitals"
arcpy.conversion.FeatureClassToFeatureClass(in_feature, gdb_path, out_name)
#Populated_place
in_feature = path_cities
out_name = "popPlaces"
arcpy.conversion.FeatureClassToFeatureClass(in_feature, gdb_path, out_name)
arcpy.ListFeatureClasses()
print("Task 2 complete")
##################################################
#Assign variables to feature classes
hospitals = "hospitals"
fc= "popPlaces"
fieldlist = arcpy.ListFields(fc)
popfield = "EST_POP"
cityname = "NAME"
city = "Courtenay"
print("Task 3 complete")
##################################################
average = 0
totalPopulation = 0
recordsCounted = 0
with arcpy.da.SearchCursor(fc,(popfield)) as cursor:
	for row in cursor:
		totalPopulation += row[0]
		recordsCounted += 1
average = totalPopulation/recordsCounted
print("Average population of all cities is "+str(average))
print("Task 4 complete")
##################################################
arcpy.analysis.Near(fc, hospitals)
distance = "NEAR_DIST"
citypop = 0
neardis = 0
where = cityname+" = '"+ city +"'"
with arcpy.da.SearchCursor(fc,(popfield, distance), where) as cursor:
	for row in cursor:
		citypop += row[0]
		neardis += row[1]
print(str(city) +" has a population of " + str(citypop) + " and the distance from the nearest hospital is " +str(neardis) + " meters")

minPop = 0
maxPop = 0
with arcpy.da.SearchCursor(fc,(popfield, distance), where) as cursor:
	for row in cursor:
		minPop += row[0]*0.9
		maxPop += row[0]*1.1
		print("The value below 10% of "+ str(city)+ "'s population is "+str(minPop))
		print("The value above 10% of "+ str(city)+ "'s population is "+str(maxPop))
print("Task 5 complete")
##################################################
where = popfield+"<="+"("+str(maxPop)+")"+ " And "+popfield+">="+"("+str(minPop)+")"
average = 0
dis_sum = 0
dis_count = 0
with arcpy.da.SearchCursor(fc,(popfield, distance, cityname), where) as cursor:
	print("The list of cities within +/- 10% of the population of Courtenay")
	for row in cursor:
		dis_sum += row[1]
		dis_count += 1
		print(str(row[2]))
average = dis_sum/dis_count
print("The average distance from the selected cities to their nearest hospital is " + str(average))
print("Task 6 complete")
##################################################
#Assign variables to fields
arcpy.management.AddFields(fc,[["SmallCities", "SHORT"],["MedCities", "SHORT"], ["LargeCities", "SHORT"]])
small = "SmallCities"
medium = "MedCities"
large = "LargeCities"
with arcpy.da.UpdateCursor(fc, (popfield, small, medium, large)) as cursor:
	for row in cursor:
		if row[0] <= 500:
			row[1] = 1
			row[2] = 0
			row[3] = 0
		elif row[0] > 500 and row[0] <= 10000:
			row[1] = 0
			row[2] = 1
			row[3] = 0
		else :
			row[1] = 0
			row[2] = 0
			row[3] = 1
		cursor.updateRow(row)
########################
DisFromHospi = "QualiDis"
arcpy.management.AddField(fc, DisFromHospi, "TEXT")
with arcpy.da.UpdateCursor(fc, (distance, DisFromHospi)) as cursor:
	for row in cursor:
		if row[0] <= 1000:
			row[1] = "Very Close"
		elif row[0] > 1000 and row[0] <= 10000:
			row[1] = "Close"
		else:
		    row[1] = "Far"
		cursor.updateRow(row)
print("Task 7 complete")
