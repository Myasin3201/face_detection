# ---------------------------------------------------------
# Dockerfile سایت تشخیص چهره
# این فایل «دستورالعمل ساخت کانتینر» است — یعنی می‌گوید چطور
# یک محیط ایزوله و قابل‌حمل بسازیم که برنامه ما همیشه یکسان
# (چه روی لپ‌تاپ شما، چه روی سرور گوگل، چه روی Hugging Face) اجرا شود.
# ---------------------------------------------------------

# ۱) از یک ایمیج پایه پایتون شروع می‌کنیم (نسخه سبک/slim برای حجم کمتر)
FROM python:3.11-slim

# ۲) پکیج‌های سیستمی موردنیاز OpenCV/Pillow/torch را نصب می‌کنیم
#    (بدون این‌ها معمولاً هنگام import کتابخانه‌های تصویر خطا می‌گیرید)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# ۳) پوشه کاری داخل کانتینر
WORKDIR /backend_of_faceDetection

# ۴) اول فقط requirements.txt را کپی می‌کنیم تا Docker بتواند لایه نصب پکیج‌ها
#    را کش کند (اگر فقط کد را عوض کنید، دیگر لازم نیست همه پکیج‌ها دوباره نصب شوند)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# ۵) حالا بقیه فایل‌های پروژه (app.py، templates، مدل و...) را کپی می‌کنیم
COPY . .

# ۶) پوشه‌های آپلود و نتیجه را از قبل بسازیم
RUN mkdir -p static/uploads static/results

# ۷) پورتی که برنامه داخلش گوش می‌دهد. Cloud Run و HF Spaces
#    این مقدار را خودشان با متغیر محیطی PORT بازنویسی می‌کنند.
ENV PORT=8080
EXPOSE 8080

# ۸) دستور اجرای نهایی: به‌جای سرور توسعه Flask، از gunicorn استفاده می‌کنیم
#    (پایدارتر و برای اجرای واقعی مناسب است)
CMD exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --timeout 120 backend_of_faceDetection:backend_of_faceDetection
