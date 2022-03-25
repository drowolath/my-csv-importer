from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from . import models, tasks

import pandas


class FileUpload(View):
    template_name = "fileStore/upload.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        filename = request.POST['filename']
        filepath = request.POST['filepath']
        nextchunk = request.POST['nextchunk']
        stop = request.POST['stop']
        csv_file = request.FILES['file']

        if filepath == 'null':  # first chunk
            path = f'media/{filename}'
            with open(path, 'wb+') as f:
                for chunk in csv_file.chunks():
                    f.write(chunk)
            obj, _ = models.File.objects.get_or_create(
                path=path,
                name=filename
            )
            obj.complete = bool(int(stop))
            obj.save()
            if int(stop):
                tasks.slice_csv.delay(path)
                print(obj.__dict__)
                return JsonResponse(
                    {'message': 'Uploaded successfully', 'filepath': path}
                )
            return JsonResponse({'filepath': filename})
        else:
            path = f'media/{filename}'
            obj = models.File.objects.get(path=path)
            if not obj.complete:
                with open(path, 'ab+') as f:
                    for chunk in csv_file.chunks():
                        f.write(chunk)
                if int(stop):
                    obj.complete = True
                    obj.save()
                    print(obj.__dict__)
                    tasks.slice_csv.delay(path)
                    return JsonResponse(
                        {'message': 'Uploaded successfully', 'filepath': obj.path}
                    )
                return JsonResponse({'filepath': obj.path})
            else:
                return JsonResponse(
                    {"message": "File is already complete"}
                )
            
