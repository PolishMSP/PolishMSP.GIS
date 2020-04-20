
print("Loading ArcGIS libraries...    ")
import sys
import os
import shutil
import arcpy
print("Loaded. \n")


#region Script parameters

script_dir = os.path.dirname(os.path.abspath(__file__))
gdb = os.path.join(script_dir, "PolishMSP.gdb")


if len(sys.argv) > 1:
    gdb = sys.argv[1]
else:
    print("MSP Geodatabase was not specified. Default file geodatabase used: ")
    print(gdb)


if not os.path.exists(gdb):
    print("Specified MSP Geodatabase does not exists.")
    print(gdb)
    exit(2)

#endregion


print("Loading feature class and table list...")
arcpy.env.workspace = gdb
gdb_info = arcpy.Describe(gdb)
is_egdb = gdb_info.workspaceType == "RemoteDatabase" and gdb_info.workspaceFactoryProgID == "esriDataSourcesGDB.SdeWorkspaceFactory.1" 


def init_msp_recordset(rs_info):
    print("- " + rs_info.name + ":")

    if rs_info.editorTrackingEnabled:        
        pass
        # Editor tracing is set automatically during importing DbSchema.xml
        # print("  (Editor tracking was already enabled)")
    else:
        print("  WARNING: Editor tracking is not enabled")
        
    if not is_egdb:
        print("  WARNING: Versioning is not supported")
        print("  WARNING: Archiving is not supported")
        return

    if rs_info.isVersioned:
        print("  (Already registered as versioned)")
    elif rs_info.isArchived:
        print("  WARNING: Versioning cannot be set on archived " + rs_info.datasetType)
    else:
        arcpy.RegisterAsVersioned_management(rs_info.name)
        print("  Registered as versioned")

    if rs_info.isArchived:
        print("  (Archiving already enabled)")
    else:
        arcpy.EnableArchiving_management(rs_info.name)        
        print("  Archiving enabled")

    print("")


#region Run script

for fc in arcpy.ListFeatureClasses():
    fc_info = arcpy.Describe(fc) 
    if fc_info.datasetType == "FeatureClass":
        init_msp_recordset(fc_info)


for tb in arcpy.ListTables():
    tb_info = arcpy.Describe(tb) 
    init_msp_recordset(tb_info)


print("")
print("Finished.")

#endregion