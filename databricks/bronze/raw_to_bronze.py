
from pyspark.sql import functions as F

# COMMAND ----------

dbutils.widgets.text("storage_account", "stweatherdevyahia")

storage_account = dbutils.widgets.get("storage_account")
container = "datalake"

raw_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/raw/weather/"
)
bronze_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/bronze/weather/"
)
catalog_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/managed/weather/"
)

# COMMAND ----------

raw_df = (
    spark.read
    .option("recursiveFileLookup", "true")
    .option("multiLine", "true")
    .json(raw_path)
)

bronze_df = (
    raw_df
    .withColumn("source_file", F.col("_metadata.file_path"))
    .withColumn("ingested_at", F.current_timestamp())
)

if bronze_df.limit(1).count() == 0:
    raise ValueError("No RAW weather data was found.")

# COMMAND ----------

(
    bronze_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(bronze_path)
)

spark.sql(
    f"""
    CREATE CATALOG IF NOT EXISTS weather
    MANAGED LOCATION '{catalog_path}'
    """
)
spark.sql("CREATE SCHEMA IF NOT EXISTS weather.bronze")
spark.sql(
    f"""
    CREATE TABLE IF NOT EXISTS weather.bronze.weather
    USING DELTA
    LOCATION '{bronze_path}'
    """
)

print(f"Bronze table created with {bronze_df.count()} rows.")
