import pymysql
import time
import os
from dotenv import load_dotenv
import logging
import pymysql.cursors
from datetime import datetime, timedelta, timezone

# โหลดค่าจาก .env
load_dotenv()

# เชื่อมต่อกับฐานข้อมูล MySQL บน XAMPP
def connect_db():
    """เชื่อมต่อกับฐานข้อมูล MySQL"""
    try:
        db_name = os.getenv("DB_NAME")
        
        if not db_name:
            raise ValueError("Database name (DB_NAME) is not set in .env file!")
        
        return pymysql.connect(
            host=os.getenv("HOST_DB"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD_DB"),
            database=db_name,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"❌ MySQL Error: {e}")
        raise  # Re-raise the error after logging it
    except ValueError as ve:
        print(f"❌ ValueError: {ve}")
        raise  # Re-raise the error after logging it
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise  # Re-raise the error after logging it


# สร้างตาราง Users และ OTP Codes ถ้ายังไม่มี
def create_tables():
    db = connect_db()
    cursor = db.cursor()
    
    sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_otp = """
    CREATE TABLE IF NOT EXISTS otp_codes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        otp VARCHAR(6) NOT NULL,
        expires_at BIGINT NOT NULL
    );
    """
    cursor.execute(sql_users)
    cursor.execute(sql_otp)
    db.commit()
    db.close()


def create_readonly_user(email: str, username: str, password: str) -> bool:
    db = connect_db()
    cursor = db.cursor()

    try:
        username_safe = pymysql.converters.escape_string(username)
        password_safe = pymysql.converters.escape_string(password)

        db.begin()  # ✅ ใช้ Transaction

        # ✅ ตรวจสอบว่า MySQL user มีอยู่แล้วหรือไม่
        sql_check_user = "SELECT COUNT(*) FROM mysql.user WHERE user = %s AND host = 'localhost';"
        cursor.execute(sql_check_user, (username,))
        result = cursor.fetchone()

        logging.debug(f"🔍 Query Result: {result}")  # ✅ Debug Log เช็คค่าจริงที่ได้

        # ✅ ป้องกัน KeyError: ตรวจสอบ `result` ก่อนใช้ index `[0]`
        user_exists = bool(result and isinstance(result, tuple) and len(result) > 0 and result[0] > 0)

        # ✅ ถ้า user ไม่มี → สร้างใหม่
        if not user_exists:
            sql_create_user = f"CREATE USER '{username_safe}'@'localhost' IDENTIFIED BY '{password_safe}';"
            cursor.execute(sql_create_user)
        else:
            sql_alter_user = f"ALTER USER '{username_safe}'@'localhost' IDENTIFIED BY '{password_safe}';"
            cursor.execute(sql_alter_user)

        # ✅ ให้สิทธิ์ SELECT แก่ user
        sql_grant_privileges = f"GRANT SELECT ON {os.getenv('DB_NAME')}.* TO '{username_safe}'@'localhost';"
        cursor.execute(sql_grant_privileges)

        # ✅ บันทึกข้อมูลลงตาราง users **หลังจากสร้าง MySQL User สำเร็จ**
        sql_insert_user = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        cursor.execute(sql_insert_user, (email, username_safe, password_safe))

        db.commit()  # ✅ บันทึกทั้งหมด
        logging.info(f"✅ สร้าง User `{username_safe}` สำเร็จ!")
        return True

    except pymysql.MySQLError as e:
        db.rollback()  # ❌ ถ้า Error, ยกเลิกทั้งหมด
        logging.error(f"❌ สร้าง User ไม่สำเร็จ: {e}")
        return False

    finally:
        cursor.close()
        db.close()

# บันทึก OTP ลง Database
def save_otp(email: str, otp: str):
    db = connect_db()
    cursor = db.cursor()
    expires_at = int(time.time()) + 300  # หมดอายุใน 5 นาที
    sql = "INSERT INTO otp_codes (email, otp, expires_at) VALUES (%s, %s, %s)"
    cursor.execute(sql, (email, otp, expires_at))
    db.commit()
    db.close()

# ตรวจสอบ OTP ใน Database
def verify_otp(email: str, user_otp: str) -> bool:
    db = connect_db()
    cursor = db.cursor()
    delete_expired_otps()

    sql = "SELECT otp FROM otp_codes WHERE email = %s AND expires_at > %s"
    cursor.execute(sql, (email, int(time.time())))
    result = cursor.fetchone()
    
    if result and result["otp"] == user_otp:
        delete_otp(email)
        db.close()
        return True
    db.close()
    return False

# ลบ OTP ที่หมดอายุ
def delete_expired_otps():
    db = connect_db()
    cursor = db.cursor()
    sql = "DELETE FROM otp_codes WHERE expires_at <= %s"
    cursor.execute(sql, (int(time.time()),))
    db.commit()
    db.close()

# ลบ OTP หลังจากใช้งาน
def delete_otp(email: str):
    db = connect_db()
    cursor = db.cursor()
    sql = "DELETE FROM otp_codes WHERE email = %s"
    cursor.execute(sql, (email,))
    db.commit()
    db.close()

def check_email_exists(email: str) -> bool:
    """ตรวจสอบว่าอีเมลมีอยู่แล้วใน Database หรือไม่"""
    db = connect_db()
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)  # ✅ ใช้ dictionary cursor

    try:
        sql = "SELECT COUNT(*) AS count FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()

        logging.info(f"🔍 Email check result: {result}")  # ✅ Debug log

        # ✅ ตรวจสอบ result ก่อนเข้าถึงค่า
        if result and "count" in result:
            return result["count"] > 0

        return False
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
        return False
    finally:
        cursor.close()
        db.close()

def create_quarantine_table():
    """ create table quarantine_people_time if not exists"""
    db = connect_db()
    cursor = db.cursor()

    sql_quarantine = """
    CREATE TABLE IF NOT EXIST quarantine_people_time (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    quarantine_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason TEXT NOT NULL
    );
    """
    cursor.execute(sql_quarantine)
    db.commit()
    db.close()

def save_quarantine(user_id: int, username: str, reason: str):
    """Save user quarantine data in the database."""
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = """
        INSERT INTO quarantine_people_time (user_id, username, reason, quarantine_time)
        VALUES (%s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE quarantine_time = NOW()
        """
        cursor.execute(sql, (user_id, username, reason))
        db.commit()
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        cursor.close()
        db.close()


def check_unquarantine_users():
    """check who should be unquarantined"""
    try:
        db = connect_db()
        cursor = db.cursor()

        sql = "SELECT user_id, username FROM quarantine_people_time WHERE quarantine_time < DATE_SUB(NOW(), INTERVAL 14 DAY)"
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()

        return result
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
        return False
    
def remove_from_quarantine(user_id: int):
    """remove the user from the quarantine table"""
    try:
        db = connect_db()
        cursor = db.cursor()

        sql = "DELETE FROM quarantine_people_time WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        db.commit()
        db.close()
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
        return False
    

def get_quarantine_remaining_time(user_id: int):
    """Get the remaining time before a user is unquarantined."""
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = "SELECT quarantine_time FROM quarantine_people_time WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()

        if not result or not result["quarantine_time"]:
            return "User is not in quarantine."

        quarantine_time = result["quarantine_time"].replace(tzinfo=timezone.utc)
        end_time = quarantine_time + timedelta(days=14)
        now = datetime.now(timezone.utc)
        remaining_time = end_time - now

        if remaining_time.total_seconds() <= 0:
            return "User is eligible for unquarantine."

        return f"Time left: {remaining_time.days}d {remaining_time.seconds // 3600}h {(remaining_time.seconds // 60) % 60}m"
    
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
        return "Database error."
    finally:
        cursor.close()
        db.close()

def store_quarantine_message(user_id: int, message_id: int, channel_id: int):
    """ Store the message ID of the quarantine embed for auto-updates. """
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = """
        UPDATE quarantine_people_time 
        SET message_id = %s, channel_id = %s
        WHERE user_id = %s
        """
        cursor.execute(sql, (message_id, channel_id, user_id))
        db.commit()
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        cursor.close()
        db.close()

def get_quarantine_messages():
    """Retrieve all active quarantine messages."""
    db = connect_db()
    cursor = db.cursor()

    try:
        sql = "SELECT user_id, message_id, channel_id FROM quarantine_people_time WHERE message_id IS NOT NULL"
        cursor.execute(sql)
        return cursor.fetchall()  # Returns a list of dicts
    except pymysql.MySQLError as e:
        logging.error(f"❌ Database error: {e}")
        return []
    finally:
        cursor.close()
        db.close()
