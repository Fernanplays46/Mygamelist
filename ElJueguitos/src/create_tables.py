#from mgl.domain.database import Base, engine
#from mgl.domain import models

print("🛠 Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")
