from pyspark.sql import SparkSession
import os

os.environ["HADOOP_USER_NAME"] = "aaryapaudel"
def main():
    spark = (
        SparkSession.builder
        .appName("quick_etl")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.4")
        .getOrCreate()
    )

    # --- Extract ---
    df = spark.read.option("header", True).csv("data/input/sample.csv")

    # --- Transform ---
    df_clean = df.dropna()

    # --- Load ---
    (
        df_clean.write
          .format("jdbc")
          .option("url", "jdbc:postgresql://localhost:5432/etl_db")
          .option("dbtable", "public.sales")
          .option("user", "etl_user")
          .option("password", "etl_password")
          .mode("overwrite")
          .save()
    )

    spark.stop()

if __name__ == "__main__":
    main()
