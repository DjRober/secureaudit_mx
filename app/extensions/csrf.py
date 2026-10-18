from flask_wtf.csrf import CSRFProtect

#Protección CSRF global (RNF-01.2, T-04): todo POST/PUT/PATCH/DELETE debe traer un token válido
csrf = CSRFProtect()
