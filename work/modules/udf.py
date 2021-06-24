from pyspark.sql.types import *
from pyspark.sql.functions import udf


@udf(returnType=StringType())
def ms_to_display_string(ms):
    m, s = divmod(ms / 1000, 60)
    return f"{int(m)}min{int(s):0>2d}"
