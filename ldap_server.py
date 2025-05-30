from ldap3 import Server, Connection, ALL

server = Server('ldap://0.0.0.0:389', get_info=ALL)
connection = Connection(server, auto_bind=True)
print("LDAP server started on port 389. Waiting for connections...")
connection.serve_forever()
