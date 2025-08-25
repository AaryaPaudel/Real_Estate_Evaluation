from pyspark.sql import SparkSession

# --- CONFIGURATION ---
input_parquet_path = "transformed_real_estate.parquet"
DB_HOST = "localhost"
DB_NAME = "real_estate_db"
DB_USER = "postgres"       # use postgres superuser unless you've created etl_user
DB_PASSWORD = "postgres"
DB_TABLE = "real_estate_data"

# --- STEP 1: CREATE SPARK SESSION ---
spark = SparkSession.builder \
    .appName("RealEstateLoad") \
    .master("local[*]") \
    .config("spark.jars", "postgresql-42.7.4.jar") \
    .config("spark.executor.extraJavaOptions", "--add-opens=java.base/java.lang=ALL-UNNAMED") \
    .config("spark.driver.extraJavaOptions", "--add-opens=java.base/java.lang=ALL-UNNAMED") \
    .getOrCreate()

print("✅ SparkSession created successfully.")

# --- STEP 2: LOAD TRANSFORMED DATA ---
try:
    df = spark.read.parquet(input_parquet_path)
    print(f"✅ Transformed data loaded from '{input_parquet_path}'.")
    print("📊 DataFrame schema:")
    df.printSchema()
except Exception as e:
    print(f"❌ Error loading transformed data: {e}")
    spark.stop()
    exit()

# --- STEP 3: ENSURE EXPECTED COLUMNS ---
expected_cols = ["house_age", "distance_to_mrt", "convenience_stores",
                 "latitude", "longitude", "house_price"]

missing_cols = [c for c in expected_cols if c not in df.columns]
if missing_cols:
    print(f"⚠️ Warning: Missing columns in DataFrame: {missing_cols}")
else:
    print("✅ All expected columns are present.")

# --- STEP 4: WRITE TO POSTGRESQL ---
try:
    df.write \
      .format("jdbc") \
      .option("url", f"jdbc:postgresql://{DB_HOST}:5432/{DB_NAME}") \
      .option("dbtable", DB_TABLE) \
      .option("user", DB_USER) \
      .option("password", DB_PASSWORD) \
      .option("driver", "org.postgresql.Driver") \
      .mode("overwrite") \
      .save()
    print(f"✅ Data loaded into PostgreSQL table '{DB_TABLE}' successfully.")
except Exception as e:
    print(f"❌ Error writing to PostgreSQL: {e}")
finally:
    spark.stop()
    print("✅ Spark session closed.")
