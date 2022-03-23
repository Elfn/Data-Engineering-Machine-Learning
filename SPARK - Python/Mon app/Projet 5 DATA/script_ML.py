import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

#----------------------------------------------ML MODELS------------------------------------------------------------
#Configure spark session
spark = SparkSession.builder.master('local[2]').appName('testJson').config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1').getOrCreate()


students_cleaned_loaded_df = spark.read.format('mongo').option('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/Student.students_df').load()

#school's growth forecasts
#Number of students by regions
students_by_regions = students_cleaned_loaded_df.select(concat('firstname',lit(" "),'lastname').alias('student_name'),'regionName','regionLatitude','regionLongitude','institutionOfOrigin')
nb_students_by_regions = students_by_regions.groupBy('regionName','regionLatitude','regionLongitude').count().withColumnRenamed('count','number_of_students')
nb_schools_by_regions = students_by_regions.groupBy('institutionOfOrigin').count().withColumnRenamed('count','number_of_schools')

# Select features to parse into our model and then create the feature vector
assembler = VectorAssembler(inputCols=['number_of_students'], outputCol='features')

# Create the model
model_reg = RandomForestRegressor(featuresCol='features', labelCol='number_of_students')


# Chain the assembler with the model in a pipeline
pipeline = Pipeline(stages=[assembler, model_reg])

# Train the model
model = pipeline.fit(nb_students_by_regions)

# Make the prediction of number of students by regions
pred_results = model.transform(nb_students_by_regions)

# Evaluate the model
# rmse should be less than 0.5 for the model to be useful
evaluator = RegressionEvaluator(labelCol='number_of_students', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(pred_results)
print('Root Mean Squared Error (RMSE) on test data = %g ' %rmse)


# Create the prediction dataset
df_pred_results = pred_results['regionName','number_of_students']

# Rename the prediction field
df_pred_results = df_pred_results.withColumnRenamed('prediction','Pred_number_of_students')

# Add more columns to our prediction dataset for 2022
df_pred_results = df_pred_results.withColumn('Year', lit(2022)).withColumn('RMSE', lit(rmse))


# Load the prediction dataset into mongodb
# Write df_pred_results
df_pred_results.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Student.df_pred_results').save()

print('Machine Learning Job ran successfully...')