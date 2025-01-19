# บอทแจ้งเตือนการ Live Streaming บน Twitch และ YouTube

โปรเจกต์นี้เป็น Discord Bot สำหรับแจ้งเตือนใน Discord Server เมื่อผู้ใช้งานเริ่ม Live Streaming บน Twitch หรือ YouTube โดยบอทนี้เชื่อมต่อกับ Twitch Helix API และ YouTube Data API เพื่อตรวจสอบสถานะการสตรีม

---

## ความสามารถของบอท
- แจ้งเตือนในช่อง Discord เมื่อมีการ Live Streaming บน Twitch หรือ YouTube
- รองรับการแจ้งเตือนหลายสตรีมเมอร์ (กำหนดค่าผ่านไฟล์ `.env` หรือฐานข้อมูล)
- โครงสร้างโค้ดแบบโมดูล ใช้งานสะดวกสำหรับการเพิ่มคำสั่งหรือปรับปรุงในอนาคต

---

## ข้อกำหนดเบื้องต้น

### สิ่งที่ต้องมี
1. **Python 3.9 ขึ้นไป**  
   [ดาวน์โหลด Python ได้ที่นี่](https://www.python.org/)
   
2. **ไลบรารีที่จำเป็น**  
   ติดตั้งแพ็คเกจที่ต้องใช้ด้วยคำสั่ง:
   ```bash
   pip install -r requirements.txt
   ```

3. **Twitch API**  
   - สมัคร Developer Application ที่ [Twitch Developer Console](https://dev.twitch.tv/console/apps)
   - รับ `Client ID` และ `Client Secret`

4. **YouTube API**  
   - สร้าง API Key ผ่าน [Google Cloud Console](https://console.cloud.google.com/)

---

## การตั้งค่า
1. **สร้างไฟล์ `.env`** ในโฟลเดอร์โปรเจกต์ และเพิ่มค่าต่อไปนี้:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   TWITCH_CLIENT_ID=your_twitch_client_id
   TWITCH_CLIENT_SECRET=your_twitch_client_secret
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

2. **เริ่มรันบอท**  
   ใช้คำสั่ง:
   ```bash
   python main.py
   ```

---

## โครงสร้างไฟล์
```
src/
├── client/
│   ├── logic/           # ฟังก์ชันประมวลผลหลัก
│   ├── client.py        # ตัวจัดการ Client หลักของ Discord Bot
├── cog/
│   ├── commands/        # โมดูลคำสั่งใน Discord
│   ├── event-listener/  # ตัวจัดการ Event
├── module/              # โมดูลสำหรับ API ของ Twitch และ YouTube
├── public/              # ไฟล์สาธารณะ เช่น รูปภาพ
.env                     # การตั้งค่าคีย์ API
main.py                  # ไฟล์เริ่มต้นบอท
requirements.txt         # รายการไลบรารีที่ต้องติดตั้ง
```
