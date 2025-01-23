import logging
import os




class AppLogger:
    """
    Clase para gestionar los logs de la aplicación.
    """
        # Ruta personalizada para los logs
    

    # Crear instancia del logger


    def __init__(self, log_file="logs/app.log"):
        """
        Inicializa el logger con la configuración básica.
        
        Args:
            log_file (str): Ruta al archivo donde se almacenarán los logs.
        """
                # Crear directorio si no existe
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger()

    def info(self, message):
        """
        Registra un mensaje informativo.
        
        Args:
            message (str): Mensaje a registrar.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Registra un mensaje de advertencia.
        
        Args:
            message (str): Mensaje a registrar.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Registra un mensaje de error.
        
        Args:
            message (str): Mensaje a registrar.
        """
        self.logger.error(message)
