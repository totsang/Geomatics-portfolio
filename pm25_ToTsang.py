##################################################

# Link to the resultant Casecade Story Map: https://arcg.is/4Dnyz

##################################################
path = r"C:\Users\totsang\Desktop\FPJ_test_4\FPJ_test_4"
path_name = r"\FPJ_test_4.gdb"
path_to_data = r"Z:\FPJ_data_TeoTsang"
##################################################
print("#####################Create new gdb######################")
gdb_path = path + path_name
arcpy.CreateFileGDB_management(path, path_name)

print("####################### Set data paths and import data ###########################")
path_air = ""
path_pm25 = ""
path_fire = ""
path_cities = ""
path_coast = ""
path_zone = ""
doc_list = [r"\bc_air_monitoring_stations.csv", r"\PM25_2018.csv", r"\fires_2018\prot_current_fire_points.shp", r"\populatedplace\NRC_POPULATED_PLACES_1M_SP\POP_PL_1M_point.shp", r"\coastline\FWA_COASTLINES_SP\FWCSTLNSSP_line.shp", r"\airzone\bc_air_zones.shp"]
path_list = [path_air, path_pm25, path_fire, path_cities, path_coast, path_zone]
name_list = ["Air stations","PM25","Fire","Populated places","Coastline","Air zone"]
out_list = ["air_stations", "PM25", "Fires", "Cities", "Coastline", "Air_zone"]
i = 0
for x in path_list:
	a = doc_list[i]
	b = name_list[i]
	c = out_list[i]
	x = path_to_data + a
	print(str(x))
	print("Path is set for "+ str(b))
	if i <=1:
		arcpy.conversion.TableToTable(x, gdb_path, c)
	else:
		arcpy.conversion.FeatureClassToFeatureClass(x, gdb_path, c)
	i = i + 1

print("#################### Set up data to become usable #####################")
print("Table to table to become editable")
in_feature = "air_stations"
out_name = "air_stations_edit"
arcpy.conversion.TableToTable(in_feature, gdb_path, out_name)
print("Add LAT LONG field to air stations")
input = "air_stations_edit"
field_name_1 = "LAT"
field_name_2 = "LONG"
field_type = "DOUBLE"
field_is_nullable = "NULLABLE"
arcpy.management.AddFields(input,[[field_name_1, field_type], [field_name_2, field_type]])
#Update cursor to delete rows without latitude or longitude
print("Update cursor to delete rows without latitude or longitude")
with arcpy.da.UpdateCursor(input, ("LATITUDE", "LONGITUDE")) as cursor:
	for row in cursor:
		if row[0] == "N/A" or row[1] == "N/A":
			cursor.deleteRow()
#Calculate field
print("Convert lat long data into new fields")
expression = "!LATITUDE!"
exp_type = "PYTHON3"
arcpy.management.CalculateField(input, field_name_1, expression, exp_type )
expression = "!LONGITUDE!"
exp_type = "PYTHON3"
arcpy.management.CalculateField(input, field_name_2, expression, exp_type )
#input air station table into point features
print("Input air station table into point features")
output = "air_stations_xy_to_point"
x_coor = "LONG"
y_coor = "LAT"
z_coor = "HEIGHT_m_"
arcpy.management.XYTableToPoint(input, output, x_coor, y_coor, z_coor)
#project 
print("Align projection")
input = "air_stations_xy_to_point"
output = "air_staions_project"
coor_sys = "Air_zone"
arcpy.management.Project(input, output, coor_sys)
#select fires in 2017
print("Select fires in 2018")
input = "Fires"
output = "Fires_2018"
where_clause = 'FIRE_YEAR = 2018'
arcpy.analysis.Select(input, output, where_clause)
#Sort the fire data descendingly according to fire size
print("Sort the fire data descendingly according to fire size")
input = "Fires_2018"
output = "CURRENT_SI_descending"
field = [['CURRENT_SI','DESCENDING']]
arcpy.management.Sort(input, output, field)
#Search cursor to find the date and size of the largest fire
print("Search cursor to find the date and size of the largest fire")
input = "CURRENT_SI_descending"
date = "IGNITION_D"
size = "CURRENT_SI"
where = "OBJECTID_1 = 1" 
radius = 0
with arcpy.da.SearchCursor(input,(date, size), where) as cursor:
	for row in cursor:
		print("The date of the largest fire is "+str(row[0])+", with the size of "+str(row[1])+" hectares")
		print("Calculate the radius of fire with the size of "+str(row[1]))
		radius = math.sqrt((int(row[1])/100) / math.pi)
		print("Radius of the largest fire is "+ str(radius)+" kilometres")
#Select the largest fire in 2018
print("Select the largest fire in 2018")
input = "CURRENT_SI_descending"
output = "largest_fire"
where = "OBJECTID_1 = 1" 
arcpy.analysis.Select(input, output, where)
#create buffer as the same size of the fire
print("create buffer as the same size of the fire")
input = "largest_fire"
output = "fire_buffer"
buffer_r = str(radius) + " Kilometers"
arcpy.analysis.Buffer(input, output, radius,"","","")	
print("################### Set up PM 2.5 data #####################")
#Select PM25 data after 2017 07 07 
print("Select PM25 data between 2018 08 04")
input = "PM25"
output = "PM25_after_aug_4"
where = "DATE >= timestamp '2018-08-04 00:00:00'"
arcpy.analysis.TableSelect(input, output, where)
#Change station names in air stations table to uppercase
print("Change station names in air stations table to uppercase")
input = "air_staions_project"
field = "STATION_NAME"
expression = "!STATION_NAME!.upper()"
type = "PYTHON3"
arcpy.management.CalculateField(input,field,expression,type)
#join the station location to PM25 data
print("Join the station location to PM25 data")
input = "PM25_after_aug_4"
in_field = "STATION_NAME_FULL"
join_input = "air_staions_project"
join_field = "STATION_NAME"
out_fields = ['LAT','LONG']
arcpy.management.JoinField(input, in_field, join_input, join_field, out_fields)
#Convert table to point features
print("Convert table to point features")
in_table = "PM25_after_aug_4"
out_feature_class = "PM25_aug_4"
x_field = "LONG"
y_field = "LAT"
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field,"","" )
#Project the data as the Fire data
print("Align projection with the Air_zone data")
input = "PM25_aug_4"
output = "PM25_points"
reference = "Air_zone"
arcpy.management.Project(input, output, reference)
#Find the nearest city from air stations
print("Find the nearest city from air stations")
input = "PM25_points"
near = "Cities"
arcpy.analysis.Near(input,near)
#join the nearest city name and population to PM25 data
print("Join the nearest city name and population to PM25 data")
in_field = "NEAR_FID"
join_input = "Cities"
join_field = "OBJECTID_1"
out_fields = ['EST_POP','NAME']
arcpy.management.JoinField(input, in_field, join_input, join_field, out_fields)
#calculate distance of stations from coastline
print("Calculate distance of stations from coastline")
near = "Coastline"
arcpy.analysis.Near(input,near)
#Add field for classifying distance from coastline
print("Add field for classifying distance from coastline")
DisFromCoast = "QualiDis"
distance = "NEAR_DIST"
arcpy.management.AddField(input, DisFromCoast, "TEXT")
print("Classify distance from coastline to city")
with arcpy.da.UpdateCursor(input, (distance, DisFromCoast)) as cursor:
	for row in cursor:
		if row[0] <=10000:
			row[1] = "Close"
		elif row[0] > 10000 and row[0] <= 50000:
			row[1] = "Medium"
		else:
		    row[1] = "Far"
		cursor.updateRow(row)
	print("update complete")	
#Select records at 00:00 and delete null and negative values
print("Remove null value rows")
output = "PM25_24_00"
where = "TIME = '24:00' And RAW_VALUE IS NOT NULL And RAW_VALUE >= 0 And EST_POP IS NOT NULL"
arcpy.analysis.Select(input, output, where)
#Select the lower Fraser river air zone
print("Set up study area")
input = "Air_zone"
output= "LFR"
where = "Airzone = 'Lower Fraser Valley'"
arcpy.analysis.Select(input, output, where)
#intersect air stations with the lower Fraser river air zone
print("Limit to only air stations within study area")
input = ["LFR", "PM25_24_00"]
output = "LFR_PM25"
arcpy.analysis.Intersect(input, output)
#select close, medium, and far
print("Select close, medium, and far")
input = "LFR_PM25"
output = "close"
where = "QualiDis = 'Close'"
arcpy.analysis.Select(input, output, where)
input = "LFR_PM25"
output = "medium"
where = "QualiDis = 'Medium'"
arcpy.analysis.Select(input, output, where)
input = "LFR_PM25"
output = "far"
where = "QualiDis = 'Far'"
arcpy.analysis.Select(input, output, where)
#Search cursor
max_pop_close = 0
max_pop_medium = 0
max_pop_far = 0
max_name_close = ""
max_name_med = ""
max_name_far = ""
with arcpy.da.SearchCursor(input, ("OBJECTID", "NAME", "QualiDis","EST_POP")) as cursor:
	for row in cursor:
		if row[2] == "Close":
			if row[3] >= max_pop_close:
				max_pop_close = 0
				max_pop_close+=row[3]
				max_name_close = str(row[1])
		if row[2] == "Medium":
			if row[3] > max_pop_medium:
				max_pop_medium = 0
				max_pop_medium+=row[3]
				max_name_med = str(row[1])
		if row[2] == "Far":
			if row[3] > max_pop_far:
				max_pop_far = 0
				max_pop_far+=row[3]
				max_name_far = str(row[1])
	print("Highest population place that is close to the coast is "+str(max_name_close)+" with population of "+	str(max_pop_close))	
	print("Highest population place that is medium distance to the coast is "+str(max_name_med)+" with population of "+	str(max_pop_medium))			
	print("Highest population place that is far from the coast is "+str(max_name_far)+" with population of "+	str(max_pop_far))	
#Find city with population similar to Cloverdale
pop_clover = max_pop_medium
close_city = ""
close_city_pop = ""
med_city = max_name_med
med_city_pop = max_pop_medium
far_city = ""
far_city_pop = ""
with arcpy.da.SearchCursor(input, ("OBJECTID", "NAME", "QualiDis","EST_POP")) as cursor:
	for row in cursor:
		if row[2] == "Close":
			if row[3] <= pop_clover* 1.1 and row[3] >= pop_clover* 0.7:
				close_city = row[1]
				close_city_pop = row[3]
		if row[2] == "Far":
			if row[3] <= pop_clover* 1.1 and row[3] >= pop_clover* 0.7:
				far_city = row[1]
				far_city_pop = row[3]
			else:
				far_city = max_name_far
				far_city_pop = max_pop_far
	print("Close: " + str(close_city)+","+str(close_city_pop))
	print("Medium: " + str(med_city)+","+str(med_city_pop))
	print("Far: " + str(far_city)+","+str(far_city_pop))
#Select the 3 cities
input = "PM25_24_00"
output = "cities_3"
where = " NAME = 'Chilliwack' Or NAME = 'Cloverdale' Or NAME = 'North Vancouver'"
arcpy.analysis.Select(input, output, where)
#Find the date with PM25 over 100
with arcpy.da.SearchCursor(input, ("NAME", "ROUNDED_VALUE", "DATE_PST")) as cursor:
	for row in cursor:
		if row[0] == "North Vancouver":
			if row[1] >= 100:
				print("On " + str(row[2])+ " PM2.5 value was over 100 in North Vancouver")
		if row[0] == "Cloverdale":
			if row[1] >= 100:
				print("On " + str(row[2])+ " PM2.5 value was over 100 in Cloverdale")
		if row[0] == "Chilliwack":
			if row[1] >= 100:
				print("On " + str(row[2])+ " PM2.5 value was over 100 in Chilliwack")
				
#Find the residence time of PM25 reaching 1, 5, and 10 in selected cities
input = "PM25_24_00"
threshold = [1, 1, 1, 5, 5, 5, 10, 10, 10]
city_list = ["North Vancouver", "Cloverdale", "Chilliwack", "North Vancouver", "Cloverdale", "Chilliwack", "North Vancouver", "Cloverdale", "Chilliwack"]
i = 0
for item in threshold:
	a = city_list[i]
	i = i + 1
	where = "DATE_PST >= timestamp '2018-08-23 00:00:00' And NAME = '"+str(a)+"'"
	count = 0
	with arcpy.da.SearchCursor(input, ("NAME", "ROUNDED_VALUE", "DATE_PST"), where) as cursor:
		for row in cursor:
			if row[1] > item:
				count += 1
			else:
				print(str(row[1]))
				print(str(row[2]))
				print("Residence time taken for PM 2.5 value to reach "+ str(item) +" in "+str(a)+" is "+ str(count)+ " days")
				break
print("##################Create IDW interpolation#####################")
print("IDW for August 23 (Peak)")
where = "DATE_PST = timestamp '2018-08-23 00:00:00'"
input = "PM25_24_00"
output = "PM25_aug23"
arcpy.analysis.Select(input, output, where)
input = "PM25_aug23"
field = "ROUNDED_VALUE"
cell_size = 700
arcpy.env.mask = "LFR"
idw_out = arcpy.sa.Idw(input, field, cell_size , "", "","")
idw_out.save(gdb_path+r"\idw_aug23")
print("IDW for August 25 ")
where = "DATE_PST = timestamp '2018-08-25 00:00:00'"
input = "PM25_24_00"
output = "PM25_aug25"
arcpy.analysis.Select(input, output, where)
input = "PM25_aug25"
field = "ROUNDED_VALUE"
cell_size = 700
arcpy.env.mask = "LFR"
idw_out = arcpy.sa.Idw(input, field, cell_size , "", "","")
idw_out.save(gdb_path+r"\idw_aug25")
print("IDW for August 30")
where = "DATE_PST = timestamp '2018-08-30 00:00:00'"
input = "PM25_24_00"
output = "PM25_aug31"
arcpy.analysis.Select(input, output, where)
input = "PM25_aug31"
field = "ROUNDED_VALUE"
cell_size = 700
arcpy.env.mask = "LFR"
idw_out = arcpy.sa.Idw(input, field, cell_size , "", "","")
idw_out.save(gdb_path+r"\idw_aug31")
print("IDW for October 3 ")
where = "DATE_PST = timestamp '2018-10-03 00:00:00'"
input = "PM25_24_00"
output = "PM25_oct3"
arcpy.analysis.Select(input, output, where)
input = "PM25_oct3"
field = "ROUNDED_VALUE"
cell_size = 700
arcpy.env.mask = "LFR"
idw_out = arcpy.sa.Idw(input, field, cell_size , "", "","")
idw_out.save(gdb_path+r"\idw_oct3")
print("All tasks completed")
###########################################################
