from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from . import models


class FileUpload(View):
    template_name = "fileStore/upload.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        filename = request.POST['filename']
        filepath = request.POST['filepath']
        nextchunk = request.POST['nextchunk']
        stop = request.POST['stop']
        csv_file = request.FILES['file'].read()

        if filepath == 'null':  # first chunk
            path = f'media/{filename}'
            with open(path, 'wb+') as f:
                f.write(csv_file)
            models.File.objects.get_or_create(
                path=path,
                name=filename,
                complete=bool(int(stop))
            )
            if int(stop):
                return JsonResponse(
                    {'message': 'Uploaded successfully', 'filepath': path}
                )
            return JsonResponse({'filepath': filename})
        else:
            path = f'media/{filename}'
            obj = models.File.objects.get(path=path)
            if not obj.complete:
                with open(f'media/{filename}', 'ab+') as f:
                    f.write(csv_file)
                if int(stop):
                    obj.complete = True
                    obj.save()
                    return JsonResponse(
                        {'message': 'Uploaded successfully', 'filepath': obj.path}
                    )
                return JsonResponse({'filepath': obj.path})
            else:
                return JsonResponse(
                    {"message": "File is already complete"}
                )
            