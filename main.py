"""
Script: reollcect Waste Collection Pickup Day application data import and update process
Purpose: Import recollect collection day map application with consitently updated data after new parcels are assigned
a pickup day by recollect
Author: Jeff Long
"""
try:
    import arcpy, os, traceback, sys
    from collections import defaultdict
    from start_stop_mapservice import stopStartServices
    from utils import automated_emails
except Exception as e:
    print e


def email(x): automated_emails.auto_email(["Jeff.Long@apexnc.org"], subject="ERROR DETECTED: Recollect Data "
                                                                            "Import/Ovewrite/Dataupload"
                                                                            "Script", text=str(x))


arcpy.env.overwriteOutput = 1
arcpy.Delete_management("in_memory")
out_direct = r"C:\GIS-Long\REQUESTS\PWT\WasteIndustries_MapApplication_pickup_days\test_output"
pub_db =r"C:\Users\Jlong\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\APEXPUBLISHER_jlong.sde"
arcpy.env.workspace = pub_db

par_csv = r"C:\GIS-Long\REQUESTS\PWT\WasteIndustries_MapApplication_pickup_days\gis_data\parcels-105479.csv"

# SDE FEATURE CLASSES
pub_sde_db_form = r"C:\Users\Jlong\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\APEXPUBLISHER.sde\APEXPUBLISHER" \
                  r".DBO.{}"

apxsubdivs = r'C:\Users\Jlong\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\APEXPL.sde\APEXPL.PL.Subdivisions\APEXPL.PL' \
             r'.ApexDevelopment_Residential'

apx_clipper = r'C:\Users\Jlong\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\APEXWCD.sde\APEXWCD.WCD.WakeCountyApex' \
              r'\APEXWCD.WCD.apex_clipper'

# IN MEMORY FEATURECLASSES FOR FASTER RUNTIME PERFORMANCE
tempfc_subs = r'in_memory\recollect_subdivisions'
arcpy.FeatureClassToFeatureClass_conversion(apxsubdivs, os.path.dirname(tempfc_subs), os.path.basename(
    tempfc_subs))

# GLOBAL DICTIONARY STORES
days_dict = {'Mon': 'Monday', 'Wed':'Wednesday','Fri': 'Friday','Tue': 'Tuesday', 'Thu': 'Thursday'}
data_dict = {}
assign_dict = {}

# APEXGIS SERVER PARAMETERS
server = r'apexgis'
port='6080'
adminUser='siteadmin'
adminPass='apexGIS1'

try:
    stopStartServices(server= server, port=port ,adminUser=adminUser, adminPass=adminPass,
                      stopStart='Stop',serviceList=['RecollectApplicationData/Recollect.MapServer'])
except Exception as e:
    tb = traceback.format_exc()
    email(tb)
    raise sys.exit()


def correct_subnames(subdivs):

    changes_subs = {"Crockett's Ridge": "Crocketts Ridge", "Grey's Landing": "Greys Landing",
                    "Hunter's Ridge": "Hunters Ridge",
                    "Riley's Pond": "Rileys Pond", "Seagrove's Farm": "Seagroves Farm"}
    try:
        with arcpy.da.UpdateCursor(subdivs, ['Class']) as ucur:
            for row in ucur:
                print row[0]
                if row[0] in changes_subs.keys():
                    print row[0], changes_subs[row[0]]
                    row[0] = changes_subs[row[0]]
                    ucur.updateRow(row)

    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()


def assign_pickup_day (subdivs, coll_grid):
    correct_subnames(subdivs)


    arcpy.MakeFeatureLayer_management(subdivs,"sub_lyr")
    arcpy.SelectLayerByLocation_management("sub_lyr", "INTERSECT", coll_grid, selection_type='NEW_SELECTION')
    sub_names_list = [row[0] for row in arcpy.da.SearchCursor("sub_lyr", ['Class'])]


    try:
        arcpy.AddField_management(subdivs, "ClctDay", "TEXT")
        arcpy.AddField_management(coll_grid, "ClctDay", "TEXT")
        arcpy.MakeFeatureLayer_management(subdivs, "SubDivs")
        arcpy.MakeFeatureLayer_management(coll_grid, "RecGrid")

    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()

    try:
        with arcpy.da.UpdateCursor(coll_grid, ['Recycling', 'ClctDay']) as ucur:
            for row in ucur:
                if row[0] in days_dict.keys():
                    row[1] = days_dict[row[0]]
                    ucur.updateRow(row)
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()


    #print sub_names_list
    for sub_name in sorted(sub_names_list):
        #print str(sub_name), type(sub_name)
        try:
            day_dict = defaultdict(int)
            arcpy.SelectLayerByAttribute_management("SubDivs", "NEW_SELECTION", "\"Class\" = '{}'".format(sub_name) )
            #print [row[0] for row in arcpy.da.SearchCursor("SubDivs", ['Class'])]

            arcpy.SelectLayerByLocation_management("RecGrid", "INTERSECT", "SubDivs", selection_type='NEW_SELECTION')
            count = int(arcpy.GetCount_management("RecGrid").getOutput(0))
        except Exception as e:
            tb = traceback.format_exc()
            email(tb)
            raise sys.exit()

        print sub_name, "-----", [row[0] for row in arcpy.da.SearchCursor("RecGrid", ['Street'])], count

        print [f.name for f in arcpy.ListFields("RecGrid")]

        try:
            with arcpy.da.SearchCursor("RecGrid", ['ClctDay']) as scur:
                for row in scur:

                    day_dict[row[0]] += 1

            for k, v in day_dict.items():

                print k, v

        except Exception as e:
            tb = traceback.format_exc()
            email(tb)
            raise sys.exit()

        v = list(day_dict.values())
        k = list(day_dict.keys())
        print k
        print v
        try:

            major_day = k[v.index(max(v))] if v.index(max(v)) else 0
            print "MAJOR DAYYYYYYYYYY", major_day, type(major_day)

            assign_dict[str(sub_name)] = str(major_day)

        except Exception as e:
            tb = traceback.format_exc()
            email(tb)
            raise sys.exit()

    for k, v in assign_dict.items():
        print type(k), k, type(v), v

    return assign_dict


def attrib_collect(subdivs, results):

    try:
        with arcpy.da.UpdateCursor(subdivs, ["Class", "ClctDay"]) as ucur:
            for row in ucur:
                print type(row[0])
                if row[0] in results.keys():
                    row[1] = str(results[str(row[0])])
                    ucur.updateRow(row)
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()


def convert_csv_shp(in_csv):

    try:
        sr = 4269
        CoordSys = arcpy.SpatialReference(sr)

        out_Layer = "parcels_waste_lyr"
        arcpy.MakeXYEventLayer_management(in_csv, "Longitude", "Latitude", out_Layer, CoordSys)

        tempfc_par= r'in_memory\pars'
        arcpy.Select_analysis("parcels_waste_lyr", tempfc_par)

        tempfc_rec = r'in_memory\recyclegrid'
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()

    try:
        arcpy.MakeFeatureLayer_management(tempfc_par, 'parclean_lyr')
        arcpy.SelectLayerByLocation_management('parclean_lyr', 'INTERSECT', select_features=apx_clipper)
        arcpy.Select_analysis('parclean_lyr', tempfc_rec)
        data_dict["rec_mem_fc"] = tempfc_rec
        #yield days_dict["rec_mem_fc"]
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()


def main():
    try:
        convert_csv_shp(par_csv)
        correct_subnames(tempfc_subs)
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()

    try:
        func_results = assign_pickup_day(tempfc_subs, data_dict["rec_mem_fc"])
        attrib_collect(tempfc_subs, func_results)

        arcpy.FeatureClassToShapefile_conversion(data_dict["rec_mem_fc"],out_direct)
        arcpy.CopyFeatures_management(data_dict["rec_mem_fc"], pub_sde_db_form.format('recollect_parcels'))
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()

    try:
        arcpy.CopyFeatures_management(tempfc_subs, pub_sde_db_form.format('recollect_subdivisions'))

        stopStartServices(server=server, port=port, adminUser=adminUser, adminPass=adminPass, stopStart='Start',
                          serviceList=['RecollectApplicationData/Recollect.MapServer'])

        # CLEARING CACHED RUNTIME EXECUTION IN MEMORY FILES
        arcpy.Delete_management("in_memory")

        automated_emails.auto_email(["Jeff.Long@apexnc.org"], subject="SCRIPT COMPLETED: Recollect Data "
                                                                            "Import/Ovewrite/Dataupload"
                                                                             "Script"
                                    , text="Recollect Map Application Data Upload script "
                                           "has successfully completed "
                                           "without errors and is ready for REST service consumption")

        raise sys.exit()
    except Exception as e:
        tb = traceback.format_exc()
        email(tb)
        raise sys.exit()


if __name__ =="__main__":
    main()