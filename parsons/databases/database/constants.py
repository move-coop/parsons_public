# These are reserved words by Redshift and cannot be used as column names.
RESERVED_WORDS = [
    "AES128", "AES256", "ALL", "ALLOWOVERWRITE", "ANALYSE", "ANALYZE", "AND",
    "ANY", "ARRAY", "AS", "ASC", "AUTHORIZATION", "BACKUP", "BETWEEN", "BINARY",
    "BLANKSASNULL", "BOTH", "BYTEDICT", "BZIP2", "CASE", "CAST", "CHECK",
    "COLLATE", "COLUMN", "CONSTRAINT", "CREATE", "CREDENTIALS", "CROSS",
    "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER",
    "CURRENT_USER_ID", "DEFAULT", "DEFERRABLE", "DEFLATE", "DEFRAG", "DELTA",
    "DELTA32K", "DESC", "DISABLE", "DISTINCT", "DO", "ELSE", "EMPTYASNULL",
    "ENABLE", "ENCODE", "ENCRYPT", "ENCRYPTION", "END", "EXCEPT", "EXPLICIT",
    "FALSE", "FOR", "FOREIGN", "FREEZE", "FROM", "FULL", "GLOBALDICT256",
    "GLOBALDICT64K", "GRANT", "GROUP", "GZIP", "HAVING", "IDENTITY", "IGNORE",
    "ILIKE", "IN", "INITIALLY", "INNER", "INTERSECT", "INTO", "IS", "ISNULL",
    "JOIN", "LEADING", "LEFT", "LIKE", "LIMIT", "LOCALTIME", "LOCALTIMESTAMP",
    "LUN", "LUNS", "LZO", "LZOP", "MINUS", "MOSTLY13", "MOSTLY32", "MOSTLY8",
    "NATURAL", "NEW", "NOT", "NOTNULL", "NULL", "NULLS", "OFF", "OFFLINE",
    "OFFSET", "OLD", "ON", "ONLY", "OPEN", "OR", "ORDER", "OUTER", "OVERLAPS",
    "PARALLEL", "PARTITION", "PERCENT", "PERMISSIONS", "PLACING", "PRIMARY",
    "RAW", "READRATIO", "RECOVER", "REFERENCES", "RESPECT", "REJECTLOG",
    "RESORT", "RESTORE", "RIGHT", "SELECT", "SESSION_USER", "SIMILAR", "SOME",
    "SYSDATE", "SYSTEM", "TABLE", "TAG", "TDES", "TEXT255", "TEXT32K", "THEN",
    "TIMESTAMP", "TO", "TOP", "TRAILING", "TRUE", "TRUNCATECOLUMNS", "UNION",
    "UNIQUE", "USER", "USING", "VERBOSE", "WALLET", "WHEN", "WHERE", "WITH",
    "WITHOUT",
]

VARCHAR = "varchar"
FLOAT = "float"

# The following values are the minimum and maximum values for MySQL int
# types. https://dev.mysql.com/doc/refman/8.0/en/integer-types.html
SMALLINT = "smallint"
SMALLINT_MIN = -32768
SMALLINT_MAX = 32767

MEDIUMINT = "mediumint"
MEDIUMINT_MIN = -8388608
MEDIUMINT_MAX = 8388607

INT = "int"
INT_MIN = -2147483648
INT_MAX = 2147483647

BIGINT = "bigint"

INT_TYPES = [SMALLINT, MEDIUMINT, INT, BIGINT]

COL_NAME_MAX_LEN = 100

IS_CASE_SENSITIVE = False
