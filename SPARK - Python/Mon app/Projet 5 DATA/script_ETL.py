import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime


#Configure spark session
spark = SparkSession.builder.master('local[2]').appName('testJson').config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1').getOrCreate()

# Extract the dataset "studentdatabase.json" and add it to dataframe

extracted_df = spark.read.option("multiline","true").json(r"/Users/Elimane/SPARK/data/studentdatabase.json")
#multiline_df.show(2)  

#df_load = spark.read.csv(r"/Users/Elimane/SPARK/data/database.csv", header=True)
#Preview extracted_df
#extracted_df.take(1)

#----------------------------------------------------CLEANSING/TRANSFORMATION------------------------------------------

# read all the students name
readData = extracted_df.withColumn('res',explode('data'))
students_df = readData.withColumn('res_curriculum',explode('res.curriculum')).select('res.firstname','res.lastname',col("res.birthdate"),'res.graduated','res.regionOfOrigin','res.institutionOfOrigin','res.attendance','res.credits','res_curriculum.experiences.business','res_curriculum.experiences.position','res_curriculum.experiences.startDate','res_curriculum.experiences.EndDate','res_curriculum.experiences.contractType','res.studies')


# 1- Most successful students [They got 300 credits or more]
successful_df = students_df.dropDuplicates(["firstname","lastname"]).select('firstname','lastname','regionOfOrigin.name','institutionOfOrigin','credits').withColumnRenamed('name', 'regionName').filter(students_df['credits'] >= 300)
successful_number_df = successful_df.dropna().count()
students_cleaned_df = students_df.dropDuplicates(["firstname","lastname"]).select('firstname','lastname','regionOfOrigin.name','regionOfOrigin.latitude','regionOfOrigin.longitude','institutionOfOrigin','credits').withColumnRenamed('name', 'regionName').withColumnRenamed('latitude', 'regionLatitude').withColumnRenamed('longitude', 'regionLongitude')

# 2- Students who stop their studies
students_studies_stopped = students_df.dropDuplicates(["firstname","lastname"]).select(concat('firstname',lit(" "),'lastname').alias('student_name'),'regionOfOrigin.name','institutionOfOrigin','credits','studies').withColumnRenamed('name', 'regionName').filter((students_df['studies'] == 'FINISHED') & (students_df['credits'] < 300))

# 3- Students by regions and institutions 
number_students_by_regions = students_df.dropna().groupBy('regionOfOrigin.name','regionOfOrigin.latitude','regionOfOrigin.longitude','institutionOfOrigin').count().withColumnRenamed('count', 'Number_of_students').withColumnRenamed('name', 'regionName').withColumnRenamed('latitude', 'regionLatitude').withColumnRenamed('longitude', 'regionLongitude')

# Regions and  By attendances
regions_by_attendances = students_df.dropDuplicates(["firstname","lastname"]).select(concat('firstname',lit(" "),'lastname').alias('student_name'),'birthdate','regionOfOrigin.name','regionOfOrigin.latitude','regionOfOrigin.longitude','attendance').withColumn("number_of_attendances",size(col("attendance"))).withColumnRenamed('attendance', 'attendances').withColumnRenamed('name', 'regionName').withColumnRenamed('latitude', 'regionLatitude').withColumnRenamed('longitude', 'regionLongitude')

# Change birthDate format and add right values
students_with_date_format_changed = students_df.dropDuplicates(["firstname","lastname"]).select(concat('firstname',lit(" "),'lastname').alias('student_name'),date_format(to_date('birthdate', "dd-MM-yyyy"),"dd/MM/yyyy").alias('birthdate_new_format'),'regionOfOrigin.name','attendance').withColumnRenamed('attendance', 'attendances').withColumnRenamed('name', 'regionName')

# Calculate students ages
students_age_df = students_df.dropDuplicates(["firstname","lastname"]).select(concat('firstname',lit(" "),'lastname').alias('student_name'),date_format(to_date('birthdate',"dd-MM-yyyy"),"dd/MM/yyyy").alias("birthdate")).withColumn("age",year(current_date()) - year(to_date(col('birthdate'),"dd/MM/yyyy"))).withColumnRenamed('attendance', 'attendances')

# students curriculum
students_curriculum = students_df.dropDuplicates(["firstname","lastname"]).select(concat('firstname',lit(" "),'lastname').alias('student_name'),'graduated','business','position','institutionOfOrigin','regionOfOrigin.name','contractType','startDate','EndDate').withColumnRenamed('name', 'regionName')
students_curriculum_ordered_df = students_curriculum.orderBy(col("student_name")).dropna()


#students currently hired and not
students_with_hiring_status = students_curriculum_ordered_df.withColumn("Currently_In_Hired",array_contains(col("EndDate"),"PRESENT"))
student_hired = students_with_hiring_status.filter(col('Currently_In_Hired') == 'true')
student_not_hired = students_with_hiring_status.select('student_name','startDate','EndDate','Currently_In_Hired').filter(col('Currently_In_Hired') == 'false')

# number of students hired and not by region
nb_students_not_hired = students_with_hiring_status.dropDuplicates(["student_name"]).select('regionName','Currently_In_Hired','institutionOfOrigin').filter(col('Currently_In_Hired') == 'false').groupBy("regionName","institutionOfOrigin").count().withColumnRenamed('count', 'Number_of_students_not_hired')
nb_students_hired = students_with_hiring_status.dropDuplicates(["student_name"]).select('regionName','Currently_In_Hired','institutionOfOrigin').filter(col('Currently_In_Hired') == 'true').groupBy("regionName","institutionOfOrigin").count().withColumnRenamed('count', 'Number_of_students_hired')

# Companies which recruit the most supinfo's students
companies_occurences_df = students_with_hiring_status.withColumn('businesses', explode('business')).groupBy('businesses').count()
most_reccurent_companies_df = companies_occurences_df.withColumnRenamed('count', 'companies_occurences').filter(col('companies_occurences') > 1)

# Graduated students
graduated_students = students_with_hiring_status['student_name','regionName','graduated','business','startDate','EndDate','contractType'].filter(col('graduated') == 'true')

# average length of time graduates are hired
hired_times = graduated_students['student_name','regionName','startDate','EndDate','contractType'].withColumn('EndDate',explode('EndDate')).withColumn('startDate',explode('startDate')).withColumn('contractType',explode('contractType')).withColumnRenamed("name","RegionName")
hired_times_cleaned = hired_times.where((col('EndDate') == "PRESENT") & (col('contractType') == "Professional_Contract")).withColumn('EndDate',when(col('EndDate') == "PRESENT",date_format(to_date(current_date(),"dd-MM-yyyy"),"dd-MM-yyyy")).otherwise(col('EndDate'))).withColumn('years', (datediff(to_date('EndDate',"dd-MM-yyyy"),to_date('startDate',"dd-MM-yyyy")))/365)
years = hired_times_cleaned.drop('student_name','startDate','EndDate','contractType')
avg = years.select(round((sum(years['years'])/count(years['years']))).alias('average_length_time_hired_years'))

#Pro contracts by regions
pro_contract_by_region = hired_times_cleaned['RegionName','contractType'].groupBy('RegionName','contractType').count().withColumnRenamed('count','number_of_pro_contracts').where(col('number_of_pro_contracts') > 1)

#----------------------------------------------------STORING/LOADING------------------------------------------

# Build the tables or collections
# Write dataframes to mongodb
successful_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.successfull_students').save()

students_studies_stopped.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.studies_stopped').save()

number_students_by_regions.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.number_students_by_regions').save()

regions_by_attendances.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.regions_by_attendances').save()

students_with_date_format_changed.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.students_with_date_format_changed').save()

students_age_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.students_age_df').save()

students_curriculum_ordered_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.students_curriculum_ordered_df').save()

student_hired.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.student_hired').save()

nb_students_not_hired.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.nb_students_not_hired').save()

pro_contract_by_region.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.pro_contract_by_region').save()

most_reccurent_companies_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.most_reccurent_companies_df').save()

graduated_students.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.graduated_students').save()

avg.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.avg_graduated_hired').save()

students_cleaned_df.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.students_df').save()

print('ETL Job ran successfully...')