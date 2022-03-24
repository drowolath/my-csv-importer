from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View


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
            with open(f'media/{filename}', 'wb+') as f:
                f.write(csv_file)
            if int(stop):
                return JsonResponse({'message': 'Upload successfull'})
            return JsonResponse({'message': filename})
        else:
            path = f'media/{filepath}'
            with open(f'media/{filename}', 'ab+') as f:
                f.write(csv_file)
            if int(stop):
                return JsonResponse({'message': 'Upload successfull'})
            return JsonResponse({'message': filename})
            
