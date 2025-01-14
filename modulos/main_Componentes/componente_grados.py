from modulos.db_conector import conectar
import streamlit as st



def obtener_grados():
    """
    Obtiene la lista de grados desde la base de datos.
    """
    conn = conectar()
    cursor = conn.cursor()
    query = 'SELECT "ID_GRADOS", "NOMBRE_GRADO" FROM "GRADOS";'
    cursor.execute(query)
    grados = cursor.fetchall()
    cursor.close()
    conn.close()
    return grados

def agregar_grado(nombre_grado):
    """
    Agrega un nuevo grado a la base de datos.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = 'INSERT INTO "GRADOS" ("NOMBRE_GRADO", "FECHA_CREACION") VALUES (%s, NOW());'
        cursor.execute(query, (nombre_grado,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al agregar el grado: {e}")
        return False

def modificar_grado(id_grado, nuevo_nombre):
    """
    Modifica el nombre de un grado existente.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = 'UPDATE "GRADOS" SET "NOMBRE_GRADO" = %s WHERE "ID_GRADOS" = %s;'
        cursor.execute(query, (nuevo_nombre, id_grado))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al modificar el grado: {e}")
        return False

def eliminar_grado(id_grado):
    """
    Elimina un grado de la base de datos si no tiene secciones asociadas.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Verificar si el grado tiene secciones asociadas
        query_check = 'SELECT COUNT(*) FROM "SECCIONES" WHERE "ID_GRADO" = %s;'
        cursor.execute(query_check, (id_grado,))
        if cursor.fetchone()[0] > 0:
            st.warning("No se puede eliminar el grado porque tiene secciones asociadas.")
            return False
        # Eliminar el grado
        query_delete = 'DELETE FROM "GRADOS" WHERE "ID_GRADOS" = %s;'
        cursor.execute(query_delete, (id_grado,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al eliminar el grado: {e}")
        return False

def asignar_grado_a_seccion(id_grado, id_seccion):
    """
    Asigna un grado a una sección existente.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = 'UPDATE "SECCIONES" SET "ID_GRADO" = %s WHERE "ID_SECCION" = %s;'
        cursor.execute(query, (id_grado, id_seccion))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al asignar el grado a la sección: {e}")
        return False