class FileUpload {
    constructor(input) {
	this.input = input
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
	document.getElementById('uploaded_files').innerHTML = progress
    }

}

(function ($) {
    $('#submit').on('click', (event) => {
	event.preventDefault();
	var uploader = new FileUpload(document.querySelector('#fileupload'))
	uploader.upload();
    });
})(jQuery);
    
