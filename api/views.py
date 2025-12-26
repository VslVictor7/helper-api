import os
import re
import json
import logging
from pathlib import Path
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.utils.text import get_valid_filename
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

IMAGE_DIR = settings.MEDIA_ROOT / "images"
MOBS_DIR = settings.MEDIA_ROOT / "mobs"
DEATHS_DIR = settings.MEDIA_ROOT / "deaths"

logging.basicConfig(filename="api.log", level=logging.INFO)


class BaseAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        logging.info(f"Request: {request.method} {request.get_full_path()}")
        return super().dispatch(request, *args, **kwargs)


class ImagesView(BaseAPIView):
    def get(self, request):
        try:
            images = os.listdir(IMAGE_DIR)
            return Response({
                "images": [
                    {
                        "filename": image,
                        "name": re.sub(
                            r"([a-z])([A-Z])",
                            r"\1 \2",
                            Path(image).stem
                        )
                    }
                    for image in images
                ]
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImagePNGView(BaseAPIView):
    
    def get(self, request, filename):
        filename = get_valid_filename(filename)
        path = IMAGE_DIR / filename

        if not path.exists():
            return Response(
                {"error": "Imagem não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )

        return FileResponse(
            open(path, "rb"),
            content_type="image/png"
        )


class ImageByNameView(BaseAPIView):

    def get_image_mapping(self):
        mapping = {}
        for image in os.listdir(IMAGE_DIR):
            friendly = Path(image).stem.replace("_", " ")
            mapping[friendly.lower()] = image
            mapping[friendly.replace(" ", "").lower()] = image
        return mapping

    def get(self, request, name):
        try:
            mapping = self.get_image_mapping()
            filename = mapping.get(name.lower()) or mapping.get(
                name.replace(" ", "").lower()
            )

            if not filename:
                return Response(
                    {"error": "Imagem não encontrada."},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                "name": filename.replace(".png", ""),
                "url": f"{request.build_absolute_uri('/')}images/png/{filename}"
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MobsView(BaseAPIView):
    def get(self, request):
        path = MOBS_DIR / "mobs.json"

        if not path.exists():
            return Response(
                {"error": "Arquivo JSON de mobs não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=4),
            content_type="application/json; charset=utf-8"
        )


class DeathsView(BaseAPIView):
    def get(self, request):
        path = DEATHS_DIR / "deaths.json"

        if not path.exists():
            return Response(
                {"error": "Arquivo JSON de mobs nao encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        return HttpResponse(
            json.dumps(data, ensure_ascii=False, indent=4),
            content_type="application/json; charset=utf-8"
        )