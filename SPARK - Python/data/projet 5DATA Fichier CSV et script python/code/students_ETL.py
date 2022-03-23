#----------------------------------------------------STAGING/EXTRACTION------------------------------------------

import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime


#Configure spark session
spark = SparkSession.builder.master('local[2]').appName('etl_app').config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1').getOrCreate()

# Extract the dataset "studentdatabase.json" and add it to dataframe
df_load = spark.read.csv(r"/Users/Elimane/SPARK/data/5_DATA_dataset.csv", header=True)
df_load.show(2)

#----------------------------------------------------CLEANSING/TRANSFORMATION------------------------------------------

# Remove null values
df_load = df_load.dropna()
df_load.show(2)

# Print schema
df_load.printSchema()

# Convert some string fields into Date
df_load = df_load['nom','prenom','sexe','birthdate','pays_de_residence','nationalite','universite','campus','annee_en_cours','date_admission','diplome','activite','ects','etude','type_contrat','debut_contrat','duree_contrat','entreprise']
df_load = df_load.withColumn('birthdate',date_format(to_date(col("birthdate"), "M/d/y"),"dd/MM/y")).withColumn('date_admission',date_format(to_date(col("date_admission"), "d/M/y"),"dd/MM/y")).withColumn('debut_contrat',date_format(to_date(col("debut_contrat"), "M/d/y"),"dd/MM/y"))
df_load.printSchema()
df_load.show(6)

# Convert some string fields into numeric(Double)
df_load = df_load.withColumn('ects', df_load['ects'].cast(DoubleType()))\
    .withColumn('duree_contrat', df_load['duree_contrat'].cast(DoubleType()))\
    .withColumn('annee_en_cours', df_load['annee_en_cours'].cast(DoubleType()))


# Print schema
df_load.show(5)

# 1-The most successful students, depending on the region / institution of origin
students_tmp_df = df_load['nom','prenom','birthdate','ects','diplome','type_contrat','duree_contrat','etude','campus','activite','entreprise','universite']
students_tmp_df = students_tmp_df.withColumn('diplome',when(col('ects') >= 300 , 'VRAI').otherwise('FAUX'))
successful_df = students_tmp_df.filter((col('diplome') == 'VRAI'))
successful_df.show()

# 2-the students who stop their studies
students_tmp_df = students_tmp_df.withColumn('etude',when(col('etude') == 'stope' , 'stop').otherwise(col('etude')))
students_tmp_df = students_tmp_df.withColumn('campus',when(col('campus') == 'CLERMONT-FD' , 'CLERMONT').when(col('campus') == 'QUAND' , 'CAEN')\
                       .when(col('campus') == 'Clermon' , 'CLERMONT')\
                       .when(col('campus') == 'CLF' , 'CLERMONT')\
                       .when(col('campus') == 'cancan' , 'CAEN')\
                       .when(col('campus') == 'can' , 'CAEN')\
                       .when(col('campus') == 'lion' , 'LYON')\
                       .otherwise(col('campus')))
student_df = students_tmp_df

student_stopped = students_tmp_df.filter((col('etude') == 'stop'))
student_stopped.show(6)

# 3- Number of students by region
nb_students_by_region = students_tmp_df.select('nom','prenom','campus').groupBy('campus').count().withColumnRenamed('count','nombre etudiants')
nb_students_by_region.show()


# 4- Number of students by activity (To know how revitalize campuses)
nb_students_by_activity = students_tmp_df.select('nom','prenom','activite').groupBy('activite').count().withColumnRenamed('count','nombre etudiants')
nb_students_by_activity.show()

# Average length of time graduates are hired
avg_length_time_hired = students_tmp_df.select((sum('duree_contrat')/count('nom')).alias('Moyenne du temps de contrat'))
avg_length_time_hired.show()

# Total number of students
nb_total_students = students_tmp_df.select(count('nom'))

# Number of students by companies for which recruit the most students from supinfo
nb_students_by_enterprise = students_tmp_df.select('nom','prenom','entreprise','universite').filter(col('universite') == 'SUPINFO').groupBy('entreprise').count().withColumnRenamed('count','nombre etudiants')
nb_students_by_enterprise = nb_students_by_enterprise.select(col('entreprise'),col('nombre etudiants')).orderBy(col('nombre etudiants').desc())

nb_students_by_enterprise.show()


# SUPINFO's competitors who are poaching  students
competitors_list = students_tmp_df.select('universite').filter(col('universite') != 'SUPINFO').dropDuplicates()
competitors_list.show()


# SUPINFO's competitors who are poaching  students
competitors_list = students_tmp_df.select('universite').filter(col('universite') != 'SUPINFO').dropDuplicates()
competitors_list.show()

# regions which have more Pro contracts and why
nb_contrat_pro_by_region = students_tmp_df.select('nom','prenom','campus','type_contrat').groupBy('campus','type_contrat').count().filter(col('type_contrat') == 'Contrat Pro').withColumnRenamed('count','nombre contrats pro')
nb_contrat_pro_by_region.show()

# Students age
students_age = students_tmp_df.select('nom','prenom','birthdate').withColumn("age",year(current_date()) - year(to_date(col('birthdate'),"d/M/y")))
students_age.show()

# SUPINFO students
students_of_SUPINFO = students_tmp_df.select('nom','prenom','campus','universite').where(col('universite') == 'SUPINFO').dropDuplicates()
students_of_SUPINFO.show()

# number of students by SUPINFO campuses
nb_students_of_SUPINFO_by_campuses = students_of_SUPINFO.select('nom','prenom','campus').groupBy('campus').count().withColumnRenamed('count','nombre etudiants')
nb_students_of_SUPINFO_by_campuses.show()


# Total number of SUPINFO's students
total_supinfo_students = nb_students_of_SUPINFO_by_campuses.select(sum('nombre etudiants').alias('total supinfo students'))
total_supinfo_students.show()


# campus geographic coordinates
students_tmp_df = students_tmp_df.select('campus')\
         
campus_geo_location = students_tmp_df.select('campus')\
         .withColumn('longitude',when(col('campus') == 'CLERMONT' , 45.783100)\
                       .when(col('campus') == 'CAEN' , -4.490000)\
                       .when(col('campus') == 'LYON' , 4.834277)\
                       .when(col('campus') == 'MONTPELIER' , 3.877200)\
                       .when(col('campus') == 'LILLE' , 3.057256)\
                       .when(col('campus') == 'PARIS' , 2.349014)\
                       .otherwise(0)).withColumn('latitude',when(col('campus') == 'CLERMONT' , 3.082400)\
                       .when(col('campus') == 'CAEN' , 49.180000)\
                       .when(col('campus') == 'LYON' , 45.763420)\
                       .when(col('campus') == 'MONTPELIER' , 43.611900)\
                       .when(col('campus') == 'LILLE' , 50.629250)\
                       .when(col('campus') == 'PARIS' , 48.864716)\
                       .otherwise(0)).dropDuplicates()
                     


campus_geo_location.show()


#----------------------------------------------------STORING/LOADING------------------------------------------
# Build the tables or collections
# Write dataframes to mongodb
nb_contrat_pro_by_region.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_contrat_pro_by_region').save()
competitors_list.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.competitors_list').save()
nb_students_by_enterprise.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_students_by_enterprise').save()
nb_total_students.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_total_students').save()
avg_length_time_hired.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.avg_length_time_hired').save()
nb_students_by_activity.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_students_by_activity').save()
nb_students_by_region.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_students_by_region').save()
student_stopped.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_students_by_region').save()
successful_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.successful_df').save()
students_age.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.students_age').save()
campus_geo_location.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.campus_geo_location').save()
student_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.students_df').save()
students_of_SUPINFO.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.students_of_SUPINFO').save()
total_supinfo_students.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.total_supinfo_students').save()
