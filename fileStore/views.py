from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View


class FileUpload(View):
    template_name = "fileStore/upload.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        filename = request.POST['filename']
        csv_file = request.FILE['file'].read()

        # if one parameter is missing
        # consider it an invalid request

        if not (filename and filepath and csv_file):
            return JsonResponse({'message': 'Invalid request'})
        else:
            with open(f'media/{filename}', 'wb+') as f:
                f.write(csv_file)
            return JsonResponse({'message': 'Upload successfull'})
