from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

def main():
    # -----------------------
    # 1️⃣ Initialize Spark
    # -----------------------
    # Set Java Home to match Spark's compiled Java version (61.0 corresponds to Java 17)
    # If Java 17 is not installed, please install it and update this path accordingly.
    import os
    
    # Attempt to find common Java installation paths for Java 17
    java_17_home = None
    if os.path.exists("/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home"):
        java_17_home = "/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home"
    elif os.path.exists("/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"):
        java_17_home = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
    elif os.path.exists("/usr/local/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"):
        java_17_home = "/usr/local/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

    if java_17_home:
        os.environ["JAVA_HOME"] = java_17_home
        os.environ["PATH"] = os.path.join(java_17_home, "bin") + os.pathsep + os.environ["PATH"]
        print(f"JAVA_HOME set to: {os.environ['JAVA_HOME']}")
    else:
        print("Warning: Java 17 not found in common paths. Please install Java 17 or set JAVA_HOME manually.")

    spark = SparkSession.builder \
        .appName("BigDataCoursework_ETL") \
        .getOrCreate()

    # Optional: set log level to WARN to reduce output
    spark.sparkContext.setLogLevel("WARN")

    # -----------------------
    # 2️⃣ Extract
    # -----------------------
    # Example: reading a CSV file
    input_path = "data/raw/data.csv"  # replace with your path
    df = spark.read.option("header", True).csv(input_path)

    print("✅ Data Extracted:")
    df.show(5)

    # -----------------------
    # 3️⃣ Transform
    # -----------------------
    # Example transformations
    # - Cast columns to correct types
    # - Filter rows
    # - Add a new column
    df_transformed = df.withColumn("price", col("price").cast("double")) \
                       .filter(col("quantity") > 0) \
                       .withColumn("total", col("quantity") * col("price"))

    print("✅ Data Transformed:")
    df_transformed.show(5)

    # -----------------------
    # 4️⃣ Load
    # -----------------------
    output_path = "data/processed/output.csv"  # replace with your path
    df_transformed.write.mode("overwrite").option("header", True).csv(output_path)
    df_transformed.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/real_estate_db") \
    .option("dbtable", "real_estate_data") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

    print(f"✅ Data Loaded to {output_path}")

    # -----------------------
    # 5️⃣ Verification (optional)
    # -----------------------
    df_check = spark.read.option("header", True).csv(output_path)
    print("✅ Loaded Data Preview:")
    df_check.show(5)

    spark.stop()


if __name__ == "__main__":
    main()
