import re

__all__ = ['redact_copy_sql']

def redact_credentials(sql):
    """
    Redact any credentials explicitly represented in SQL (e.g. COPY statement)
    """

    sql_censored = re.sub(pattern, 'CREDENTIALS REDACTED', sql, flags=re.IGNORECASE)
    
    return sql_censored