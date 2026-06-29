#!/usr/bin/env python3
"""
Script de setup para GeoRef Colaborativo

Ejecutar: python setup.py
"""

import os
import sys
from getpass import getpass
from pathlib import Path

def setup_database():
    """Inicializa la base de datos"""
    print("\n📚 Inicializando Base de Datos...")
    
    try:
        from app.database import init_db
        init_db()
        print("✅ Base de datos inicializada")
        return True
    except Exception as e:
        print(f"❌ Error inicializando BD: {e}")
        return False

def create_admin_user():
    """Crea usuario admin inicial"""
    print("\n👤 Crear Usuario Admin")
    print("-" * 40)
    
    from app.database import SessionLocal
    from app.services.user_service import UserService
    
    db = SessionLocal()
    
    try:
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = getpass("Contraseña: ")
        password_confirm = getpass("Confirmar contraseña: ")
        
        if password != password_confirm:
            print("❌ Las contraseñas no coinciden")
            return False
        
        # Validar contraseña
        from app.utils.validators import validate_password
        is_valid, msg = validate_password(password)
        if not is_valid:
            print(f"❌ Contraseña débil: {msg}")
            return False
        
        # Crear usuario
        user = UserService.create_user(
            db,
            username=username,
            email=email,
            password=password,
            first_name="Admin",
            last_name="User"
        )
        
        # Actualizar rol a admin
        user.role = "admin"
        db.commit()
        
        print(f"✅ Admin creado: {username}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

def check_env():
    """Verifica archivo .env"""
    print("\n🔧 Configuración de Entorno")
    print("-" * 40)
    
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("⚠️  No encontrado .env")
            response = input("¿Copiar desde .env.example? (s/n): ").lower()
            if response == "s":
                import shutil
                shutil.copy(".env.example", ".env")
                print("✅ .env creado desde .env.example")
                print("⚠️  Edita .env con tus credenciales de Azure SQL")
                return False
        else:
            print("❌ No encontrado .env ni .env.example")
            return False
    else:
        print("✅ .env encontrado")
        return True

def main():
    print("\n" + "="*50)
    print("🗺️  GeoRef Colaborativo - Setup Inicial")
    print("="*50)
    
    # 1. Verificar .env
    env_ok = check_env()
    
    if not env_ok:
        print("\n⚠️  Por favor, configura el archivo .env antes de continuar")
        print("   Instrucciones en: AZURE_SQL_SETUP.md")
        sys.exit(1)
    
    # 2. Inicializar BD
    if not setup_database():
        print("\n❌ No se pudo inicializar la BD")
        print("   Verifica tu conexión a Azure SQL en .env")
        sys.exit(1)
    
    # 3. Crear admin
    print("\n¿Crear usuario admin? (recomendado) (s/n):", end=" ")
    response = input().lower()
    
    if response == "s":
        if not create_admin_user():
            print("⚠️  Admin no creado, pero BD inicializada")
    
    # 4. Test de conexión
    print("\n🧪 Testing conexión a BD...")
    try:
        from app.database import engine
        with engine.connect() as conn:
            print("✅ Conexión exitosa a BD")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)
    
    # 5. Done
    print("\n" + "="*50)
    print("✅ Setup completado")
    print("="*50)
    print("\n🚀 Para ejecutar la app:")
    print("   streamlit run streamlit_app.py")
    print("\n📚 Documentación:")
    print("   - README_FASE1.md - Setup general")
    print("   - README_FASE2.md - Autenticación")
    print("   - AZURE_SQL_SETUP.md - Azure SQL")

if __name__ == "__main__":
    main()
