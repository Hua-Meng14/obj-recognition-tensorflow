from django.shortcuts import render
from rest_framework import viewsets
from .models import Image
from .serializers import ImageSerializer
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from urllib import request as urllib_request
import numpy as np
import io

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        if 'image' in request.FILES:
            # Image uploaded via form
            uploaded_file = request.FILES['image']
            image_content = uploaded_file.read()

        elif 'image_url' in request.data:
            # Image provided as URL
            image_url = request.data['image_url']
            image_content = urllib_request.urlopen(image_url).read()

        else:
            return JsonResponse({'error': 'No image or image URL provided'}, status=400)

        # Process the image content as needed
        img = image.load_img(io.BytesIO(image_content), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        model = MobileNetV2(weights='imagenet')

        predictions = model.predict(img_array)
        decoded_predictions = decode_predictions(predictions)

        # Extract the top prediction
        prediction = decoded_predictions[0][0][1]

        # Save the image and prediction to the database
        Image.objects.create(image=ContentFile(image_content, name='uploaded_image.jpg'), prediction=prediction)

        return JsonResponse({'prediction': prediction})
