## obj-recognition-tensorflow

# Clone project
- git clone `https://github.com/Hua-Meng14/obj-recognition-tensorflow.git`
- cd `obj-recognition-tensorflow`
# Installations
  - tensorflow: `pip install tensorflow`
  - django_rest_framework: `pip install djangorestframework`
# Migrations
Inside direcotry contains `manage.py` file:
  - run `python manage.py makemigrations`
  - run `python manage.py migrate`
# Run project
  - run `python manage.py runserver`
# Sample Request:
  - Upload Image via file path: `curl -X POST -H "Content-Type: multipart/form-data" -F "image=@path/to/your/image.jpg" http://127.0.0.1:8000/api/images/`
  - Image url: `curl --location --request GET 'http://127.0.0.1:8000/api/images/' \
--form 'image_url="{{img_url}}"'`
