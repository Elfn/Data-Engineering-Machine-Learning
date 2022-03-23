#-----------------------------------------------Machine Learning Part---------------------------------------------------------
#----------------------------------------------ML MODELS------------------------------------------------------------
from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

# Load students data from mongodb
#students_cleaned_loaded_df = spark.read.format('mongo').option('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/studentsdb.students_df').load()
nb_students_by_region_loaded = spark.read.format('mongo').option('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_students_by_region').load()
total_supinfo_students_loaded = spark.read.format('mongo').option('spark.mongodb.input.uri', 'mongodb://127.0.0.1:27017/studentsdb.total_supinfo_students').load()

nb_students_by_region_loaded.show()
total_supinfo_students_loaded.show()
nb_students_by_region_loaded.printSchema()

# school's growth forecasts (To predict total number of students by campus)

# Select features to parse into our model and then create the feature vector
assembler = VectorAssembler(inputCols=['nombre etudiants'], outputCol='features')

# Create the model
model_reg = RandomForestRegressor(featuresCol='features', labelCol='nombre etudiants')


# Chain the assembler with the model in a pipeline
pipeline = Pipeline(stages=[assembler, model_reg])

# Train the model
model = pipeline.fit(nb_students_by_region_loaded)

# Make the prediction of number of students by regions
pred_results_forecast = model.transform(nb_students_by_region_loaded)
pred_results_forecast = pred_results_forecast.withColumnRenamed('prediction','nombre etudiants(Prediction)')
pred_results_forecast.show(5)

# Load the prediction dataset into mongodb
# Write df_pred_results
nb_supinfo_students_by_region_prediction = pred_results_forecast.drop('features').withColumn("nombre etudiants(Prediction)",col('nombre etudiants(Prediction)').cast(IntegerType()))
nb_supinfo_students_by_region_prediction.write.format('mongo').mode('overwrite').option('spark.mongodb.output.uri', 'mongodb://127.0.0.1:27017/studentsdb.nb_supinfo_students_by_region_prediction').save()