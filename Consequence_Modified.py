from Simple_CSV_updated import SimpleCSV

csv = SimpleCSV()

csv.set_work_dir("C:\\Path\\to\\Working\\Directory\\")

csv.read_csv("WaterMains_Attribute_Table.csv") # will need to replace this with the name of the updated watermains attribute table once downloaded.

# Create variables for factors by calling their field names
Prov_Signif_Areas = csv.return_column(column="Type", type= "Text") 
Trails = csv.return_column(column="CrossTrail", type= "Text")
Landuse = csv.return_column(column="Landuse", type= "Text")
Waterways = csv.return_column(column="Thru_Water", type="Text")
pipeDiameter = csv.return_column(column="DIAMETER_m")
Railways = csv.return_column(column="Cross_Rail", type= "Text")


FactorList = ["Type", "CrossTrail", "Landuse", "Thru_Water", "DIAMETER_m", "Cross_Rail"], #check that these are right- these are the field names for the columns needed.


# RESCALE EVERYTHING
Prov_Signif_Areas_List= ["Other", "Provincially_Significant"]
Prov_Signif_Areas_rescale = csv.math_rescale_categorical(Prov_Signif_Areas, Prov_Signif_Areas_List, new_min=0,new_max=100) # notice that now the functions take the lists you previously grabbed, instead of acting directly on columns

Trails_List= ["No","Yes"]
Trails_rescale= csv.math_rescale_categorical(Trails, Trails_List, new_min=0,new_max=100)


Railways_List= ["No","Yes"]
railways_rescale = csv.math_rescale_categorical(Railways, Railways_List, new_min=0,new_max=100) 
Waterways_List= ["No","Yes"]
Waterways_rescale = csv.math_rescale_categorical(Waterways, Waterways_List, new_min=0,new_max=100)
# alter the max (and maybe the min) to suit the condition. The lower the max, the higher the rescaled value (the more important it is)
# For example, if a pipe material, say PVC, was more important, set the max lower than the other factors.
# also, the 100 in each equation represents the new scale. Set this to whatever you want to chance the scale.

Landuse_rescale = []
for val in Landuse:
    if val == "Residential" or val == "OpenSpace" or val== "Other":
        Landuse_rescale.append(0)
    elif val == "CorridorCommercial" or val == "NeighbourhoodCommercial" or val == "Industrial" or val == "MajorInstitutional":
        Landuse_rescale.append(50)
    elif val == "DowntownCore":
        Landuse_rescale.append(75)
    elif val == "Hospital20mBuff":
        Landuse_rescale.append(100)


pipeDiameter_rescale = [] #anything 400mm or greater is bad
for val in pipeDiameter:
    if val >= 400:
        pipeDiameter_rescale.append(100)
    if val < 400:
        pipeDiameter_rescale.append(0)


# Weightings!
all_criteria_not_weighted = [Trails_rescale, railways_rescale, Waterways_rescale, Landuse_rescale, Prov_Signif_Areas_rescale, pipeDiameter_rescale] # this list holds all the lists of criteria
weights = [0.0318,0.3495,0.2276,0.1660,0.0431,0.1820] #the weights need to be defined in the same order that the criteria were added to the list above


# Significant Environmental Areas = 0.0431
# Trails = 0.0318
# Land Use = 0.1660
# Waterways = 0.2276
# Pipe Diameter = 0.1820
# Railways = 0.3495

# Calculate scores from weighted sum
all_weighted_criteria = [] # we make a new list that will hold all of the other lists of criteria data once we've weighted them. You'll see why in a moment.

for i in range(len(all_criteria_not_weighted)):
    weighted = csv.math_multiply(vals = all_criteria_not_weighted[i],spec_value=weights[i]) # we multiply each unweighted criteria by its corresponding weight in the weights list
    all_weighted_criteria.append(weighted) # then we add the new weighted criteria to the list of all weights


criteria_sum = csv.math_add(all_weighted_criteria) #so this produces a new list which is the addition of each row of each of the weighted criteria in the all_weighted_criteria list
print(criteria_sum)
# if you also have constraints, you will need to multiply these by the criteria. For now I think you just have pipe diameter, but if there's more add them to this list too


# finally, we can add the full MCE score to the CSV
csv.append_column(criteria_sum,"MCE Consequence Score")

csv.write_csv("Consequence_MCE_Output_FINAL") # write the final file. Notice that none of the changes you've made so far are saved in the real file until you write it to a file here