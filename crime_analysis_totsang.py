#Task 4
#Question 1
#Create new work space
out_folder_path = r"Z:\Lab_2\Lab_2\Lab_2_a"
out_name = "Lab2.gdb"
arcpy.CreateFileGDB_management(out_folder_path, out_name)
#Move to the new work space
arcpy.env.workspace = "Z:\\Lab_2\\Lab_2\\Lab_2_a\\Lab_2.gdb"
#Intersect park and crime data
intersect_input = ["park", "crime"]
intersect_output = "crime_in_park"
arcpy.analysis.Intersect(intersect_input, intersect_output)
#Get Count
arcpy.management.GetCount(intersect_output)
<Result '2098'>



#Question 2
#Select workspace
arcpy.env.workspace = r"Z:\Lab_2\Lab_2\Lab_2_a\Lab_2.gdb"
#Select property crime in 2016
in_feature = "crime"
out_feature = "propcrime_2016"
where_clause = "date_incid >= timestamp '2016-01-01' And date_incid <= timestamp '2016-12-31' And parent_inc = 'Property Crime'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#Select Oaklands, Fernwood, and North/South Jubilee neighbourhoods
in_feature = "neighbourhood"
out_feature = "neigh_OFNS"
where_clause = "Neighbourh = 'Oaklands' Or Neighbourh = 'Fernwood' Or Neighbourh = 'North Jubilee' Or Neighbourh = 'South Jubilee'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#Intersect park with neighOFNS
intersect_in = ["park", "neigh_OFNS"]
intersect_out = "parks_in_OFNS"
arcpy.analysis.Intersect(intersect_in, intersect_out)
#create 500m buffer for parks_in_OFNS
input = "parks_in_OFNS"
output = "ofnspark_500m"
distance = "500 meters"
arcpy.Buffer_analysis(input, output, distance, 'FULL', 'ROUND', 'ALL')
#Intersect propcrime_2016 with ofnspark_500m]
input = ["propcrime_2016", "ofnspark_500m"]
output = "crime_in_500m"
arcpy.analysis.Intersect(input, output)
#Get Count
arcpy.management.GetCount(output)
<Result '282'>



#Question 3
#Select workspace
arcpy.env.workspace = r"Z:\Lab_2\Lab_2\Lab_2_a\Lab_2.gdb"
#Select drug, liquor, and disorder crime
in_feature = "crime"
out_feature = "drug_liq_dis"
where_clause = "parent_inc = 'Drugs' Or parent_inc = 'Disorder' Or parent_inc = 'Liquor'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#Select drug, liquor, and disorder crime in 2017
in_feature = "drug_liq_dis"
out_feature = "drug_liq_dis_2017"
where_clause = "date_incid >= timestamp '2017-01-01' And date_incid <= timestamp '2017-12-31'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#Select neighbourhood except Victoria West
in_feature = "neighbourhood"
out_feature = "neigh_noVW"
where_clause = "Neighbourh <> 'Victoria West'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#intersect drug_liq_dis_2017 crime with neighbourhood exccept Victoria West
in_intersect = ["drug_liq_dis_2017", "neigh_noVW"]
out_intersect = "drug_liq_dis_2017_in_neigh_noVW"
arcpy.analysis.Intersect(in_intersect, out_intersect)
#500 meters buffer for all schools
input = "school"
output = "school_500m"
distance = "500 meters"
arcpy.Buffer_analysis(input, output, distance, 'FULL', 'ROUND', 'ALL')
#Intersect drug_liq_dis_2017_in_neigh_noVW with 500m buffer
input = ["drug_liq_dis_2017_in_neigh_noVW", "school_500m"]
output = "crime2017_noVW_in_500m_school"
arcpy.analysis.Intersect(input, output)
#Get Count
arcpy.management.GetCount(output)
<Result '778'>



#Question 4
#Select workspace
arcpy.env.workspace = r"Z:\Lab_2\Lab_2\Lab_2_a\Lab_2.gdb"
#Select property crime in 2017
in_feature = "crimes"
out_feature = "propcrime_2017"
where_clause = "date_incid >= timestamp '2017-01-01' And date_incid <= timestamp '2017-12-31' And parent_inc = 'Property Crime'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#parks_in_OFNS was already created previously
input = "parks_in_OFNS"
output = "ofnspark_100m"
distance = "100 meters"
arcpy.Buffer_analysis(input, output, distance, 'FULL', 'ROUND', 'ALL')
#Intersect propcrime_2017 with 100m buffer
input = ["propcrime_2017", "ofnspark_100m"]
output = "crime_in_100m"
arcpy.analysis.Intersect(input, output)
#Get Count
arcpy.management.GetCount(output)
<Result '50'>



#Question 5
#drug, liquor, and disorder crime has already been selected previously
#Select drug, liquor, and disorder crime in 2015
in_feature = "drug_liq_dis"
out_feature = "drug_liq_dis_2015"
where_clause = "date_incid >= timestamp '2015-01-01' And date_incid <= timestamp '2015-12-31'"
arcpy.analysis.Select(in_feature, out_feature, where_clause)
#neighbourhood except Victoria West has been created previously
#Intersect drug_liq_dis_2015 with neighOFNS
intersect_in = ["drug_liq_dis_2015", "neigh_noVW"]
intersect_out = "crime2015_in_neigh_noVW"
arcpy.analysis.Intersect(intersect_in, intersect_out)
#100 meters buffer for all schools
input = "school"
output = "school_100m"
distance = "100 meters"
arcpy.Buffer_analysis(input, output, distance, 'FULL', 'ROUND', 'ALL')
#Intersect drug_liq_dis_2017 with 100m buffer
input = ["crime2015_in_neigh_noVW", "school_100m"]
output = "crime2017_noVW_in_100m_school"
arcpy.analysis.Intersect(input, output)
#Get Count
arcpy.management.GetCount(output)
<Result '156'>



#Task 5
#Create new gdb
out_folder_path = r"Z:\Lab_2\Lab_2\Lab_2_b"
out_name = "q5.gdb"
arcpy.CreateFileGDB_management(out_folder_path, out_name)
#Set workspace
arcpy.env.workspace = r"Z:\Lab_2\Lab_2\Lab_2_b\q5.gdb"
#Copy the original data so that you don't have to re-download it if messed up
input = r"Z:\Lab_2\Data\crime\geo_export_6ec860a6-7175-41d9-8195-13bc0f93ba9e.shp"
output = "crimes.shp"
arcpy.management.Copy(input, output)
#Select crime in 2018
in_select = "crimes"
out_select = "crimes_2018"
where_clause = "date_incid >= timestamp '2018-01-01' And date_incid <= timestamp '2018-12-31'"
arcpy.analysis.Select(in_select, out_select, where_clause)
#Copy the original data so that you don't have to re-download it if messed up
input = r"Z:\Lab_2\Data\neighbourhood\Neighbourhood_Boundaries.shp"
output = "neighbourhood.shp"
arcpy.management.Copy(input, output)
#Create new workspace for split output
out_folder_path = r"Z:\Lab_2\Lab_2\Lab_2_b"
out_name = "q5_split.gdb"
arcpy.CreateFileGDB_management(out_folder_path, out_name)
#Split neighbourhood
in_feature = "neighbourhood"
split_feature = "neighbourhood"
split_field = "Neighbourh"
out = r"Z:\Lab_2\Lab_2\Lab_2_b\q5_split.gdb"
arcpy.analysis.Split(in_feature, split_feature, split_field, out)
#Move to new workspace
arcpy.env.workspace = r"Z:\Lab_2\Lab_2\Lab_2_b\q5_split.gdb"
#Create a list for all feature classes
split_list = arcpy.ListFeatureClasses()
for item in split_list:
	#Intersect splited neighbourhood with crimes
	print(item)
	intersect_in = [item, "crimes_2018"]
	intersect_out = "cri_in_" + item
	arcpy.analysis.Intersect(intersect_in, intersect_out)
	#Frequency	
	print("check1")
	in_table = "cri_in_" + item
	out_table = r"Z:\Lab_2\Lab_2\Lab_2_b\q5_freq.gdb\freq_" + item
	frequency_fields = "parent_inc"
	arcpy.analysis.Frequency(in_table, out_table, frequency_fields,)
	#Table Select	
	print("check2")
	in_table = "freq_" + item
	out_table = item + '_count'
	where_clause = "parent_inc='Property Crime' Or parent_inc = 'Drugs' Or parent_inc='Theft' Or parent_inc = 'Assault' Or parent_inc ='Liquor'"
	arcpy.analysis.TableSelect(in_table, out_table, where_clause)
	#Table to Table
	print("check3")
	in_table = item +'_count'
	out_path = r"Z:\Lab_2\Lab_2\Lab_2_b\excel"
	name = item + '_final.csv'
	arcpy.conversion.TableToTable(in_table, out_path, name)


	
#Task 6
#create new gdb
out_folder_path = "Z:\\Lab_2\\Lab_2\\Lab_2"
out_name = "q7.gdb"
arcpy.CreateFileGDB_management(out_folder_path, out_name)
#move to new workspace
arcpy.env.workspace = "Z:\\Lab_2\\Lab_2\\Lab_2\\q7.gdb"
#create list
robbery_day = [0,0,0,0,0,0,0]
assault_day = [0,0,0,0,0,0,0]
property_crime_day = [0,0,0,0,0,0,0]
theft_vehicle_day = [0,0,0,0,0,0,0]
theft_day = [0,0,0,0,0,0,0]
#create a add count with searchCur
columns = ['day_of_wee', 'parent_inc']
curObj = arcpy.da.SearchCursor('Z:\Lab_2\Data\crime\crime.shp', columns)
for row in curObj:
#robbery list
	if row[1] =='Robbery':
		if row[0] =='Monday':
			robbery_day[0]= robbery_day[0] + 1
		elif row[0] =='Tuesday':
			robbery_day[1]= robbery_day[1] + 1
		elif row[0] =='Wednesday':
			robbery_day[2]= robbery_day[2] + 1
		elif row[0] =='Thursday':
			robbery_day[3]= robbery_day[3] + 1
		elif row[0] =='Friday':
			robbery_day[4]= robbery_day[4] + 1
		elif row[0] =='Saturday':
			robbery_day[5]= robbery_day[5] + 1
		elif row[0] =='Sunday':
			robbery_day[6]= robbery_day[6] + 1
#assault list
	elif row[1] =='Assault':
		if row[0] =='Monday':
			assault_day[0]= assault_day[0] + 1
		elif row[0] =='Tuesday':
			assault_day[1]= assault_day[1] + 1
		elif row[0] =='Wednesday':
			assault_day[2]= assault_day[2] + 1
		elif row[0] =='Thursday':
			assault_day[3]= assault_day[3] + 1
		elif row[0] =='Friday':
			assault_day[4]= assault_day[4] + 1
		elif row[0] =='Saturday':
			assault_day[5]= assault_day[5] + 1
		elif row[0] =='Sunday':
			assault_day[6]= assault_day[6] + 1
#property crime list
	elif row[1] =='Property Crime':
		if row[0] =='Monday':
			property_crime_day[0]= property_crime_day[0] + 1
		elif row[0] =='Tuesday':
			property_crime_day[1]= property_crime_day[1] + 1
		elif row[0] =='Wednesday':
			property_crime_day[2]= property_crime_day[2] + 1
		elif row[0] =='Thursday':
			property_crime_day[3]= property_crime_day[3] + 1
		elif row[0] =='Friday':
			property_crime_day[4]= property_crime_day[4] + 1
		elif row[0] =='Saturday':
			property_crime_day[5]= property_crime_day[5] + 1
		elif row[0] =='Sunday':
			property_crime_day[6]= property_crime_day[6] + 1
#theft list			
	elif row[1] =='Theft':
		if row[0] =='Monday':
			theft_day[0]= theft_day[0] + 1
		elif row[0] =='Tuesday':
			theft_day[1]= theft_day[1] + 1
		elif row[0] =='Wednesday':
			theft_day[2]= theft_day[2] + 1
		elif row[0] =='Thursday':
			theft_day[3]= theft_day[3] + 1
		elif row[0] =='Friday':
			theft_day[4]= theft_day[4] + 1
		elif row[0] =='Saturday':
			theft_day[5]= theft_day[5] + 1
		elif row[0] =='Sunday':
			theft_day[6]= theft_day[6] + 1		
#theft from vehicle list
	elif row[1] =='Theft from Vehicle':
		if row[0] =='Monday':
			theft_vehicle_day[0]= theft_vehicle_day[0] + 1
		elif row[0] =='Tuesday':
			theft_vehicle_day[1]= theft_vehicle_day[1] + 1
		elif row[0] =='Wednesday':
			theft_vehicle_day[2]= theft_vehicle_day[2] + 1
		elif row[0] =='Thursday':
			theft_vehicle_day[3]= theft_vehicle_day[3] + 1
		elif row[0] =='Friday':
			theft_vehicle_day[4]= theft_vehicle_day[4] + 1
		elif row[0] =='Saturday':
			theft_vehicle_day[5]= theft_vehicle_day[5] + 1
		elif row[0] =='Sunday':
			theft_vehicle_day[6]= theft_vehicle_day[6] + 1	
#print result
print("Assault")			
print(assault_day)
print("Robbery")
print(robbery_day)
print("Property_Crime")
print(property_crime_day)
print("Theft")
print(theft_day)
print("Theft_From_Vehicle")
print(theft_vehicle_day)

#result
Assault
[332, 361, 345, 416, 482, 526, 489]
Robbery
[120, 93, 98, 107, 133, 109, 114]
Property_Crime
[1388, 1268, 1228, 1211, 1324, 1367, 1219]
Theft
[3202, 3351, 3231, 3288, 3201, 2885, 2755]
Theft_From_Vehicle
[1828, 1790, 1589, 1525, 1514, 1277, 1306]