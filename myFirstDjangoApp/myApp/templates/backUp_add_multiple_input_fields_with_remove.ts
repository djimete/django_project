<!--input type="file" id="fileInput" name="files[]" multiple accept="image/*, .pdf"-->
<input type="file" id="fileInput" name="myFiles[]" multiple>
<button id="uploadButton">Envoyer</button>                
<div id="fileListContainer"></div>


<script>
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const fileListContainer = document.getElementById('fileListContainer');
    let selectedFiles = []; // To store the actual File objects

    fileInput.addEventListener('change', (event) => {
        const files = Array.from(event.target.files);
        files.forEach(file => {
            selectedFiles.push(file); // Add to our internal array
            displayFile(file);
        });
        // Clear the input value to allow selecting the same file again if needed
        fileInput.value = '';
    });

    function displayFile(file) {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.innerHTML = `
            <span>${file.name}</span>
            <button class="remove-file-btn" data-filename="${file.name}">Supprimer</button>
        `;
        fileListContainer.appendChild(fileItem);
    }

    fileListContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-file-btn')) {
            const fileNameToRemove = event.target.dataset.filename;
            // Remove from internal array
            selectedFiles = selectedFiles.filter(file => file.name !== fileNameToRemove);
            // Remove from display
            event.target.closest('.file-item').remove();
        }
    });
});
</script>