from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os

# إعداد مسار tesseract إذا لم يكن موجوداً في PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_and_boxes(image_path):
    """استخراج النص والمربعات المحيطة به من الصورة"""
    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    return data




def remove_text_from_image(image, boxes):
    """إزالة النصوص من الصورة عن طريق تغطيتها بخلفية الصورة"""
    draw = ImageDraw.Draw(image)

    # إزالة النص عن طريق ملء المناطق بالنصوص بخلفية مشابهة
    for i in range(len(boxes['level'])):
        if boxes['text'][i].strip():
            (x, y, w, h) = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
            draw.rectangle((x, y, x + w, y + h), fill=image.getpixel((x, y)))

    return image


def get_text_color(image, boxes):
    """تحديد لون النص الأصلي بناءً على موقع النص"""
    text_colors = []
    for i in range(len(boxes['level'])):
        if boxes['text'][i].strip():
            # نحصل على لون أول بكسل في منطقة النص
            (x, y, w, h) = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
            text_colors.append(image.getpixel((x, y)))  # أخذ لون البكسل في الزاوية العلوية اليسرى
    return text_colors


def add_text_to_image(image, boxes, edited_text, text_colors):
    """إضافة النص المعدل إلى الصورة في نفس الأماكن القديمة وبنفس الألوان الأصلية"""
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # يمكنك تغيير الخط هنا إذا لزم الأمر

    text_index = 0  # لمطابقة النصوص القديمة والجديدة
    for i in range(len(boxes['level'])):
        if boxes['text'][i].strip():
            (x, y, w, h) = (boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i])
            if text_index < len(edited_text):
                # استخدام لون واضح
                text_color = (255, 255, 255)  # الأبيض
                draw.text((x, y), edited_text[text_index], font=font, fill=text_color)
                draw.text((50, 50), "Hello", font=font, fill=(255, 255, 255))  # استخدم الإحداثيات المناسبة
                text_index += 1
            else:
                break

    return image




def main():
    # المسار إلى الصورة الأصلية
    image_path = 'test-image.png'  # ضع اسم ملف الصورة هنا

    # استخراج النصوص والمربعات المحيطة بها
    image = Image.open(image_path)
    boxes = extract_text_and_boxes(image_path)

    # استخراج النصوص الحالية لعرضها على المستخدم
    original_text = ''.join(boxes['text']).strip()
    print("النص المستخرج:")
    print(original_text)

    # # تعديل النص
    # edited_text = input("أدخل النص المعدل: ").split()
    #
    # # استخراج لون النصوص الأصلية
    # text_colors = get_text_color(image, boxes)
    #
    # # إزالة النص القديم من الصورة
    # clean_image = remove_text_from_image(image, boxes)
    #
    # # إضافة النص الجديد إلى الصورة بنفس اللون الأصلي
    # output_image = add_text_to_image(clean_image, boxes, edited_text, text_colors)
    #
    # # حفظ الصورة المعدلة
    # output_path = 'output_image.png'  # اسم ملف الصورة المعدلة
    # output_image.save(output_path)
    # print(f"تم حفظ الصورة المعدلة بنجاح في: {output_path}")
    # output_image.show()


if __name__ == "__main__":
    main()
