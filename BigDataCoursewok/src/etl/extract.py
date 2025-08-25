# extract.py
import os

os.environ["HADOOP_USER_NAME"] = "aaryapaudel"
from pyspark.sql import SparkSession

# --- CONFIGURATION ---
input_csv_path = "/Users/aaryapaudel/BigDataCoursewok/data/raw/data.csv"
output_parquet_path = "raw_real_estate.parquet"

# --- STEP 1: CREATE SPARK SESSION ---
# This is the entry point for all PySpark functionality.
spark = SparkSession.builder \
    .appName("RealEstateExtraction") \
    .master("local[*]") \
    .getOrCreate()

print("✅ SparkSession created successfully.")

# --- STEP 2: EXTRACT (Read the raw CSV) ---
try:
    # Read the raw CSV file into a PySpark DataFrame
    df = spark.read.csv(input_csv_path, header=True, inferSchema=True)
    print("✅ Raw data loaded into Spark DataFrame.")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    spark.stop()
    exit()

# --- STEP 3: SAVE TO INTERMEDIATE LOCATION (Parquet file) ---
# Write the raw DataFrame to a Parquet file, which is optimized for big data.
try:
    df.write.mode("overwrite").parquet(output_parquet_path)
    print(f"✅ Raw data successfully saved to '{output_parquet_path}'.")
except Exception as e:
    print(f"❌ Error saving data to Parquet: {e}")
finally:
    spark.stop()
    print("✅ Spark session closed.")

