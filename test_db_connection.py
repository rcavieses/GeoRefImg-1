import sys
from app.config import settings
from app.database import engine

def test_connection():
    """Prueba la conexión a la base de datos"""
    print(f"🔧 Ambiente: {settings.app_env}")
    print(f"📊 Base de datos configurada: {settings.database_url.split('@')[0]}...")
    print()

    try:
        with engine.connect() as connection:
            print("✅ Conexión exitosa a la base de datos")

            # Obtener información de la conexión (compatible con pymssql)
            try:
                from sqlalchemy import text
                result = connection.execute(text("SELECT SERVERPROPERTY('ProductVersion') as version"))
                version = result.scalar()
                if version:
                    print(f"📌 SQL Server Version: {version}")
            except Exception as version_error:
                print(f"📌 Base de datos conectada (versión no disponible)")

            return True
    except Exception as e:
        print(f"❌ Error de conexión:")
        print(f"   {type(e).__name__}: {str(e)}")
        
        # Sugerencias de troubleshooting
        if "ODBC" in str(e):
            print("\n💡 Tip: Verifica que el ODBC Driver 17 esté instalado")
        elif "Login failed" in str(e):
            print("\n💡 Tip: Verifica las credenciales en el archivo .env")
        elif "Cannot open database" in str(e):
            print("\n💡 Tip: Verifica que la base de datos existe en Azure SQL")
        elif "timeout" in str(e).lower():
            print("\n💡 Tip: Verifica la conectividad de red y el firewall de Azure")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
