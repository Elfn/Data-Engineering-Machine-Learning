import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *


#----------------------------------------------EXTRACTION-------------------------------------


# Configure spark session
spark = SparkSession.builder.master('local[2]').appName('quake_etl').config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1').getOrCreate()

# Load the dataset "database.csv"
df_load = spark.read.csv(r"/Users/Elimane/SPARK/data/database.csv", header=True)

#Drop fields we don't need from df_load
lst_dropped_columns = ['Depth Error', 'Time', 'Depth Seismic Stations','Magnitude Error','Magnitude Seismic Stations','Azimuthal Gap', 'Horizontal Distance','Horizontal Error',
    'Root Mean Square','Source','Location Source','Magnitude Source','Status']
df_load = df_load.drop(*lst_dropped_columns)

# Create year fields and add it to dataframe
df_load = df_load.withColumn('Year', year(to_timestamp('Date', 'dd/MM/yyyy')))


#Build the quake frequency dataframe using the year field
df_quake_freq = df_load.groupBy('Year').count().withColumnRenamed('count', 'Count')

#----------------------------------------------TRANSFORMATION-------------------------------------
# Cast some fields from string into numeric types

df_load = df_load.withColumn('Latitude', df_load['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_load['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_load['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_load['Magnitude'].cast(DoubleType()))

# Create avg magnitude and max magnitude fields and add to df_quake_freq
df_max = df_load.groupBy('Year').max('Magnitude').withColumnRenamed('max(Magnitude)', 'Max_Magnitude')
df_avg = df_load.groupBy('Year').avg('Magnitude').withColumnRenamed('avg(Magnitude)', 'Avg_Magnitude')

# Join df_max, and df_avg to df_quake_freq
df_quake_freq = df_quake_freq.join(df_avg, ['Year']).join(df_max, ['Year'])

# Remove nulls
df_load.dropna()
df_quake_freq.dropna()

#----------------------------------------------LOADING-------------------------------------

# Build the tables or collections
# Write df_load to mongodb
df_load.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Quake.quakes').save()

# Write df_quake_freq to mongodb
df_quake_freq.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Quake.quake_freq').save()



print(df_quake_freq.show(5))
print(df_load.show(5))


print('Job ran successfully...')