# transform.py
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, round

os.environ["HADOOP_USER_NAME"] = "aaryapaudel"
# --- CONFIGURATION ---
input_parquet_path = "raw_real_estate.parquet"
output_parquet_path = "transformed_real_estate.parquet"

# --- STEP 1: CREATE SPARK SESSION ---
spark = SparkSession.builder \
    .appName("RealEstateTransformation") \
    .master("local[*]") \
    .getOrCreate()

print("✅ SparkSession created successfully.")

# --- STEP 2: EXTRACT (Read the Parquet file) ---
try:
    # Read the raw data from the Parquet file
    df = spark.read.parquet(input_parquet_path)
    print(f"✅ Data loaded from '{input_parquet_path}'.")
except Exception as e:
    print(f"❌ Error loading Parquet file: {e}")
    spark.stop()
    exit()

# --- STEP 3: TRANSFORM (Clean, rename, and aggregate) ---
print("🔧 Starting data transformation...")

# Rename the columns for clarity and easier use in the web app
df = df.withColumnRenamed("X2 house age", "house_age") \
       .withColumnRenamed("X3 distance to the nearest MRT station", "distance_to_mrt") \
       .withColumnRenamed("X4 number of convenience stores", "convenience_stores") \
       .withColumnRenamed("X5 latitude", "latitude") \
       .withColumnRenamed("X6 longitude", "longitude") \
       .withColumnRenamed("Y house price of unit area", "house_price") \
       .drop("No", "X1 transaction date") # Drop irrelevant columns

# Remove any null values and ensure data quality
df_clean = df.dropna()

print("✅ Data transformed successfully.")
df_clean.show()

# --- STEP 4: SAVE THE TRANSFORMED DATA ---
# Save the transformed DataFrame to a new Parquet file.
try:
    df_clean.write.mode("overwrite").parquet(output_parquet_path)
    print(f"✅ Transformed data saved to '{output_parquet_path}'.")
except Exception as e:
    print(f"❌ Error saving transformed data: {e}")
finally:
    spark.stop()
    print("✅ Spark session closed.")

