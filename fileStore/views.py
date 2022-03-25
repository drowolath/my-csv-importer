from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from . import models, tasks

import pandas


class FileUpload(View):
    template_name = "fileStore/upload.html"

    def close_file(self, stop, path):
        if int(stop):
            tasks.slice_csv.delay(path)
            return JsonResponse(
                {'message': 'Uploaded successfully', 'filepath': path}
            )
        return JsonResponse({'filepath': path})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        filename = request.POST['filename']
        filepath = request.POST['filepath']
        nextchunk = request.POST['nextchunk']
        stop = request.POST['stop']
        csv_file = request.FILES['file'].read()

        path = f'media/{filename}'

        if filepath == 'null':  # first chunk
            with open(path, 'wb+') as f:
                f.write(csv_file)
            obj, _ = models.File.objects.get_or_create(
                path=path,
                name=filename
            )
            obj.complete = bool(int(stop))
            obj.save()
            return self.close_file(stop, path)
        else:
            path = f'media/{filename}'
            obj = models.File.objects.get(path=path)
            if not obj.complete:
                with open(path, 'ab+') as f:
                    f.write(csv_file)
                obj.complete = bool(int(stop))
                obj.save()
                return self.close_file(stop, path)
            else:
                return JsonResponse(
                    {"message": "File is already complete"}
                )
            
