from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import argparse

spark = SparkSession.builder.appName("EMR job").getOrCreate()

def transformation(source_input1, source_input2, output_location):
    df = spark.read.format("csv").option("header", "true").load(source_input1)
    df_trip_type = spark.read.format("csv").option("header", "true").load(source_input2)

    df.show(n=5,truncate=False)
    df_trip_type.show()

    #filtere necessary columns
    df_selected = df.select('VendorID','PULocationID','DOLocationID','passenger_count','total_amount','trip_type')

    #Null check
    null_count = df_selected.select([sum(col(c).isNull().cast('int')).alias(c +'_nulls') for c in df_selected.columns])
    null_count.show()

    #join two datas
    df_joined = df_selected.join(broadcast(df_trip_type),on="trip_type",how='inner')
    df_final = df_joined.select(col('VendorID'),
                                col('PULocationID').alias('pickup_loc_id'),
                                col('DOLocationID').alias('drop_loc_id'),
                                col('passenger_count'),
                                col('total_amount'),
                                col('description').alias('trip_type'))

    df_final.write.mode('overwrite').parquet(output_location)
    print(f"Data successfully written to: {output_location}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("emr parser")
    parser.add_argument("--source_input1",required = True, help="s3 path to tripdata.csv")
    parser.add_argument("--source_input2",required = True, help="s3 path to trip_type.csv")
    parser.add_argument("--output_location",required = True, help="s3 path to save data as parquet")
    args = parser.parse_args()

    transformation(args.source_input1, args.source_input2, args.output_location)