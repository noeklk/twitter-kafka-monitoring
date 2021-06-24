def import_json(db, json, table_name):
    table = db[table_name]
    table.delete_many({})
    table.insert_many(json)


def import_pandas_df(db, df, table_name):
    import_json(db, df.to_dict(orient='records'), table_name)


def import_spark_df(db, df, table_name):
    import_pandas_df(db, df.toPandas(), table_name)


def clear_avg(col):
    return col.replace('avg(', '').replace(')', '')
