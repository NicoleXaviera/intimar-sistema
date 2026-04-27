### intimar

Sistema de gestión y reservas para Intimar

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app intimar_erp
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/intimar_erp
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit



# Intimar ERP - Guía de Instalación y Desarrollo

Este proyecto es la migración del sistema **Intimar** al framework **Frappe**. Esta guía detalla cómo se configuró el entorno desde cero y para qué sirve cada componente.

---

## 🚀 Guía de Inicio Rápido (Uso Diario)

Para empezar a trabajar cada día, abre tu terminal de Ubuntu y ejecuta:

```bash
cd ~/frappe-bench
bench start
```
Luego entra en tu navegador a: [http://localhost:8000](http://localhost:8000)

---

## 🛠️ Manual de Instalación desde Cero (Paso a Paso)

Si alguna vez necesitas repetir todo el proceso en otra computadora, estos son los comandos exactos en el orden correcto:

### 1. Preparación de Windows (PowerShell como Admin)
```powershell
wsl --install
# Reiniciar computadora después de esto
```

### 2. Dependencias iniciales (Terminal de Ubuntu)
```bash
# Actualizar el sistema Linux
sudo apt update && sudo apt upgrade -y

# Instalar Python, MariaDB, Redis y librerías de desarrollo
sudo apt install -y python3-dev python3-pip python3-venv git curl redis-server mariadb-server libmysqlclient-dev

# Instalar Node.js 18 (Específico para Frappe)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar Yarn
sudo npm install -g yarn
```

### 3. Configuración de Base de Datos
1.  **Editar archivo de configuración:**
    `sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf`
2.  **Agregar bajo [mysqld]:**
    ```ini
    character-set-client-handshake = FALSE
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci
    ```
3.  **Reiniciar y asegurar MySQL:**
    ```bash
    sudo service mysql restart
    sudo mysql_secure_installation
    # Respuestas: Enter -> n -> Y (poner clave) -> Y -> Y -> Y -> Y
    ```

### 4. Instalación de Frappe Bench
```bash
# Instalar el comando bench
sudo pip3 install frappe-bench --break-system-packages

# Inicializar el entorno (Tarda 5-10 min)
cd ~
bench init frappe-bench --frappe-branch version-15
```

### 5. Configuración del Proyecto Intimar
```bash
cd ~/frappe-bench

# Crear el sitio (Base de Datos)
bench new-site intimar.localhost

# Crear la aplicación personalizada
bench new-app intimar_erp

# Instalar la app en el sitio
bench --site intimar.localhost install-app intimar_erp

# Establecer sitio por defecto
bench use intimar.localhost
```

---

## 🏗️ Conceptos Clave

1.  **WSL2:** Tu entorno Linux real dentro de Windows.
2.  **MariaDB:** Donde viven tus datos. Clave root: la que pusiste en `mysql_secure_installation`.
3.  **Bench:** Tu herramienta de control.
4.  **Site (`intimar.localhost`):** El sitio web que contiene la base de datos.
5.  **App (`intimar_erp`):** Donde escribes tu código (Python/JS).

---

## ❓ Comandos Útiles

- **Ver logs del servidor:** `bench start`
- **Consola de Python con el contexto de la app:** `bench --site intimar.localhost console`
- **Limpiar caché:** `bench clear-cache`
- **Migrar cambios de base de datos:** `bench migrate`

---
*Desarrollado para Intimar - 2024*
