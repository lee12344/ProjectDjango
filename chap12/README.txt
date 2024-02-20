1. 준비
pip install easyocr

2. 폴더
chap12안에 uploaded_images 폴더 생성

3. 실행
python app3.py

4. api호출
post 방식으로 http://localhost:5001/upload_and_extract_license_plate_text

    <form action="/upload_and_extract_license_plate_text" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>