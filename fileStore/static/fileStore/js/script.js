class FileUpload {
    constructor(input) {
	this.input = input;
	this.chunk_size = 10 * 1024 * 1024;
    }

    upload() {
	var progress = `
          <div class="file-details">
            <p class="filename"></p>
            <small class="textbox"></small>
            <div class="progress" style="margin-top: 5px;">
              <div class="progress-bar bg-infos" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
              </div>
            </div>
          </div>`
	document.getElementById('uploaded_files').innerHTML = progress;
	this.file = this.input.files[0];
	this.upload_chunk(0, null);
    }

    upload_chunk(start, path) {
	var form = new FormData();
	var filepath = path;
	var nextChunk = start + this.max_length + 1;
	var currentChunk = this.file.slice(start, nextChunk);
	var uploadedChunk = start + currentChunk.size;

	form.append('filename', this.file.name);
	form.append('file', currentChunk);
	form.append('filepath', filepath);
	form.append('nextchunk', nextChunk);
	$('.filename').text(this.file.name);
	$('.textbox').text("Uploading file...");

	$.ajaxSetup({
	    // csrf token ... tricky django stuff
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        $.ajax({
            xhr: function () {
                var xhr = new XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        if (this.file.size < this.max_length) {
                            var percent = Math.round((e.loaded / e.total) * 100);
                        } else {
                            var percent = Math.round((uploadedChunk / this.file.size) * 100);
                        }
                        $('.progress-bar').css('width', percent + '%')
                        $('.progress-bar').text(percent + '%')
                    }
                });
                return xhr;
            },

            url: '/upload/',
            type: 'POST',
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            data: form,
            error: function (xhr) {
                alert(xhr.statusText);
            },
            success: function (res) {
                if (nextchunk < this.file.size) {
                    filepath = res.filepath
                    this.upload_file(nextchunk, filepath);
                } else {
                    $('.textbox').text(res.message);
                    alert(res.message)
                }
            }
        });
    }
}

(function ($) {
    $('#submit').on('click', (event) => {
	event.preventDefault();
	var uploader = new FileUpload(document.querySelector('#fileupload'))
	uploader.upload();
    });
})(jQuery);
    
