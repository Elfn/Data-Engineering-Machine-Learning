import findspark
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
import numpy as np

# Configure spark session
spark = SparkSession.builder.master('local[2]').appName('quake_etl').config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:2.4.1').getOrCreate()

"""

Data Pre-processing

"""

# Load the data file
df_test = spark.read.csv(r"/Users/Elimane/SPARK/data/query.csv", header=True)


# Load training data from mongo
df_train = spark.read.format('mongo').option('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/Quake.quakes').load()


# Select field we will use and discard fields we don't need
df_test_cleaned = df_test['time','latitude','longitude','mag','depth']

# Rename fields
df_test_cleaned = df_test_cleaned.withColumnRenamed('time', 'Date')\
    .withColumnRenamed('latitude', 'Latitude')\
    .withColumnRenamed('longitude', 'Longitude')\
    .withColumnRenamed('mag', 'Magnitude')\
    .withColumnRenamed('depth', 'Depth')\

# Cast some string fields into numeric fields
df_test_cleaned = df_test_cleaned.withColumn('Latitude', df_test_cleaned['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_test_cleaned['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_test_cleaned['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_test_cleaned['Magnitude'].cast(DoubleType()))


# Create testing and training dataframes
df_testing = df_test_cleaned['Latitude','Longitude','Magnitude','Depth']
df_training = df_train['Latitude','Longitude','Magnitude','Depth']

df_testing = df_testing.withColumn('Latitude', df_testing['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_testing['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_testing['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_testing['Magnitude'].cast(DoubleType()))

df_training = df_training.withColumn('Latitude', df_training['Latitude'].cast(DoubleType()))\
    .withColumn('Longitude', df_training['Longitude'].cast(DoubleType()))\
    .withColumn('Depth', df_training['Depth'].cast(DoubleType()))\
    .withColumn('Magnitude', df_training['Magnitude'].cast(DoubleType()))
    
    
    # Drop records with null values from our dataframes
df_testing = df_testing.dropna()
df_training = df_training.dropna()

#----------------------------------------------ML MODELS------------------------------------------------------------

# Select features to parse into our model and then create the feature vector
assembler = VectorAssembler(inputCols=['Latitude','Longitude','Depth'], outputCol='features')

# Create the model
model_reg = RandomForestRegressor(featuresCol='features', labelCol='Magnitude')


# Chain the assembler with the model in a pipeline
pipeline = Pipeline(stages=[assembler, model_reg])

# Train the model
model = pipeline.fit(df_training)

# Make the prediction
pred_results = model.transform(df_testing)
    
    
    
# Evaluate the model
# rmse should be less than 0.5 for the model to be useful
evaluator = RegressionEvaluator(labelCol='Magnitude', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(pred_results)
print('Root Mean Squared Error (RMSE) on test data = %g ' %rmse)


"""

Create the prediction dataset
"""

# Create the prediction dataset
df_pred_results = pred_results['Latitude','Longitude','prediction']

# Rename the prediction field
df_pred_results = df_pred_results.withColumnRenamed('prediction','Pred_Magnitude')

# Add more columns to our prediction dataset
df_pred_results = df_pred_results.withColumn('Year', lit(2017)).withColumn('RMSE', lit(rmse))


# Load the prediction dataset into mongodb
# Write df_pred_results
df_pred_results.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/Quake.df_pred_results').save()


print('Job ran successfully...')