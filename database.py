from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://0fvx8dgasopvzuc9g07j:pscale_pw_xQUDLz8qHU22EVaWU6JPm6jxJMRPWvG6CPZHUX7yrUl@ap" \
                       "-south.connect.psdb.cloud/bank_management?charset=utf8mb4"
mydb = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })
my_cursor = mydb.connect()
print(my_cursor)
