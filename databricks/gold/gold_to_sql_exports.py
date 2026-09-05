
from pyspark.sql import functions as F


dbutils.widgets.text("storage_account", "stweatherdevyahia")

storage_account = dbutils.widgets.get("storage_account")
container = "datalake"

gold_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/"
    "gold/daily_city_weather/"
)
serving_path = (
    f"abfss://{container}@{storage_account}.dfs.core.windows.net/serving/sql/"
)

gold_df = spark.read.format("delta").load(gold_path)

if gold_df.limit(1).count() == 0:
    raise ValueError("No Gold weather data is available for the SQL exports.")

dim_city_df = (
    gold_df
    .select(
        F.col("city_id").alias("city_key"),
        F.col("city").alias("city_name"),
        "country",
        "latitude",
        "longitude",
    )
    .dropDuplicates(["city_key"])
)

dim_date_df = (
    gold_df
    .select(F.col("weather_date").alias("full_date"))
    .distinct()
    .select(
        F.date_format("full_date", "yyyyMMdd").cast("integer").alias("date_key"),
        "full_date",
        F.year("full_date").alias("year"),
        F.month("full_date").alias("month"),
        F.dayofmonth("full_date").alias("day"),
        F.date_format("full_date", "MMMM").alias("month_name"),
    )
)

fact_weather_df = gold_df.select(
    F.col("city_id").alias("city_key"),
    F.date_format("weather_date", "yyyyMMdd").cast("integer").alias("date_key"),
    "average_temperature",
    "minimum_temperature",
    "maximum_temperature",
    "average_humidity",
    "average_wind_speed",
    "observation_count",
)

# COMMAND ----------

exports = {
    "dim_city": dim_city_df,
    "dim_date": dim_date_df,
    "fact_weather": fact_weather_df,
}

for export_name, export_df in exports.items():
    export_df.write.mode("overwrite").parquet(f"{serving_path}{export_name}/")
    print(f"{export_name}: {export_df.count()} rows exported.")
