import ibm_db

conn = ibm_db.connect(
    "DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT"
    "=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=kzg03731;PWD=f4Jb4Y6d8YHaha5F",
    '', '')
print(conn)
print("connection successful...")
