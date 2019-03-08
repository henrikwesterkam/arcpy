import arcpy
import os

from timeit import default_timer as timer
start = timer()

arcpy.env.overwriteOutput = True

# defining variables
variable = "air_temperature"
x_dimension = "lon"
y_dimension = "lat"
out_feature = "temp_file"
band_dimension = ""
dimension = "day"
valueSelectionMethod = "BY_VALUE"
mask = r"D:\State.shp" # Whatever you want to mask your extraction by
temp_name = r"in_memory\proj_temp" # Stores intermediate files as temporary

outLoc = r"D:\Min_AirTemp_out\\" # Directory to extract files to
directory = r"C:\Min_AirTemp\\" # Directory where your NetCDFs are


index_list = range(0, 365, 1) # regular year
index_leap = range(0, 366, 1) # leap year

for filename in os.listdir(directory):
    print filename
    year = filename[3:7]
    if year == "2004" or year == "2008" or year == "2012" or year == "2016":
        print "leapyear"
        index = index_leap
        print index
    else:
        print "regular"
        index = index_list
        print index

    inNetCDF = directory + filename
    print inNetCDF

    nc_FP = arcpy.NetCDFFileProperties(inNetCDF)

    for i in index:
        print i
        print nc_FP.getDimensionValue(dimension, i)

        # extract the layer from the NetCDF
        dimension_values = nc_FP.getDimensionValue(dimension, i)
        dvl = [dimension, dimension_values]
        dimension_values = [dvl]
        arcpy.MakeNetCDFRasterLayer_md(inNetCDF, variable, x_dimension, y_dimension,
                                       out_feature, band_dimension, dimension_values,
                                       valueSelectionMethod)

        # rename the ouput correctly
        outdate = str(nc_FP.getDimensionValue(dimension, i))
        outdate = outdate.replace("/", "_")
        year = outdate[-4:]
        day = str(i + 1)
        outname = outLoc + variable + "_" + year + "_" + day + ".img"  # change this
        print outname

        # project raster
        out_coord_sys = arcpy.SpatialReference("NAD 1983 StatePlane Montana FIPS 2500 (Meters)")
        arcpy.ProjectRaster_management(out_feature, temp_name, out_coord_sys)

        # clip raster to Montana
        arcpy.CheckOutExtension("Spatial")
        outExtractByMask = arcpy.sa.ExtractByMask(temp_name, mask)

        arcpy.CopyRaster_management(outExtractByMask, outname, "", "", "", "NONE", "NONE", "")
        end = timer()
        print(end - start)

end = timer()
print(end-start)