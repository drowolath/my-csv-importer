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
        csv_file = request.FILES['file'].read()

        if filepath == 'null':  # first chunk
            path = f'media/{filename}'
            #with open(path, 'wb+') as f:
            #    f.write(csv_file)
            obj, _ = models.File.objects.get_or_create(
                path=path,
                name=filename
            )
            obj.complete = int(stop)
            obj.save()
            print(obj.__dict__)
            if int(stop):
                df = pandas.read_csv(path)
                limit = 0
                while limit <= df.shape[0]:
                    data = df[limit:limit+100].to_json()
                    tasks.store_products.delay(data)
                    limit += 100
                return JsonResponse(
                    {'message': 'Uploaded successfully', 'filepath': path}
                )
            return JsonResponse({'filepath': filename})
        else:
            path = f'media/{filename}'
            obj = models.File.objects.get(path=path)
            print(obj.__dict__)
            if not obj.complete:
                #with open(f'media/{filename}', 'ab+') as f:
                #    f.write(csv_file)
                if int(stop):
                    obj.complete = True
                    obj.save()
                    df = pandas.read_csv(path)
                    limit = 0
                    while limit <= df.shape[0]:
                        data = df[limit:limit+100].to_json()
                        tasks.store_products.delay(data)
                        limit += 100
                    return JsonResponse(
                        {'message': 'Uploaded successfully', 'filepath': obj.path}
                    )
                return JsonResponse({'filepath': obj.path})
            else:
                return JsonResponse(
                    {"message": "File is already complete"}
                )
            
